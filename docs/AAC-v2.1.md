# AAC v2.1 — Tool Reality + Harness Maintenance Operating Package

Status: canonical operating package patch, released 2026-06-17.

AAC v2.1 keeps the AAC v1.1 core rubric intact and extends AAC v2.0's creation-time operating package with two missing runtime-governance surfaces:

1. **Tool Reality Gate** — tools are first-class review/proof objects, not assumed safe because they appear in an agent prompt or runtime.
2. **Harness Maintenance Loop** — deployed harnesses update through trigger → prune → proposal → replay/Fable proof → approval, not through silent self-rewrite.

## Version map

- **AAC v1.1** — locked core readiness rubric: 57 items, D/C/A/H, five closed-loop disciplines.
- **AAC v2.0** — creation-time operating package: workflow/node/agent/run-card artifacts and executable gates.
- **AAC v2.1** — v2.0 plus Tool Cards, Tool Pool Contracts, Tool Reality Gates, Maintenance Contracts, and an AAC/Factory sync contract.

AAC v2.1 does **not** change the v1.1 rubric. It prevents drift between design-time cards, runtime tools, and post-launch maintenance.

## New required artifacts

### `aac_sync_contract`

Every workflow card must pin the operating versions:

```json
{
  "aac_operating_package_version": "2.1",
  "aac_core_rubric_version": "1.1",
  "aac_factory_version": "0.3.0",
  "capability_set": "tool-reality-maintenance-v0.1"
}
```

### Tool Card

Each available tool gets a card with responsibility, schemas, side-effect profile, permission tier, max lane, proof status, owner, audit path, and rollback/reversal.

### Tool Pool Contract

Every node and agent envelope declares its smallest allowed tool set. Empty is valid and preferred when no tool is needed. Adding a tool requires a Tool Card, proof status, and approval.

### Tool Reality Gate

Every node and agent envelope declares whether its tool pool is unverified, simulated, sandbox-proven, real-runtime-proven, or not applicable. Promotion is blocked until allowed tools are sandbox-proven or real-runtime-proven.

### Maintenance Contract

Every workflow declares owner, technical owner, residue accepter, maintenance triggers, replay refs, update-proposal ledger, rollback plan, and `autonomous_self_update_allowed: false`.

## Harness update rule

```text
Agents may detect drift and propose changes.
Agents may not silently rewrite durable instructions, memory, tools, reach, or external-action behavior.
High-risk changes require proposal + replay/Fable proof + approval.
```

## Gate behavior

`scripts/aac_gate.py --all` now validates workflow, node, agent, and tool artifacts. It fails if:

- the sync contract is missing or points to the wrong AAC/Factory version;
- a workflow lacks a maintenance contract;
- a node or agent lacks a tool pool or tool reality gate;
- an allowed tool lacks a Tool Card or proof status;
- autonomous self-update is allowed.

## Relationship to AAC Factory

AAC Factory v0.3.0 generates and validates these exact fields. The shared `capability_set` value is the drift guard between repos.
