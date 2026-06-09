# MyBCAT Outreach Rules v0.1 (DRAFT)

Status: assembled by the interviewer from Ankit's documented writing preferences and MyBCAT positioning. Needs Ankit's confirmation before it becomes the eval_ref target. This is the machine-readable home for "context rules, writing rules, passes QA".

Target repo path: `evals/mybcat-outreach-rules.md`
Consumed by: hsd4-draft-outreach node (eval_ref) and the Evaluator.

## Voice

1. Register: peer to practice owners. MyBCAT Sales and Marketing voice. Warm, direct, zero corporate filler.
2. Short sentences. One idea per sentence.
3. Specific numbers over vague claims. Any statistic carries a source id.
4. No em-dashes.

## Banned words

leverage, seamless, holistic, synergy, unlock, streamline, robust, empower, game-changer, revolutionize, cutting-edge, world-class.

## Content rules

5. Identify as MyBCAT in every message. No pretending a prior relationship exists.
6. Grounded: every claim about the recipient traces to a source id (their site visit, their practice, public info). No invented details, no fake personalization.
7. One CTA per message.
8. Length caps: email 120 words max, SMS 300 characters max.
9. No pricing promises, no competitor claims, no guarantees of outcomes.

## Hard refuse (zero exceptions)

10. PHI in any outreach.
11. Any contact on the do-not-contact list or without a consent basis.
12. Sending, CRM mutation beyond hs_lead_status, or sequence enrollment while lane is draft.

## QA pass definition

A draft passes QA when all are true: zero banned words, length cap respected, exactly one CTA, every recipient-specific claim sourced, register check passes, no hard-refuse trigger. This is the machine check behind "20 consecutive no-edit approvals".
