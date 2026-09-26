# Studionet lifecycle evidence

Date: 2026-09-25 (Asia/Bangkok)  
Result: **SUPERSEDED BY V3**. The lifecycle below passed, but a later adversarial cross-chain test showed V2 accepted an OP Mainnet/Sepolia notice registered as `ARBITRUM_ONE`. V3 moves this boundary out of semantic inference and rejects unsupported chains deterministically.

Adversarial discovery transactions:

- [Cross-chain registration accepted by V2](https://explorer-studio.genlayer.com/tx/0x6bbf96db4e2bd7384ffca1fc8c27939587a61bef50a79c359a2ce1d28b24a219)
- [V2 semantic assessment incorrectly attested the mismatched chain](https://explorer-studio.genlayer.com/tx/0x54b97b9db35ff3a9b059c89c8a45e68001c982c39160e7ca200d8c3ca3958e9c)

## Release identity

- Contract: [`0x28a0fd18441AB802f3b80ed7D6F80Ba48DF3977D`](https://explorer-studio.genlayer.com/address/0x28a0fd18441AB802f3b80ed7D6F80Ba48DF3977D)
- Version readback: `ROLLUP_RELIEF_V2`
- Source SHA-256: `EFD99872B7FB7E966B2E476A0DE2D4848BF38172163A7B564F3A6871380C4F24`
- Access readback: `PERMISSIONLESS_PER_INCIDENT_TWO_WALLET`
- Reporter for these fixtures: `0xFeD97e2aE1A8C1983b7cA206B3545e6A2c685E43`
- Independent verifier: `0xc67532aeF9D2879cBA9375a02E6217A3524657B8`

The addresses above are test participants, not privileged constructor roles. Any reviewer can repeat the lifecycle with two different wallets.

## Positive lifecycle — material write-inclusion failure

Official source: [`cmrazrvph0am30rns9tzwb2oa`](https://status.optimism.io/en-us/cmrazrvph0am30rns9tzwb2oa)  
Official cross-check: [Optimism notice history](https://status.optimism.io/history/1)

1. [Register incident — finalized success](https://explorer-studio.genlayer.com/tx/0xdbf92264b0b92c4cc737ae3e8629079a16bf8baff4f71baae38b2470f67a938c)
2. [Reporter self-assessment — finalized expected error](https://explorer-studio.genlayer.com/tx/0x8d19b42b0bfe34ec4245602a81a5ebfdc54a5714dd9b936722c48aeceda9718d)
3. [Duplicate registration — finalized expected error](https://explorer-studio.genlayer.com/tx/0x28e63efb1f6d0df7706e085626fd2d1ac04f08ad845ca902fbbd8b0f970afa6a)
4. [Independent assessment — finalized success](https://explorer-studio.genlayer.com/tx/0x27770299b053fc6f7cac8bbd43da6898a5db60401cb00135720eb950f14bc45e)
5. [Terminal replay — finalized expected error](https://explorer-studio.genlayer.com/tx/0x37cd9ad8437d039b16f89c1abf1d3394a4b5aae9b0a9632f5e087350c3eae053)

Final readback: `ATTESTED`, `RESOLVED`, `WRITE_INCLUSION`, `MATERIAL`, `qualifies_for_relief=true`, revision `1`. Both content and complete evidence-bundle digests are persisted on-chain.

## Negative lifecycle — non-disruptive maintenance

Official source: [`cmthk6pbx0at41ms2q9i1iqlu`](https://status.optimism.io/en-us/cmthk6pbx0at41ms2q9i1iqlu)  
Official cross-check: [Optimism notice history](https://status.optimism.io/history/1)

1. [Register maintenance notice — finalized success](https://explorer-studio.genlayer.com/tx/0x83aed2bb05e5779fe284b32df739c5dbbae885103873cb2664b968f87d9a0e04)
2. [Independent assessment — finalized success](https://explorer-studio.genlayer.com/tx/0x29d32ebc427ae9ef4c982c1d08348f25b7255ade58dc23110c2f550dda0209ff)

Final readback: `ATTESTED`, `MAINTENANCE`, `NONE`, `NONE`, `qualifies_for_relief=false`, reason `NON_DISRUPTIVE_MAINTENANCE`, revision `1`.

## Verification conclusion

All seven transactions finalized with `MAJORITY_AGREE`. The three deliberately invalid calls finalized with execution errors and did not mutate the registered/attested state. The positive and negative official sources produced distinct non-zero content and evidence-bundle digests. Machine-readable readbacks are preserved in [`studionet-e2e.json`](studionet-e2e.json).
