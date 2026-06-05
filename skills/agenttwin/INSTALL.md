# AgentTwin — Install Guide

This skill is surface-agnostic. The canonical artifact is the skill bundle in this folder. To activate AgentTwin on each AI surface, add a trigger pointer to that surface's instruction file.

The pointer is a short paragraph that tells the AI on that surface: "when the user asks to diagnose an agent, follow the AgentTwin skill in this location."

---

## Trigger paragraph (copy verbatim into each surface)

```
AgentTwin skill: when the user asks to diagnose, audit, score, map, visualize, or
"AgentTwin" an AI agent / automation workflow / vendor proposal / agent spec, follow
the skill at: <path-to-skill>/SKILL.md. Read SKILL.md, then walk the user's workflow
through AAC 2.0 first, then the v1.1 core rubric (assets/rubric-aac-v1-1.md), build the JSON per
assets/data-schema.md, render via assets/template.html (replace ONLY the agent-data
JSON block), save to /mnt/user-data/outputs/agenttwin-{slug}-{date}.html, present.
Capture the run to OB_mybcat as decision/observation with topics ['agenttwin',
'aac-v2-0', 'aac-v1-1-core', 'agent-diagnostic', '{agent-slug}']. Do not invent missing data — gaps
surface as gaps.
```

Substitute `<path-to-skill>` with the actual install path on each surface.

---

## Surface-by-surface install

### 1. Claude Code (CLAUDE.md)

Install path: `~/.claude/skills/agenttwin/` (user-level) or `./skills/agenttwin/` (project-level).

```bash
mkdir -p ~/.claude/skills/agenttwin
cp -r /path/to/agenttwin-skill/* ~/.claude/skills/agenttwin/
```

Then add the trigger paragraph to your `CLAUDE.md` (with `<path-to-skill>` = `~/.claude/skills/agenttwin`).

### 2. Codex (AGENTS.md)

Install path: anywhere on disk Codex can read. Most natural: `~/codex-skills/agenttwin/`.

```bash
mkdir -p ~/codex-skills/agenttwin
cp -r /path/to/agenttwin-skill/* ~/codex-skills/agenttwin/
```

Add the trigger paragraph to your `AGENTS.md`. Codex follows AGENTS.md the same way Claude Code follows CLAUDE.md.

### 3. Gemini CLI (GEMINI.md)

Install path: `~/.gemini/skills/agenttwin/`.

```bash
mkdir -p ~/.gemini/skills/agenttwin
cp -r /path/to/agenttwin-skill/* ~/.gemini/skills/agenttwin/
```

Add the trigger paragraph to your `GEMINI.md`.

### 4. Claude.ai (web/mobile)

Claude.ai doesn't read skill folders. Install path: User Preferences (Settings → Profile → Preferences).

Add this shorter trigger paragraph to your preferences:

```
AGENTTWIN: When I ask to diagnose, audit, score, map, or "AgentTwin" an AI agent
or workflow, walk AAC 2.0 stored in OB_mybcat under topic 'aac-v2-0', then the v1.1 core rubric under topic 'aac-v1-1-core',
extract elements per the AgentTwin data contract (properties × 5, process_map with
nodes/edges/memory/state/recommendations, all conditional blocks for C and H nodes),
produce the wellness-report HTML matching the v4 visual contract (locked May 16
2026, stored in OB_mybcat under topic 'agenttwin'), save to outputs, present.
Capture the run to OB_mybcat. Do not invent missing data.
```

Claude.ai pulls the rubric + template spec from OB_mybcat at runtime instead of from skill files.

### 5. Hermes (SOUL.md)

Install path: `~/hermes/skills/agenttwin/` or wherever your Hermes loads skills.

```bash
mkdir -p ~/hermes/skills/agenttwin
cp -r /path/to/agenttwin-skill/* ~/hermes/skills/agenttwin/
```

Add the trigger paragraph to your `SOUL.md`.

### 6. File-snapshot-readers (e.g. NotebookLM, vector-search RAGs)

For surfaces that read from a corpus snapshot rather than skill files: drop the entire `agenttwin-skill/` folder into the corpus root. The reader will pick up SKILL.md as a top-level instruction document and use the assets/ files for rubric/schema lookup.

---

## Verification (after install)

On each surface, test with this prompt:

> "AgentTwin this: we have an agent that pulls patients from RevolutionEHR who haven't had an exam in 12+ months, generates a recall message using Claude Sonnet 4.6, runs the message through a validator, then sends via Twilio SMS. No kill switch. No DLQ on the send path. Bre reviews refused messages but coverage drops during her PTO."

Expected behavior: surface reads SKILL.md (or pulls from OB_mybcat for Claude.ai), walks the rubric, asks for any missing detail it can't infer, produces an HTML file at `/mnt/user-data/outputs/agenttwin-recall-outreach-{date}.html`, captures to OB_mybcat.

If the surface produces text-only output instead of HTML: the trigger paragraph isn't being read. Confirm install path and try again.

---

## WIP graduation tracking

This skill is v1, WIP status. Graduates to canonical after 3 successful real-agent runs with operator confirmation. Track progress in OB_mybcat:

```
search_thoughts query="agenttwin run" → should return 3+ run captures before graduating
```

Proposed 3 real agents for graduation: **Recall Outreach** (this example), **After-Hours Intake**, **Rx Fax → RevolutionEHR**.

After graduation, replace "v1 · WIP" version pill in template.html with "v1 · Canonical" and update all surface trigger configs to drop the WIP qualifier.

---

## Maintenance

- **AAC changes** → apply AAC 2.0 creation-gate logic from the repo/root instructions, but do NOT auto-edit the pinned v1.1 rubric snapshot. Re-snapshot `assets/rubric-aac-v1-1.md` only on an intentional AgentTwin skill version bump.
- **Visual template changes** → require operator approval. Modify `assets/template.html` only; the JS renderer reads its data from the same JSON contract regardless.
- **Schema changes** → require a real-agent run that surfaced a missing field. Don't pre-emptively expand the schema. Add the new field to `assets/data-schema.md`, the JSON block in `assets/template.html`, and the corresponding render function in the embedded JS.
