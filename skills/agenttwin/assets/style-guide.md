# AgentTwin Style Guide

How AgentTwin reports look and sound. Apply consistently.

## Plain-English property names

The 5 closed-loop properties have a formal AAC name and a 5th-grader-readable name. Always show both — plain name as the card title (large), formal name as a small caps subtitle below.

| Formal (AAC) | Plain (Summary card title) | What it means in one sentence |
|---|---|---|
| Bounded | Stays in its lane | The agent can only do things from a short approved list. It can't invent new actions. |
| Grounded | Checks its facts | When the agent says something, it should be looking it up first — not guessing from memory. |
| Gated | Checks before doing | Before the agent does anything real, something double-checks the message and recipient. |
| Observed | Nothing is hidden | We can see exactly what the agent did, when, and how confident it was. |
| Governed | Has a stop button | A real person is in charge — and can shut the agent down in one click. |

These names are **locked**. Do not paraphrase. Consistency across reports makes the framework recognizable.

## Status names

Three only. No "mostly working." No "partially complete." No "yellow."

| Status | When to use | Color |
|---|---|---|
| **Healthy** | Property is implemented, documented, monitored, and has not failed in the last 30 days. | Green (#15803D) |
| **Needs work** | Partially implemented OR has documented gaps OR has failed 1–3 times in last 30 days. | Amber (#B45309) |
| **Broken** | Missing, undocumented, OR has failed 4+ times / caused an incident in last 90 days. | Red (#BE123C) |

When between two levels, downgrade. Surface problems clearly.

## Grade derivation

| Grade | Rule |
|---|---|
| A | All 5 healthy |
| B | 4 healthy, 1 needs-work, 0 broken |
| C | ≥ 1 broken OR ≥ 2 needs-work |
| D | 2+ broken |
| F | 3+ broken OR AAC §A/B/C category kill (process not graphable, work elements undefined, runtime mis-assigned) |

## Language rules — Summary view

Read by non-technical operators, clients, and clinicians. Strict rules:

1. **No jargon.** "Hallucinations" → "makes things up." "Latency p99" → "how fast." "Idempotency" → "doesn't double-do."
2. **Active voice.** "The agent makes things up" not "Hallucinations are observed."
3. **Concrete behavior.** "Texts patients old clinic hours" not "Has data freshness issues."
4. **Specific fix.** "Pull clinic hours from the live system on every send" not "Improve data sourcing."
5. **No acronyms** in Summary cards. Move them to Process Map only.
6. **Sentence case** for everything except proper nouns. Not "Stays In Its Lane."

## Language rules — Process Map view

Read by operators, engineers, vendors, auditors. Technical precision allowed:

1. **Cite specific systems.** "Pull from `clinic_config.live_hours` in RevolutionEHR" not "the system."
2. **Cite specific people.** "Owner: Vince" not "the team."
3. **Cite specific time windows.** "SLA: 4 business hours" not "soon."
4. **Use real model strings.** "claude-sonnet-4-6-20260301" not "Claude Sonnet."
5. **Numbers, not adjectives.** "~600 messages / day" not "high volume."

## Typography

- **Display font:** Fraunces (Google Fonts), 400–800. Used for: section titles, card titles, headlines, grade letter, action plan numbers. Italic 400/500 for accent words. Loads via Google Fonts CDN.
- **Body font:** Plus Jakarta Sans (Google Fonts), 400–700. Used for: all body text, labels, metadata, badges.
- **Monospace:** System monospace stack (`ui-monospace, "SF Mono", Menlo, Consolas, monospace`). Used only inside prompt blocks for code/prompt content.

Do not substitute fonts. Do not add new fonts. Do not use Inter, Roboto, Arial, or any system default font.

## Color palette

Locked. Use the CSS variables defined in `template.html` `:root`.

| Variable | Hex | Purpose |
|---|---|---|
| `--cream` | `#FAF7F2` | Body background |
| `--paper` | `#FFFFFF` | Card background |
| `--ink` | `#1A1B1F` | Primary text |
| `--muted` | `#6B6D73` | Secondary text |
| `--line` | `#E8E5DE` | Borders |
| `--brand` | `#0F766E` | Teal accent (links, brand) |
| `--success` | `#15803D` | Healthy state |
| `--warning` | `#B45309` | Needs-work state |
| `--danger` | `#BE123C` | Broken state |
| `--type-d` | `#0369A1` | Deterministic (blue) |
| `--type-c` | `#A16207` | Cognitive (amber) |
| `--type-a` | `#7E22CE` | Approval (purple) |
| `--type-h` | `#475569` | Human (slate) |

Each color has a `--{name}-soft` companion (light tint) for backgrounds, and many have an `--{name}-ink` darker variant for text on light backgrounds.

Do not add colors. Do not substitute.

## Card style

- **Border radius:** 20px for primary cards, 12–16px for nested.
- **Padding:** 22px–28px for primary cards, 12px–14px for nested.
- **Border:** 1px solid `--line` default; 1.5px solid status color when status-coded.
- **Shadow:** None. Stay flat.
- **Background:** `--paper`. Cards with broken status get a subtle gradient: `linear-gradient(to bottom right, var(--paper) 60%, var(--danger-soft) 220%)`.

## Iconography

- **Property icons:** Hand-drawn line SVGs at 24×24, 1.8 stroke. One per property. See `exemplar.html` for the locked icon set.
- **Status dots:** 8–10px filled circles. Color = status.
- **Type pills:** Tiny 9px font, 3px padding, 4px border-radius. Use the matching type color.
- **No emojis.** Anywhere. The clinical / professional context doesn't permit them.

## Section ordering

The two views have a strict section order. Do not rearrange.

### Summary view
1. Headline + eyebrow
2. Before/After toggle
3. Grade card (grade circle + verdict text + count pills)
4. Section heading: "The 5 things every AI agent needs"
5. 5 property cards (in canonical order: Bounded, Grounded, Gated, Observed, Governed)
6. Compare card ("The Twin")
7. Action card ("Your Fix List")

### Process Map view
1. Headline + eyebrow
2. Map overview (flow at a glance, with lane + runtime legends, vertical node list + edge connectors + branch dividers)
3. Recommendations card (ranked list with priority badges)
4. Section heading: "Cross-cutting"
5. Memory card
6. State machine card
7. Section heading: "Steps · N nodes"
8. Node detail cards (in order)
9. Section heading: "Connections · N edges"
10. Edge detail cards (in order)

## Things that are NOT allowed

- Emojis (anywhere)
- New fonts beyond Fraunces and Plus Jakarta Sans
- New colors beyond the CSS variables
- "Yellow" status (use "needs work")
- Bold red text in the Summary (the colored card border + badge is enough)
- Paraphrasing the 5 property plain-names
- Decorative imagery, illustrations, stock photos
- More than 3 items in the Summary Action Plan
- More than 4 priority levels in Recommendations (Critical / High / Medium / Optimization — no more)

## Print + screenshot behavior

The report is regularly screenshotted for decks, vendor conversations, and client meetings. Verify:
- The Summary view fits cleanly in a portrait screenshot at 720px width.
- The Process Map flow overview fits on one screen height on most laptops.
- Detail cards each fit a single screenshot at common screen sizes.

Test by viewing the rendered HTML in a 720×1280 mobile viewport. If anything wraps awkwardly, fix the data, not the template.
