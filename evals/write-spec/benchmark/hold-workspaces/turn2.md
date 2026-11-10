Earlier in this conversation I gave you this input:

> Team workspaces in the notes service: a workspace has members and one or more admins. Admins invite people by email; an invite is valid for 72 hours. Members can read and edit every note in the workspace. Only admins can delete notes. When the last admin leaves, the oldest member becomes admin.

You replied:

FR-001: When an admin of a workspace submits an invitation for an email address, the notes service shall send the invitation to that email address.

FR-002: When a member of a workspace requests a note in that workspace, the notes service shall return the note.

FR-003: When a member of a workspace submits an edit to a note in that workspace, the notes service shall store the edit.

FR-004: When an admin of a workspace requests deletion of a note in that workspace, the notes service shall delete the note.

FR-005: If a member of a workspace who is not an admin requests deletion of a note in that workspace, then the notes service shall not delete the note.

Q-001: From which instant is an invitation valid for 72 hours? Proposed: from the time the invitation is sent.

Q-002: What does the notes service do when a person accepts an invitation after its 72 hours have passed? Proposed: reject the acceptance.

Q-003: Does "oldest member" mean the member who joined the workspace earliest, or the member with the oldest account?

Q-004: What does the notes service do when the last admin leaves and the workspace has no other members?

Q-005: Can admins also read and edit notes, or only members who are not admins?

Q-006: What does the notes service do when an admin submits an invitation for an invalid email address?


My answers:

Q-001: accept. Q-002: accept. Q-003: the member who joined the workspace earliest. Q-004: the notes service deletes the workspace. Q-005: admins are members, so yes. Q-006: reject the invitation and display "Enter a valid email address".
