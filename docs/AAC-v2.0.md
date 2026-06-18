# AAC v2.0 — Agent Automation Creator

Status: canonical operating package, released 2026-06-05.

AAC v2.0 promotes AAC from a static workflow-readiness framework into a creation-time governance system for agentic work. The v1.1 core remains intact: the 12 work-element types, D/C/A/H runtime modes, 57-item rubric, and five closed-loop disciplines still govern readiness. The major version changes because the contract changed: before an agentic workflow can be created, promoted, scheduled, committed, or given tools, it now needs a portable AAC packet, executable creation gates, and runtime proof expectations.

## Why this is 2.0, not a v1.1 addendum

The earlier boundary/creation material was conservative and labeled as a practice-layer addendum. That was useful while the new pieces were only explanatory. It stopped being enough once AAC took on three new responsibilities:

1. **Creation gating** — AAC now blocks under-specified agents before build, not just audits them after the fact.
2. **Artifact contract** — workflow, node, agent-envelope, registry, and run-card artifacts are now expected review objects.
3. **Cross-surface enforcement** — the same packet can be used by Hermes, GitHub, Claude Code, Codex, Gemini, and manual chat surfaces.

That is a major-version boundary. AAC 2.0 does not replace the v1.1 rubric. It wraps the rubric in an operating contract that makes agent creation governable.

## Version map

- **AAC v1.0** — initial framework structure and 51-item rubric.
- **AAC v1.1** — pressure-tested core rubric: 57 items, cost bands, hard-refuse policy, data constraints, value modes, and calibrated confidence thresholds.
- **AAC v2.0** — v1.1 core plus the creation-time operating package: boundary model, agent envelopes, run cards, portable AAC packet, executable creation gates, GitHub/Hermes enforcement, and calibration evidence.

Backward compatibility: existing v1.1 specs can still be audited. A workflow is not 2.0-ready for creation, promotion, scheduling, or merge until it has the AAC 2.0 packet and passes the creation gates.

## Object hierarchy

AAC certifies a bounded workflow system, not an agent by vibe.

1. **Workflow Box** — the business/process object being moved from trigger to finish.
2. **Node** — one bounded work element inside the workflow.
3. **Agent Envelope** — the actor/runtime allowed to perform one or more nodes.
4. **Run Card** — evidence from one execution.

Core sentence:

> A node is the work. An agent is the performer. A workflow is the box. A run card is the proof.

## Loop architecture

AAC creation and promotion sit inside a parent loop architecture:

> A loop is a bounded improvement system with an objective function, gates, proof, promotion rules,
> and human-over-loop residue ownership. AAC Factory is one intervention-builder inside that loop.

See [`docs/aac/loop-architecture.md`](aac/loop-architecture.md) for the canonical map: Parent
System → Loop → Objective Function → Gate/Router → TBR Gate → Boundary Maps → AAC Factory
intervention → Run Card → Champion-Challenger + Holdout → Improvement Ledger → Readiness Ladder →
Human-over-loop.

## Mandatory workflow box declaration

Before creating, auditing, promoting, scheduling, or certifying an agentic workflow, declare the box being judged.

Required fields:

```yaml
workflow_box: "<noun being moved through the system>"
control_topology: "unit | graph_directed | agent_directed_envelope | hybrid"
in_scope: []
out_of_scope: []
happy_sink: ""
refuse_sink: ""
hard_refuse_sink: ""
```

If the box or topology is missing, return:

```text
FAIL: box undefined. Cannot create, audit, or certify the agentic workflow. First declare the workflow box, topology, in-scope boundary, out-of-scope boundary, and sinks.
```

## AAC 2.0 creation gates

Each gate is executable: binary PASS/FAIL, exact failure code, remediation, and a passing example. A single FAIL blocks creation, promotion, scheduling, merge, or execution until remediated.

### Gate 1 — Box + control topology

```text
IF the artifact does not declare workflow_box, control_topology, in_scope, out_of_scope, happy_sink, refuse_sink, and hard_refuse_sink,
THEN RETURN FAIL: missing workflow box/control topology.
Remediation: add the bounded work object, topology, explicit scope boundary, and all three sinks.
Passing example: workflow_box="warm recovery candidate packet"; control_topology="graph_directed"; in_scope=["draft private review packet"]; out_of_scope=["send SMS", "mutate CRM"]; sinks={happy:"packet ready", refuse:"hold for context", hard_refuse:"safety block"}.
```

### Gate 2 — Cost + value framing

```text
IF the artifact does not quantify cost_of_failure or cost_of_inaction in concrete terms (time, money, errors, compliance exposure, trust, delay, or downstream workload), or does not declare value_mode,
THEN RETURN FAIL: missing operational cost/value framing.
Remediation: add a cost_framing block and set value_mode to replace, augment, or extend.
Passing example: value_mode="augment"; cost_of_failure="40 candidates/day remain unworked, creating 3-5 staff hours of rework and delayed patient follow-up"; cost_of_inaction="warm leads decay after 7 days and require manual reseed"; per_error_cost_band="medium".
```

### Gate 3 — Owner + residue + escalation

```text
IF process_owner, technical_owner, reviewer/approval_owner, residue_accepter, or escalation_path is missing or unknown,
THEN RETURN FAIL: missing owner/residue/escalation path.
Remediation: name the accountable humans or block until they are named; do not assign ownership to "the team".
Passing example: owners={process_owner:"Bre", technical_owner:"Hermes/AAC builder", reviewer:"Bre", residue_accepter:"Ankit for pilot only"}; escalation_path="hard-refuse and low-confidence cases route to Bre before any external action".
```

### Gate 4 — Action authority + lane limits

```text
IF the artifact does not declare data_classification, allowed reads, allowed writes, autonomous actions, approval-required actions, forbidden actions, max_lane, hard_refuse classes, and kill switch,
THEN RETURN FAIL: missing action authority/lane limits.
Remediation: add the effective-permission boundary before any write/send/label/pay/escalate capability is granted.
Passing example: max_lane="draft"; autonomous_actions=["read approved snapshots", "write private review packet"]; approval_required_actions=["send_sms", "crm_mutation"]; forbidden_actions=["send", "write_crm", "pay", "delete"]; kill_switch="disable agent profile or remove writer tool".
```

### Gate 5 — Closed-loop controls for every C node

```text
IF any Closed-Loop AI (C) node lacks bounded, grounded, gated, observed, or governed controls,
THEN RETURN FAIL: missing C-node closed-loop controls.
Remediation: add all five controls: finite action set, source/schema policy, confidence/validator/action gates, run-card telemetry/review cadence, and kill switch/rollback/model-prompt versioning.
Passing example: bounded={finite_action_vocabulary:["draft", "refuse", "hard_refuse"]}; grounded={source_ids_required:true}; gated={confidence_floor:0.8, input:true, output:true, cross_check:true, action:true}; observed={run_card_required:true, review_cadence:"weekly"}; governed={refusal_available:true, kill_switch:"disable draft generation"}.
```

## Harness integration requirements

AAC 2.0 gates should run before durable or higher-blast-radius actions:

- Hermes `cronjob` create/update for autonomous jobs, tool-using jobs, external sends, writes, or file mutations.
- Hermes `kanban_create` when creating cards that build or modify agentic workflows.
- Hermes `skill_manage` create/edit when the skill controls an agent/workflow/gate.
- Hermes `delegate_task` when granting write/send/deploy/external-action authority.
- MCP/tool/plugin/webhook creation that changes agent capabilities or event-triggered execution.
- Git commits/PRs touching agent specs, workflow prompts, repo instructions, skills, cron configs, or runbooks.

Required behavior:

1. Any single FAIL blocks the artifact.
2. The failure message tells the builder exactly what to add and shows a passing example.
3. The check completes in under 90 seconds.
4. The repo or runbook documents which checker runs it, at which pipeline stage, which files/artifacts it covers, and the escalation path when it fails.

## Portable AAC packet

Use a small YAML/JSON packet that travels across Hermes, Claude Code, Codex, Gemini, GitHub, and manual chat surfaces.

Minimum fields:

```yaml
aac_framework: "2.0"
workflow_box: ""
control_topology: "unit | graph_directed | agent_directed_envelope | hybrid"
value_mode: "replace | augment | extend"
owners:
  process_owner: ""
  technical_owner: ""
  reviewer: ""
  residue_accepter: ""
cost_framing:
  cost_of_failure: ""
  cost_of_inaction: ""
  per_error_cost_band: "low | medium | high | critical"
data_classification: ""
action_authority:
  max_lane: "read | recommend | draft | write | send | pay | label | escalate"
  autonomous_actions: []
  approval_required_actions: []
  forbidden_actions: []
hard_refuse: []
closed_loop_controls:
  bounded: {}
  grounded: {}
  gated: {}
  observed: {}
  governed: {}
evals:
  holdout_set: ""
  graduation_threshold: ""
residue:
  accepted_by: ""
  review_cadence: ""
escalation_path: ""
```

## Effective permission rule

Effective permission is the most restrictive intersection of:

1. workflow max lane
2. node max lane
3. agent envelope
4. tool permission
5. user approval
6. runtime gate result

An agent never upgrades itself to a higher lane.

Example:

```text
Agent envelope allows draft + send.
Node max_lane is draft_only.
Workflow pilot forbids sends.
Effective permission: draft_only.
```

## Builder / retrofit process

Use this sequence to create a new agentic workflow or retrofit an existing one into AAC compliance.

1. Declare the workflow box — noun, trigger, finish, sinks, topology.
2. Quantify cost/value — cost of failure, cost of inaction, value mode, per-error cost band.
3. Extract nodes — one bounded work element per node, one owner per node.
4. Assign runtime modes — D/C/A/H by attributes, not preference.
5. Declare max lanes — read/recommend/draft/write/send/pay/label/escalate.
6. Map agent envelopes — which actor may perform which nodes.
7. Apply five disciplines — at node level and agent-envelope level.
8. Write cards — workflow card, node cards, agent cards, registry row, run-card schema.
9. Run the AAC 2.0 creation gate — fix every FAIL before creation/promotion/merge.
10. Run AgentTwin — assess workflow health, node health, and agent-envelope health.
11. Collect run cards — prove behavior before calling a lane runtime-green.
12. Calibrate with three prompts/workflows — record pass/fail, remediation, before/after, and duration.

## AgentTwin role

AgentTwin assesses three layers, not an abstract "agent":

1. **Workflow health** — is the process graphable and governed end to end?
2. **Node health** — does each node satisfy Bounded, Grounded, Gated, Observed, and Governed?
3. **Agent-envelope health** — is the actor's tool and action authority safe across all nodes it can touch?

Suggested verdict shape:

```text
Workflow: C
Nodes: 6 pass, 2 fail
Agent envelope: draft-safe, send-unsafe
Approved lane: draft_only
Blocked lanes: send, write, autonomous CRM mutation
```

## GitHub enforcement role

GitHub Actions should validate the artifact set before merge:

```text
docs/aac/workflows/<workflow>.aac.json
docs/aac/nodes/<workflow>/<node>.aac.json
docs/aac/agents/<agent>.aac.json
docs/aac/agent-registry.json
docs/aac/run-card.schema.json
```

The gate should fail if:

- workflow has no box
- control topology is missing
- cost/value framing is missing
- owner, reviewer, residue accepter, or escalation path is missing
- AI or write-capable node has no five-discipline declarations
- agent has no card
- agent references missing nodes
- node max lane exceeds workflow max lane
- write/send/pay/label/escalate exists without action gate
- hard-refuse path is missing
- kill switch is missing
- run-card/eval location is missing for production-readiness claims

## Calibration evidence

Before calling a gate calibrated, run three real prompts/workflow specs through it:

1. A confident prompt/spec expected to pass.
2. A suspiciously under-specified prompt/spec expected to fail.
3. A middle case expected to reveal hidden authority, owner, cost, or observability gaps.

For each record:

- gates passed
- gates failed
- exact remediation applied
- before/after artifact
- duration of full check

A confident prompt failing is a calibration win. It means AAC caught what manual review missed.

## Cross-surface rollout order

1. **Hermes first** — skill/spec, validator script, calibration records, and hard-gate integration points.
2. **Repo/GitHub** — pre-commit and GitHub Action for AAC-relevant file changes.
3. **Claude Code / Codex / Gemini** — same portable gate packet and repo-local instructions.
4. **Claude.ai/manual surfaces** — pointer-only validation prompt; no hard block unless routed through a repo/Hermes gate.
5. **Agent Registry** — no production agent without registry row, owner, max lane, kill switch, review cadence, and run-card proof.

## What did not change from v1.1

AAC 2.0 keeps these locked:

- 12 canonical work element types
- D / C / A / H runtime modes
- Bounded / Grounded / Gated / Observed / Governed
- Refusal-first architecture
- Confidence thresholds by action consequence
- Data-handling constraint dimensions
- 57-item readiness rubric

The change is where the gates sit. In v1.1, AAC primarily judged a workflow after it was specified. In v2.0, AAC also blocks weak agent creation before the system becomes durable.
