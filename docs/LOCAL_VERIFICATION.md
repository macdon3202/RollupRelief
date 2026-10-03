# Local verification

Updated: 2026-10-03 (Asia/Bangkok)

- Release state: `STUDIONET_V3_VERIFIED`
- Contract SHA-256: `77C761971468A017A17C21995C5A6ADF8BB51594E1DFD2AB622C53B058F38D2C`
- Direct Mode: `11 passed`
- GenVM lint: `PASS (3 checks)`
- Contract validation: `PASS`
- Public methods: `5 (3 view, 2 write)`
- Frontend transaction/workflow tests: `7 passed`
- Vite production build: `PASS`

Auxiliary wallets reserved for the reproducible live E2E only:

- Reporter: `0xFeD97e2aE1A8C1983b7cA206B3545e6A2c685E43`
- Verifier: `0xc67532aeF9D2879cBA9375a02E6217A3524657B8`

These addresses are not constructor inputs and are not privileged in the contract. A reviewer can use any two independent wallets. The deterministic account-A/account-B UI state-machine test and reviewer workflow are recorded in [`FRONTEND_TWO_WALLET_E2E.md`](FRONTEND_TWO_WALLET_E2E.md); complete V3 live consensus evidence is recorded in [`STUDIONET_V3_E2E.md`](STUDIONET_V3_E2E.md).
