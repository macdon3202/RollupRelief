# Test resource manifest

Expected outcomes are fixed before live execution. A URL is a locator, not proof. Validators must fetch the source themselves and the contract stores the digest of the fetched representation.

## Positive fixture

```yaml
resource_id: optimism-write-outage-2026-07-07
purpose: positive
authoritative_owner: Optimism
canonical_origin: https://status.optimism.io
canonical_url_or_api: https://status.optimism.io/en-us/cmrazrvph0am30rns9tzwb2oa
cross_check_url: https://status.optimism.io/history/1
repository_and_object_id: optimism-status/cmrazrvph0am30rns9tzwb2oa
revision_or_commit: terminal resolved/postmortem observation
expected_content_type: text/html rendered as text
expected_digest_algorithm: sha256
expected_digest: sha256 over canonical URLs and both validator-fetched representation digests
expected_deterministic_facts: OP Mainnet; transaction throughput near zero; submissions did not land
expected_contract_result: ATTESTED / WRITE_INCLUSION / MATERIAL / relief=true
mutable_or_immutable: mutable publisher page; digest locked at observation
availability_checked_at: 2026-09-25 Asia/Bangkok
```

## Negative fixture

```yaml
resource_id: optimism-nondisruptive-maintenance-2026-08-31
purpose: negative
authoritative_owner: Optimism
canonical_origin: https://status.optimism.io
canonical_url_or_api: https://status.optimism.io/en-us/cmthk6pbx0at41ms2q9i1iqlu
cross_check_url: https://status.optimism.io/history/1
repository_and_object_id: optimism-status/cmthk6pbx0at41ms2q9i1iqlu
revision_or_commit: completed maintenance observation
expected_content_type: text/html rendered as text
expected_digest_algorithm: sha256 bundle commitment
expected_digest: computed from canonical URLs and both fetched representation digests
expected_deterministic_facts: OP Mainnet scheduled 200 ms subblocks enablement; no service disruption expected; block production intended to continue
expected_contract_result: ATTESTED / MAINTENANCE / NONE / relief=false
mutable_or_immutable: mutable publisher page; digest locked at observation
availability_checked_at: 2026-09-25 Asia/Bangkok; HTTP 200
```

## Failure controls

| Control | Expected result |
|---|---|
| Non-Optimism origin | `NON_CANONICAL_INCIDENT_URL` |
| Optimism URL with another object ID | `NON_CANONICAL_INCIDENT_URL` |
| Missing/503 page | `UNRESOLVED`, no relief |
| Malformed model output | `UNRESOLVED`, no relief |
| Relief true with operation `NONE` | schema contradiction, `UNRESOLVED` |
| Duplicate incident registration | `INCIDENT_ALREADY_REGISTERED` |
| Same fetched digest used for another object | `SOURCE_DIGEST_REPLAY` |
| Reporter attempts assessment | `INDEPENDENT_VERIFIER_REQUIRED` |
| Unrelated wallet registers an unused canonical incident | accepted; it becomes reporter |
| Assessment after terminal state | `INCIDENT_TERMINAL` |

Both sources are mutable. This release does not pretend otherwise: one bundle digest commits the exact incident representation, history representation and canonical URLs observed by validators. A source/model failure is recorded as an immutable `UNRESOLVED` attestation; a later independent verification may append a new revision. `ATTESTED` and `REJECTED` decisions remain terminal and cannot be silently overwritten.
