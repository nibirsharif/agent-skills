Here is the task list for the password-reset plan.

## 1. Overview

Build it in layers.

## 2. Tasks

### Phase 1: Reset link email and expiry

#### T-1.1: Build password reset

**Covers:** FR-001, FR-002, NFR-001

**Files:** `src/auth/reset.ts`, `src/auth/tokens.ts`, `src/mail/mailer.ts`, `migrations/001.sql`

**Depends on:** T-1.2

**Done when:** it works

#### T-1.2: Add tests

**Covers:** FR-001

**Files:** `test/reset.test.ts`

**Depends on:** None.

**Done when:** tests pass
