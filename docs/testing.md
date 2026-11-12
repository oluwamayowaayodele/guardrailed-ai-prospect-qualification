# Testing

These are results from my own n8n executions. Execution #485 used the sanitised release files after reimporting and relinking them; the others ran on the working versions before sanitisation.

- **#467:** the Governance Engine was unavailable to the Processor. Four prospects came back as `PROCESSOR_FAILURE`, with their identifying fields kept, and no business actions were taken. This is the fail-safe behaviour working, not a successful batch.
- **#473:** five-prospect mock batch. Four `COMPLETED`, one deliberate `MALFORMED_AI_JSON` rejection. One priority queue outcome and three holds. `PARTIAL_SUCCESS`, verification `PASS`.
- **#483:** 26 mock records, refused against the 25-record limit before any processing.
- **#484:** 6 live records, refused against the 5-record limit before any Dust call.
- **#485:** the release files, reimported and relinked, gave the same results as #473.

Details are in [`../evidence/test-execution-summary.md`](../evidence/test-execution-summary.md). [`../evidence/release-reimport-mock-485.json`](../evidence/release-reimport-mock-485.json) is a summary of the #485 output, not a raw n8n export.

## What these tests don't cover

- Live Dust runs against the release files. Live runs succeeded during development, but I haven't included their raw output here.
- A separate n8n installation. #485 was a reimport into my own workspace.
- Real CRM data, real signals or real outreach.
