# Setup

These workflows were built and tested on n8n Cloud, version 2.45.5. I've tested importing and relinking them in my own workspace (mock batch, execution #485). I haven't tested them on a separate n8n installation, so you may need to adjust node versions or settings.

## Before you start

- The workflows are inactive and contain no credentials.
- Nothing writes to a CRM, an SDR queue or any outreach tool. All actions are simulated.
- **Don't run `single-prospect-live-uat.json` until you've set up live mode deliberately.** Its trigger sends a real request to Dust.

## Import and relink

1. Import `workflows/crm-governance-engine.json` as a new workflow.
2. Import `workflows/prospect-processor.json` as a new workflow.
3. In the Processor, open `Processor - Call Hardened CRM Governance`. Set the workflow to the Governance Engine you just imported (Database, From list), keep **Wait for Sub-Workflow Completion** on, and save.
4. Publish the Governance Engine if your n8n version requires it before another workflow can call it. Mine did. If the Processor doesn't appear in the list in step 6, publish it too.
5. Import `workflows/batch-uat.json` and `workflows/single-prospect-live-uat.json` as separate workflows.
6. In each of these, open `Batch - Call Prospect Processor`. Set the workflow to the Processor you just imported. Check that **Run once for each item** and **Wait for Sub-Workflow Completion** are on, and that **Settings → On Error** is set to **Continue (using error output)**. Save.
7. Run **Batch UAT** only. It uses mock mode.

The workflow references in the export are deliberately empty. n8n workflow IDs are specific to each instance; the names shown in the nodes are just hints.

n8n documentation:
- Export and import: https://docs.n8n.io/workflows/export-import/
- Execute Sub-workflow: https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.executeworkflow/

## What you should see

Five prospects: four `COMPLETED` and one `REJECTED` with `MALFORMED_AI_JSON` (P-B004, which is deliberate).

- P-B001 goes to the priority queue.
- P-B002, P-B003 and P-B005 are held by CRM rules (open opportunity, recent contact and existing owner).
- The batch is `PARTIAL_SUCCESS`, `verification_status` is `PASS`, and every completed prospect has `final_validation_status: PASS`.
- No Dust calls are made.

## Live mode (optional)

Only if you want to run a live assessment:

- In `Processor - Prepare Live Dust Request`, replace `YOUR_DUST_AGENT_CONFIGURATION_ID` with your agent's ID.
- In `Processor - Dust Create Conversation` and `Processor - Get Dust Conversation`, replace `YOUR_DUST_WORKSPACE_ID` in the URL.
- Add your own HTTP Header Auth credential to both Dust HTTP Request nodes. Never commit credentials or API keys.
- Configure the agent to return the documented output contract. The original verbatim agent instructions are not bundled; see [`dust-agent.md`](dust-agent.md) for an explanatory configuration outline.
- Test with a single synthetic record first.

Live mode ran successfully during development, but I haven't rerun it against these release files.

## Known limitations

The 120-second polling deadline rejects late results. It doesn't cancel a request already in progress.

Some audit fields that exist part-way through the Processor, such as Dust cost credits and message IDs, aren't carried through to the final outcome record. That's something I'd add in a later version.
