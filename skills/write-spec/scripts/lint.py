#!/usr/bin/env python3
"""Check EARS requirement and question lines against the mechanical rules in ears-rules.md.

Usage: python3 lint.py FILE [FILE ...]    (use - to read standard input)

Checks every `REQ-NNN:` and `Q-NNN:` line. A file whose first heading is
`# Requirements Specification` is also checked against the file template.

ERROR  breaks a rule. Fix it.
CHECK  may break a rule, depending on the sense of the words. Confirm it against the rule.

Exits 1 when there is at least one ERROR. The rules stay in ears-rules.md; this script only
catches what a reread can miss. The banned words are read from that file.
"""

import re
import sys
from pathlib import Path

RULES = Path(__file__).resolve().parent.parent / "references" / "ears-rules.md"

LINE_RE = re.compile(r"^(- )?((REQ|Q)-\d{3,})(?: \((?:new|changed)\))?: (.*)$")
COMMENT_RE = re.compile(r"\s*<!--.*?-->")
QUOTED_RE = re.compile(r'"[^"]*"|“[^”]*”|`[^`]*`')
CLAUSE_RE = re.compile(r"(?:^|, )(Where|where|While|while|When|when|If|if) ")
SYSTEM_RE = re.compile(r"(?:^|, (?:then )?)(?:The|the) ([^,]+?) shall\b")

# Banned words with a common sense the rules allow ("a message about the order").
# A match on one of these is a CHECK, not an ERROR.
TWO_SENSES = {
    "about", "around", "clean", "fast", "few", "handle", "high", "large", "low", "manage", "many",
    "most", "process", "simple", "slow", "small", "some", "support", "secure", "regularly",
}
UPPERCASE_WORDS = {"TBD", "TBC", "TBA", "XX", "ASAP"}
NOT_SYSTEM_NAMES = {
    "system", "application", "app", "platform", "service", "software", "server", "backend", "frontend",
}
MODALS = r"\b(should|may|might|will|can|must|needs to|has to|is required to)\b"
QUESTION_WORDS = r"(what|which|how|when|where|who|whom|whether|does|do|is|are|must|should|can)"
DAYS = r"(monday|tuesday|wednesday|thursday|friday|saturday|sunday)s?"
SCHEDULE = rf"\b(every|each) (\d[\d.,]* )?(seconds?|minutes?|hours?|days?|weeks?|months?|years?|{DAYS})\b|\b(daily|hourly|weekly|monthly|nightly)\b"
DAY_BOUNDARY = rf"\b(midnight|noon|\d{{1,2}}(st|nd|rd|th) (day )?of|{DAYS}|each day|every day|new day)\b"
FILE_HEADINGS = [
    "## 1. Summary", "## 2. Scope", "## 3. Functional Requirements", "## 4. Non-Functional Requirements",
    "## 5. Open Questions", "## 6. Revision History", "## 7. References",
]


def banned_patterns():
    """Return (word, compiled regex) for each banned word listed in ears-rules.md."""
    text = RULES.read_text()
    section = text.split("## Banned words", 1)[1].split("\n## ", 1)[0]
    words = []
    for line in section.splitlines():
        label, sep, rest = line.partition(":")
        if line.startswith("- ") and sep and "**" not in label:
            words += re.findall(r"`([^`]+)`", rest)
    patterns = []
    for word in words:
        suffix = r"(?:s|es|d|ed|ing|ly)?" if re.fullmatch(r"[A-Za-z]+", word) else ""
        patterns.append((word, re.compile(r"(?<![\w/])" + re.escape(word) + suffix + r"(?![\w/])", re.I)))
    return patterns


class Linter:
    def __init__(self, patterns):
        self.patterns = patterns
        self.findings = []

    def add(self, where, level, ident, message):
        self.findings.append((where, level, ident, message))

    def requirement(self, where, ident, text):
        if text == "Withdrawn.":
            return
        bare = QUOTED_RE.sub('""', text)
        head, _, response = bare.partition(" shall ")

        if not text.endswith("."):
            self.add(where, "ERROR", ident, "does not end with a full stop")
        if len(re.findall(r"\bshall\b", bare)) != 1:
            self.add(where, "ERROR", ident, "needs exactly one `shall`")
        if not re.match(r"(The|Where|While|When|If) ", text):
            self.add(where, "ERROR", ident, "must start with The, Where, While, When, or If")

        clauses = CLAUSE_RE.findall(head)
        ranks = [{"where": 0, "while": 1, "when": 2, "if": 2}[c.lower()] for c in clauses]
        if ranks != sorted(ranks) or len(ranks) != len(set(ranks)):
            self.add(where, "ERROR", ident, "clauses out of order or repeated: Where, While, then one When or If")
        for i, c in enumerate(clauses):
            if (i == 0 and head.startswith(c)) != c[0].isupper():
                self.add(where, "ERROR", ident, f"`{c}` is capitalised only when it starts the sentence")
        if any(c.lower() == "if" for c in clauses) and not re.search(r", then the ", head + " shall"):
            self.add(where, "ERROR", ident, "`If` clause needs `, then the <system> shall`")
        if re.search(SCHEDULE, response, re.I):
            self.add(where, "CHECK", ident, "a schedule after `shall` is a trigger: put it in a When clause")
        if re.search(r"\b(when|if|while|where)\b", response, re.I):
            self.add(where, "CHECK", ident, "condition after `shall`? Conditions go before the system")

        systems = SYSTEM_RE.findall(bare)
        system = systems[-1].strip() if systems else ""
        if re.search(r"(^|, (then )?)it shall\b", bare, re.I) or system.lower() in NOT_SYSTEM_NAMES:
            self.add(where, "ERROR", ident, f"`{system or 'it'}` is not a system name")
        elif not system:
            self.add(where, "ERROR", ident, "no `the <system> shall` found")

        if re.search(r"\bshall (not )?be \w+(ed|en)\b", bare):
            self.add(where, "ERROR", ident, "passive response: make the system the subject")
        if re.search(r"\b(be able to|have the ability to|be capable of)\b", bare):
            self.add(where, "ERROR", ident, "states a capability, not behaviour")
        for m in re.finditer(MODALS, bare, re.I):
            self.add(where, "ERROR", ident, f"modal `{m.group(1)}`: use `shall` only")
        if re.search(r"\bup to\b", bare, re.I):
            self.add(where, "ERROR", ident, "`up to` leaves the boundary open")
        if re.search(r"\bbetween\b[^,]+\band\b", bare, re.I):
            self.add(where, "CHECK", ident, "`between X and Y` leaves the boundaries open if it is a limit")
        for m in re.finditer(r"\bwithin \d[\d.,]*\s*[A-Za-z]+\b(?!\s+of\b)", bare):
            self.add(where, "ERROR", ident, f"`{m.group(0)}` has no starting point: `within N <unit> of <event>`")
        zoned = re.search(r"UTC|GMT|time zone", bare)
        if re.search(r"\b([01]?\d|2[0-3]):[0-5]\d\b", bare) and not zoned:
            self.add(where, "ERROR", ident, "time of day with no time zone")
        elif re.search(DAY_BOUNDARY, head, re.I) and not zoned:
            self.add(where, "CHECK", ident, "a date or day boundary in a condition needs a time zone")
        if re.search(r"\b[A-Za-z]+/[A-Za-z]+\b", bare):
            self.add(where, "CHECK", ident, "slash between words: write what it stands for")
        if " or " in head:
            self.add(where, "CHECK", ident, "`or` in a condition: one requirement per alternative")
        if " or " in response:
            self.add(where, "CHECK", ident, "`or` in the response: alternatives hide the condition that picks one")

        for word, pattern in self.patterns:
            for m in pattern.finditer(bare):
                found = m.group(0)
                if found.isupper() and len(found) > 1 and found not in UPPERCASE_WORDS:
                    continue
                level = "CHECK" if word.lower() in TWO_SENSES else "ERROR"
                self.add(where, level, ident, f"banned word `{found}`" + (" (allowed only in another sense)" if level == "CHECK" else ""))

    def question(self, where, ident, text):
        if text.startswith("Closed."):
            if not text.startswith("Closed. Answer: "):
                self.add(where, "ERROR", ident, "a closed question keeps its answer: `Closed. Answer: <answer>`")
            return
        asked, sep, proposed = text.partition(" Proposed:")
        if not asked.endswith("?"):
            self.add(where, "ERROR", ident, "the question does not end with `?`")
        if asked.count("?") > 1:
            self.add(where, "ERROR", ident, "asks more than one question: one gap per question")
        # "How many ..., and in what time window?" or "..., and for what percentage?" is one threshold
        # with its parts: not two gaps.
        joined = r"[,;:]? (and|or) ((in|at|for|from|to|by|on|with) )?" + QUESTION_WORDS + r"\b"
        if re.search(joined + r"(?! (time )?(window|period|unit|percentage)\b)", asked, re.I):
            self.add(where, "CHECK", ident, "may ask two things: one gap per question")
        if sep and re.fullmatch(r"\s*(none|n/?a|tbd|-)?\.?\s*", proposed, re.I):
            self.add(where, "ERROR", ident, "empty proposal: leave `Proposed:` out instead")
        elif sep and re.search(r"\d|\b(midnight|noon)\b", proposed, re.I):
            self.add(where, "CHECK", ident, "a number or time in a proposal: propose it only if the input suggests it "
                     "or a named standard sets it, never for a business decision")

    def lint(self, name, text):
        lines = text.splitlines()
        seen, prev_is_id, run_reported = {}, False, False
        for n, line in enumerate(lines, 1):
            where = f"{name}:{n}"
            m = LINE_RE.match(line)
            if not m:
                prev_is_id = run_reported = False
                continue
            bullet, ident, kind, body = m.groups()
            if bullet:
                self.add(where, "ERROR", ident, "no bullet before the ID")
            if prev_is_id and not run_reported:
                self.add(where, "ERROR", ident, "needs a blank line before it and before each ID line after it, "
                         "or the lines render as one paragraph")
                run_reported = True
            seen.setdefault(ident, []).append(n)
            body = COMMENT_RE.sub("", body).strip()
            (self.requirement if kind == "REQ" else self.question)(where, ident, body)
            prev_is_id = True

        first_heading = next((l for l in lines if l.startswith("# ")), "")
        if first_heading.startswith("# Requirements Specification"):
            self.lint_file(name, text, seen)

    def lint_file(self, name, text, seen):
        for ident, lines in seen.items():
            if len(lines) > 1:
                self.add(f"{name}:{lines[1]}", "ERROR", ident, f"duplicate ID, first on line {lines[0]}")
        visible = COMMENT_RE.sub("", text)
        for heading in FILE_HEADINGS:
            if not re.search(rf"^{re.escape(heading)}\s*$", text, re.M):
                self.add(name, "ERROR", "file", f"missing heading `{heading}`")
        for m in re.finditer(r"\[[^\]\n]*\](?!\()|<[a-z][a-z ]*>|YYYY-MM-DD", visible):
            self.add(name, "ERROR", "file", f"placeholder left in: `{m.group(0)}`")

        systems_line = re.search(r"^\*\*Systems:\*\* (.*)$", text, re.M)
        if not systems_line:
            self.add(name, "ERROR", "file", "missing `**Systems:**` line in Scope")
        else:
            listed = {s.strip().lower().removeprefix("the ") for s in systems_line.group(1).split(",")}
            for line in text.splitlines():
                m = LINE_RE.match(line)
                if m and m.group(3) == "REQ":
                    found = SYSTEM_RE.findall(QUOTED_RE.sub('""', COMMENT_RE.sub("", m.group(4))))
                    if found and found[-1].strip().lower() not in listed:
                        self.add(name, "ERROR", m.group(2), f"system `{found[-1]}` is not on the Systems line")

        for heading in FILE_HEADINGS[2:5]:
            body = text.split(heading, 1)[-1].split("\n## ", 1)[0] if heading in text else ""
            for line in COMMENT_RE.sub("", body).splitlines():
                line = line.strip()
                if line and not LINE_RE.match(line) and not re.fullmatch(r"None given\.|None\.|Pending: .+", line):
                    self.add(name, "ERROR", "file", f"`{heading}` holds a line that is not an ID line: `{line[:60]}`")

        open_questions = re.findall(r"^Q-\d{3,}: (?!Closed\.)", text, re.M)
        for heading in FILE_HEADINGS[2:4]:
            body = text.split(heading, 1)[-1].split("\n## ", 1)[0]
            if open_questions and body.strip() == "None given.":
                self.add(name, "CHECK", "file", f"`{heading}` says None given. while questions are open: "
                         "if requirements for it wait on them, write `Pending: Q-...`")


def main(argv):
    if not argv:
        print(__doc__.strip())
        return 2
    linter = Linter(banned_patterns())
    for arg in argv:
        text = sys.stdin.read() if arg == "-" else Path(arg).read_text()
        linter.lint("stdin" if arg == "-" else arg, text)
    for where, level, ident, message in linter.findings:
        print(f"{where}: {level} {ident}: {message}")
    errors = sum(1 for f in linter.findings if f[1] == "ERROR")
    print(f"{errors} errors, {len(linter.findings) - errors} checks")
    print("Do not mention this lint or its results in the reply.")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
