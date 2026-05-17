# AAC — Agent Automation Creator

**A process-first framework for AI-augmented workflow design.**

Most failed AI projects design the AI first and try to fit a process around it. AAC reverses the order. Map the process correctly. Then assign the right runtime to each piece of work. Then apply closed-loop AI discipline only where AI is the runtime.

The result is workflows that are fast, reliable, observable, governed, and cost-disciplined. Not a vibe. A specification.

![Turn Any Process Into an Automated Workflow](docs/turn-any-process-into-a-workflow.png)

---

## What's in this repo

| File | What it is | Who it's for |
|---|---|---|
| [`docs/AAC-v1.1.pdf`](docs/AAC-v1.1.pdf) | The full framework specification, 34 pages, 57-item rubric | Builders, operators, vendors, auditors |
| [`docs/turn-any-process-into-a-workflow.png`](docs/turn-any-process-into-a-workflow.png) | One-page visual explainer: manual chaos vs automated workflow | Execs, clients, prospects |
| [`docs/how-the-workflow-is-built.png`](docs/how-the-workflow-is-built.png) | Deeper visual: 12 primitives, 4 runtimes, 5 disciplines, reference flow | Builders, technical reviewers |
| [`skills/agenttwin/`](skills/agenttwin/) | A drop-in AI assistant skill that runs the AAC rubric on any agent and produces a visual report | Anyone running AI agents |
| [`examples/example-recall-outreach.html`](examples/example-recall-outreach.html) | Fully-rendered sample AgentTwin report | Anyone evaluating the framework |

---

## The framework in one screen

![How the Workflow Is Built](docs/how-the-workflow-is-built.png)

AAC has three layers. You build bottom-up. You cannot skip a layer.

**Layer 1: Process Map.** Draw the workflow before thinking about AI. Three levels of granularity: work elements (atomic, one verb each), nodes (transactional groupings with one owner), processes (the full graph with triggers, edges, queues, sinks).

**Layer 2: Runtime Assignment.** Every work element gets exactly one of four runtimes: Deterministic Code (D), Closed-Loop AI (C), Assisted AI (A), or Human Only (H). The runtime is read off the work's attributes, not chosen by preference. Cheapest runtime that satisfies all constraints wins.

**Layer 3: Closed-Loop AI Framework.** Applies only to work assigned to C. Five disciplines, all required:

| Discipline | What it means |
|---|---|
| **Bounded** | Finite, code-enumerated action vocabulary. AI never picks the action class. |
| **Grounded** | Factual claims tied to retrieved sources. Every claim has a source ID. |
| **Gated** | Input gate, output gate, cross-check gate, action gate. All four must pass. |
| **Observed** | Per-run telemetry. Drift monitored on input, output, and confidence independently. |
| **Governed** | Refusal is always available. Confidence thresholds explicit. Kill switches per action class. |

If any of the five fails, the element runs as Assisted AI until fixed. No exceptions.

---

## Why this exists

AI workflows fail in predictable ways:
- Mega-nodes that do ten things, with no clean rollback
- Implicit decisions buried inside prose ("if it seems urgent, escalate")
- AI selecting the action class instead of just the parameters
- No refuse path, so the system improvises under uncertainty
- Telemetry that's just logs, not control charts
- Cost that creeps because cheap models are never re-benchmarked

AAC names each of these and gives you the structural fix. The 57-item rubric in the PDF walks every check. Pass it = production-ready. Fail any A/B/C item = redesign before build.

The framework has been pressure-tested against two structurally different real workflows: a high-volume, low-stakes Replace mode (after-hours intake at an optometry practice, ~80 calls/day, $0.012 per contact) and a low-volume, high-stakes Augment mode (Rx fax to RevolutionEHR entry, ~5 faxes/day, permanent human approval, $0.048 per fax). The 8 changes from v1.0 to v1.1 came from running the Rx workflow and finding what the original framework missed.

---

## Read the PDF first

The PDF is the canonical spec. 34 pages, 8 parts, 4 appendices, the 57-item rubric. Everything else in this repo refers back to it.

[📄 Download AAC v1.1 (PDF)](docs/AAC-v1.1.pdf)

The four parts that matter most:
- **Part I — Process Mapping Discipline.** The 12 canonical work element types and the rules for composing them.
- **Part II — Runtime Assignment.** The four runtimes and the eligibility matrix that picks among them.
- **Part III — The Closed-Loop AI Framework.** The five disciplines, with the gated reference architecture diagram.
- **Part VIII — Evaluation Rubric (57 items).** The acceptance checklist. Walk it in order.

The two worked examples (Parts VI and VII) show the framework applied end-to-end on real workflows. Read them after the framework parts.

---

## AgentTwin: the diagnostic tool

AAC is the framework. **AgentTwin is the instrument that runs it.**

AgentTwin is a drop-in skill for AI assistants. Point it at any agent, automation, vendor pitch, or workflow spec. It walks the AAC v1.1 rubric, scores every element, and produces a two-view HTML report:

- **Summary view** — a 5th-grader-readable wellness report with a letter grade. For execs, clients, stakeholders.
- **Process Map view** — operator-grade detail with model identity, expandable prompts, node and edge specs, ranked recommendations, memory and state machine views. For builders and auditors.

The 5 disciplines from Layer 3 are renamed for the Summary view:

| Layer 3 discipline | Summary plain English |
|---|---|
| Bounded | Stays in its lane |
| Grounded | Checks its facts |
| Gated | Checks before doing |
| Observed | Nothing is hidden |
| Governed | Has a stop button |

**See it rendered:** [examples/example-recall-outreach.html](examples/example-recall-outreach.html) (open in a browser)

**Install it:**

```bash
# Claude Code (most common)
mkdir -p ~/.claude/skills/agenttwin
cp -r skills/agenttwin/* ~/.claude/skills/agenttwin/
# Then paste the trigger paragraph from skills/agenttwin/QUICKSTART.md into your CLAUDE.md
```

Full per-surface install (Claude Code, Codex, Gemini CLI, Claude.ai, Hermes, file-snapshot readers): see [skills/agenttwin/INSTALL.md](skills/agenttwin/INSTALL.md).

**Test it after install:**

> "AgentTwin this: a daily batch agent that pulls patients from RevolutionEHR who haven't had an exam in 12+ months, generates a recall message using Claude Sonnet via Bedrock, runs the message through a validator, then sends via Twilio SMS. No kill switch. No DLQ on the send path. A human reviewer covers refused messages but coverage drops during PTO."

Expected output: an HTML file with grade **C**, 5 property cards (2 broken, 1 needs work, 2 healthy), 8-node process map, ranked recommendations.

---

## Direct downloads

| Asset | Size | Link |
|---|---|---|
| AAC v1.1 framework spec (PDF) | 250 KB | [docs/AAC-v1.1.pdf](docs/AAC-v1.1.pdf) |
| Workflow infographic (PNG) | 1.8 MB | [docs/turn-any-process-into-a-workflow.png](docs/turn-any-process-into-a-workflow.png) |
| Operating logic infographic (PNG) | 1.6 MB | [docs/how-the-workflow-is-built.png](docs/how-the-workflow-is-built.png) |
| AgentTwin skill bundle | 60 KB | [skills/agenttwin/](skills/agenttwin/) |
| Sample report | 92 KB | [examples/example-recall-outreach.html](examples/example-recall-outreach.html) |

Or grab the whole repo as a zip from the Releases page (right side of the GitHub view).

---

## How to use this framework

### If you're evaluating an existing AI workflow

1. Open `docs/AAC-v1.1.pdf` and jump to Part VIII (the 57-item rubric, page 28)
2. Walk the rubric in order, scoring each item
3. Or: install AgentTwin and let it do the walk for you, producing a visual report

### If you're designing a new AI workflow

1. Read Parts 0 through III of the PDF (frame, process mapping, runtime assignment, closed-loop AI)
2. Complete the 16-section spec document (PDF Part IV)
3. Walk the rubric (Part VIII) before handing to a builder
4. Use AgentTwin to validate during build and after deploy

### If you're a vendor or partner being evaluated against AAC

1. Read the PDF in full
2. Provide your workflow spec following the 16-section structure
3. Your deliverable should pass the 57-item rubric before acceptance

### If you're onboarding a fractional TPL or AI engineer

Day one reading is the PDF. Day two is running AgentTwin against an existing workflow to see the framework applied.

---

## What this framework is NOT

This is one piece of a larger system. AAC and AgentTwin do not provide:

- **Continuous evaluation.** For that, build a regression pipeline against a frozen dataset.
- **Live production telemetry.** For that, instrument your agent with structured logging plus a dashboard.
- **Pre-deployment quality gates.** For that, add an LLM-as-judge step that catches bad outputs before users see them.

A complete agent operations stack has four layers: snapshot diagnostic (AgentTwin), pre-deployment gate, continuous eval, live telemetry. AgentTwin is layer one. Build the rest separately.

---

## Status

**v1.1, May 2026.** Framework locked. AgentTwin v1.0.0 is at WIP status — graduates to canonical after three structurally different real-agent runs with operator confirmation.

The framework is pinned. AgentTwin pulls from it. If AAC moves to v1.2, that is a deliberate re-snapshot, not auto-propagation.

---

## License

MIT. See [LICENSE](LICENSE). Use freely. Modify. Fork. Credit appreciated but not required.

---

## Credit

Authored at [MyBCAT](https://mybcat.com), a healthcare BPO running AI-augmented operations across 70+ optometry and medical practices. AAC was built to solve a real problem: how do you ship AI agents that pass an audit, survive a vendor handoff, and don't burn money. The framework is what we use internally. The PDF and AgentTwin skill are what we share publicly.

If you use this framework and find it useful, drop a note. If you find a gap, open an issue. If you build something on top, send a link.

---

## Contributing

Issues and pull requests welcome. Two contribution paths:

1. **Framework gaps.** If you apply AAC to a real workflow and the rubric misses something, open an issue describing the workflow, the missing check, and the closed-loop property it relates to. Real-world precedent required; no speculative additions.
2. **AgentTwin surface installs.** If you wire AgentTwin into a new AI surface, send a PR adding the install pattern to `skills/agenttwin/INSTALL.md`.

What's locked and not open to change: the five disciplines, the four runtimes, the three status levels (Healthy / Needs work / Broken), the color palette, the typography. Fork if you need different choices. Diluting the framework's calibration is not in scope.
