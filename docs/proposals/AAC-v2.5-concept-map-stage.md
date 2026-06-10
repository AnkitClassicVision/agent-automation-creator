# AAC 2.5 — S4 Concept-Map Stage (DRAFT PROPOSAL ADDENDUM)

Status: draft for Ankit review. Extends `AAC-v2.5-draft.md`. Not canonical until committed.
Produced from: knowledge_repo integration build, 2026-06-09, Claude Code surface.
Reference implementation: `learning_github/knowledge_repo` (template, 5 scripts, worked example, regression test).

## Problem

The 2.5 draft defines S4 as "Graph + VERIFY" — one artifact. Calibration showed the human needs the
WHY layer rendered separately from the HOW layer or the verify step degrades into rubber-stamping a
flowchart. The knowledge_repo already enforces this discipline for human processes
(Concept Flow Map -> Procedural Map, with a self-correcting alignment loop). This addendum imports it.

## S4 becomes a stage family

| Stage | Name | Does | Artifact out |
|---|---|---|---|
| S4a | ATLAS territory | Interview answers + probe results land as nodes with confidence / provenance / status / proof-slot; spine locked as one falsifiable claim | `atlas/atlas.json` |
| S4b | Concept synthesis | Deterministic generator turns spine -> trunk, clusters -> chunked branches (2-3, no single child), typed edges with why/how; lint-clean river map | `<slug>_concept_map/` (SQLite + JSON + Mermaid exports) |
| S4c | Process graph + cards | Workflow card (nodes, conditional edges, director, three sinks) plus one node card per node carrying deliverable, artifact, owner, runtime mode, gates, telemetry, hard-refuse, kill switch — each traced to its concept node and ATLAS node | `process/workflow.aac.json`, `process/nodes/*.aac.json` |
| S4 VERIFY | Human confirm | seeit/Mermaid render of BOTH layers plus the serves-links between them; human confirms the picture before S5 | combined `exports/agent_map.{mmd,json}` |

Synthesis rules (all deterministic, all lint-enforced):
spine_path -> trunk chain; clusters -> branches chunked 2-3 with bridge concepts when >3; ATLAS edge
types translate (serves->enables, prereq->requires, part-of->part_of, causes->causes, feeds->triggers,
differentiated-by->is_a); `shaky`/`tension` edges NEVER become map edges — they become flags and
validation-backlog rows; the generator refuses with precise fixes rather than emit a dirty map.

## Schema additions (diff against `schemas/aac-card.schema.json`)

Node card adds (all required at S4c):

```json
"concept_ref": "node_mybcat_icp_rules_21bea0",
"atlas_ref": "N105",
"deliverable": "what this node must produce, in owner language",
"artifact": "process/run-cards/<node_id>/"
```

Workflow card adds:

```json
"concept_map_ref": "<slug>_concept_map/knowledge/exports/latest.rivermap.json",
"atlas_ref": "atlas/atlas.json"
```

Schema gap found during integration: `workflow_card.nodes` is typed as an array of strings, but the
HSD4 packet (and this pipeline) use objects `{node_id, runtime_mode, purpose}`. Recommend the 2.5
schema allow both, preferring objects.

## Validation + readiness ladder (lane x ring, applied at S4)

`validate_agent_package.py` checks all three layers and emits `exports/readiness_report.json`:

| Ring | Pass means | Blocked by |
|---|---|---|
| R0 design_scaffold | ATLAS spine locked; concept lint PASS; workflow card structurally valid; crosswalk complete | structural defects |
| R1 read/recommend | zero TODO fields; every C node has model + prompt_ref + eval_ref; concept_ref resolves | unanswered grill fields (counted, named) |
| R2 draft | golden set harvested AND human-graded (>=3, no pending) | pending grades — human gate |
| R3 / R4 | never auto-passed | human gates by definition |

TODO fields carry provenance `assumed` and are counted as blockers: paper gates pass on fiction,
data probes do not. Trunk coverage: every trunk concept must be served by >=1 process node
(membership rolls up the structural tree) or the report warns.

## Traceability contract

`atlas/crosswalk.json` holds the three-layer mapping: ATLAS node <-> concept node <-> process node,
plus synthesized bridges, skipped crosslinks (with reasons), and tension flags. THROUGHLINE checks read it:
Aim (card serves the spine), Ground (claims tie to Evidenced ATLAS nodes or measured probes),
Thread (crosswalk links connect all three layers).

## Skill slot map update

| Skill | Slot |
|---|---|
| ATLAS | S0 index + **S4a territory capture** (was: "S4 territory map") |
| **aac-agent-mapper** (new, local-surface bridge) | S4a-S4c orchestration via knowledge_repo pipeline |
| seeit | S4 VERIFY of the **combined** concept+process render |
| mapit | S2 engine when the subject is an existing human process (unchanged) |
| THROUGHLINE | S7 output gate (unchanged) — now also reads crosswalk.json |

## Worked example (proof)

`knowledge_repo/concepts/hsd4_dispositioner`: built from this repo's public HSD4 packet (redacted refs).
Result: 22 ATLAS nodes -> 23-concept lint-clean river map -> 6 node cards with full traceability.
Readiness: R0 PASS; R1 blocked by 17 named TODO fields; R2 blocked by the 3 pending golden grades —
which are exactly this PR's existing human gates. The pipeline reports the same truth the PR carries.

Regression test: `knowledge_repo/tests/test_agent_pipeline.py` (scaffold -> synthesize -> cards ->
strict validate -> combined export, on a synthetic 12-node atlas).

## Decisions

1. **DECIDED (Ankit, 2026-06-09): S4a/S4b/S4c is REQUIRED for any workflow targeting lanes
   send / write / pay or touching PHI; optional for read/recommend lanes.** Rationale: the HSD4
   calibration showed verify steps rubber-stamp flowcharts when the why-layer is missing; cost is
   minutes per risky agent.
2. Runtime per node stays D / C / A / H per AAC Step 2 (cheapest runtime satisfying the attributes).
   The pipeline now emits a `runtime_suggestion` (mode + signal + reason) on any node left TODO;
   the human assigns the final mode at the grill. Deterministic tooling builds the maps; the agent
   itself mixes deterministic and LLM nodes per node.

## Open decisions for Ankit

1. Schema: allow object form of `workflow_card.nodes` (recommended) or keep strings + separate node list?
2. Where does the package live long-term: knowledge_repo (current), this repo, or per-agent repos?
