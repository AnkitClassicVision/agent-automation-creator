# Calibration record: HSD4 dispositioner grill

Target repo path: `docs/aac/calibration/2026-06-09-hsd4-dispositioner.md`

- Source prompt/spec: raw idea, "Awareness/Heartbeat agent" (resolved mid-grill to HSD4 dispositioner lane)
- Case type: under-specified spec, expected to partially fail
- Expected confidence before gate: medium (subject was believed to be a designed first build)
- Date: 2026-06-09, single session on Claude.ai surface
- Duration: not instrumented (clock tool unavailable on this surface; instrument next run)
- Reviewer/owner: Ankit
- Verdict: calibration win. The grill caught a wrong subject, fictional cost numbers, a dead output field, and owner concentration that manual review had passed.

## Gates

| Gate | Result | Note |
|---|---|---|
| G1 Box + topology | FAIL then PASS | Failed on subject identity: the idea resolved to HSD4, not a new agent. Passed after resolution and plain-language re-ask |
| G2 Cost + value | FAIL then PASS | First pass ran on the example card's invented numbers (40/day). Passed only after live data probe (21/day, 47% pollution, 89% undispositioned) |
| G3 Owners + residue | PASS with warning | Single human in all four roles. No rule fired. Should have |
| G4 Authority + lanes | PARTIAL | Lane confirmed (draft). Promotion condition captured but current schema has no field to hold it |
| G5 C-node disciplines | NOT REACHED | Node cards are next phase |

## Remediation applied

Subject resolution step added (S0). Live data probe added (S3). Measured numbers replaced invented ones. lane_promotion field drafted into the 2.5 schema. Owner-concentration warning written into the packet.

## Before / after

Before: a one-line idea with no retrievable brain capture.
After: `hsd4-dispositioner.aac.json` draft packet with per-field provenance, measured Gate 2 numbers, a 6-node graph proposal, and a 3-item golden set pending grades.

## Run records

- 2026-06-06 AAC v2 assess-mode audit: HSD4 appointment-movement was safe only for design scaffold/read-only review-packet/manifest work; production send/write/draft-creation lanes remained blocked. Key gaps were missing node cards, incomplete edge contracts, missing D/C/A/H assignments, weak C-node calibration/model evidence, incomplete observability/cost discipline, and unsigned residue.
- 2026-06-07 HSD4 live read-only run test: live run completed with no external sends/writes and leak scan clean; source health was yellow and the selected inbound item remained context-blocked. Next safe move was to resolve source health and complete identity/HubSpot/Gmail/calendar context before any draft or booking lane.

## Gap log (full)

| ID | Finding | Fix target |
|---|---|---|
| L1 | No prefill contract; interviewer improvised sources and mapping | S1 spec in Flow Interviewer |
| L2 | The "recommended first build" had zero retrievable OB capture; design lived in an old chat | Capture discipline + S0 |
| L3 | No per-field provenance in packet schema | provenance block, 2.5 schema |
| L4 | OB full-text fetch blocked on Claude.ai surface, three attempts ("no approval received"); get_thought throws a server error (missing source_type column) | Infra fix; Pointer-to-Brain risk until fixed |
| L5 | Framework author could not parse the framework's own opening question | Plain-language rule, S2 |
| L6 | No Step 0 subject resolution; author could not tell HSD4 from a new agent | S0 |
| L7 | Gate 3 passed silently with one human in every owner role | Concentration warning rule |
| L8 | Schema cannot express lane promotion; max_lane is static | lane_promotion field |
| L9 | Graduation criteria arrive qualitative ("passes QA") | Propose-defaults A/B rule, S2 |
| L10 | Humans will not author golden examples; they will grade harvested ones in seconds | S5 harvest-and-grade |
| L11 | "Context rules / writing rules / QA" referenced as canonical with no machine-readable home | Outreach rules doc drafted as eval_ref target |
| L12 | Gate 2 passed on invented numbers; output field (hs_lead_status) empty on 89% of live stream | S3 mandatory data probe |

## Decisions locked this run

1. Lane promotion condition: option B. 20 consecutive drafts approved with zero edits enables send, weekly spot-QA after. Interviewer added one floor: any hard-refuse violation also resets the counter. Veto open.
2. The grill is a grading session, not a writing assignment: golden sets are harvested from live systems and graded by the human.

## Open items

1. Ankit grades the 3 golden examples in the packet (right / wrong / edit).
2. Ankit confirms or edits the outreach rules draft (eval_ref target).
3. Version number for the pipeline spec at commit: 2.1 / 2.5 / 3.0.
4. Closed from Hermes on 2026-06-09: HSD4 run records (6/6 audit, 6/7 live read-only test) appended under Run records.
