import json
from pathlib import Path
import pytest

CONTRACT = Path(__file__).parents[1] / "contracts" / "rollup_relief.py"
DEPLOYER = bytes.fromhex("11" * 20)
REPORTER = bytes.fromhex("22" * 20)
VERIFIER = bytes.fromhex("33" * 20)
OUTSIDER = bytes.fromhex("44" * 20)
IID = "cmrazrvph0am30rns9tzwb2oa"
URL = f"https://status.optimism.io/en-us/{IID}"

def deploy(vm, direct_deploy):
    vm.strict_mocks = True
    vm.check_pickling = True
    with vm.prank(DEPLOYER):
        return direct_deploy(CONTRACT, sdk_version="v0.2.16")

def result(binding="MATCH", status="RESOLVED", operation="WRITE_INCLUSION", impact="MATERIAL", relief=True, reason="WRITE_SUBMISSIONS_DID_NOT_LAND"):
    return {"source_binding": binding, "incident_status": status, "affected_operation": operation, "impact_level": impact}

def register(c, vm, iid=IID, url=URL):
    with vm.prank(REPORTER):
        c.register_incident("OP_MAINNET", iid, url)

def mock(vm, model=None, body="Official Optimism incident: submitted transactions did not land. Resolved."):
    vm.mock_web(r"status\.optimism\.io/en-us/", {"method":"GET", "status":200, "body":body})
    vm.mock_web(r"status\.optimism\.io/history/1", {"method":"GET", "status":200, "body":f"Official incident history includes {IID}. {body}"})
    vm.mock_llm("ROLLUP_RELIEF_ASSESSMENT_V2", model or result())

def test_permissionless_config(direct_vm, direct_deploy):
    c = deploy(direct_vm, direct_deploy)
    cfg = c.get_config()
    assert cfg["access"] == "PERMISSIONLESS_PER_INCIDENT_TWO_WALLET"

def test_positive_incident_attests_relief(direct_vm, direct_deploy):
    c = deploy(direct_vm, direct_deploy); register(c, direct_vm); mock(direct_vm)
    with direct_vm.prank(VERIFIER): assert c.assess_incident(IID) == "ATTESTED"
    item = c.get_incident(IID)
    assert item.qualifies_for_relief is True
    assert item.affected_operation == "WRITE_INCLUSION"
    assert len(item.content_digest) == 64
    assert len(item.source_digest) == 64

def test_non_disruptive_maintenance_does_not_qualify(direct_vm, direct_deploy):
    c = deploy(direct_vm, direct_deploy); register(c, direct_vm)
    mock(direct_vm, result(status="MAINTENANCE", operation="NONE", impact="NONE", relief=False, reason="NO_SERVICE_DISRUPTION"), "Official planned maintenance. No service disruption expected.")
    with direct_vm.prank(VERIFIER): assert c.assess_incident(IID) == "ATTESTED"
    assert c.get_incident(IID).qualifies_for_relief is False

def test_any_wallet_including_deployer_can_register(direct_vm, direct_deploy):
    c = deploy(direct_vm, direct_deploy)
    with direct_vm.prank(DEPLOYER): c.register_incident("OP_MAINNET", IID, URL)
    assert c.get_incident(IID).reporter == "0x" + "11" * 20

def test_reporter_cannot_self_verify_and_unknown_incident_rejects(direct_vm, direct_deploy):
    c = deploy(direct_vm, direct_deploy)
    register(c, direct_vm)
    with direct_vm.prank(REPORTER), direct_vm.expect_revert("INDEPENDENT_VERIFIER_REQUIRED"): c.assess_incident(IID)
    with direct_vm.prank(VERIFIER), direct_vm.expect_revert("INCIDENT_NOT_FOUND"): c.assess_incident("unknown-incident")

def test_canonical_origin_and_object_binding(direct_vm, direct_deploy):
    c = deploy(direct_vm, direct_deploy)
    with direct_vm.prank(REPORTER), direct_vm.expect_revert("NON_CANONICAL_INCIDENT_URL"): c.register_incident("OP_MAINNET", IID, "https://example.com/incident")
    with direct_vm.prank(REPORTER), direct_vm.expect_revert("NON_CANONICAL_INCIDENT_URL"): c.register_incident("OP_MAINNET", IID, "https://status.optimism.io/en-us/wrong")
    with direct_vm.prank(REPORTER), direct_vm.expect_revert("UNSUPPORTED_CHAIN"): c.register_incident("ARBITRUM_ONE", IID, URL)

def test_duplicate_and_terminal_replay_leave_state(direct_vm, direct_deploy):
    c = deploy(direct_vm, direct_deploy); register(c, direct_vm)
    with direct_vm.prank(REPORTER), direct_vm.expect_revert("INCIDENT_ALREADY_REGISTERED"): c.register_incident("OP_MAINNET", IID, URL)
    mock(direct_vm)
    with direct_vm.prank(VERIFIER): c.assess_incident(IID)
    before = c.get_incident(IID)
    with direct_vm.prank(VERIFIER), direct_vm.expect_revert("INCIDENT_TERMINAL"): c.assess_incident(IID)
    assert c.get_incident(IID) == before

def test_unavailable_source_fails_closed(direct_vm, direct_deploy):
    c = deploy(direct_vm, direct_deploy); register(c, direct_vm)
    direct_vm.mock_web(r"status\.optimism\.io/en-us/", {"method":"GET", "status":503, "body":"unavailable"})
    with direct_vm.prank(VERIFIER): assert c.assess_incident(IID) == "UNRESOLVED"
    assert c.get_incident(IID).qualifies_for_relief is False

    # A later healthy observation may recover the same object without an
    # admin reset, while preserving the failed revision as audit evidence.
    mock(direct_vm)
    with direct_vm.prank(VERIFIER): assert c.assess_incident(IID) == "ATTESTED"
    item = c.get_incident(IID)
    assert int(item.revision) == 2
    assert c.get_attestation(IID, 1).reason_code == "SOURCE_OR_MODEL_UNRESOLVED"
    assert c.get_attestation(IID, 2).qualifies_for_relief is True

@pytest.mark.parametrize("bad", [
    {"source_binding":"MATCH", "incident_status":"RESOLVED", "affected_operation":"INVALID", "impact_level":"MATERIAL"},
    {"verdict":"RELIEF"},
])
def test_contradictory_or_malformed_output_fails_closed(direct_vm, direct_deploy, bad):
    c = deploy(direct_vm, direct_deploy); register(c, direct_vm); mock(direct_vm, bad)
    with direct_vm.prank(VERIFIER): assert c.assess_incident(IID) == "UNRESOLVED"
    assert c.get_incident(IID).qualifies_for_relief is False

def test_digest_replay_across_objects_rejected(direct_vm, direct_deploy):
    c = deploy(direct_vm, direct_deploy); register(c, direct_vm); mock(direct_vm)
    with direct_vm.prank(VERIFIER): c.assess_incident(IID)
    iid2="another-incident"
    with direct_vm.prank(REPORTER): c.register_incident("OP_MAINNET", iid2, f"https://status.optimism.io/en-us/{iid2}")
    with direct_vm.prank(VERIFIER), direct_vm.expect_revert("SOURCE_DIGEST_REPLAY"): c.assess_incident(iid2)
