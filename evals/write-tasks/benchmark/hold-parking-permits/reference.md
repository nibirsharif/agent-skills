Set: hold. A pasted plan and no codebase: the plan write-plan 0.14.0 gave for its own benchmark input of the same name. Four phases, eleven IDs, two blocked entries.

IDs (11): Phase 1: FR-002, FR-003, FR-004, FR-005, NFR-002. Phase 2: FR-001, NFR-001. Phase 3: FR-006, FR-007. Phase 4: FR-008, FR-009.

Order (the first task is earlier in the phase than the second):
- O1: Phase 1: the task that creates an application comes before the task that rejects one for a plate with a valid permit.
- O2: Phase 1: creating an application comes before approving one, and before rejecting one with a reason.
- O3: Phase 3: the permit-issued event comes before the email that it triggers.
- O4: No task of Phase 2, 3, or 4 is depended on by a task of an earlier phase, and every cross-phase dependency names a real task.

Manual:
- M1: no ID is `manual:`. The plan gives each a test: integration tests for the emails, a load test for NFR-001, a controlled clock for FR-007, a test of the purge job for NFR-002. An email "arriving in an inbox" as a manual check saves work a test can do.

Files: every file is `new:`. A path is invented.

Blocked: `Blocked by Q-001: permit cost in each zone` and `Blocked by Q-002: limit on visitor permits per household`, each copied once, word for word, and not merged. No task builds payment or visitor permits.
