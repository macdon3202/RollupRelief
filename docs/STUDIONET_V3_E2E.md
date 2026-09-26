# RollupRelief V3 — complete Studionet evidence

Date: 2026-09-26 (Asia/Bangkok)  
Result: **PASS**

Live frontend: [https://rollup-relief.pages.dev](https://rollup-relief.pages.dev). The production alias was opened after deployment and re-read the positive terminal record, incident count, revision and both digests from Studionet successfully.

## Release identity

- Contract: [`0x71101772507a3Dc6fD4376Da2506b81b2187FFc9`](https://explorer-studio.genlayer.com/address/0x71101772507a3Dc6fD4376Da2506b81b2187FFc9)
- Version readback: `ROLLUP_RELIEF_V3`
- Source SHA-256: `77C761971468A017A17C21995C5A6ADF8BB51594E1DFD2AB622C53B058F38D2C`
- Scope: `OP_MAINNET` only; unsupported-chain claims fail before semantic inference.
- Test reporter: `0xFeD97e2aE1A8C1983b7cA206B3545e6A2c685E43`
- Independent verifier: `0xc67532aeF9D2879cBA9375a02E6217A3524657B8`

The test wallets have no contract privilege. Any reviewer may repeat the lifecycle with two independent wallets.

## Core lifecycle

| Check | Expected result | Transaction |
|---|---|---|
| Register material incident | Finalized success | [`0x4b643e…67270`](https://explorer-studio.genlayer.com/tx/0x4b643e1d398733f7ffc1b52427b29409d39f24a86fef53c0b434458414667270) |
| Reporter self-verification | Finalized error, no mutation | [`0x659e91…6f41d`](https://explorer-studio.genlayer.com/tx/0x659e916f8826a02d7fb54aa8fab448fb8e3774f509f0497ae6c23b267206f41d) |
| Duplicate registration | Finalized error, no mutation | [`0xb8c37e…07c97`](https://explorer-studio.genlayer.com/tx/0xb8c37ee92a0ad9568d14904691edc18d80985b21e816f4c6f9cdc69992607c97) |
| Independent positive assessment | Finalized success | [`0xa2e1df…62fb6`](https://explorer-studio.genlayer.com/tx/0xa2e1df954ad4436a80cfc9874b24f71322a9976050b6fd2c142a658ce7a62fb6) |
| Positive terminal replay | Finalized error, no mutation | [`0x4bfe11…ed2f7`](https://explorer-studio.genlayer.com/tx/0x4bfe115260a90b989464d1e5cc2042ac8fc0295a60e59fa95d26bac81a2ed2f7) |
| Register non-disruptive maintenance | Finalized success | [`0x935d26…50951`](https://explorer-studio.genlayer.com/tx/0x935d263052b1a6cc0ecbf59bf16e0fca9b610cfbf6512cc52b3fe03d91750951) |
| Independent negative assessment | Finalized success | [`0x88c313…1c2fa`](https://explorer-studio.genlayer.com/tx/0x88c3137d1503a70b198d6dd99d6bb598f0c37bdfe5a101c63c69dc298dc1c2fa) |

Positive readback: `ATTESTED / RESOLVED / WRITE_INCLUSION / MATERIAL / true`.  
Negative readback: `ATTESTED / MAINTENANCE / NONE / NONE / false`.

## Conflict and adversarial audit

| Check | Expected result | Transaction |
|---|---|---|
| Assess unknown object | Finalized error | [`0xd6e71d…a42ad`](https://explorer-studio.genlayer.com/tx/0xd6e71da281bbcb6d502972f0a9f1b098b53f4792f4c2fa11a3b5f4ad5d4a42ad) |
| Non-canonical origin | Finalized error | [`0x1b438f…f6798`](https://explorer-studio.genlayer.com/tx/0x1b438f848d47db6b8d2acc3924e2d1b203b27fea9220a587a56ef41d344f6798) |
| Malformed chain token | Finalized error | [`0x929ba6…fabae`](https://explorer-studio.genlayer.com/tx/0x929ba64dda791ff181b4abe6ddb018241f20d0afb3566569fa0a460e1a0fabae) |
| Official OP notice claimed as `ARBITRUM_ONE` | Finalized `UNSUPPORTED_CHAIN` error | [`0x80ed8d…b0693`](https://explorer-studio.genlayer.com/tx/0x80ed8d35f9dfa2ba691670cd1e0d64fbdcc2dc981e11874b4d54305fe39b0693) |
| Negative terminal replay | Finalized error, no mutation | [`0x45be3d…fc5c6`](https://explorer-studio.genlayer.com/tx/0x45be3de955b5f1e0ffa13729cbb8e6fbbef2073d9d1ee93477bcc62a469fc5c6) |

The unsupported-chain attempt left `incident_count` unchanged at `2`. Post-adversarial readbacks exactly matched both pre-existing terminal records, including distinct non-zero evidence digests.

## Frontend parity

The production-configured frontend was loaded against this address and synchronized after a full reload.

- Positive UI: `ATTESTED`, `WRITE_INCLUSION`, `MATERIAL`, `QUALIFIES`, revision `1`, with the exact on-chain digests.
- Negative UI: `ATTESTED`, `NONE`, `NONE`, `DOES NOT QUALIFY`, reason `NON_DISRUPTIVE_MAINTENANCE`, revision `1`, with the exact on-chain digests.
- Header readback: incident count `2` and the correct V3 contract Explorer link.
- Transaction reconciliation only reports success at `FINALIZED`; `ACCEPTED` remains pending and `UNDETERMINED` is surfaced as failure. Five frontend transaction-state tests pass.

Machine-readable records: [`studionet-e2e.json`](studionet-e2e.json) and [`studionet-adversarial.json`](studionet-adversarial.json).

## Atomic rollback audit

A second snapshot-based audit captured `get_config` and both terminal incident records, executed six invalid writes, then captured the same surfaces again. Every transaction finalized with execution error and `MAJORITY_AGREE`; the complete before/after structures were byte-for-byte equal, including `incident_count=2`, revisions and both digests.

| Reverted write | Transaction |
|---|---|
| Unknown incident assessment | [`0x7876f2…47270`](https://explorer-studio.genlayer.com/tx/0x7876f21ad191a2224d05f7d6b5581ba8acb242a1a84e7d27bdf42f4abc947270) |
| Non-canonical origin | [`0xe9ae39…1635e`](https://explorer-studio.genlayer.com/tx/0xe9ae399ad8efc7deaf6a56f0edbaf8d68cbcef1bc2f90fe39cf51813d361635e) |
| Malformed chain token | [`0x6ad22a…8bd87`](https://explorer-studio.genlayer.com/tx/0x6ad22a496b282d9c7380a4a8d13034daac97a7d1089ab47ab80eb5f2ec08bd87) |
| Unsupported-chain conflict | [`0x224038…62575`](https://explorer-studio.genlayer.com/tx/0x224038e58e0648005e0d891d025adae3b298f73da7906ec69e0b6446a0662575) |
| Positive terminal replay | [`0xaf812c…e2fe5`](https://explorer-studio.genlayer.com/tx/0xaf812c9dd74173c901d1212edcf0011090df0ec578230e3fbe6c03046a7e2fe5) |
| Negative terminal replay | [`0x4bb589…7211c`](https://explorer-studio.genlayer.com/tx/0x4bb58938d080259d78eaefa292082b4b1b4a6b57a0d1d3f939c413330b77211c) |

After these transactions, the frontend re-read both records from Studionet and displayed the exact unchanged outcomes and digests documented above. Full snapshots are preserved in [`studionet-rollback-audit.json`](studionet-rollback-audit.json).
