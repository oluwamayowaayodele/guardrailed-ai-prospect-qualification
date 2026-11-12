# Design decisions

## CRM governance sits outside the AI

The AI can recommend; it can't authorise outreach. After every assessment, a separate workflow checks the CRM for do-not-contact, an open opportunity, an existing customer, an existing owner or relationship, a previous disqualification, and contact within the last 14 days. Any of these puts the prospect on hold, even if the AI recommended priority outbound.

The reverse is allowed. If the AI recommends a hold and the CRM is clear, the hold stands and the record is flagged for review. The AI can be more cautious than the CRM, never less. Each outcome records `suppression_source` (`AI`, `CRM`, `BOTH` or `NONE`) so it's clear which layer made the call.

## Bad output is rejected, not repaired

The AI's response is checked against a fixed contract before anything is routed. If it doesn't match, the prospect is rejected. The mock batch includes one deliberately malformed response (P-B004) to show this happens rather than the system filling in a default.

## Processing status and business outcome are separate fields

`processing_status` says whether the system did its job (`COMPLETED`, `REJECTED`, `TIMED_OUT`, `DUST_API_ERROR`, `PROCESSOR_FAILURE`). `action_outcome` says what happened to the prospect (`QUEUED_PRIORITY`, `HELD`, and so on). An earlier version used a single `ROUTED` status, which overstated things by counting nurture and not-prioritised prospects as routed.

This also means a batch can be `PARTIAL_SUCCESS` while its verification passes. One expected rejection isn't a failed run, and a passing verification doesn't mean every prospect succeeded.

## One prospect per sub-workflow call

The batch calls the Processor once per record and waits for each to finish. My first version used n8n's Loop Over Items node, but its output collected extra, incomplete records across runs. Calling the sub-workflow per item removed the problem and made each prospect's outcome easy to trace. Unexpected Processor failures go to an error output and become `PROCESSOR_FAILURE` records, so one failure can't stop the rest of the batch. This is sequential, not parallel.

## Mock and live modes share one path

Mock mode replaces only the Dust call. Governance and validation are the same in both modes, so the mock batch tests the real rules and runs without credentials or network calls.

## The Dust POST is never retried automatically

A timed-out request to create a Dust conversation doesn't mean Dust didn't receive it. Retrying could create a duplicate conversation and a second charge, so a failed creation becomes a `DUST_API_ERROR` outcome instead. Polling requests are safe to repeat because they only read.

## Limits on batches and waiting

Batches are capped at 25 records in mock mode and 5 in live mode, to prevent an accidentally large or expensive run. Live polling has a 120-second deadline by default. The deadline rejects late results; it doesn't cancel a request already in flight.

## Logic stays in n8n

The validation and governance logic runs in n8n Code nodes rather than a separate Python service. That keeps the project importable as workflows with nothing else to deploy, and the logic is visible in the execution history. The trade-off is that it's tied to n8n. A larger product might move it into its own service.
