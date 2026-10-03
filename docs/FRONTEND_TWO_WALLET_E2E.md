# Frontend two-wallet E2E proof

This document answers the reviewer question: **can a user actually play both
roles from the live frontend?**

## What changed

The frontend now exposes a guided handoff instead of treating wallet connection
as a single opaque step:

1. Account A connects and registers an unused canonical incident.
2. The UI reads the returned incident and displays Account A as the on-chain
   reporter.
3. The reporter is visibly prevented from assessing, and the UI offers
   **Switch to verifier wallet**.
4. The wallet account chooser is opened. Account B must be selected.
5. The UI recomputes the role from `incident.reporter`, enables assessment only
   for Account B, waits for finalization, and re-reads the terminal record.

Role derivation is not trusted for security. The deployed V3 contract also
enforces `verifier != reporter`, so bypassing the UI still cannot permit
self-verification.

## Executable frontend workflow test

`frontend/transactions.test.mjs` now executes the complete frontend state
machine with distinct account A and account B values:

```text
REPORTER_CANDIDATE / REGISTER
  -> REPORTER / SWITCH_TO_VERIFIER
  -> INDEPENDENT_VERIFIER / ASSESS
  -> INDEPENDENT_VERIFIER / COMPLETE
```

It separately proves that address comparison is case-insensitive and that the
reporter never receives permission to assess. Run it with:

```bash
cd frontend
npm test
```

This is deterministic UI logic evidence. It does not replace live network
evidence.

## Live two-wallet contract evidence

The exact deployed lifecycle was executed with two unprivileged auxiliary
wallets against contract
[`0x71101772507a3Dc6fD4376Da2506b81b2187FFc9`](https://explorer-studio.genlayer.com/address/0x71101772507a3Dc6fD4376Da2506b81b2187FFc9):

- Account A registered the incident:
  [`0x4b643e1d398733f7ffc1b52427b29409d39f24a86fef53c0b434458414667270`](https://explorer-studio.genlayer.com/tx/0x4b643e1d398733f7ffc1b52427b29409d39f24a86fef53c0b434458414667270)
- Account A's prohibited self-verification finalized with an execution error
  and no mutation:
  [`0x659e916f8826a02d7fb54aa8fab448fb8e3774f509f0497ae6c23b267206f41d`](https://explorer-studio.genlayer.com/tx/0x659e916f8826a02d7fb54aa8fab448fb8e3774f509f0497ae6c23b267206f41d)
- Account B performed the independent assessment successfully:
  [`0xa2e1df954ad4436a80cfc9874b24f71322a9976050b6fd2c142a658ce7a62fb6`](https://explorer-studio.genlayer.com/tx/0xa2e1df954ad4436a80cfc9874b24f71322a9976050b6fd2c142a658ce7a62fb6)

The terminal readback is `ATTESTED / RESOLVED / WRITE_INCLUSION / MATERIAL /
true`. Full transaction signals, negative controls, terminal replay and atomic
rollback snapshots remain in [STUDIONET_V3_E2E.md](STUDIONET_V3_E2E.md).

## Reviewer reproduction path

Open the live dApp, enter an unused canonical Optimism incident ID, connect
account A, and register it. Select **Switch to verifier wallet**, choose account
B, confirm that the role reads `INDEPENDENT VERIFIER`, and assess. The reviewer
does not need either project test wallet; roles are permissionless and derived
per incident.

