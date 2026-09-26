# Deployment and verification procedure

Status: `STUDIONET_V3_VERIFIED` at [`0x71101772507a3Dc6fD4376Da2506b81b2187FFc9`](https://explorer-studio.genlayer.com/address/0x71101772507a3Dc6fD4376Da2506b81b2187FFc9). See [`STUDIONET_V3_E2E.md`](STUDIONET_V3_E2E.md).

## Permissionless role boundary

Deploy with **no constructor arguments**. The contract stores no owner, administrator or globally privileged reporter/verifier.

- Any wallet may register an unused canonical incident and becomes that incident's reporter.
- Any different wallet may independently assess that incident.
- The reporter cannot assess its own incident.
- The deployer is treated exactly like any other wallet and receives no special authority.

This lets reviewers test the complete dApp with any two wallets they control.

## Release gate

1. Record contract SHA-256 and run lint, validation and Direct Mode tests.
2. Deploy the exact source with no constructor arguments.
3. Verify Explorer source/schema and `get_config` readback.
4. Any wallet A registers the official positive incident and becomes its reporter.
5. Any different wallet B assesses it; require finalized consensus, execution success and exact state readback.
6. Run reporter self-assessment, duplicate and terminal-replay controls.
7. Run the official non-disruptive maintenance negative fixture.
8. Record all transaction hashes, execution/consensus outcomes and pre/post readbacks in `docs/STUDIONET_E2E.md`.
9. Configure the one accepted address in frontend production environment, README and Explorer links.
10. Build, deploy, connect the correct role wallets, perform a signed write, reload and verify the same state.

The bundled E2E runner uses two auxiliary wallets only for reproducibility; they are not hardcoded into the contract. Never expose their private keys in the repository, frontend bundle, docs or logs.
