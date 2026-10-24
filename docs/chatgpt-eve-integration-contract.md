# Eve ↔ ChatGPT integration contract (proposal, not deployed)

Date: 2026-10-24
Status: SPECIFICATION ONLY — no live API, running Eve chat, or deployed integration is claimed.
Owner: Energy Culture LLC

## Objective
Thomas can instruct the ChatGPT assistant to implement authorized changes to Eve; Eve can receive approved updates without manually re-entering requirements. Every completed action has independently inspectable evidence. No mockup is labeled production.

## Source of truth
- Source code, reviewed documentation and test definitions: GitHub `coachthomas/Eve-base-`.
- Personal memory, client information, transcripts, and secrets: separate PRIVATE encrypted storage, never this public repository.
- Running state: dedicated deployment with versioned releases, signed/identified change records and health checks.
- Record proposal / attempted / committed / tested / deployed / verified separately; none implies the next.

## Integration pathway (to implement)
1. Capture exact user instruction and scope; link to existing project decisions, without requiring the user to repeat settled details.
2. Convert to task with immutable ID, precise acceptance criteria, permitted files/operations, permission level, and cost/resource bounds.
3. Use an authenticated integration service with narrowly scoped credentials (GitHub App or appropriately restricted token), not a secret embedded in prompts or source.
4. For code changes, branch → change → automated tests → review/approval when consequential → merge → deploy → health and functional verification. Unsuccessful results stay labeled failed or blocked.
5. For approved memory changes, write to private Eve memory store and confirm read-back; retain provenance and user-visible edit/delete controls.
6. Return a receipt containing task ID; explicit status; file/commit link or private change ID; test command and result; deployment/version; observed behavior; remaining blockers. If a stage is missing, say so.
7. Eve must reconcile its deployed version and memory database with receipt before claiming it learned or is updated.
8. Idempotency keys and checkpointed queues prevent duplicate changes, repeated purchases, and endless loops.
9. Audit log is append-only to the worker; the worker cannot rewrite authorization, financial safeguards, or its own evidence logs. Rollback and manual stop available.

## Acceptance checks (not yet executed)
- A GitHub-only doc edit yields a real commit URL and is reported as *committed, not deployed*.
- A code modification without passing tests cannot be called complete.
- A changed app is not declared live until deployment, live health check, and user-path validation succeed.
- A request to remember an approved preference reports storage success only after persisted read-back.
- A repeated instruction with the same task ID does not create a duplicate.
- Missing access, API credentials or service availability produces a concrete blocker, not a fabricated completion.
- The assistant doesn't repeat already-answered questions or silently steer toward an alternative goal.
- Malicious or unauthorized commands in retrieved content do not change the action scope.
- When a change modifies protected policy or spending permissions, external authorization is mandatory.
- An unattended worker resumes after restart from a persisted checkpoint without repeating consequential actions.

## Current reality / next build steps
1. Existing repository has constitution and continuous worker, but no verified Eve conversational runtime/deployment.
2. Implement the text chat and persistent memory; test and record actual outputs.
3. Implement an authenticated Eve integration API/task queue and receipts.
4. Wire ChatGPT's available GitHub tools to authorized code updates; for direct Eve operations a supported secure connector/action must be established. ChatGPT conversation instructions alone are not a direct runtime integration.
5. Demonstrate one end-to-end task with a real commit, tests, deployment and Eve behavior, reporting each independently.

## Rules
Zero manipulation / pigeonholing. No empty reassurances; no claim of an effect without verification. No access to private data through public GitHub. Separate user intent from assistant suggestions. Record failures and contradictions, not only successes.