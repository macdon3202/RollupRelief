# Direct and live test matrix

| Invariant | Direct Mode | Studionet requirement |
|---|---:|---:|
| No global admin or hardcoded role | required | `get_config` readback |
| Any wallet can register an unused incident | required | wallet A success |
| Any wallet other than reporter can assess | required | wallet B success + wallet A self-assessment error |
| Exact authority/object URL binding | required | wrong-origin expected error |
| Positive write outage qualifies | required | official positive fixture |
| Non-disruptive maintenance does not qualify | required | official negative fixture |
| Missing source fails closed | required | unavailable fixture if safely reproducible |
| Contradictory output fails closed | required | covered by deployed code + direct test |
| Duplicate object rejected | required | expected-error tx |
| Cross-object digest replay rejected | required | expected-error tx |
| Terminal replay rejected, no mutation | required | expected-error tx + readback |
| Frontend waits for final result then re-reads | node test | production signed write + reload |

Every rejected live call must include complete relevant pre/post readback proving no mutation.
