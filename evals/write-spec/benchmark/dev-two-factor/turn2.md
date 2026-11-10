Earlier in this conversation I gave you this input:

> Add two-factor authentication to login.

You replied:

Q-001: Which service performs the login and the second-factor check?

Q-002: Which second factor must the login require: a code from an authenticator app, an SMS code, an email code, or another factor?

Q-003: For which accounts is the second factor required: all accounts, or only accounts that enable it?

Q-004: What does the service do when a user submits an incorrect or expired code?

Q-005: How many consecutive incorrect codes are allowed for one account before the service responds?

Q-006: What does the service do once that number of consecutive incorrect codes is reached?

Q-007: How many seconds is a code valid after it is issued?


My answers:

Q-001: the auth service. Q-002: a 6-digit code from an authenticator app. Q-003: only accounts that enable it. Q-004: reject the login and display "Incorrect code". Q-005: 5. Q-006: lock the account for 15 minutes. Q-007: 30 seconds.
