# Implementation Plan: Backup Verify

**Version:** 1.0
**Date:** 2026-03-04
**Requirements:** requirements.md, version 1.0
**Status:** Draft

## 1. Approach

The checksum is written where the archive is written, in `backup/archive.py`, so every caller gets it. `backup verify` is a second command beside `create`. The nightly run in `backup/schedule.py` verifies its own archive and reports a failure through the mailer and the panel light, which both exist. Two phases: checksums and the command first, then the nightly report, which needs them.

| Phase | Delivers | Requirements |
|-------|----------|--------------|
| 1 | Checksums and the verify command | FR-001, FR-002, FR-003, NFR-001 |
| 2 | Reporting a failed nightly backup | FR-004, FR-005 |

## 2. Phases

### Phase 1: Checksums and the verify command

**Scope:** Write a checksum file beside each archive, and add `backup verify`, which prints `OK` or `CORRUPT` within the time limit. The nightly run does not verify yet.

**Requirements:** FR-001, FR-002, FR-003, NFR-001

**Size:** about 5 files

**Reuse:**

- `backup/archive.py`: `write_archive` writes every archive
- `backup/cli.py`: the `create` command and its parser
- `tests/test_archive.py`: the `unittest` pattern with a temporary folder

**Interface and data changes:**

- `<archive>.sha256` beside each archive, written by `write_archive`
- `verify(archive)` in `backup/archive.py`, which returns whether the checksum matches
- `backup verify <archive>` in `backup/cli.py`

**Verify:**

- FR-001: `write_archive` leaves a `.sha256` file that holds the SHA-256 of the archive
- FR-002: `backup verify` on an untouched archive prints `OK` and exits with status 0
- FR-003: `backup verify` on an archive with one changed byte prints `CORRUPT` and exits with status 1
- NFR-001: `backup verify` on a 1 GB archive prints within 60 seconds of the command

**Open questions:** None.

### Phase 2: Reporting a failed nightly backup

**Scope:** The nightly run verifies the archive it wrote. On a failure it emails the configured address and turns the status light red, in place of green.

**Requirements:** FR-004, FR-005

**Size:** about 4 files

**Reuse:**

- `backup/schedule.py`: `run` is the nightly run
- `backup/mailer.py`: `send` takes the SMTP connection as an argument
- `backup/panel.py`: `set_light`

**Interface and data changes:**

- `run(source, folder, mail_to, today=None)` in `backup/schedule.py`: `mail_to` is the address a failure is mailed to, which the cron entry passes; `run` calls `verify` on the archive it wrote

**Verify:**

- FR-004: a nightly run whose archive fails verification sends one email to the configured address
- FR-005: a nightly run whose archive fails verification turns the status light red

**Open questions:** None.

## 3. Blocked Requirements

None.

## 4. Open Questions

None.

## 5. Revision History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-03-04 | Initial plan from requirements.md 1.0 |
