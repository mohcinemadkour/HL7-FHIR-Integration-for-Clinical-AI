# Track A Hands-on — Scope the readmission integration

Recording script — the speaker notes from each slide, in order.
About 1009 words, roughly 7 minutes at a natural pace.


## Slide 1 — Scope the readmission integration

Welcome to the Track A hands-on exercise.

You’ve learned three things in Module 1: how to decide whether to build, how to pick a pattern, and how to write the Interface Design Document. Now you’ll use all three on one realistic request, from start to finish.

There’s no code in this exercise. But it’s still hands-on: you’ll produce four real documents, and at the end you’ll open a real HL7 v2 feed and find the problems in it.

Budget about four hours. You don’t have to do it in one sitting. Everything you need is in the resources for this lecture.

## Slide 2 — Four deliverables, one request

Here’s what you hand in. Four deliverables, all for the same request.

One: a Build Decision Record — your five Build Check scores, the math, and a verdict.

Two: a pattern map — every data flow the solution needs, with one pattern each and the reason.

Three: an Interface Design Document — all eight sections, kept to a few pages.

And four, the new part: a feed review. You’ll open a small sample of real HL7 v2 discharge messages, find what’s wrong with them, and feed what you find back into your design.

The first three use the templates from Module 1. The fourth is a preview of Track B.

## Slide 3 — scenario

Here’s the request. It’s fictional, but it’s the kind you’ll actually get.

The care-transitions director at Lakeside Regional wants a model that flags patients at high risk of readmission within 30 days, so her team can call them after discharge. And she asks: can you plug it into Epic?

Here’s what you learn on a 30-minute call. Two nurses make about 25 calls a day, out of about 120 discharges. They work from a call list in a spreadsheet, not from the chart. The interface team has a three-month backlog. And nobody has said who would own the model after go-live.

The full scenario is in Resource 3. Read it carefully — every detail matters. And notice the wording of the request. “Plug it into Epic” is a solution. Your job is to find out whether it’s the right one.

## Slide 4 — Do them in order. Each feeds the next.

Four steps, in order, because each one feeds the next.

Step one: run the Build Check with Resource 1. Score the five questions, do the math with what the scenario gives you, and reach a verdict. Write down what’s missing as questions for the director. About an hour.

Step two: list every data flow the solution needs, and map each one to a pattern with the decision tree in Resource 4. Thirty minutes.

Step three: write the Interface Design Document with Resource 5. All eight sections. This is the longest step.

Step four: review the sample feed — next slide.

One important rule. If your verdict comes out as “Don’t build yet,” you’re not done. Do steps two to four anyway, for the pilot you would run once the blocking issue is fixed — and say what has to change first. That’s exactly what you’d do at work.

## Slide 5 — Five discharge messages. Find what’s wrong.

Step four is where this exercise gets hands-on.

In the resources you’ll find a file with five HL7 v2 discharge messages — ADT A03 — from Lakeside’s test system. The patients are fictional.

On screen is the first message, and it’s a clean one. I’ve highlighted the four fields to check. MSH-10, the message control ID — it should be unique for every message. PID-3, the patient’s MRN. PV1-36, the discharge disposition — 01 means discharged home. And PV1-45, the discharge date and time.

You don’t need to know HL7 v2 in depth yet; that’s Track B. To find a field, count the pipe characters. One tip: in the MSH segment, the first pipe is itself field one.

Now open the file and check the other four messages. Every problem you find is a real decision for your IDD: what happens to that message, who gets alerted, and which assumption you now have to test. Find at least three.

## Slide 6 — Six of eight, and you’re ready for Track B

When you’re done, check your own work against these eight points. They’re also in the exercise brief.

One: your decision names a role, a moment and an action — not “clinicians.”
Two: every Build Check score has a one-line reason.
Three: your verdict follows the rule, and if there’s a Stop, you’ve written what has to change.
Four: you chose each pattern from the trigger in the workflow — not from the words in the request.
Five: your IDD says what’s out of scope.
Six: your matching rule names the field, and what happens when there’s no match.
Seven: your metrics cover all three layers — it works, people use it, it changes the outcome.
And eight: you found at least three problems in the feed, and each one has a row in your error handling.

Six out of eight, and you’re ready for Track B.

## Slide 7 — The right answer might be “not yet.”

One last thing before you start.

Don’t assume the answer is “build it.” Go back to Lecture 1: a well-reasoned “not yet” is a real deliverable. Look hard at who would own this, and at how the nurses actually work, before you decide what to build — and where.

When you’re done, post your verdict and your pattern map in the Q&A. I read them, and it’s interesting to see how different people reason about the same request.

Then, and only then, open the reference solution in the resources. It’s one defensible answer, not the only one. If yours is different, check whether your reasons hold up. If they do, tell me in the Q&A — I’d like to hear it.

## Slide 8 — Now we open the hood.

That’s the end of Track A.

You now have something most engineers who start in health IT never get: a way to decide what to build, how it should move, and what can go wrong — before writing a line of code.

In Track B we open the hood. We start with HL7 v2, segment by segment — and those five discharge messages you just reviewed will feel very familiar. Bring your IDD with you. We’ll build against it.

See you in Module 2.
