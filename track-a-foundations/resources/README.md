# Track A Resources — How to Use Them

Seven resources: two templates, three worked examples, a practice scenario and a cheat sheet. Together they take a request from “can you build this?” to a signed design.

## The flow

```
Request ──► Build Decision Record ──► Pattern choice ──► Interface Design Document
            (Resources 1, 2)          (Resource 4)        (Resources 5, 6)
                        practice request: Resource 3
```

## Each resource

| # | Resource | When to use it | How to use it |
| --- | --- | --- | --- |
| 1 | [Build Decision Record — template](01-build-decision-record-template.md) | A new integration or AI request lands on your desk | Copy it. Fill it in **with** the requester and the interface lead in one session, not alone. Score all five questions, do the math, apply the verdict rule, get three signatures. |
| 2 | [Build Decision Record — sepsis example](02-build-decision-record-sepsis-example.md) | After you've drafted your own record | Compare section by section. Look at how each score has a one-line reason, and how a Caution becomes a written requirement instead of a blocker. |
| 3 | [Readmission practice scenario](03-readmission-practice-scenario.md) | You don't have a real request from work | Use it as your request for the Lecture 1 and Lecture 3 assignments and for the [Track A hands-on](../hands-on/README.md). Read the hints only after you've tried. |
| 4 | [Pattern cheat sheet](04-pattern-cheat-sheet.md) | Choosing how each data flow moves | List the data flows first. Then, for each flow, ask the decision-tree questions in order and stop at the first yes. One pattern per flow; most products need two to four. |
| 5 | [Interface Design Document — template](05-interface-design-document-template.md) | Your request passed the Build Check (Build or Pilot) | Copy sections 1 and 7 from your Build Decision Record. Write sections 2–6 with the interface team. Keep it to a few pages; leave unknowns as `[fill in]` — they become your question list. |
| 6 | [Interface Design Document — sepsis example](06-interface-design-document-sepsis-example.md) | After drafting your own IDD | Compare, then revise. Note the level of detail in section 2 (versions, scopes, transport) and section 5 (one row per error type, plus a freshness alert). |

| 7 | [Worked practice example — medication reconciliation](07-worked-example-medication-reconciliation.md) | Before your first assignment, or when a template field feels unclear | Read it top to bottom once. Every filled-in section has a **Why** note explaining the choice. It ends in **Pilot** and uses SMART App Launch and C-CDA — the patterns the sepsis example doesn't cover. |

## Using them at work

- **Reuse the templates as they are.** They're Markdown: paste them into Confluence, Notion, Google Docs or a Git repo.
- **One record per request, one IDD per interface.** Keep them next to the code so the next engineer can see why it was built that way.
- **Revisit both** at the review date you set, and whenever the EHR is upgraded.

All hospitals, names and figures in the examples are fictional and illustrative.
