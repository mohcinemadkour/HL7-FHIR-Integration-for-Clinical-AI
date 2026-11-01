# Track A Hands-on — Scope the readmission integration

Recording script — the speaker notes from each slide, in order.
About 593 words, roughly 4 minutes at a natural pace.


## Slide 1 — Scope the readmission integration

- Welcome to the Track A hands-on exercise.
- You'll use all of Module 1 on one realistic request.
- No code. But you'll produce four real documents.
- And at the end you'll open a real HL7 v2 feed and find its problems.
- About four hours. You don't have to do it in one sitting.

## Slide 2 — Four deliverables, one request

- Four deliverables, one request.
- 1 · Build Decision Record: five scores, the math, a verdict.
- 2 · Pattern map: each data flow, one pattern, and why.
- 3 · Interface Design Document: all eight sections, a few pages.
- 4 · Feed review: find what's wrong in a sample HL7 v2 feed.
- The first three use Module 1's templates. The fourth previews Track B.

## Slide 3 — scenario

- The request is fictional, but you'll get ones like it.
- Lakeside Regional wants a model that flags 30-day readmission risk.
- The goal: nurses call high-risk patients after discharge.
- Two nurses, about 25 calls a day, out of about 120 discharges.
- They work from a spreadsheet, not the chart.
- Three-month interface backlog. No model owner named.
- “Plug it into Epic” is a solution. Find out if it's the right one.
- Full scenario: Resource 3.

## Slide 4 — Do them in order. Each feeds the next.

- Four steps, in order. Each feeds the next.
- 1 · Build Check with Resource 1. About an hour.
- 2 · Pattern map with Resource 4. Thirty minutes.
- 3 · IDD with Resource 5. The longest step.
- 4 · Feed review. Next slide.
- Verdict is “Don't build yet”? Still do steps 2–4 for the pilot.
- And say what has to change first. That's what you'd do at work.

## Slide 5 — Five discharge messages. Find what’s wrong.

- Step 4 is the hands-on part.
- Five HL7 v2 discharge messages, ADT A03. Patients are fictional.
- This first one is clean. Check the four highlighted fields.
- MSH-10: control ID. Should be unique.
- PID-3: the patient's MRN.
- PV1-36: discharge disposition. 01 means home.
- PV1-45: discharge date and time.
- Count the pipes to find a field. In MSH, the first pipe is field one.
- Check the other four messages. Find at least three problems.
- Each problem becomes a row in your IDD.

## Slide 6 — Six of eight, and you’re ready for Track B

- Check your work against eight points.
- 1 · The decision names a role, a moment, an action.
- 2 · Every score has a reason.
- 3 · The verdict follows the rule; any Stop has a fix.
- 4 · Patterns come from the trigger, not the request's words.
- 5 · The IDD lists what's out of scope.
- 6 · Matching names the field and the no-match rule.
- 7 · Metrics cover all three layers.
- 8 · Three or more feed problems, each handled.
- Six of eight, and you're ready for Track B.

## Slide 7 — The right answer might be “not yet.”

- Don't assume the answer is “build it.”
- A well-reasoned “not yet” is a real deliverable.
- Look hard at ownership and at how the nurses actually work.
- Post your verdict and pattern map in the Q&A. I read them.
- Then open the reference solution — not before.
- It's one defensible answer. If yours differs and holds up, tell me.

## Slide 8 — Now we open the hood.

- That's the end of Track A.
- You can now decide what to build, how it moves, and what can break — before coding.
- Track B opens the hood: HL7 v2, segment by segment.
- Those five discharge messages will look familiar.
- Bring your IDD. We'll build against it.
- See you in Module 2.
