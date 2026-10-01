Break the password-reset plan into tasks. There is no codebase in this folder, and neither file is on disk. This is docs/specs/password-reset/plan.md, Phase 2 only:

```markdown
### Phase 2: Set a new password

**Scope:** Accept a new password through a valid reset link.

**Requirements:** REQ-003, REQ-004

**Size:** about 4 files

**Reuse:** None found.

**Interface and data changes:**

- `POST /auth/password-reset/confirm` accepts a reset token and a new password

**Verify:**

- REQ-003: integration test that a valid token and a new password update the password
- REQ-004: unit test that a password of 11 characters is rejected

**Open questions:** None.
```

And this is the functional section of docs/specs/password-reset/requirements.md:

```markdown
## 3. Functional Requirements

REQ-001: When a registered user requests a password reset, the authentication service shall email a reset link to the user's registered email address.

REQ-002: If a user opens a reset link more than 15 minutes after the reset link was sent, then the authentication service shall reject the reset link.

REQ-003: Withdrawn.

REQ-004: If a user submits a new password shorter than 12 characters, then the authentication service shall reject the new password.
```
