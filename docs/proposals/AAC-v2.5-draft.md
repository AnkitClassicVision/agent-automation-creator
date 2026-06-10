# AAC 2.5 Pipeline (DRAFT PROPOSAL)

Status: draft for Ankit review. Not canonical until committed.
Produced from: calibration run 2026-06-09, HSD4 dispositioner, Claude.ai surface.
Target repo path: `docs/AAC-v2.5.md`
Version number is Ankit's call at commit (2.1 / 2.5 / 3.0). By the repo's own rule, the contract changes again here, from gating creation to producing agents, so this is at least 2.5.

## What 2.5 adds

AAC 2.0 governs creation. AAC 2.5 produces working agents and keeps improving them. Five additions:

1. Front door: Flow Interviewer (the grill)
2. Executable cards: model, prompt, eval, edges, lane promotion
3. Compiler: cards in, runnable agent out
4. Evaluator: golden-set regression on every change
5. Improver: run cards in, proposed card diffs out

Every change, human or machine, re-enters the same gates. One governance path, multiple entry points.

## The 10-stage pipeline

| Stage | Name | Does | Artifact out |
|---|---|---|---|
| S0 | Resolve | Match the idea against agent registry + ATLAS index. Verdict: exists / new / overlaps X | resolution note |
| S1 | Prefill | Query named brain sources, map hits to gate fields, tag provenance: prefilled | partial packet |
| S2 | Grill | Plain-language questions, one batch per gate, five max. Propose measurable defaults for qualitative answers | packet, provenance: confirmed |
| S3 | Data probe | Mandatory live queries against the system of record. Verify volumes, field usage, owners | packet, provenance: measured |
| S4 | Graph | Nodes, edges, director declared. Render. Human VERIFY (seeit) | workflow card |
| S5 | Golden harvest | Pull real records, propose dispositions, human grades right/wrong/edit | golden set (eval_ref) |
| S6 | Compile | aac_build.py: cards become system prompts, orchestration graph, registry row | runnable agent |
| S7 | Gate + evaluate | aac_gate.py + Evaluator runs golden set + THROUGHLINE output gate | pass/fail report |
| S8 | Launch | PILOT rings. Lane x ring promotion table. Go-Live Gate is human | live agent |
| S9 | Improve | Weekly: run cards feed the Improver, which proposes card diffs that re-enter S7 | card diff PR |

S0 to S5 = Flow Interviewer skill. S6 to S7 = build tools. S8 = PILOT. S9 = Improver agent.

## Schema additions (diff against schemas/aac-card.schema.json)

All cards gain per-field provenance:

```json
"provenance": {
  "<field>": { "source": "prefilled | confirmed | measured | assumed", "ref": "<query, record id, or thought id>" }
}
```

Node card adds:

```json
"model": "claude-sonnet-4-6",
"prompt_ref": "prompts/<node>.md",
"prompt_version": "1.0.0",
"eval_ref": "evals/<node>.golden.json",
"token_budget": { "per_run_max": 4000 }
```

Workflow card adds:

```json
"edges": [ { "from": "<node_id>", "to": "<node_id>", "condition": "<rule>" } ],
"director": "<node_id or 'deterministic_router'>",
"pilot_ring": "R0 | R1 | R2 | R3 | R4",
"lane_promotion": {
  "target_lane": "send",
  "condition": "20 consecutive drafts approved with zero edits",
  "counter_reset_on": ["any edit", "any hard-refuse violation"],
  "post_promotion_qa": "weekly spot-QA, 10% sample",
  "evidence_ref": "run cards"
},
"golden_set_ref": "evals/<workflow>.golden.json"
```

Golden set file format:

```json
[ { "record_ref": "", "input_summary": "", "proposed": "", "grade": "right | wrong | edit | pending", "graded_by": "", "corrected": "" } ]
```

## Lane x ring promotion table (where AAC joins PILOT)

| Lane | PILOT ring | Gate to advance |
|---|---|---|
| read / recommend | R1 | creation gates pass + AgentTwin grade B or better |
| draft | R2 | golden set at threshold + named owner |
| supervised send (shadow) | R3 | clean run cards for the cadence window |
| autonomous send | R4 | Go-Live Gate: human reviews lane_promotion evidence |

Lane promotion is ring promotion. One table, two frameworks joined.

## Contracts

**Interviewer.** Input: raw idea. Output: packet with every gate field filled or deferred (owner + date), provenance on every field, golden set drafted. Stop condition: no field unaccounted. Never outputs prose summaries.

**Compiler (aac_build.py).** Input: workflow, node, and agent cards that pass aac_gate. Output: one system prompt per C/A node assembled from prompt_ref plus the card's gates, hard_refuse list, and output contract; an orchestration graph file for the target runtime; a registry row. Deterministic: same cards, same output. Refuses on missing model, prompt_ref, or eval_ref.

**Evaluator.** Input: a card diff (new agent, model swap, prompt edit, threshold change). Runs the golden set against affected nodes. Scores against the output contract plus THROUGHLINE: THREAD (traces to the request), GROUND (source ids present), AIM (matches what the human graded right). Pass threshold lives in lane_promotion or eval_ref. Any fail blocks merge.

**Improver.** Weekly cron. Input: run cards per node plus eval scores. Output: nothing, or a proposed card diff with rationale and predicted effect. The diff enters S7 like any human change. The Improver never edits live agents. SCOUT research patterns apply when evaluating model or prompt alternatives.

## Eval set lifecycle (golden sets are versioned, not static)

A golden set is the machine-readable definition of correct plus the control group for every change. Live traffic cannot serve as the benchmark: when the agent and the inflow change at the same time, a score delta attributes to nothing.

1. Seed: graded examples from the grill (S5). Day one this is a smoke test, not a benchmark.
2. Accrete from production: every human-review action (approve, edit, reject) is a labeled example. The review node's output stream is the harvest source. Disagreements promote first, novel input types second.
3. Version: every addition or retirement bumps set_version. Eval scores cite agent version and set version. Comparisons hold the set version constant.
4. Retire by diff, never by silent mutation. A golden set change is a card change and enters S7 like a prompt edit.
5. Holdout split: the Improver develops against the open half; the Evaluator alone runs the sealed half at merge. Prevents the Improver from overfitting the benchmark. Same information-barrier pattern as Dark Factory QA. This is what the packet's holdout_set field holds.

## Token discipline

1. Prefill before asking. The interviewer asks only what the brain and the data probe could not answer.
2. Tiered depth. Lanes read/recommend/draft: 5 creation gates plus the 15 killer rubric items. Lanes send/write/pay or any PHI: full 57.
3. Compiled prompts carry pointers (eval_ref, rules doc paths), not rubric text.
4. Questions in batches of five max, numbered for shorthand answers.

## Skill slot map

| Skill | Slot |
|---|---|
| mapit | S2 engine when the subject is an existing human process |
| ATLAS | S0 index + S4 territory map; the alignment source downstream agents read |
| seeit | S4 human VERIFY of the rendered graph |
| THROUGHLINE | S7 output-integrity gate inside Gated |
| PILOT | S8 rings; Go-Live Gate at R3 to R4 |
| Make Sense | session protocol the interviewer runs under |
| AgentTwin | S7 snapshot diagnostic, plus post-launch audits |

## Open decisions for Ankit

1. Version number at commit: 2.1 / 2.5 / 3.0.
2. Killer-15 rubric subset: which 15 of the 57 are tier-1. Proposal: the A/B/C category kills.
3. Improver cadence: weekly default, per-workflow override allowed.
