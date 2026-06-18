# AAC 2.5 — Autonomy, QA, and Self-Healing Addendum (DRAFT PROPOSAL)

Status: draft for Ankit review. Extends `AAC-v2.5-draft.md` + the S4 concept-map stage.
Produced from: knowledge_repo pipeline build, 2026-06-09, directed by Ankit.
Reference implementation: `learning_github/knowledge_repo` (qa_agent_package, heal_agent_package,
run_pipeline, runcard; regression suite passing; HSD4 worked example healed live).

## Operating stance: human OVER the loop, never in it

The pipeline runs automated end to end. Humans supervise through queues, sampling, and
escalation; they do not sit inline. Inline human gates exist ONLY for the highest-risk classes.

Workflow cards now carry an `automation_policy`:

```json
"automation_policy": {
  "stance": "human_over_loop",
  "auto_advance": {"R0": true, "R1": true, "R2": "auto_when_golden_graded", "R3": false, "R4": false},
  "human_gates_only": [
    "golden grading (async review queue, never inline per run)",
    "residue statement signing",
    "lane promotion to R3/R4",
    "any irreversible or external action (send/write/pay/delete)"
  ],
  "self_healing": { "enabled": true, "auto_fix_classes": [...], "proposal_only_classes": [...], "max_iterations": 3 }
}
```

Node cards carry a `supervision` block by runtime:
- C/A: `human_over_loop` — async review queue, 10% weekly sampling, escalation triggers
  (confidence below floor, hard-refuse, QA block, drift alarm). `inline_approval: false`.
- H: `inline_human_gate` — must carry a highest-risk justification or QA flags it for demotion.
- D: `automated` — run cards + weekly spot-check.

## QA stage: dark-factory holdout, incorporated

Adapted from the StrongDM Dark Factory pattern (information barrier between builder and evaluator):

- The deterministic auditor re-derives every expectation from the SOURCES (atlas.json + schema
  requirement lists) and grades built artifacts blind. It re-runs lint itself; it never trusts
  generator logs or CONTROL_STATE claims.
- Scoring: weighted holdout (critical=3, major=2, minor=1; PASS/PARTIAL/FAIL;
  satisfaction threshold 0.75). Verdicts: allow / revise / block.
- Criteria live in `<package>/.holdout/` (gitignored). The builder reads findings only
  (`exports/qa_findings.md`): WHAT failed, never the criteria or weights.
- Judgment criteria (spine falsifiability, concept map reads as why-not-steps, owner-language
  cards) are marked `llm_required` and graded by a blind LLM pass via the dark-factory-qa skill.
- Hard gates include a leak scan (emails, phones, SSN patterns, API keys) — any hit is a
  critical FAIL and a blocking verdict; leak findings are never auto-healed.

## Self-healing from QA feedback

`heal -> validate -> QA` loops until stable (max per policy). Two fix classes, never mixed:

| Class | Examples | Action |
|---|---|---|
| AUTO (derivable by convention) | stale exports, missing prompt stubs, telemetry blocks, supervision blocks, automation_policy, CONTROL_STATE sync | applied silently, re-QA'd |
| PROPOSAL (meaning or risk) | TODO fills, runtime assignment (suggestion attached), golden grades, H-gate justification, leak findings | queued in `exports/repair_proposals.json` for the human-over-the-loop queue |

Evidence from the worked example: HSD4 cards generated before the policy existed were caught by
QA (REVISE, 0.81, 2 auto-fixable), healed in one pass (supervision + policy injected on 6 cards),
re-QA'd to ALLOW (0.97, zero fails). Final human queue: 3 pending golden grades + the blind LLM
pass. Nothing inline waits.

## Telemetry as contract (run cards)

Every node card requires `telemetry.run_card_required`, metrics, and an artifact path; QA fails
the package otherwise (critical). Compiled agents (S6) emit per-run cards via `runcard.py`:
run/gate outcomes, confidence, model + prompt versions, cost, refusals with reasons,
`external_actions_taken` (0 unless the lane allows), and escalations that auto-queue to
`process/run-cards/_review_queue/`. Run cards are the promotion evidence and the Improver's food.

## Pipeline command

One command, end to end: `python3 scripts/run_pipeline.py concepts/<slug>` — synthesize, cards,
validate, QA, heal loop, re-validate, export, print the human queue. Exit 0 on allow/revise,
1 on block.

## Open decisions for Ankit

1. Satisfaction threshold per lane (0.75 default; raise to 0.9 for send/write/pay/PHI?).
2. Blind LLM QA pass: run via dark-factory-qa manually, or wire as a scheduled weekly cron per package?
3. Promotion automation: keep R2 auto-advance on graded goldens, or require a human click even there?
