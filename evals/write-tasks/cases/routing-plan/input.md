Here are the requirements for our password reset feature. Write the implementation plan: what phases should we build, in what order, each as one reviewable PR? There is no codebase yet.

FR-001: When a registered user requests a password reset, the authentication service shall email a reset link to the user's registered email address.

FR-002: If a user opens a reset link more than 15 minutes after the reset link was sent, then the authentication service shall reject the reset link.
