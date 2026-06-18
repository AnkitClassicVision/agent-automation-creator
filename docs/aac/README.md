# AAC card artifacts

These files are examples of the deterministic artifacts the GitHub Actions gate validates before agent/workflow changes merge. AAC card versions are `2.0`.

The card model follows canonical [`docs/AAC-v2.0.md`](../AAC-v2.0.md):

- workflow card = the process box
- node cards = bounded work elements
- agent cards = actor/runtime envelopes
- run-card schema = runtime proof contract
- agent registry = accountable inventory of agent envelopes

The loop model follows [`loop-architecture.md`](loop-architecture.md): a loop is the bounded
improvement system, a gate/router chooses repeat/repair/escalate/exit/promote, and AAC Factory is
one intervention-builder inside larger business/life loops.

Run the gate locally:

```bash
python3 scripts/aac_gate.py --all
```

The example workflow is intentionally draft-only. It shows the effective-permission rule: even if a future tool can send or mutate CRM state, the workflow, node, and agent cards constrain the pilot to read/recommend/draft unless a human-approved card change raises the lane.
