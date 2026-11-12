# Architecture

A batch workflow takes a set of prospect records, checks the batch against its limits, then calls the Prospect Processor once for each record.

The Processor validates the record and picks an assessment mode. In mock mode it generates a synthetic AI decision without calling Dust. In live mode it creates a Dust conversation and polls until the agent responds, the response fails, or the deadline passes.

Whatever the AI recommends, the Processor then calls the CRM Governance Engine, a separate workflow that applies the CRM rules deterministically. The Processor turns the result into one standard outcome record: completed, rejected or failed. The batch workflow then checks that every prospect it sent in came back exactly once before summarising the run.

## The four workflows

1. `crm-governance-engine.json`: the sub-workflow that enforces the CRM rules.
2. `prospect-processor.json`: handles one prospect: input checks, mock or live assessment, governance and the final outcome.
3. `batch-uat.json`: runs the five synthetic prospects in mock mode and summarises the results. Start here.
4. `single-prospect-live-uat.json`: runs one prospect in live mode. It calls Dust, so only run it once you've set up your own Dust workspace, agent and API key on purpose.

The diagram is in the README and in [`../diagrams/architecture.mmd`](../diagrams/architecture.mmd). Read [`setup.md`](setup.md) before importing anything.
