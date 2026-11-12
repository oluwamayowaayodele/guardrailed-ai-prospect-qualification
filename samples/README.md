# Sample data

[`prospects-mock-batch.json`](prospects-mock-batch.json) holds the five prospect records produced by the `Batch - Generate Synthetic Prospects` node in `workflows/batch-uat.json`. The node itself is the source; this file is a copy for easy reading.

Each record tests one scenario:

- P-B001: clean CRM, should reach the priority queue.
- P-B002: open opportunity.
- P-B003: contacted 5 days ago.
- P-B004: the mock AI response is deliberately malformed.
- P-B005: existing relationship or owner.

All companies and details are fictional. Running the batch in mock mode makes no Dust calls and writes to no CRM.
