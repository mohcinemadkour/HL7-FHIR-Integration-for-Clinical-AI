# Module 1 · Lecture 1 — Should you build this integration?

Recording script — the speaker notes from each slide, in order.
About 1306 words, roughly 9 minutes at a natural pace.


## Slide 1 — Should you build this integration?

- Welcome to Module 1.
- Skipped Module 0? Go back — it's short and explains the labs.
- This is the only module with no code. On purpose.
- Every other module teaches how to build. This one teaches whether to build.
- The most expensive mistake isn't a bug. It's a working pipeline nobody needed.
- You build it, run it, and get paged for it — so you should ask first.
- By the end: a five-question check and a one-page decision record.

## Slide 2 — Decide what to build before you build it

- Module 1 has three lectures, three decisions, in this order.
- Lecture 1: should we build it? Output: a Build Decision Record.
- Lecture 2: which pattern? HL7 v2, FHIR, bulk export, API or CDS Hooks.
- Lecture 3: the Interface Design Document — the spec everyone signs.
- Most teams start with lecture 3, or jump straight to code.
- We earn the right to build first.

## Slide 3 — What decision will this change — and what will it cost to keep running for five years?

- The question almost nobody asks at the start.
- Not “Can we connect it?” Not “Does Epic support FHIR for this?”
- First: what decision will this change, and who makes it?
- No decision and no person? Then it's a plumbing project, not a use case.
- Second: what will it cost to keep running for five years?
- Not to build it. To run it. That's where the money and the pain go.
- Let's start with that second question.

## Slide 4 — The build is the part you can see

- The build is what everyone sees: channel, mappings, model wrapper, tests.
- The run is underneath, and it never ends.
- EHR upgrades change the feed.
- Someone always wants one more field.
- Messages fail. Someone gets paged at 2 a.m.
- Security reviews it every year.
- Clinical AI adds a second thing that ages: the model. It drifts and needs revalidation.
- [Optional: your own rule of thumb — run cost vs. build cost on a real project.]
- Honest cost = build + yearly run × years you keep it alive.

## Slide 5 — Technically perfect. Clinically ignored.

- Here's a failure you'll never see in an incident report.
- Left: the pipeline is perfect. Feed up, scoring every hour, zero errors in 30 days.
- Right: the question nobody asked — who acted on the last score?
- If the score lands where nobody looks, or after the decision, it changed nothing.
- So we start from the decision, not from the data.

## Slide 6 — Five questions before any code

- This is the tool for this lecture: the Build Check.
- Five questions, answered before anyone writes code.
- Decision, data, lightest path, ownership, proof.
- Score each one Go, Caution or Stop.
- One working session with the requester and the interface team.
- It ends in a one-page record.
- I'll run each question on our sepsis pipeline.

## Slide 7 — What decision changes — and who acts on it?

- Question one: what decision changes, and who acts on it?
- Write down four things.
- One: the person who acts. A role, not “the care team.”
- Two: the moment in their workflow.
- Three: how often it happens.
- Four: the stakes. Safety first, then revenue and compliance, then convenience.
- Stop signal: “clinicians will find it useful.” That’s not a use case yet.
- Sepsis example: the rapid response nurse, at the vitals check, escalates earlier.
- Every shift, safety-critical. A clear Go.
- Remember: a person, a moment, an action. Missing one? Stop here.

## Slide 8 — Is the data there, on time, and trustworthy?

- Question two: is the data there, on time, and trustworthy?
- Latency: does it arrive inside the decision window?
- Completeness: pull a real sample and measure. Don't trust the data dictionary.
- Coding: LOINC, or local codes that change site to site?
- Source of truth: if a value lives in three systems, pick one.
- Stop signal: the data arrives after the decision is made.
- Sepsis: Caution. Vitals are on time; lactate often isn't.
- That becomes a requirement: the model must handle a missing lactate.

## Slide 9 — What is the simplest pattern that works?

- Question three: what's the simplest pattern that works?
- Engineers love the top of this ladder. It's also the most expensive to run.
- Step 1: a manual step or report. Fine for rare events.
- Step 2: nightly batch or Bulk export. Enough if the decision is tomorrow.
- Step 3: FHIR query on demand. No feed to maintain.
- Step 4: real-time HL7 v2 feed. Now you monitor and replay messages.
- Step 5: CDS Hook in the EHR. Highest impact, highest cost.
- Rule: climb only as high as the decision window needs.
- First ask: would a workflow change or training fix it?
- Sepsis: window is hours, action is in the EHR. Steps 4–5 justified. Go.

## Slide 10 — Who owns it after go-live?

- Question four: who owns it after go-live?
- The feed and the channel: usually the interface team.
- The model and its monitoring: you, or your ML team.
- The alert and the workflow: a clinical owner, like a nurse manager.
- Vendors: write each one's responsibility into the contract.
- Stop signal: the owner is “the project team.” Projects end. Pipelines don't.
- [Optional: a quick story of a pipeline that lost its owner.]
- Sepsis: interface team, ML owner, nurse manager. Three names. Go.

## Slide 11 — How will we know it worked?

- Question five: how will we know it worked?
- I care most about this one — it's what I do at EvalTrust.
- One primary metric tied to the decision. Not AUC — the action.
- A baseline measured before go-live.
- Guardrails: false-alert rate and override rate.
- Kill criteria and a review date, decided in advance.
- Stop signal: “we'll figure out how to measure it after launch.”
- Sepsis: time to escalation, override rate, review at [__] days. Go.

## Slide 12 — Put both sides in dollars

- Put both sides in dollars. Leaders understand it.
- Left: cost of the problem per year.
- Events per day × minutes lost × 365 ÷ 60 × hourly cost.
- Example, made-up inputs: 40 × 6 × 365 ÷ 60 = 1,460 hours. At $60/hour: $87,600 a year.
- Measure your own inputs. Don't guess.
- Right: five-year cost = build + 5 × yearly run cost.
- Safety and compliance risks don't fit in hours. List them next to the number.
- [Optional: real numbers from a project of yours.]

## Slide 13 — From five scores to one decision

- Five scores become one decision.
- Build: all Go, or each Caution has a written fix.
- Pilot: two or more Cautions. One unit, small scope, fixed end date.
- Don't build yet: any Stop. Fix it, or take a lighter path.
- Must-haves (regulation, safety): run the check anyway. It shapes how you build.
- Sepsis: Go, Caution, Go, Go, Go → Build, with missing-lactate handling.
- Decide with the clinical owner and the interface lead — not alone.

## Slide 14 — A “no” is a deliverable too

- Every verdict goes into a Build Decision Record. One page, eight fields.
- 1 · The request and who asked.
- 2 · The decision: person and moment.
- 3 · Five scores, each with a reason.
- 4 · Problem cost vs. five-year cost.
- 5 · The verdict.
- 6 · The alternative you offer instead.
- 7 · When to look again.
- 8 · Signatures: clinical owner, interface lead, you.
- A well-documented no is a real deliverable. It protects your team's time.
- [Optional: a time you said no — or wish you had.]

## Slide 15 — Run the Build Check on a real request

- Your turn.
- Step 1: pick a real request — or the readmission scenario in the resources.
- Step 2: score all five questions, with a reason each. Do the math.
- Step 3: fill in the Build Decision Record. Then compare with my sepsis example.
- Budget about an hour.
- Done in ten minutes? You probably wrote “clinicians will find it useful.” Go back to question one.
- Post your verdict in the Q&A. I'm most interested in the “Don't build” ones.
- Next lecture: which pattern?
