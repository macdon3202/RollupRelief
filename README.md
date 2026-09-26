# RollupRelief

RollupRelief is a GenLayer dApp that turns official L2 incident narratives into bounded, replay-protected on-chain attestations for deadline-relief decisions.

It answers one narrow question: **did an official Optimism incident materially prevent transaction inclusion, or was it only read degradation / non-disruptive maintenance?** It does not claim that a particular user attempted a transaction.

## Architecture

```text
official Optimism incident page
  -> exact origin + incident ID binding
  -> independent validator fetch
  -> semantic operational-impact classification
  -> deterministic cross-field validation
  -> append-only on-chain attestation
```

This is a permissionless role-separated registry, not escrow. The deployment wallet has no application privilege and deployment requires no constructor arguments:

- Any wallet may register an unused canonical incident and becomes its reporter.
- Any different wallet may trigger assessment and becomes its verifier.
- A reporter cannot verify its own submission.

## Outcomes

- `WRITE_INCLUSION / MATERIAL`: may qualify for relief.
- `READ_ONLY`, `FINALITY`, `NONE`: does not qualify automatically.
- `MAINTENANCE` with no disruption: does not qualify.
- unavailable, ambiguous or malformed evidence: `UNRESOLVED`, fail closed; a later independent verification may retry as a new immutable revision.

## Local verification

```powershell
python -m pip install -r requirements.txt
python -X utf8 -m genvm_linter.cli check contracts/rollup_relief.py
python -m pytest -q
cd frontend
npm install
npm test
npm run build
```

## Release status

`STUDIONET_V3_VERIFIED`. Contract: [`0x71101772507a3Dc6fD4376Da2506b81b2187FFc9`](https://explorer-studio.genlayer.com/address/0x71101772507a3Dc6fD4376Da2506b81b2187FFc9). Core, negative, conflict and adversarial suites all passed with finalized majority consensus, and frontend readbacks match the terminal state after reload.

Verified locally: **11 Direct Mode tests** (including `UNRESOLVED` recovery with preserved revisions), GenVM lint/validation **PASS**, **5 frontend transaction-state tests**, and Vite production build **PASS**.

See [complete V3 Studionet evidence](docs/STUDIONET_V3_E2E.md), [test resources](docs/TEST_RESOURCE_MANIFEST.md), [test matrix](docs/TEST_MATRIX.md), [local verification](docs/LOCAL_VERIFICATION.md), and [deployment procedure](docs/DEPLOYMENT.md).
