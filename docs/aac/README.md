# AAC card artifacts

These files are examples of the deterministic artifacts the GitHub Actions gate validates before agent/workflow changes merge.

The card model follows `docs/AAC-boundary-creation-addendum-v0.1.md`:

- workflow card = the process box
- node cards = bounded work elements
- agent cards = actor/runtime envelopes
- run-card schema = runtime proof contract
- agent registry = accountable inventory of agent envelopes

Run the gate locally:

```bash
python3 scripts/aac_gate.py --all
```

The example workflow is intentionally draft-only. It shows the effective-permission rule: even if a future tool can send or mutate CRM state, the workflow, node, and agent cards constrain the pilot to read/recommend/draft unless a human-approved card change raises the lane.
