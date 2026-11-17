Set: dev. Ten written requirements and two withdrawn lines, limit 8 per phase. One withdrawn line moved to an `NFR`.

Written IDs (10): FR-001, FR-003, FR-004, FR-005, FR-006, FR-007, FR-009, FR-010, NFR-001, NFR-002.

Not planned: FR-002 (`Withdrawn. Moved to NFR-002.`) and FR-008 (`Withdrawn.`) appear in no phase.

Phase count: 2 to 4.

Before (the first is in the same phase as the second, or an earlier one):
- D1: FR-001 before FR-003. Edit access is a setting of a share.
- D2: FR-001 before FR-004. A revocation needs a share.
- D3: FR-001 before FR-005.
- D4: FR-001 before FR-009. The panel lists shares.
- D5: FR-006 before FR-007. A link expires after it exists.

Together (same phase):
- T1: NFR-002 with FR-004, the response it limits.
- T2: FR-006 with FR-007: a link and its expiry.
- T3: NFR-001 in a later phase whose scope says why it can be met afterwards, or in a behaviour phase.
- T4: FR-010 is in the first phase that changes access, or in an earlier one. Placed after, the earlier phases change access with no log and must be reopened.

Blocked: none. Section 3 is `None.`

One sensible cut: shares with users (FR-001, FR-003, FR-004, NFR-002, FR-005, FR-010); the sharing panel and public links (FR-009, FR-006, FR-007); availability (NFR-001).
