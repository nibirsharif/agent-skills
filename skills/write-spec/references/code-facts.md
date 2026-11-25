# Facts the Code Holds

Read this when the input, or an answer, names a system and a top-level folder of the project holds code for that system. With no code for a named system, nothing here applies.

Before writing, read that code within the limits below, and ask about each fact it shows that would change a requirement. What the project already does is still not input: the code never gives a requirement, a system, a value, or a name. It gives questions only.

## What to read

- Read code only for a system that the input or an answer names. A name the project supplied, in a `Proposed:` the user has not confirmed, is not named yet.
- Find the files by searching the project for the input's own word for each thing its statements use, change, or rely on: one search for each word.
- Read at most 5 files for one system, once in a conversation: the files of that system that the searches hit most, each in full. A search hit shows which file to read and never a fact. Never read a test, a file of another system, or a file reached only by following an import.
- When those files do not show whether a fact holds, there is no fact: ask nothing about it, and read no further.

## What makes a question

A fact is worth a question only when the user's answer would add, remove, or reword a requirement. There are three kinds:

- **Something a statement relies on that the code does not have.** The statement can only hold when the system already does or records something ("the existing audit log", "bookings made earlier count"), and the code does not do or record it.
- **A constraint that limits a response.** The code enforces a rule (a uniqueness rule, a fixed limit, a scope every transaction is held to) under which a response the input asks for cannot happen as stated.
- **A contradiction.** The input says what the system does today, and the code does otherwise.

These are not facts to ask about:

- What the input asks for and the code does not do yet, or does differently. That is the feature.
- How the code is built: its names, paths, fields, status codes, libraries, and structure. write-plan reads those.
- A case that a statement in the input, an answer, or the target file already decides.
- A fault in the code that the input's statements do not touch.

## The question

- Ask one question for each fact, on one line. State the fact first, naming the file that shows it as a path from the project root in backticks, then ask what the user must decide.
- Give it no `Proposed:`. Whether the code or the input is right is the user's decision.
- A fact adds a question. It holds back a statement only when that statement cannot be true while the fact stands: one that relies on what the code lacks, or one the code contradicts. Every other statement the input fully supports is still written, from the input's words. That includes a statement a constraint limits: the answer adds the exception or lifts the constraint, and the statement stays as it is.
- It counts toward the 10 questions, in the place of the statement it is about.
- The answer is input, and the code still is not: write the requirement from the answer's words.

## Example

Input: "Requirements for the loan service: When a member renews a loan, the loan service extends the due date of the loan by 14 days. If a member renews a loan that has already been renewed 2 times, the loan service rejects the renewal. Renewals made before this change count toward the 2."

The project has a `loans/` folder. Searches for `renew` and `due date` hit `loans/renew.py` and `loans/models.py`. `loans/renew.py` adds 21 days to the due date. `loans/models.py` stores a due date for each loan and nothing about its renewals.

The third statement relies on a record of earlier renewals that the code does not keep, so it is not written and gets Q-001. The 21 days are what the input changes, and the counter that FR-002 needs is how the limit is built: neither is a fact to ask about. Nothing in FR-001 or FR-002 comes from the code.

```
FR-001: When a member renews a loan, the loan service shall extend the due date of that loan by 14 days.

FR-002: If a member renews a loan that has already been renewed 2 times, then the loan service shall reject the renewal.

Q-001: `loans/models.py` stores no record of a loan's renewals: how many renewals does the loan service count for a loan that was renewed before this change?
```
