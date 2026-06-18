# AAC loop architecture

Status: canonical design note, locked by Ankit on 2026-06-18.

AAC uses this loop model for agentic workflow creation, audit, promotion, and retrofit work. It does not replace the AAC v1.1 core rubric or the AAC v2.0 operating package. It names the parent structure that decides when AAC Factory should build or repair an intervention.

## Core sentence

> A loop is a bounded improvement system with an objective function, gates, proof, promotion rules, and human-over-loop residue ownership. AAC Factory is one intervention-builder inside that loop.

## Object hierarchy

```text
Parent System
└── Loop
    ├── Objective Function
    ├── Evidence Inputs
    ├── Gate / Router
    ├── TBR Gate
    ├── Boundary Maps
    ├── AAC Factory Intervention
    ├── Evidence Envelope / Run Card
    ├── Champion-Challenger + Holdout
    ├── Improvement Ledger
    ├── Readiness Ladder
    └── Human-over-loop
```

## Loop

A loop is any bounded cycle that reads evidence, decides what to do next, and improves or exits.

A loop can wrap:

- a card;
- a node;
- a QA check;
- a runtime improvement lane;
- a whole AAC Factory package;
- a whole business or life process.

Loop scope is fractal. The same structure can govern a small node repair or a full business process.

## Gate / Router

A gate is not the loop. A gate is the router inside or at the edge of the loop.

A gate reads evidence and chooses one of five actions:

```text
repeat
repair
escalate
exit
promote
```

This keeps loops from becoming endless spinning. Every loop needs a clear exit condition, a repair path, and an escalation path.

## Objective Function

The objective function says what better means.

Every C/A judgment node should have an objective. Larger loops should also name their objective, even when the measurement is qualitative or business-facing.

Examples:

- increase golden accuracy without new hard-refuse violations;
- reduce operator follow-up time without losing traceability;
- improve booking completion while preserving consent and payment boundaries;
- reduce recovery leakage while keeping external sends human-approved.

## TBR Gate

TBR is the meaning / permission / proof wrapper.

- **Translator:** what does this term, field, decision, or artifact mean?
- **Bouncer:** is this actor allowed to read, write, decide, or route here?
- **Recorder:** what evidence proves what happened?

TBR belongs inside the loop gate stack. It prevents a loop from improving the wrong thing, accessing the wrong thing, or claiming progress without proof.

## Boundary Maps

Three prior AAC Factory concepts make loop execution safe and inspectable:

1. **Context Authority Map** — separates instruction vs data, trusted vs untrusted, tenant/scope, and allowed effects.
2. **Resource Envelope** — caps tokens, money, runtime, tool calls, turns, retries, and review pressure.
3. **Contract Surface Map** — shows where contracts are enforced: schema, prompt, tool gateway, runtime, telemetry, and QA.

These are not new frameworks. They are the boundary layer that makes loop behavior auditable.

## AAC Factory Intervention

AAC Factory should be invoked only after the parent loop identifies that an agentic/process intervention is the right move.

Bad containment:

```text
AAC Factory
└── Loop Card
```

Correct containment:

```text
Business / Life Loop
└── Gate identifies needed intervention
    └── AAC Factory builds or repairs the intervention
        └── Card, node, QA, run-card, and improvement loops improve it
            └── Evidence returns to parent loop
```

AAC Factory can contain loops, but it also sits inside larger loops.

## Evidence Envelope / Run Card

The run card is the evidence envelope for one execution. It should preserve enough proof to replay, audit, or dispute the claim.

Expected evidence includes, where applicable:

- workflow, node, and run identifiers;
- prompt/config/policy version or hash;
- model identity and verification status;
- input/output refs or hashes;
- retrieval/tool payload refs or hashes;
- gate outcomes;
- cost, latency, and usage, using `unknown` rather than fake zero when unavailable;
- human edit diff when relevant;
- final artifact ref or hash.

## Champion-Challenger + Holdout

Improvement requires an information barrier.

- Champion = current approved behavior.
- Challenger = proposed model, prompt, threshold, policy, or node change.
- Open split = used for iteration.
- Holdout = sealed truth set used once for promotion.

A challenger does not promote because it looks better in development. It promotes only when it passes the relevant gate and holdout policy.

## Improvement Ledger

The improvement ledger records learning over time.

Each entry should answer:

- what changed;
- what objective it targeted;
- what evidence supported it;
- what gates re-ran;
- whether it was adopted, queued, or rejected;
- who owns any remaining residue.

## Readiness Ladder

Readiness remains explicit.

- **R0:** structure exists.
- **R1:** required fields/contracts are complete.
- **R2:** human-graded goldens and QA evidence support design-time confidence.
- **R3:** shadow/live-limited lane with sampling and run-card proof.
- **R4:** scaled lane with ongoing monitoring and promotion controls.

A loop can improve an artifact, but the readiness ladder decides whether it can promote.

## Human-over-loop

Human-over-loop means the human owns promotion, residue, and risk, not every micro-step.

Humans stay responsible for:

- golden grading;
- residue statement signing;
- irreversible or external actions;
- lane promotion;
- policy exceptions;
- deciding that a capability gap has become migration-eligible.

The loop should minimize unnecessary inline approval while preserving human authority where consequence, policy, or trust requires it.

## Artifact names

Do not create a vague top-level `Loop Card` unless no narrower artifact works. Prefer:

- **Loop Spec** — describes the parent improvement cycle.
- **Gate Card** — describes one router decision.
- **Node Card** — describes one bounded work element.
- **Run Card** — proves one execution.
- **Improvement Ledger** — proves learning over time.

## Locked map

```text
Parent System
└── Loop
    ├── Objective Function
    ├── Evidence Inputs
    ├── Gate / Router
    │   ├── repeat
    │   ├── repair
    │   ├── escalate
    │   ├── exit
    │   └── promote
    ├── TBR Gate
    │   ├── Translator
    │   ├── Bouncer
    │   └── Recorder
    ├── Boundaries
    │   ├── Context Authority Map
    │   ├── Resource Envelope
    │   └── Contract Surface Map
    ├── Intervention
    │   └── AAC Factory
    │       ├── Workflow card
    │       ├── Node cards
    │       ├── QA
    │       ├── Run cards
    │       └── Improvement ledger
    └── Readiness / Promotion
        ├── Champion-challenger
        ├── Holdout
        ├── Readiness ladder
        └── Human-over-loop
```
