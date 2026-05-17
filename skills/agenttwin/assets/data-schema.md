# AgentTwin Data Schema

The JSON contract between the AAC walk (input) and the HTML template (output). Build this object during Step 3 of the skill. Pass it to the renderer in Step 4.

Top-level shape:

```json
{
  "agent": { ... },
  "verdict": { ... },
  "properties": [ ... ],          // exactly 5, in order
  "after_state": { ... },
  "action_plan": [ ... ],         // 3 items for Summary view
  "process_map": {
    "flow_summary": "...",
    "nodes": [ ... ],
    "edges": [ ... ],
    "branches": [ ... ],          // refuse/hard-refuse branch markers
    "memory": { ... },
    "state_machine": { ... },
    "recommendations": [ ... ]    // ranked, full list
  }
}
```

## `agent`

```json
{
  "name": "Recall Outreach AI",
  "description": "Texts and emails patients due for their annual exam.",
  "evaluated_at": "2026-05-16",
  "slug": "recall-outreach"
}
```

- `name` — Human-friendly agent name. Title case.
- `description` — One sentence, plain English, what the agent does.
- `evaluated_at` — ISO date of this report.
- `slug` — kebab-case for filename.

## `verdict`

```json
{
  "grade": "C",
  "label": "Needs work before launch.",
  "sub": "2 things are missing. 1 is shaky. The other 2 are solid.",
  "counts": { "healthy": 2, "needs_work": 1, "broken": 2 }
}
```

- `grade` — Single letter A/B/C/D/F. Derived from property statuses:
  - A = all 5 healthy
  - B = 4 healthy + 1 needs-work, no broken
  - C = ≥ 1 broken OR ≥ 2 needs-work
  - D = 2+ broken
  - F = 3+ broken OR an AAC §A/B/C category kill
- `label` — Plain-English verdict sentence. End with a period.
- `sub` — Sub-headline explaining the count breakdown.
- `counts.healthy/needs_work/broken` — Sums of properties at each status.

## `properties` (array, exactly 5 in this order)

Each property:

```json
{
  "key": "bounded",
  "plain_name": "Stays in its lane",
  "formal_name": "Bounded",
  "status": "healthy",
  "description": "The agent can only do things from a short approved list...",
  "doing": "Uses 3 pre-approved message templates only.",
  "problem": null,
  "fix": null
}
```

Required order and plain-name mapping (see `style-guide.md` for full rationale):

| Index | `key` | `plain_name` | `formal_name` |
|---|---|---|---|
| 0 | `bounded` | Stays in its lane | Bounded |
| 1 | `grounded` | Checks its facts | Grounded |
| 2 | `gated` | Checks before doing | Gated |
| 3 | `observed` | Nothing is hidden | Observed |
| 4 | `governed` | Has a stop button | Governed |

- `status` — `"healthy"` | `"needs-work"` | `"broken"`.
- `description` — Plain-English explanation of what the property means. Same regardless of status. ~1 sentence.
- `doing` — If healthy: one-sentence concrete behavior. Set to `null` if not healthy.
- `problem` — If not healthy: one sentence describing what's wrong with this specific agent. Set to `null` if healthy.
- `fix` — If not healthy: one sentence prescriptive fix. Set to `null` if healthy.

## `after_state`

The "After the fix" view for the Summary toggle. Mirrors the same structure as the current state but with all properties at healthy.

```json
{
  "grade": "A",
  "label": "Ready for real patients.",
  "sub": "All 5 essentials in place. Cleared to launch.",
  "properties": [
    { "key": "bounded", "description": "...", "doing": "Live: 3 templates, code-enforced." },
    { "key": "grounded", "description": "...", "doing": "Source: live EHR field, verified on each send." },
    ...
  ]
}
```

The after-state property objects only need `key`, `description`, and `doing` (assumed healthy). `description` should match the current-state description (the property meaning is constant). `doing` is the realized future state.

## `action_plan` (3 items)

The Summary view's Fix List. Top 3 recommendations rewritten for a non-technical reader.

```json
[
  {
    "num": 1,
    "text": "Pull clinic hours from the live system on every send.",
    "owner": "Vince",
    "effort": "~2 hrs"
  },
  ...
]
```

Pick the top 3 by impact from the full `process_map.recommendations` list. Rewrite the title in plain English (no jargon).

## `process_map.flow_summary`

A short text summary shown at the top of the map overview.

```
"8 steps · 7 connections · 2 broken · 1 shaky"
```

Format: `{N} steps · {M} connections · {X} broken · {Y} shaky`. Use `· ` (middle dot) as separator.

## `process_map.nodes` (array)

One per work element. See AAC §B for canonical types.

Common fields (every node):

```json
{
  "id": "node-1",
  "num": 1,
  "name": "Daily trigger",
  "type": "D",
  "type_label": "Trigger",
  "lane": "system",
  "status": "healthy",
  "plain_description": "Wakes up every morning at 8 a.m. and starts the recall job.",
  "input": "— (clock-based)",
  "output": "JobStartEvent {date, run_id}",
  "specs": {
    "runtime": "AWS EventBridge cron",
    "latency": "< 1s",
    "volume": "1 run / day",
    "cost": "~$0.00 / run",
    "failure_mode": "Page on-call if missed",
    "owner": "Vince"
  },
  "quality_chips": [
    { "label": "Observed", "status": "pass" },
    { "label": "Grounded n/a", "status": "na" }
  ]
}
```

- `id` — `"node-{num}"`. Used for anchor links.
- `num` — Display number (1-indexed, sequential).
- `type` — `"D"` | `"C"` | `"A"` | `"H"`.
- `type_label` — Short archetype name: Trigger / Query / Filter / Transform / Cognitive / Gate / Action / Sink / Human / etc.
- `lane` — `"system"` | `"ai"` | `"human"`.
- `status` — `"healthy"` | `"needs-work"` | `"broken"`.
- `quality_chips` — One chip per closed-loop property that applies. `status` is `"pass"` | `"fail"` | `"na"`. Label can include extra context (e.g., `"Gated · partial"`, `"Bounded · 2 outcomes"`).

### C-node extensions (when `type === "C"`)

Add these fields:

```json
{
  "model": {
    "name": "Claude Sonnet 4.6",
    "via": "AWS Bedrock",
    "model_id": "claude-sonnet-4-6-20260301",
    "region": "us-east-1",
    "baa_status": "verified",
    "last_changed": "2026-03-15"
  },
  "prompts": {
    "system": { "content": "ROLE\nYou are...", "meta": "412 tokens · v6" },
    "user": { "content": "PATIENT\n- first_name: ...", "meta": "per-call · ~280 tokens" },
    "schema": { "content": "{ ... JSON schema ... }", "meta": "enforced by validator" },
    "example": { "content": "EXAMPLE INPUT:\n...", "meta": "included for grounding" }
  },
  "model_candidacy": {
    "status_label": "Eligible to migrate to Claude Haiku 4.5",
    "meter_pct": 96,
    "meter_over": true,
    "meta": "Shadow agreement: 96% over 14 days (threshold ≥ 95%) · Cost delta: −68% · Latency delta: −40%",
    "recommendation": "Graduate to Haiku 4.5 after 14 more days of shadow at ≥ 95%. Owner: Vince. Watch for: confidence drift on edge cases."
  }
}
```

- `prompts` — Each sub-object's `content` is a raw multi-line string. The HTML will preserve whitespace. Escape only `<` and `>` if they appear as literal HTML.
- `model_candidacy.meter_over` — `true` if the agreement is at or above the graduation threshold (renders green). `false` otherwise (renders teal).
- If no candidacy review is active, set `model_candidacy` to `null`.

### H-node extensions (when `type === "H"`)

Add these fields:

```json
{
  "judgment": {
    "question": "\"Is this refused message recoverable? If so, what does it need to say?\"",
    "meta": "Volume: ~20 / day · Time per decision: ~30s · Reviewer: Bre (rotating) · Inter-rater agreement: 92%"
  },
  "automation_candidacy": {
    "status_label": "Not yet ready to graduate",
    "meter_pct": 85,
    "meter_over": false,
    "meta": "Shadow AI agreement: 85% over 90 days (threshold ≥ 95%) · Gap: AI struggles with ambiguous refusals.",
    "recommendation": "Path to graduation: fix the Compose grounding issue upstream — drops refuse volume and gives AI cleaner training data. Re-check in 60 days."
  }
}
```

- `judgment.question` — Wrap in quotes; renders in italic serif.
- `automation_candidacy.meter_over` — Same rule as model_candidacy.

### Optional fix block (any node)

If the node has a fix recommendation:

```json
{
  "fix": {
    "severity": "broken",
    "text": "The clinic hours come from a stale config file. <strong>Fix:</strong> read clinic hours from the live RevolutionEHR field on every compose."
  }
}
```

- `severity` — `"warning"` (amber) or `"broken"` (red). Use `"broken"` for fail-state, `"warning"` for needs-work.
- `text` — Limited HTML allowed (`<strong>` only). Otherwise plain text.

## `process_map.edges` (array)

One per connection between work elements.

```json
{
  "id": "edge-1",
  "from": 1,
  "to": 2,
  "label": null,
  "plain_description": "Trigger fires the EHR query.",
  "status": "healthy",
  "edge_specs": {
    "trigger_type": "Synchronous invoke",
    "latency_budget": "< 500ms p99",
    "volume": "1 / day",
    "baseline_failure": "< 0.1%",
    "data_contract": "JobStartEvent (empty payload)",
    "retry_dlq": "EventBridge DLQ on 3 fails"
  },
  "fix": null
}
```

- `id` — `"edge-{N}"` where N is sequential across all edges.
- `from` / `to` — Node numbers.
- `label` — Optional short label shown next to "Step X → Step Y" (e.g., `"approved"`, `"refused"`). `null` if no label needed.
- `fix` — Same shape as node fix. `null` if edge is healthy.

## `process_map.branches`

Marks where the flow forks (refuse, hard-refuse, parallel). Inserted into the map overview as visual divider.

```json
[
  { "after_node": 5, "label": "Refuse branch from step 5" }
]
```

The renderer places a divider after the indicated node and shows the branched-off edge + node below it.

## `process_map.memory`

```json
{
  "working_memory": "Patient context object passed through pipeline. Lives only for the duration of one run (~30s). Not persisted.",
  "persistent_state": "Dedup key store (DynamoDB) — last 90 days of send history per patient.",
  "audit_log": "All send events + outcomes. 7-year retention (HIPAA). Encrypted at rest.",
  "conversation_memory": "None — single-turn agent.",
  "classification": "PHI (patient identifiers + contact data). Confidential.",
  "owner": "Vince (technical) · Bre (operational)"
}
```

If the agent has no memory of a given type, use `"None"` or `"Not applicable"`. Always include all 6 fields for consistency.

## `process_map.state_machine`

```json
{
  "main_flow": [
    { "name": "Triggered" },
    { "name": "Fetching" },
    { "name": "Filtering" },
    { "name": "Composing" },
    { "name": "Gating" },
    { "name": "Sending" },
    { "name": "Sent", "type": "terminal" }
  ],
  "branch_flow": [
    { "name": "Gating" },
    { "name": "Human review" },
    { "name": "Sent (edited)", "type": "terminal" },
    { "name": "Dropped", "type": "error" }
  ],
  "slas": [
    { "state": "Composing", "sla": "Max 60s, then escalate to retry queue" },
    { "state": "Gating", "sla": "Max 5s, then auto-route to refuse" },
    { "state": "Sending", "sla": "Max 30s, then DLQ + page on-call" },
    { "state": "Human review", "sla": "Max 4 business hours, then auto-drop" }
  ],
  "storage": "DynamoDB · run_state table, partition by run_id"
}
```

- `type` per state: `"terminal"` (success end, green), `"error"` (error end, red), or omit (intermediate, neutral).
- `branch_flow` — Optional. Show as a second line below main_flow.

## `process_map.recommendations`

Full ranked list of fixes. Source: every fix block in nodes/edges/properties, plus governance/cost/ops gaps from cross-cutting analysis.

```json
[
  {
    "priority": "critical",
    "priority_label": "Critical",
    "title": "Pull live clinic hours into Compose",
    "affects": [
      { "label": "Node 4 · Compose", "target_id": "node-4" }
    ],
    "meta_extra": "Grounded fail · Owner Vince · ~2 hrs",
    "impact": "Stops outdated info from reaching patients. Removes the root cause behind the C grade."
  },
  ...
]
```

- `priority` — `"critical"` | `"high"` | `"medium"` | `"opt"`.
- `priority_label` — Display label (Critical / High / Medium / Optimization).
- `affects` — One or more link objects. `target_id` is a node-N or edge-N anchor.
- `meta_extra` — The line under the title with category, owner, effort.
- `impact` — The arrow line explaining what this rec unlocks. Renders with `→ ` prefix.

## Validation rules before rendering

Before passing the JSON to the renderer, validate:

1. **5 properties exactly**, keys in canonical order.
2. **action_plan has exactly 3 items.**
3. **Every node has all common fields.** C nodes have model + prompts (model_candidacy optional). H nodes have judgment (automation_candidacy optional).
4. **Every edge references real node numbers** in `from`/`to`.
5. **Verdict grade matches property statuses** per the derivation rule.
6. **Recommendation `target_id` values exist** as node or edge ids.
7. **No null fields where strings are required** — use empty string or descriptive placeholder, never `undefined`.

If a validation fails, do not render. Surface the gap to the user and ask for clarification.
