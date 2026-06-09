---
name: flow-interviewer
description: Turn any raw agent or automation idea into a complete, gate-ready AAC packet by interviewing the human in plain language, prefilling from the brain first, probing live data, and harvesting a graded golden set. Always use this skill when the user describes a new agent idea, says "grill this", "AAC this idea", "spec this agent", "turn this into a workflow", asks to design or scope an automation, or pastes a rough process description. Fire BEFORE AgentTwin: this skill creates the packet, AgentTwin audits it. Also fire when retrofitting an existing undocumented automation into AAC cards.
---

# Flow Interviewer

The front door of the AAC pipeline. v0.1 draft, June 2026. Output is never prose. Output is a packet.

Target repo path: `skills/flow-interviewer/SKILL.md`

## When to fire this skill

Fire when the user is:
- **Starting** a new agent, automation, or workflow idea, however rough
- **Retrofitting** an existing undocumented automation into AAC cards
- **Scoping** what it would take to automate a process

Do NOT fire for:
- Auditing an existing spec or build (AgentTwin)
- Deploying or promoting (PILOT)
- Strategy questions not tied to a buildable workflow

When in doubt, fire. A wasted S0 check costs one registry read. A skipped grill costs a weak agent becoming durable.

## What you produce

1. A draft workflow packet at `docs/aac/workflows/<slug>.aac.json` with provenance on every field
2. A golden set at `evals/<slug>.golden.json` carrying human grades
3. A calibration note appended under `docs/aac/calibration/`

## Process

### S0: Resolve the subject (mandatory first move)

Match the idea against, in order: agent registry (`docs/aac/agent-registry.json`), ATLAS index in OB, OB search.

Return one verdict before asking anything: "this exists as X", "this is new", or "this overlaps X, here is the boundary".

Calibration evidence for why this is non-skippable: on 2026-06-09 the framework's own author could not tell whether the idea being grilled was HSD4 or a new agent. Subject confusion upstream poisons every answer downstream.

### S1: Prefill (brain first, named sources)

Query in order: OB_mybcat (3 queries max), ATLAS index, agent registry, repo cards, conversation memory. Map every hit to a gate field. Tag provenance: prefilled.

If a source is unreadable from the current surface, log exactly which source in the calibration note and proceed with fields tagged assumed. Never pretend a source was checked.

### S2: Grill (plain language only)

Rules, all earned in calibration:

- Translate gate fields into plain questions. Never say "declare your workflow box, trigger to finish" to a human. Ask "what does this thing do, start to end, in one sentence".
- One batch per gate. Five questions max. Numbered, so the human can answer in shorthand.
- Qualitative answers get converted, not accepted. "Passes QA" becomes a proposed measurable default offered as A/B. The human picks. Provenance: confirmed.
- Cheapest-answer rule: humans answer the easiest item of a multi-part ask and skip the rest. Re-ask the remaining items as the single next question. Never silently drop them. Untouched items are tagged pending, never assumed-yes.
- The human's confusion is data. If a question fails to land, the question was wrong. Log it.

### S3: Data probe (mandatory before Gate 2 locks)

Query the live system of record: real volumes, field usage, owner assignment, and whether the output field the happy sink depends on actually exists and gets set.

Calibration evidence: the repo's example card claimed 40 candidates/day. Production measured 21/day with 47% pollution, and the output field sat empty on 89% of the live stream. Paper gates pass on fiction. Data probes do not. Provenance: measured.

### S4: Graph + VERIFY

Declare nodes, edges with conditions, and the director. Render the graph (seeit). The human confirms the picture before any build step.

### S5: Golden harvest (grade, never author)

Pull 3 to 5 real records from the live system. Propose a disposition and next step for each. The human grades each: right, wrong, or edit. Grades become eval_ref.

Humans will not invent good examples from memory. They will grade real ones in seconds. The grill is a grading session, not a writing assignment.

### Stop condition

Every gate field is filled or explicitly deferred with an owner and a date. Then hand off to aac_gate and the compiler. If the human goes quiet mid-grill, capture the partial packet with pending tags rather than losing the session.

## Token discipline

Prefill before asking. Tier rubric depth by lane: read/recommend/draft gets the 5 creation gates plus the 15 killer items; send/write/pay or any PHI gets the full 57. Never restate the framework to the human.

## OB capture rules

On completion, capture one WIP thought: subject, packet path, provenance summary, open grades, and the graduation condition for the build. Follow the three-tier convention: WIP captures carry a graduation condition.

## What this skill does NOT do

Build (compiler), audit (AgentTwin), deploy (PILOT), improve (Improver). It produces the packet all of those consume.

## Graduation criteria (for skill versioning)

v0.1 to v1: three real packets completed where the human's only inputs were plain-language answers, A/B picks, and grades. If the human had to explain the framework back to the interviewer, that run does not count.
