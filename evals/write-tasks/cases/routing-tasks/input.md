Here is the implementation plan for our password reset feature. Can you break Phase 1 into small tasks we can work through one at a time, each with a way to tell it's done? There is no codebase yet.

```markdown
### Phase 1: Reset link email and expiry

**Scope:** Send the reset link and reject an expired link.

**Requirements:** REQ-001, REQ-002

**Size:** about 5 files

**Reuse:** None found.

**Interface and data changes:**

- `POST /auth/password-reset` accepts an email address
- `password_reset_tokens` table with a `sent_at` column

**Verify:**

- REQ-001: integration test that a reset request for a registered user sends one email with a link
- REQ-002: unit test that a link opened 15 minutes and 1 second after `sent_at` is rejected

**Open questions:** None.
```
