# AgentTwin — Quick Start

You just unzipped the AgentTwin skill bundle. Here's how to install it.

## 30-second version (Claude Code)

```bash
# 1. Copy the bundle into your Claude Code skills folder
mkdir -p ~/.claude/skills/agenttwin
cp -r ./agenttwin-skill/* ~/.claude/skills/agenttwin/

# 2. Add this paragraph to your ~/.claude/CLAUDE.md
```

Paste this trigger paragraph into your `CLAUDE.md`:

```
AgentTwin skill: when I ask to diagnose, audit, score, map, visualize, or
"AgentTwin" an AI agent, automation workflow, vendor proposal, or agent spec,
follow the skill at ~/.claude/skills/agenttwin/SKILL.md. First identify the
workflow box and control topology (unit / graph-directed / agent-directed
envelope / hybrid). Assess workflow health, node health, and agent-envelope
health against AAC 2.0, then walk the v1.1 core
rubric (assets/rubric-aac-v1-1.md), build the JSON per assets/data-schema.md,
render via assets/template.html (replace ONLY the agent-data JSON block), save to
/mnt/user-data/outputs/agenttwin-{slug}-{date}.html, present. Do not invent
missing data — gaps surface as gaps; if the box is undefined, report FAIL: box
undefined.
```

## Test it

In a new Claude Code session, paste:

> "AgentTwin this: a daily batch agent that pulls patients from RevolutionEHR who haven't had an exam in 12+ months, generates a recall message using Claude Sonnet via Bedrock, runs the message through a validator, then sends via Twilio SMS. No kill switch. No DLQ on the send path. A human reviewer covers refused messages but coverage drops during PTO."

Expected output: an HTML file at `agenttwin-recall-outreach-{date}.html` with a letter grade (should be **C**), 5 property cards (2 broken, 1 needs work, 2 healthy), 8-node process map, and a ranked recommendations list.

## What's in this bundle

| File | Purpose |
|---|---|
| `SKILL.md` | The 5-step process an AI assistant follows when you trigger it |
| `INSTALL.md` | Detailed install for 6 surfaces (Claude Code, Codex, Gemini, Claude.ai, Hermes, file-snapshot readers) |
| `assets/template.html` | Data-driven HTML template — replace the JSON block, get a new report |
| `assets/rubric-aac-v1-1.md` | The 57-item framework reference |
| `assets/data-schema.md` | JSON contract between rubric and template |
| `assets/style-guide.md` | Plain-English mappings + color + typography discipline |
| `assets/exemplar.html` | Fully-rendered sample report (Recall Outreach AI) |

## Other install paths

- **Codex** → `~/codex-skills/agenttwin/`, trigger in `AGENTS.md`
- **Gemini CLI** → `~/.gemini/skills/agenttwin/`, trigger in `GEMINI.md`
- **Hermes** → wherever Hermes loads skills, trigger in `SOUL.md`
- **Claude.ai** → User Preferences (no filesystem); see INSTALL.md §4 for the prefs-friendly trigger

Full details: see `INSTALL.md`.

## What you're agreeing to

This skill follows opinionated discipline. It will:
- Refuse to invent data — gaps surface as fails
- Use locked plain-English property names (Stays in its lane / Checks its facts / etc.)
- Use 3 status levels (Healthy / Needs work / Broken — no "yellow")
- Downgrade when between two statuses
- Produce HTML output you can screenshot, share, or archive

If you need different choices, fork the skill rather than overriding silently.

## Verification

The skill should produce a report nearly identical to `assets/exemplar.html` when given the recall outreach test prompt. If your output diverges significantly: the install isn't quite right, the trigger paragraph isn't being read, or the assistant is filling in too many gaps with invented data. Re-check the install path and try again.

---

**Version:** 1.0.0 (May 2026, WIP — graduates to canonical after 3 successful real-agent runs)
**License:** MIT
**Source:** github.com/[your-org]/agenttwin (if you have access to the public repo)
