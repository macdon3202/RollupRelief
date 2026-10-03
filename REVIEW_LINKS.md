# RollupRelief public review links

All links below are public, require no repository checkout, and correspond to
the verified V3 deployment.

| Item | Public URL |
|---|---|
| Live dApp | https://rollup-relief.pages.dev/ |
| Source repository | https://github.com/macdon3202/RollupRelief |
| Studionet V3 contract | https://explorer-studio.genlayer.com/address/0x71101772507a3Dc6fD4376Da2506b81b2187FFc9 |
| Complete transaction-level E2E ledger | https://github.com/macdon3202/RollupRelief/blob/main/docs/STUDIONET_V3_E2E.md |
| Frontend two-wallet handoff proof | https://github.com/macdon3202/RollupRelief/blob/main/docs/FRONTEND_TWO_WALLET_E2E.md |
| Test resource manifest | https://github.com/macdon3202/RollupRelief/blob/main/docs/TEST_RESOURCE_MANIFEST.md |
| Test matrix | https://github.com/macdon3202/RollupRelief/blob/main/docs/TEST_MATRIX.md |

## Reviewer fixtures

- Positive incident ID: `cmrazrvph0am30rns9tzwb2oa`
- Negative incident ID: `cmj0st2o7002dq8r8rd71ad3b`

The positive fixture is loaded by default in the live frontend. Select
**Sync existing incident** to reproduce the on-chain readback without connecting
a wallet. To reproduce both roles on a fresh unused incident, use account A to
register, select **Switch to verifier wallet**, then use account B to assess.
The repository evidence ledger links every happy, negative, conflict,
role-separation, rollback, and terminal-replay transaction.
