---
name: agenttwin
description: Diagnose any AI agent, automation workflow, or proposed agent build against the AAC v1.1 framework and produce a marketing-grade HTML wellness report (Summary view + Process Map view). Always use this skill when the user asks to evaluate, audit, score, diagnose, map, visualize, or "AgentTwin" an AI agent, automation, workflow, vendor proposal, agent spec, or agentic build. Trigger on phrases like "AgentTwin this", "run AgentTwin on", "is this agent ready", "what's broken in this workflow", "diagnose this automation", "map this agent", "show me the health of", "should we ship this agent", "before/after on this agent". Also use proactively when the user shares an agent spec / vendor pitch / workflow diagram / Lambda code / Step Function definition and asks any evaluative question. The output is a single self-contained HTML file with two tabs — a 5th-grader-readable Summary (letter grade, 5 plain-English property cards, before/after toggle, action plan) and an operator-grade Process Map (node + edge detail cards, model identity, prompts, automation candidacy, ranked recommendations, memory + state machine).
---

# AgentTwin

A diagnostic instrument for AI agent workflows. Locked at v1, May 2026. Built on AAC v1.1 (Agent Automation Creator, MyBCAT framework, locked 2026-05-14) plus the Boundary + Creation Addendum v0.1 practice-layer object model. Produces a standalone HTML report that works without any external dependencies.

## When to fire this skill

Fire when the user is doing any of these on an AI agent, automation, or agentic workflow:
- **Designing** — drafting a new agent, planning an automation, scoping a workflow
- **Evaluating** — auditing an existing agent, reviewing a vendor pitch, scoring a build
- **Modifying** — changing prompts, models, gates, or any agent component
- **Diagnosing** — investigating drift, hallucination, cost spike, missed escalation
- **Accepting** — reviewing a builder/vendor/internal-team deliverable as ready
- **Onboarding** — giving a new AI engineer / fractional TPL day-one context

Do NOT fire for:
- Generic AI questions not tied to a workflow ("how does Claude work?")
- Personal AI use ("draft me an email")
- Strategy/business questions not involving workflow design
- Pure code bugs unrelated to AI workflow elements

When in doubt, fire. A redundant retrieval is one OB query; a missed AgentTwin run means a workflow ships without governance.

## What you produce

A single HTML file named `agenttwin-{slug}-{date}.html` saved to `/mnt/user-data/outputs/` and presented to the user via `present_files`. The HTML is fully self-contained — embedded CSS, embedded fonts via Google Fonts CDN, no build step, opens in any browser, screenshots cleanly for decks.

The report has two tabs:

1. **Summary** — 5th-grader-readable wellness report
   - Letter grade (A/B/C/D/F) in a colored circle
   - 5 property cards (Stays in lane, Checks facts, Checks before doing, Nothing is hidden, Has a stop button) with status + plain-English description + (if broken) problem + fix
   - Before/After toggle showing the "twin" (current state vs ideal state)
   - 3-item Action Plan for non-technical readers

2. **Process Map** — operator-grade detail
   - Flow overview (vertical list of nodes with status colors, lane tags, type pills)
   - Ranked Recommendations (Critical / High / Medium / Optimization)
   - Cross-cutting cards (Memory + State Machine with SLAs)
   - Node detail cards (one per step, with IO, specs, quality chips, fix block)
   - For C nodes: model identity + expandable prompts + model-change candidacy
   - For H nodes: what's being judged + automation candidacy meter
   - Edge detail cards (one per connection, with trigger type, latency, retry/DLQ)

## Process — how to run AgentTwin on any workflow

Follow these steps in order. Do not skip.

### Step 1 — Identify the workflow box and control topology

The user will provide one of:
- A natural-language description ("we have an agent that texts patients...")
- A spec document (markdown, PDF, Google Doc)
- A code reference (GitHub repo, AWS Lambda, Step Function ARN)
- A vendor pitch / proposal
- An existing agent name in their system

Before scoring, declare what object is being judged:

- **Workflow Box** — the business/process object moving through the system
- **Control Topology** — unit, graph-directed, agent-directed envelope, or hybrid
- **Node set** — bounded work elements inside the workflow
- **Agent Envelope set** — actors/runtimes allowed to perform one or more nodes
- **Run evidence** — run cards or logs proving what happened, if available

If the workflow box or topology is unclear, do not claim readiness. Return: `FAIL: box undefined` and list the missing fields. Continue the diagnostic only as a gap assessment.

Read everything available. If a code or doc is referenced, fetch and read it. **Do not proceed with assumptions** — if essential information is missing, mark those fields as gaps and proceed (do not invent).

### Step 2 — Extract the AAC elements

Walk the workflow and extract these structured elements. Use `assets/data-schema.md` for the full field list and types.

**Per node:**
- Number, name, runtime type (D/C/A/H), max lane, performer/agent envelope, status
- Plain-English description (5th grader version)
- Input class, output class
- Runtime detail, latency budget, daily volume, cost budget, failure mode, named owner
- Quality chips: Bounded / Grounded / Gated / Observed / Governed status for that node
- If C (cognitive): model name, version, provider, region, BAA status, last-changed date
- If C: system prompt, user prompt template, output schema, one-shot example (all expandable)
- If C: model-change candidacy (champion-challenger status, shadow agreement %, cost/latency delta, recommendation)
- If H (human): what question is being judged, volume, time per decision, reviewer, inter-rater agreement
- If H: automation candidacy (shadow AI agreement %, threshold, gap analysis, path to graduation)
- If broken / needs work: fix block with severity + prescriptive text

**Per agent envelope:**
- Agent id, purpose, owner, residue accepter
- Allowed workflows and nodes
- Tools, reads, writes, autonomous actions, approval-required actions, forbidden actions
- Memory policy and source policy
- Quality chips: Bounded / Grounded / Gated / Observed / Governed status for the envelope
- Kill switch and escalation path

**Per edge:**
- From → To, label (approved/refused/etc.), status
- Plain-English description
- Trigger type (sync/async/queue/event)
- Latency budget, daily volume, baseline failure rate
- Data contract (schema name + enforcement)
- Retry policy, DLQ destination

**Cross-cutting:**
- Memory: working / persistent / audit log / conversation / classification / owner
- State machine: main flow states, branch states, SLA per state, storage location

**Verdict (from AAC v1.1):**
- Score each of the 5 closed-loop properties (BOUNDED / GROUNDED / GATED / OBSERVED / GOVERNED)
- Apply verdict logic from `assets/rubric-aac-v1-1.md`
- Derive overall letter grade:
  - **A** = all 5 healthy
  - **B** = 4 healthy, 1 needs-work, no broken
  - **C** = at least 1 broken or 2+ needs-work
  - **D** = 2+ broken
  - **F** = 3+ broken or any A/B/C category killer per AAC

**Recommendations:**
- Pull every fix block from nodes, edges, properties, and cross-cutting
- Rank by priority:
  - **Critical** = closes a closed-loop property fail OR fixes safety/governance gap
  - **High** = closes a gated/grounded gap or schema enforcement gap
  - **Medium** = retry/DLQ/SLA improvements
  - **Optimization** = cost/latency improvements with no quality regression
- Each rec includes: priority, title, affected element link (node-N or edge-N), owner, effort, impact statement
- Order: Critical first, Optimization last

### Step 3 — Build the data JSON

Construct a JSON object matching the schema in `assets/data-schema.md`. This is the single source of truth for the report. Every field in the HTML output comes from this JSON.

### Step 4 — Render the HTML

Read `assets/template.html`. Find the `<script id="agent-data" type="application/json">` block. Replace its contents (everything between the opening and closing script tags) with your data JSON, formatted with 2-space indentation. **This is the only modification needed.** The template's embedded render JS does the rest.

Save the result to `/mnt/user-data/outputs/agenttwin-{slug}-{YYYY-MM-DD}.html` where `{slug}` is a kebab-case version of the agent name (e.g., `recall-outreach`, `after-hours-intake`).

### Step 5 — Present and capture

1. Call `present_files` with the new HTML file path.
2. Write a brief summary in chat: overall grade, top 3 findings, top 3 recommendations.
3. Capture the run to OB_mybcat via `OB_mybcat:capture_thought` with:
   - Type: `decision` if user accepted the report; `observation` if exploratory
   - Topics: `agenttwin`, `aac-v1-1`, `agent-diagnostic`, `{agent-slug}`
   - Content: agent name + verdict grade + top recommendations + path to HTML output

## Failure modes

- **Missing info to score a node** → mark that field "Unknown" in the data, mark the relevant quality chip as `fail` (not `pass`), and add a recommendation to surface that data. Do not invent.
- **No model info available** for a C node → show "Model: unspecified" and add Critical recommendation: "Document the model on run."
- **No human-judgment metrics** for an H node → show "Inter-rater agreement: not measured" and add Medium recommendation to start measurement.
- **Workflow only partially specified** → render what you can, mark the rest as gaps, and the report itself will show the gaps as fails — this is correct behavior (AAC §A1 demands a graphable process).
- **Vendor refuses to share prompts** for a C node → mark prompts as "Not disclosed" and add Critical recommendation: "Vendor must disclose prompts before acceptance."

## Calibration anchors

When deciding status (healthy / needs-work / broken), apply these anchors:
- **Healthy** = property is implemented, documented, monitored, and has not failed in the last 30 days.
- **Needs work** = property is partially implemented OR has documented gaps OR has failed 1-3 times in the last 30 days.
- **Broken** = property is missing, undocumented, OR has failed 4+ times / caused an incident in the last 90 days.

When uncertain between adjacent levels, downgrade (lean broken). The visual workplace principle: surface problems clearly, don't soften them.

## Plain-English language rules

The Summary view is read by non-technical operators. Strict rules:
- **No jargon** in summary cards. "Bounded" → "Stays in its lane." "Grounded" → "Checks its facts." See `assets/style-guide.md` for the full mapping.
- **Active voice.** "The agent makes things up" not "Hallucinations have been observed."
- **Concrete behavior.** "Texts patients old clinic hours" not "Has data freshness issues."
- **Specific fix.** "Pull clinic hours from the live system on every send" not "Improve data sourcing."

The Process Map view is for operators. Technical precision allowed, but still concrete:
- Cite specific tables/queues/Lambdas, not "the system"
- Cite specific people for owners, not "the team"
- Cite specific time windows for SLAs, not "soon"

## OB_mybcat capture rules

After each run, capture to OB_mybcat. Use this template:

```
AgentTwin run on {agent_name} ({date}). Verdict: {grade} — {label}.
Closed-loop status: Bounded {X}, Grounded {X}, Gated {X}, Observed {X}, Governed {X}.
Top fixes: 1) {rec1}, 2) {rec2}, 3) {rec3}.
HTML output: {path}.
Source spec: {spec_reference}.
```

Topics: `agenttwin`, `aac-v1-1`, `agent-diagnostic`, `{agent-slug}`, plus any system-specific tags (e.g., `recall-outreach`, `after-hours-intake`).

Type: `decision` if the user accepted/locked the report (production gate), `observation` if exploratory.

## Assets in this skill

- `assets/template.html` — the HTML template. Contains all CSS, the render JS, and a placeholder `<script id="agent-data">` block. **Only the JSON in that block changes per run.**
- `assets/data-schema.md` — full field-by-field reference for the JSON contract. Read this before building the JSON.
- `assets/rubric-aac-v1-1.md` — AAC v1.1 snapshot. The 57-item rubric, verdict logic, and triggers. Source of truth for scoring.
- `assets/style-guide.md` — plain-English mappings, color discipline, typography rules, content style.
- `assets/exemplar.html` — a fully-rendered example (Recall Outreach AI) showing the locked v4 visual contract. Reference for what the output should look like.

Read assets as needed — `data-schema.md` and `rubric-aac-v1-1.md` are essential for every run; `style-guide.md` and `exemplar.html` are for calibration when in doubt about language or layout.

## What this skill does NOT do

- It does not modify the agent. It only diagnoses and reports.
- It does not call the AAC rubric remotely. The rubric is inlined here.
- It does not require a live OB_mybcat connection to run (capture is best-effort; the report renders regardless).
- It does not invent missing data. Gaps surface as gaps.
- It does not declare an agent "ready" without all 5 closed-loop properties at Healthy.

## Graduation criteria (for skill versioning)

This skill is v1 (May 2026), locked from AgentTwin mockup v4. Update conditions:
- Promote to v2 only after the skill has run on at least 3 structurally different real agents (e.g., Recall Outreach, After-Hours Intake, Rx Fax) AND the operator has confirmed each report was accurate and actionable.
- Add new fields to the data schema only when a real run surfaces a missing element. Do not pre-emptively expand the schema based on speculation.
- AAC v1.1 changes do not auto-propagate. If AAC graduates to v1.2, this skill's `rubric-aac-v1-1.md` stays pinned until intentional re-snapshot.

## Final reminder

Do not skip steps. Do not assume. Do not soften broken statuses. The report's value is its honesty.
