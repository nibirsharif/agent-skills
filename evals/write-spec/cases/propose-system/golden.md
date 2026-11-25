Q-001: Which system rejects a reading that a field device uploads with a timestamp later than the time of the upload? Proposed: the meter service.

Draft: If a field device uploads a reading with a timestamp that is later than the time of the upload, then the [Q-001] shall reject the reading and return HTTP status 422.
