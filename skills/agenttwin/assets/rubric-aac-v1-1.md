# AAC v1.1 — 57-Item Evaluation Rubric (Snapshot)

**Pinned version:** v1.1, locked 2026-05-14. Do not auto-update from OB. Re-snapshot only on intentional skill version bump.

Walk this checklist in order when evaluating ANY agentic AI workflow. Items marked `[v1.1]` are new in this version.

## A. PROCESS-LEVEL

1. Work object defined as single noun with explicit in/out scope?
2. Process drawn as a graph with trigger, nodes, edges, queues, decisions, sinks?
3. Every node has single named human owner?
4. Every edge declares latency budget, daily volume, baseline failure rate, data contract, trigger type?
5. Process has happy-path sink + refuse sink + hard-refuse sink?
6. Hidden queues (DLQs, retries) drawn on the map?
7. Implicit decisions made explicit as work elements?
8. No mega-nodes (10+ things)?

## B. WORK ELEMENT

9. Each element is exactly one of 12 canonical types?
10. Each has one input class and one output class?
11. Required fields complete (type, schemas, latency budget, cost budget, failure mode)?
12. Runtime (D/C/A/H) justified by attribute scoring not preference?

## C. RUNTIME ASSIGNMENT

13. Scored: decision class, action consequence, input type, volume × stakes?
14. **[v1.1]** Scored: data classification, provider contract, data residency, retention + deletion?
15. Assigned cheapest runtime satisfying all attributes + constraint dimensions?
16. C element passes runtime eligibility matrix?
17. C + irreversible-unbounded action → STOP downgrade?
18. C + ambiguous input → STOP downgrade?
19. C + novel or value-laden decision → STOP downgrade?
20. **[v1.1]** All tools in stack pass all 4 constraint dimensions?

## D. CLOSED-LOOP PROPERTY CHECKS (per C element)

### BOUNDED
21. Action vocabulary finite, enumerated, code-defined?
22. AI selects parameters but NEVER selects action class?
23. OOD detector with explicit threshold?
24. Explicit refuse path with logged reason?
25. **[v1.1]** Hard-refuse policy classes enumerated for the element's domain?

### GROUNDED
26. Factual claims anchored to retrieved sources?
27. Output schema requires source IDs for factual fields?
28. Validator rejects ungrounded outputs?

### GATED
29. **[v1.1]** Hard-refuse check runs BEFORE any other gate?
30. Input gate: schema + value ranges + content policy + OOD?
31. Output gate: schema + policy + grounding + confidence ≥ floor (0.6 / 0.8 / 0.92)?
32. **[v1.1]** Cross-check policy matches action consequence (unconditional for irreversible-bounded)?
33. Action gate: idempotency + rate + blast radius + sanity?

### OBSERVED
34. Per-run telemetry: input hash, output, model version, latency, cost, confidence, validator outcomes?
35. Control charts on every key metric?
36. Input drift + output drift + confidence drift each monitored independently?
37. Champion-challenger on every model/prompt change?

### GOVERNED
38. Refuse always available, cheap, logged?
39. Confidence thresholds explicit and version-controlled?
40. **[v1.1]** Hard-refuse events audit-logged separately from graceful refuse?
41. Ambiguous inputs route to deterministic fallback (not AI improvisation)?
42. Kill switch + circuit breakers per action class?

## E. SPEC DOCUMENT

43. All 16 spec sections present and complete (Work Object → Ownership + Operations)?

## F. COST DISCIPLINE

44. Tiered routing (cheap first, escalate on low-confidence / high-stakes)?
45. Prompt caching for static system prompts?
46. Right-size retrieval with top-K cap?
47. Input gate refuses malformed before AI call?
48. Cross-check conditional where allowed by action consequence?
49. Rule-expressible work pushed to D not C?
50. Cost alarms per-run, per-day, per-month?

## G. OPERATIONS

51. Named owner with weekly trace-review ritual (10-20 raw traces)?
52. Monthly eval set refresh defined?
53. Quarterly model re-bake defined?
54. Incident response runbook with SEV-1/2/3/4 thresholds and response times?
55. Change management path (Propose → Eval → Canary → Rollout) with approvals per change class?
56. **[v1.1]** Every H element declared terminal / migration-eligible with reason class (Regulatory / Contractual / Risk Policy / Capability Gap / Cultural-Brand)?
57. **[v1.1]** Per-error cost band declared; graduation threshold matches band (≥95% / ≥99% / ≥99.5% / ≥99.9% / not-eligible)?

## Verdict logic

| Failure pattern | Consequence |
|---|---|
| All 57 pass | Production-ready under AAC v1.1 |
| Any A/B/C fail | Redesign process before build |
| Any D fail on a C element | Downgrade element to A or fix gap |
| E fail | Spec incomplete; not ready to hand to builder |
| F fail | Workflow will hemorrhage cost; refactor before deploy |
| G fail | Workflow will silently decay; add operations discipline |

## Mapping rubric → 5 closed-loop properties (for the Summary view)

| Property | Plain name (5th grader) | Rubric items | Failure means |
|---|---|---|---|
| BOUNDED | Stays in its lane | 21–25 | AI can invent actions outside the approved set |
| GROUNDED | Checks its facts | 26–28 | AI makes claims without source backing |
| GATED | Checks before doing | 29–33 + edges 4 (input gate), 5 (output gate), 33 (action gate) | AI can act without validation gates |
| OBSERVED | Nothing is hidden | 34–37 | No telemetry to detect failures or drift |
| GOVERNED | Has a stop button | 38–42 | No human in control when things go wrong |

## Status calibration

- **Healthy** = item passes; property is implemented, documented, monitored, no fails in last 30 days.
- **Needs work** = item is partially implemented OR has documented gaps OR has failed 1–3 times in last 30 days.
- **Broken** = item fails; property is missing, undocumented, OR has failed 4+ times / caused an incident in last 90 days.

When uncertain between adjacent levels, downgrade (lean broken). Visual workplace rule: surface problems clearly.

## Refusal escalation

If the user is asking to ship a workflow that fails the rubric, the surface should:
- State which rubric items fail.
- Offer two paths: (a) fix the gaps and re-evaluate, (b) document why the rubric doesn't apply and capture the exception in OB_mybcat.
- Refuse to silently approve.

This is jidoka — stop the line on defect. AgentTwin stops the line when AAC says stop.

## Source

This rubric is a pinned snapshot of AAC v1.1 (Agent Automation Creator). Canonical source: OB_mybcat thoughts under topic `aac` / `agent-automation-creator`. Locked 2026-05-14. Supersedes AAC v1.0 (formerly MSP-FLOW v1.0).

Do not modify the rubric body in this file. If AAC gets a later core-rubric snapshot, re-snapshot intentionally by bumping the AgentTwin skill version and regenerating this asset.
