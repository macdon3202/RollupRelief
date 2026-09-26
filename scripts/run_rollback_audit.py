"""Prove failed writes atomically roll back every relevant state surface."""
import json, sys
from pathlib import Path
from genlayer_py import create_client
from genlayer_py.chains import studionet
from run_studionet_e2e import RPC, read, send, wallets

POS = "cmrazrvph0am30rns9tzwb2oa"
NEG = "cmthk6pbx0at41ms2q9i1iqlu"

def snapshot(client, address, wallet):
    return {
        "config": read(client, address, wallet, "get_config"),
        "positive": read(client, address, wallet, "get_incident", [POS]),
        "negative": read(client, address, wallet, "get_incident", [NEG]),
    }

def main():
    if len(sys.argv) != 2:
        raise SystemExit("usage: run_rollback_audit.py CONTRACT_ADDRESS")
    address = sys.argv[1]
    reporter, verifier = wallets()
    client = create_client(chain=studionet, account=reporter, endpoint=RPC)
    before = snapshot(client, address, reporter)
    txs = [
        send(client, address, verifier, "assess_incident", ["rollback-unknown"], True),
        send(client, address, reporter, "register_incident", ["OP_MAINNET", "rollback-origin", "https://example.com/rollback-origin"], True),
        send(client, address, reporter, "register_incident", ["bad chain!", "rollback-token", "https://status.optimism.io/en-us/rollback-token"], True),
        send(client, address, reporter, "register_incident", ["ARBITRUM_ONE", "rollback-conflict", "https://status.optimism.io/en-us/rollback-conflict"], True),
        send(client, address, verifier, "assess_incident", [POS], True),
        send(client, address, verifier, "assess_incident", [NEG], True),
    ]
    after = snapshot(client, address, reporter)
    if before != after:
        raise AssertionError({"before": before, "after": after})
    proof = {
        "network": "studionet",
        "contract": address,
        "result": "PASS",
        "assertion": "all six finalized-error transactions left config and both terminal incident records byte-for-byte unchanged",
        "before": before,
        "after": after,
        "transactions": txs,
    }
    out = Path(__file__).resolve().parents[1] / "docs" / "studionet-rollback-audit.json"
    out.write_text(json.dumps(proof, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(proof, indent=2))

if __name__ == "__main__":
    main()
