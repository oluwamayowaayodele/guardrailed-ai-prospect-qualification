# Test results (11 November 2026)

Results from my n8n executions.

| Execution | Test | Result | Status |
|---|---|---|---|
| #467 | Governance Engine unavailable | Four `PROCESSOR_FAILURE` outcomes, no business actions, identifying fields kept. A deliberate failure case, not a successful batch. | Fail-safe behaviour confirmed |
| #473 | Five-prospect mock batch | 4 `COMPLETED`, 1 `REJECTED` (`MALFORMED_AI_JSON`); 1 `QUEUED_PRIORITY`, 3 `HELD`; `PARTIAL_SUCCESS`, verification `PASS` | PASS |
| #483 | Mock batch limit | 26 records refused by the 25-record limit before processing | PASS (expected error) |
| #484 | Live batch limit | 6 records refused by the 5-record limit before any Dust call | PASS (expected error) |
| #485 | Release files reimported and relinked, mock batch | 4 `COMPLETED`, 1 expected `REJECTED`; 1 `QUEUED_PRIORITY`, 3 `HELD`; verification `PASS` | PASS |

A summary of #485 is in [`release-reimport-mock-485.json`](release-reimport-mock-485.json).

## Static checks

[`../tools/validate_release.py`](../tools/validate_release.py) checks the four workflow files: every node is connected and reachable from the trigger, there are no credentials or instance IDs, and the workflow links are empty. Results are in [`static-validation-summary.json`](static-validation-summary.json). These are file checks, not runtime tests.

## Limits of this evidence

All data is synthetic. These results don't show signal discovery, CRM writes, live Dust runs against the release files, or behaviour on a separate n8n installation.
