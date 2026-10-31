# Resource 5 — Interface Design Document (template)

**Track A · Module 1 · Lecture 3 — Write the Interface Design Document**

Keep it to a few pages. Every unknown stays as a `[fill in]` placeholder: together they are your list of questions for the interface team.

**Header:** interface name, version, date, author, status (draft, in review, signed).

## 1. Purpose and workflow

- Problem and decision (copy from your Build Decision Record): [fill in]
- Person who acts, and the moment: [fill in]
- Trigger events: [fill in]
- Workflow diagram: source system → integration layer → your service → where the user sees the result

## 2. Pattern, standard and security

One row per data flow.

| Data flow | Pattern | Standard and version | Profiles or message types | Auth and scopes | Transport |
| --- | --- | --- | --- | --- | --- |
| | | | | | |

## 3. Data scope and mapping

- Must (version 1): [fill in]
- Later (version 2): [fill in]
- Out of scope: [fill in]

| Source field | Destination field | Rule or transformation | Code system (LOINC, SNOMED CT, RxNorm, UCUM) |
| --- | --- | --- | --- |
| | | | |

## 4. Identity and matching

- Approach (shared identifier, deterministic, probabilistic): [fill in]
- Fields used, and the source field for each: [fill in]
- What happens when there's no match: [fill in]
- Owner of match failures: [fill in]

## 5. Errors and monitoring

| Error type | Example | What happens to the message | Who is alerted | How it's resolved |
| --- | --- | --- | --- | --- |
| Validation | | | | |
| Business rule | | | | |
| System | | | | |

- Data freshness alert (no messages for longer than normal): [fill in]
- Audit log — what's kept, and for how long: [fill in]

## 6. Constraints and assumptions

- Constraints (fixed): [fill in]

| Assumption | Owner | How we test it | By when |
| --- | --- | --- | --- |
| | | | |

## 7. Success metrics — one per layer

| Layer | Metric | Baseline | Target | Review date |
| --- | --- | --- | --- | --- |
| It works | | | | |
| People use it | | | | |
| It changes the outcome | | | | |

## 8. Owners and sign-off

| Part | Owner | Signed | Date |
| --- | --- | --- | --- |
| Feed and channel | | | |
| Model and monitoring | | | |
| Alert and clinical workflow | | | |
| Security review | | | |
