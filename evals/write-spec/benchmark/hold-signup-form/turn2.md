Earlier in this conversation I gave you this input:

> Signup form for the web app: email, password, confirm password. Password needs to be strong. Show errors inline. After signing up the user lands on the onboarding page and gets a welcome email.

You replied:

Q-001: Which component displays the signup form and its inline errors?

Q-002: Which service creates the account when the signup form is submitted?

Q-003: Which service sends the welcome email?

Q-004: What does a password need to count as strong: minimum length, and any required character types or blocked passwords? Proposed: at least 8 characters, per NIST SP 800-63B.

Q-005: What exact inline error text is displayed for an invalid email address, for a password that is not strong, and for a confirm password that does not match the password?

Q-006: What makes an email address valid?

Q-007: At which moment is an inline error displayed: when the user leaves a field, or when the user submits the form?

Q-008: What exact inline error text is displayed when the submitted email address is already registered?

Q-009: What are the subject and body text of the welcome email?

Q-010: What does the service do when the welcome email cannot be sent?


My answers:

Q-001: the web client. Q-002: the account service. Q-003: the email service. Q-004: at least 12 characters with at least one digit. Q-005: "Enter a valid email address", "Password must be at least 12 characters and contain a digit", and "Passwords do not match". Q-006: it contains exactly one @ with at least one character on each side. Q-007: when the user submits the form. Q-008: "An account with this email already exists". Q-009: subject "Welcome", body "Thanks for signing up." Q-010: the email service retries once after 5 minutes, then logs the failure.
