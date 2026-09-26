"""Additional live conflict and adversarial checks for the verified deployment."""
import json, sys
from pathlib import Path

from run_studionet_e2e import EX, RPC, plain, read, send, wallets
from genlayer_py import create_client
from genlayer_py.chains import studionet

CONFLICT_ID = "cmsry9mtt00261bqtq5uqi212"
CONFLICT_URL = f"https://status.optimism.io/en-us/{CONFLICT_ID}"

def main():
    if len(sys.argv) != 2:
        raise SystemExit("usage: run_adversarial_e2e.py CONTRACT_ADDRESS")
    address = sys.argv[1]
    reporter, verifier = wallets()
    client = create_client(chain=studionet, account=reporter, endpoint=RPC)
    proof = {"contract": address, "network": "studionet", "transactions": [], "readbacks": {}}

    # Input-boundary failures must finalize as errors and create no object.
    proof["transactions"].append(send(client, address, verifier, "assess_incident", ["never-registered"], True))
    proof["transactions"].append(send(client, address, reporter, "register_incident", ["OP_MAINNET", "bad-source-object", "https://example.com/bad-source-object"], True))
    proof["transactions"].append(send(client, address, reporter, "register_incident", ["bad chain!", "bad-chain-object", "https://status.optimism.io/en-us/bad-chain-object"], True))

    # This release is deliberately scoped to one chain. Cross-chain claims are
    # rejected deterministically before any semantic/model decision.
    before_count = read(client, address, reporter, "get_config")["incident_count"]
    proof["transactions"].append(send(client, address, reporter, "register_incident", ["ARBITRUM_ONE", CONFLICT_ID, CONFLICT_URL], True))
    after_count = read(client, address, reporter, "get_config")["incident_count"]
    if after_count != before_count:
        raise AssertionError("unsupported-chain conflict mutated state")
    proof["readbacks"]["unsupported_chain_count_unchanged"] = after_count

    # Audit the two terminal decisions produced by the core E2E and prove that
    # further writes cannot rewrite either record.
    positive_id = "cmrazrvph0am30rns9tzwb2oa"
    negative_id = "cmthk6pbx0at41ms2q9i1iqlu"
    positive = read(client, address, verifier, "get_incident", [positive_id])
    negative = read(client, address, verifier, "get_incident", [negative_id])
    if positive["state"] != "ATTESTED" or negative["state"] != "ATTESTED" or positive["source_digest"] == negative["source_digest"]:
        raise AssertionError("audit readback mismatch")
    proof["transactions"].append(send(client, address, verifier, "assess_incident", [negative_id], True))
    if read(client, address, verifier, "get_incident", [negative_id]) != negative:
        raise AssertionError("negative terminal replay mutated state")
    proof["readbacks"]["positive_audit"] = positive
    proof["readbacks"]["negative_audit"] = negative
    proof["result"] = "PASS"
    out = Path(__file__).resolve().parents[1] / "docs" / "studionet-adversarial.json"
    out.write_text(json.dumps(proof, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(proof, indent=2))

if __name__ == "__main__":
    main()
