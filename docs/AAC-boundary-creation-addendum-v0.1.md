# AAC v1.1 Boundary + Creation Addendum v0.1

Status: practice-layer addendum, not a new AAC framework version.

AAC v1.1 remains canonical. This addendum clarifies how to apply AAC when the object being judged is an AI agent, agentic workflow, automation, or tool-using assistant. It exists because the word "agent" is ambiguous: sometimes it means the business workflow, sometimes a node in the workflow, sometimes the runtime actor, and sometimes one execution.

This addendum keeps those objects separate so builders, AgentTwin, and GitHub checks judge the right thing.

## Object hierarchy

AAC certifies a bounded workflow system, not an agent by vibe.

1. **Workflow Box** — the business/process object being moved from trigger to finish.
2. **Node** — one bounded work element inside the workflow.
3. **Agent Envelope** — the actor/runtime allowed to perform one or more nodes.
4. **Run Card** — evidence from one execution.

Core sentence:

> A node is the work. An agent is the performer. A workflow is the box. A run card is the proof.

## Mandatory box declaration

Before applying AAC or AgentTwin, declare the box being judged.

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

If the box or topology is missing, the correct answer is:

```text
FAIL: box undefined. Cannot create, audit, or certify the agentic workflow. First declare whether this is a workflow, node, agent envelope, or run evidence.
```

## Workflow Box

The workflow box names the business/process object AAC is judging.

Examples:

- inbound patient SMS follow-up
- HubSpot warm-recovery candidate review
- daily ops brief
- applicant triage

A workflow card must declare:

- trigger
- finished state
- happy, refuse, and hard-refuse sinks
- control topology
- owner and residue accepter
- workflow max lane
- node list
- agent envelope list
- observability and review cadence

## Node

A node is a bounded work element in the process graph. Every node has one owner, one runtime mode, explicit input/output contracts, and an action lane limit.

Required node fields:

```yaml
node_id: ""
workflow: ""
runtime_mode: "D | C | A | H"
max_lane: "read | recommend | draft | write | send | pay | label | escalate"
owner: ""
input_contract: {}
output_contract: {}
data_classification: ""
bounded: {}
grounded: {}
gated: {}
observed: {}
governed: {}
```

The five AAC disciplines apply to every node. For deterministic or human-only nodes, a discipline may be implemented by deterministic rules or human operating procedure, but it still must be declared.

## Agent Envelope

An agent envelope is the actor/runtime allowed to perform one or more nodes. It is not the workflow itself.

Examples:

- Hermes worker
- warm-recovery drafting agent
- reply classifier
- GitHub review agent
- cron daily brief agent

Required agent-envelope fields:

```yaml
agent_id: ""
purpose: ""
allowed_workflows: []
allowed_nodes: []
tools: []
allowed_action_classes: []
forbidden_action_classes: []
approval_required_actions: []
memory_policy: "none | read_only | proposal_only | approved_write"
telemetry_required: true
kill_switch: ""
owner: ""
residue_accepter: ""
bounded: {}
grounded: {}
gated: {}
observed: {}
governed: {}
```

The five disciplines apply at the agent level too:

- **Bounded** — what action classes and tools this actor may use.
- **Grounded** — what source policy governs claims and decisions.
- **Gated** — what permission, approval, and escalation gates wrap tool use.
- **Observed** — what telemetry, cost, refusal, and external-action logs are captured.
- **Governed** — who owns the envelope, how memory writes are controlled, and how to stop it.

## Run Card

A run card is the proof that one execution followed the declared workflow, node, and agent-envelope constraints.

A run card records:

- input reference
- workflow and node path
- agent envelope used
- model/tool versions
- source IDs
- gate results
- confidence
- refusals
- human approvals
- actions taken
- external side effects
- telemetry and cost

No real run card means no runtime-green claim. A design can be AAC-specified before run cards exist, but production readiness requires run evidence.

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

1. **Declare the workflow box** — noun, trigger, finish, sinks, topology.
2. **Extract nodes** — one bounded work element per node, one owner per node.
3. **Assign runtime modes** — D/C/A/H by attributes, not preference.
4. **Declare max lanes** — read/recommend/draft/write/send/pay/label/escalate.
5. **Map agent envelopes** — which actor may perform which nodes.
6. **Apply five disciplines** — at node level and agent-envelope level.
7. **Write cards** — workflow card, node cards, agent cards, registry row, run-card schema.
8. **Run AgentTwin** — assess workflow health, node health, and agent-envelope health.
9. **Enforce in GitHub** — CI fails if required cards or fields are missing.
10. **Collect run cards** — prove behavior before calling a lane runtime-green.

## AgentTwin role

AgentTwin should assess three layers, not an abstract "agent":

1. **Workflow health** — is the process graphable and governed end to end?
2. **Node health** — does each node satisfy Bounded, Grounded, Gated, Observed, Governed?
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
- AI or write-capable node has no five-discipline declarations
- agent has no card
- agent references missing nodes
- node max lane exceeds workflow max lane
- write/send/pay/label/escalate exists without action gate
- owner or residue accepter is missing
- hard-refuse path is missing
- kill switch is missing
- run-card/eval location is missing for production-readiness claims

## Version discipline

This is an operating-package/practice-layer addendum. It does not change AAC v1.1's core primitives, 57-item rubric, runtime modes, or closed-loop disciplines.

Promote any part of this addendum into a future AAC framework version only after multiple real workflows show that the practice-layer artifact consistently catches failures the framework alone does not catch.
