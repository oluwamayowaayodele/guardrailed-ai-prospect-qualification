# The Dust agent

Dust handles the AI assessment. n8n handles orchestration, validation and the CRM rules. The agent receives one self-contained prospect record and returns a structured decision. It's instructed to work only from the record it's given and not to invent facts.

## What the agent returns

- `prospect_id`
- `account_priority`: `HIGH`, `MEDIUM` or `LOW`
- `prospect_fit`: `HIGH`, `MEDIUM` or `LOW`
- `outreach_disposition`: `ADD_TO_PRIORITY_OUTBOUND_QUEUE`, `ADD_TO_STANDARD_OUTBOUND_QUEUE`, `RESEARCH_BETTER_PERSONA`, `NURTURE_OR_MONITOR`, `HOLD` or `DO_NOT_PRIORITISE`
- `suppression_applied`: true or false
- `suppression_reason`: `NONE`, `OPEN_OPPORTUNITY`, `RECENT_CONTACT`, `DO_NOT_CONTACT`, `EXISTING_CUSTOMER`, `EXISTING_RELATIONSHIP_OR_OWNER`, `PREVIOUS_DISQUALIFICATION` or `OTHER`
- `decision_summary` and `decision_rationale`

n8n rejects any response that doesn't match this contract. A valid response still goes through the CRM Governance Engine, so the agent's recommendation never decides on its own whether outreach is allowed.

## Agent instructions

## Recreating the assessment (configuration outline)

The full, verbatim Dust agent instructions and Dust-native structured-output schema are **not included** in this release. The points below document the intended assessment behaviour from the project's design notes, **not a copy of the exact running agent prompt**. A different agent configured from these notes may return different classifications. The mock-mode reproduction does not depend on a Dust agent.

For a comparable live setup, configure a Dust agent to:

1. Assess **one supplied prospect record at a time**, relying on that record alone. Treat evidence, hypotheses and unknowns differently; do not invent pain points, budget, intent, procurement status, projects or ERP decisions.
2. Consider these separate assessment dimensions: finance/ICP fit (0–25), finance transformation need (0–25), buying/change signals (0–20), prospect/persona fit (0–20), and CRM/outreach timing (0–10). Account priority is derived from the first three dimensions: `HIGH` at 55–70, `MEDIUM` at 35–54 and `LOW` at 0–34. Prospect fit is separately `HIGH` at 16–20, `MEDIUM` at 6–15 and `LOW` at 0–5. The current n8n decision contract expects the **categories**, not these component scores.
3. Return one structured JSON object containing **exactly the fields and enums listed above**, including a concise `decision_summary` and an evidence-grounded `decision_rationale`. Use Dust's structured-output facility where available.
4. Treat an AI-proposed `HOLD` consistently: `suppression_applied` must be `true` and `suppression_reason` must not be `NONE`. For a non-`HOLD` AI disposition, `suppression_applied` must be `false` and `suppression_reason` must be `NONE`. The independent n8n Governance Engine still makes the final CRM-suppression determination.
5. Test against your own synthetic data and inspect the n8n parser/governance results before enabling real Dust calls. These notes are not a substitute for validating the agent you configure.

See [`design-decisions.md`](design-decisions.md) for the governance rationale and [`setup.md`](setup.md) for the live credentials and import steps.


## Using your own agent

To run live mode you need your own Dust workspace, an agent configured with the instructions above, and an API key. The workflows contain placeholders (`YOUR_DUST_WORKSPACE_ID`, `YOUR_DUST_AGENT_CONFIGURATION_ID`) and no credentials. See [`setup.md`](setup.md).
