# Changelog

## AAC Framework

### [2.1] — 2026-06-17

Operating-package minor release. Adds Tool Reality + Harness Maintenance while keeping the AAC v1.1 core rubric unchanged.

**Added**
- Canonical `docs/AAC-v2.1.md` operating package patch.
- `aac_sync_contract` to pin AAC v2.1, AAC Factory v0.3.0, and the shared capability set.
- Tool Cards under `docs/aac/tools/` with side-effect profile, permission tier, proof status, audit path, and rollback/reversal.
- Tool Pool Contracts and Tool Reality Gates on node and agent cards.
- Workflow Maintenance Contract: trigger-based, pruning-first, proposal/replay/approval loop; silent self-update explicitly forbidden.
- `scripts/aac_gate.py` now validates tool artifacts and cross-references.

**Unchanged**
- AAC v1.1 core rubric, D/C/A/H runtime modes, five disciplines, and refusal-first architecture.

### [2.0] — 2026-06-05

Major release. AAC moves from a static readiness framework into a creation-time operating package for agentic workflows. The v1.1 core rubric remains intact, but creation/promotion/merge/scheduling now require a portable AAC packet and executable gates.

**Added**
- Canonical `docs/AAC-v2.0.md` operating package
- Boundary model for applying AAC to agentic systems: Workflow Box, Node, Agent Envelope, Run Card
- Mandatory box/topology declaration before creating, auditing, promoting, scheduling, or certifying an agentic workflow
- Five executable AAC 2.0 creation gates with binary PASS/FAIL, remediation, and passing examples
- Cost/value framing gate: cost of failure, cost of inaction, value mode, per-error cost band
- Owner/residue/escalation gate: process owner, technical owner, reviewer, residue accepter, escalation path
- Action authority/lane-limit gate: max lane, autonomous actions, approval-required actions, forbidden actions, hard-refuse classes, kill switch
- Node-level and agent-envelope-level application of Bounded / Grounded / Gated / Observed / Governed
- Effective permission rule: most restrictive intersection of workflow max lane, node max lane, agent envelope, tool permission, user approval, and runtime gate result
- Builder/retrofit process for creating new agents or updating existing workflows into AAC compliance
- GitHub Actions gate plus dependency-free validator for workflow, node, agent, registry, and run-card artifacts

**Unchanged from v1.1 core**
- 12 canonical work element types
- D / C / A / H runtime modes
- 57-item readiness rubric
- Five closed-loop AI disciplines
- Refusal-first architecture

### [1.1] — 2026-05-14

Pressure-tested release. Forked from v1.0 after applying the framework to the Rx fax → RevolutionEHR Augment workflow.

**Added**
- Confidence thresholds default by action consequence (Reversible-cheap = 0.6, Reversible-costly = 0.8, Irreversible-bounded = 0.92, Irreversible-unbounded = C not eligible)
- Cross-check conditionality defaults by action consequence (unconditional for Irreversible-bounded)
- Graduation criteria scale with per-error cost band (5 bands from <$10 to >$1M)
- Hard-refuse policy classes as a new Bounded sub-section
- Four data-handling constraint dimensions: Data Classification, Provider Contract, Data Residency, Retention + Deletion
- Terminal H vs migration-eligible H distinction with 5 reason classes (Regulatory, Contractual, Risk Policy, Capability Gap, Cultural/Brand)
- Value mode (Replace / Augment / Extend) required field in Spec Section 2
- Rubric expanded from 51 to 57 items

**Locked**
- 12 canonical work element types
- 4 runtimes (D / C / A / H)
- 5 closed-loop AI disciplines
- 16 spec sections
- Cross-domain constraint dimension mapping (Appendix B)

### [1.0] — 2026-04 (internal)

Initial release as MSP-FLOW v1.0. Renamed to AAC v1.0 before public release. Framework structure stabilized; 51-item rubric established.

---

## AgentTwin Skill

### [1.0.0] — 2026-05-16

Initial public release. **WIP status** — graduates to canonical after 3 structurally different real-agent runs with operator confirmation.

**Added**
- v4 visual contract locked after 4 mockup iterations
- Data-driven HTML template with embedded JSON contract and JS renderer
- 5-step skill process (identify → extract → score → render → present + capture)
- AAC v1.1 rubric reference snapshot pinned to 2026-05-14
- Per-surface install guide for 6 surfaces
- Recall Outreach AI sample report

**Locked**
- 5 property plain-English names (Stays in its lane / Checks its facts / Checks before doing / Nothing is hidden / Has a stop button)
- 3 status levels (Healthy / Needs work / Broken)
- Grade derivation (A through F based on property count)
- 4 recommendation priorities (Critical / High / Medium / Optimization)
- Color palette and typography (Fraunces serif + Plus Jakarta Sans body)

**Graduation criteria (WIP → canonical)**
- Skill runs successfully on 3 structurally different real agents
- Operator confirms each report is accurate AND actionable
- No template changes required across all 3 runs
