# AAC 2.0 gate calibration records

Use this folder to save the three required gate runs before calling a new AAC 2.0 gate calibrated for a repo or surface.

For each run, record:

- source prompt/spec path
- expected confidence before the gate
- start/end time and duration
- gates passed
- gates failed
- exact remediation applied
- before artifact
- after artifact
- reviewer/owner decision

Required set:

1. One confident prompt/spec expected to pass.
2. One under-specified prompt/spec expected to fail.
3. One middle case expected to reveal hidden owner, authority, cost, or observability gaps.

Do not backfill fake "passes." A confident prompt failing is a calibration win.
