# Track A Hands-on — Scope the Readmission Integration

**Time:** about 4 hours · **Code:** none · **Do it after:** Module 1, Lecture 3

You've learned to decide whether to build, pick a pattern and write the design document. Now do all three on one realistic request, then check your design against a real (synthetic) data feed.

## The request

Lakeside Regional Hospital wants an AI model that flags patients at high risk of 30-day readmission, so the transition nurses can call them after discharge. The director asks: *“Can you plug it into Epic?”*

The full scenario — including what you learn in a 30-minute call — is in [Resource 3](../resources/03-readmission-practice-scenario.md). Read it first.

## What you hand in

| # | Deliverable | Template | Time |
| --- | --- | --- | --- |
| 1 | **Build Decision Record** — five scores, the math, a verdict | [Resource 1](../resources/01-build-decision-record-template.md) | ~60 min |
| 2 | **Pattern map** — one row per data flow, with the pattern and why | Table below | ~30 min |
| 3 | **Interface Design Document** — all eight sections | [Resource 5](../resources/05-interface-design-document-template.md) | ~90–120 min |
| 4 | **Feed review** — problems found in the sample discharge feed, added to your IDD | [Sample feed](sample-feed/adt-a03-discharges.hl7) | ~30 min |

If your verdict in step 1 is *Don't build yet*, still do steps 2–4 for the version you would pilot once the Stop is fixed. Say what has to change first.

## Step by step

### Step 1 — Build Check (Lecture 1)

Score the five questions Go, Caution or Stop, each with a one-line reason. Do the math with what the scenario gives you, and write down what's missing as questions for the director. Reach a verdict using the rule: all Go → Build; two or more Cautions → Pilot; any Stop → Don't build yet.

### Step 2 — Pattern map (Lecture 2)

List every data flow the solution needs. For each one, walk the decision tree in the [cheat sheet](../resources/04-pattern-cheat-sheet.md) and stop at the first yes.

| Data flow | Trigger | Who's in the loop | How many patients | Pattern | Why |
| --- | --- | --- | --- | --- | --- |
| | | | | | |

### Step 3 — Interface Design Document (Lecture 3)

Fill in all eight sections. Keep it to a few pages. Every unknown stays as a placeholder — those placeholders are your question list for the interface team.

### Step 4 — Read the feed

[`sample-feed/adt-a03-discharges.hl7`](sample-feed/adt-a03-discharges.hl7) holds five HL7 v2 discharge messages (ADT^A03) from Lakeside's test system. All patients are fictional.

You don't need to know HL7 v2 in depth yet — Track B covers it. Use these field positions:

| Field | Meaning |
| --- | --- |
| MSH-10 | Message control ID — should be unique per message |
| PID-3 | Patient identifier (MRN) |
| PV1-19 | Visit number |
| PV1-36 | Discharge disposition (01 = home, 06 = home with home health) |
| PV1-45 | Discharge date and time |

Count the fields by the `|` separators (in the MSH segment, the first `|` is MSH-1). Find the problems, then for each one add a row to your IDD: section 5 (what happens to the message, who's alerted) and, where it applies, section 6 (an assumption you now need to test).

## Check your own work

| # | Check | Yes / no |
| --- | --- | --- |
| 1 | The decision names a role, a moment and an action — not “clinicians” | |
| 2 | Every Build Check score has a one-line reason | |
| 3 | The verdict follows the rule, and any Stop comes with what must change | |
| 4 | Each data flow has one pattern, chosen from the trigger, not from the request's wording | |
| 5 | The IDD lists what's out of scope | |
| 6 | Patient matching names the field and what happens on no match | |
| 7 | Success metrics cover all three layers: it works, people use it, it changes the outcome | |
| 8 | The feed review found at least three problems, each with an error-handling row in the IDD | |

Six or more yeses: you're ready for Track B.

## Then compare

Post your verdict and pattern map in the course Q&A. Then open the [reference solution](reference-solution.md) — after you've finished, not before. There's more than one defensible answer; what matters is that your reasons hold up.
