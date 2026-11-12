# Security and scope

## What I removed before publishing

- n8n instance, workflow and version IDs, and workflow tags.
- Every credential reference, including the Dust API credential on the HTTP Request nodes.
- The links between workflows. Each one needs relinking after import; see [`setup.md`](setup.md).
- Webhook IDs on the Wait nodes. n8n generates new ones on import.
- All pinned execution data.
- Node IDs, which were regenerated. Node names and connections are unchanged.

All four workflows are inactive. The live Dust path uses placeholders for the workspace and agent IDs. The private Dust agent instructions and native structured-output configuration have not been exported; the documentation provides the decision contract and a non-verbatim configuration outline.

If you change and re-export these workflows, check them again before committing. n8n can reattach credentials and add new instance and webhook IDs when you edit or export.

## Built and tested

- Deterministic CRM rules that override the AI's recommendation.
- Mock batch generation and one Processor call per prospect.
- Validation of the AI's output, with rejection and error handling that always produce an outcome record.
- Batch limits for mock and live mode, and verification of the collected results.
- The Dust integration: conversation creation, polling, a bounded deadline and failure handling. This has run successfully live, but not against these exact release files.

## Simulated or out of scope

- Queue outcomes are simulated. Nothing is written to Salesforce, a CRM or an SDR queue.
- Prospect records are supplied. The project doesn't find or verify transformation signals.
- It isn't a hosted service or a product, and there's no live monitoring.
