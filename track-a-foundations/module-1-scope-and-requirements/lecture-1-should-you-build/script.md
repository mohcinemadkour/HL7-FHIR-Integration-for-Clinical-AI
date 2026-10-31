# Module 1 · Lecture 1 — Should you build this integration?

Recording script — the speaker notes from each slide, in order.
About 2790 words, roughly 20 minutes at a natural pace.


## Slide 1 — Should you build this integration?

Welcome to Module 1.

If you skipped Module 0, go back and watch it. It’s short, and it explains how the labs and the lesson loop work.

This module is the only one in the course where we don’t write code. That’s on purpose. Every module after this one teaches you how to build an integration. This one teaches you whether you should.

Here’s why that matters to you as an engineer. The most expensive mistake in clinical AI integration isn’t a bug in your transformer. It’s a perfectly working pipeline that nobody needed. And as the person who will build it, run it and get paged when it breaks, you have more reason than anyone to ask this question early.

By the end of this lecture, you’ll have a five-question check you can run on any integration request in about an hour, and a one-page decision record to go with it.

## Slide 2 — Decide what to build before you build it

Here’s how Module 1 is laid out. Three lectures, three decisions, in this order.

Today, lecture 1: should you build this integration at all? You’ll leave with a Build Decision Record — a one-page document that captures the decision and the reasons behind it.

Lecture 2: if the answer is yes, which pattern? A real-time HL7 v2 feed, a FHIR query, a bulk export, a plain API, or a CDS Hook inside the EHR workflow. Each one has a very different cost and failure profile.

Lecture 3: you’ll write the Interface Design Document — the spec that the interface team, the clinical owner and you can all sign.

Notice the order. Most teams start with lecture 3, or skip straight to Track B and start coding. We’re going to earn the right to build first.

## Slide 3 — What decision will this change — and what will it cost to keep running for five years?

Let’s start with the question almost nobody asks at the start of an integration project.

When a request lands on your desk — “can we get the lab results into the model in real time?” — the conversation usually jumps straight to feasibility. Can we connect to it? Does Epic expose this through FHIR? Is there an HL7 feed we can tap?

Those are good questions. They’re just not the first ones.

The first questions are these two. One: what clinical or operational decision will this change? If you can’t name the decision and the person who makes it, you don’t have a use case yet — you have a data plumbing project.

Two: what will it cost to keep this running for five years? Not to build it. To keep it running. Because in a hospital, that’s where the money and the pain actually go.

Let’s look at that second question first.

## Slide 4 — The build is the part you can see

Here’s the picture I want you to keep in your head for the rest of the course.

The build is the part everyone sees: the Mirth channel, the mappings, the model wrapper, the testing. It gets a budget and a project plan.

The run is underneath, and it never ends. Every EHR upgrade can change the feed. Someone will ask for one more field. Messages will fail, and someone gets paged at two in the morning. Security will review it every year.

And here’s the part that’s specific to clinical AI: you don’t have one thing aging, you have two. The interface ages, and the model ages. Patient populations shift, lab assays change, documentation habits change — and your model drifts. That means monitoring, revalidation and sometimes retraining, for as long as it’s live.

[Optional: give your own rule of thumb here — for example, how the yearly run cost compared to the build cost on a project you worked on. Use your real numbers.]

So when someone asks “how much will it cost?”, the honest answer always has two parts: the build, and the run per year, times the years you expect to keep it alive.

## Slide 5 — Technically perfect. Clinically ignored.

Here’s a failure you’ll never see in an incident report.

On the left, the pipeline is perfect: the feed is up, the model scores every hour, zero errors in thirty days.

On the right is the question nobody asked: who acted on the last score?

If the score lands where nobody looks, or after the decision is made, the pipeline changed nothing. So we start from the decision, not from the data.

## Slide 6 — Five questions before any code

This is the tool for this lecture: the Build Check. Five questions, answered before anyone writes code.

Decision, data, lightest path, ownership and proof. You score each one Go, Caution or Stop.

It takes one working session with the requester and the interface team, and it ends in a one-page record.

I’ll run each question on our sepsis pipeline.

## Slide 7 — What decision changes — and who acts on it?

Question one: what decision changes, and who acts on it?

On the left are the four things you need to write down. First, the person who acts — a role, not “the care team.” Second, the moment in their workflow where they act. Third, how often that moment happens — every shift for every patient is very different from once a month. Fourth, the stakes. Rank the problem: patient safety first, then revenue and compliance, then convenience. Convenience is real, but on its own it rarely justifies a real-time integration.

The Stop signal is the vague answer. If the best anyone can say is “clinicians will find it useful,” you don’t have a use case yet. Go back to the requester and ask: who, when, and what will they do differently?

Here’s the sepsis pipeline. The person is the rapid response nurse. The moment is the routine vitals check. The decision is whether to escalate — call the physician, start the sepsis workup — earlier than they would have. It happens for many patients, every shift, and it’s a safety issue. That’s a clear Go.

If you take one thing from this slide: a use case is a person, a moment and an action. If you can’t fill in all three, stop here.

## Slide 8 — Is the data there, on time, and trustworthy?

Question two: is the data there, on time, and trustworthy?

This is where ML engineers usually feel at home, but in a hospital the traps are different.

Latency first. Your decision has a window. If the nurse decides at the vitals check, and the data you need arrives two hours later, the integration is useless — no matter how good the model is.

Completeness. Don’t trust the data dictionary. Pull a real sample, de-identified, and measure how often the field is actually filled in. A field that exists in the schema and is empty for half the patients is a very different input.

Coding. Are labs coded in LOINC, or in local codes that change from site to site? That decides how much mapping work — and mapping maintenance — you’re signing up for.

And the source of truth. If the same value lives in three systems, pick one and write it down.

The Stop signal: the data arrives after the decision is made. An interface can’t fix that, and neither can a better model. Garbage in, garbage out — and late in is just as bad.

On the sepsis pipeline, I’d score this Caution. Vitals are charted on time. Lactate is the problem: turnaround varies, so at the moment of scoring it’s often missing. That’s not a Stop — it’s a requirement. The model has to handle a missing lactate, and you’ll do exactly that in Track C, when we build features from FHIR.

## Slide 9 — What is the simplest pattern that works?

Question three: what is the simplest pattern that would work?

Engineers love to jump to the top of this ladder. Real-time, event-driven, inside the EHR — it’s the most interesting thing to build. It’s also the most expensive thing to run.

So look at the ladder from the bottom.

Step one: a manual step or a report. For something that happens a few times a month, a well-designed report or a checklist can deliver most of the value for almost none of the cost.

Step two: a nightly batch, or a FHIR Bulk Data export. If the decision happens tomorrow morning, real-time buys you nothing.

Step three: a FHIR query on demand — your app asks for the data when a user opens it. No feed to maintain.

Step four: a real-time HL7 v2 feed through Mirth. Now you have a channel to monitor, messages to replay, and an upgrade to survive every year.

Step five: a CDS Hook inside the EHR workflow. The highest impact and the highest cost — app registration, security review, alert design, clinician sign-off.

The rule: climb only as high as the decision window from question one requires. And before you climb, ask whether a non-integration fix — a workflow change, or training — solves the real problem.

For sepsis, the window is hours, and the action happens inside the EHR. So steps four and five are justified. That’s a Go — and in lecture 2 we’ll go deeper on choosing between these patterns.

## Slide 10 — Who owns it after go-live?

Question four: who owns it after go-live?

A clinical AI integration has at least three moving parts, and each one needs a named owner.

The feed and the channel: usually the interface team. When an Epic upgrade changes a segment, they fix it.

The model and its monitoring: that’s probably you, or your ML team. When performance drifts, you investigate and revalidate.

The alert and the workflow: that needs a clinical owner — a nurse manager, a medical director. When nurses start ignoring the alert, someone on the clinical side has to care, and has the authority to change the workflow.

And if there are vendors — the EHR, an integration engine, a third-party app — write down who is responsible for what, and get it into the contract before signing. When something breaks at a boundary between two vendors, you don’t want to discover then that each one thinks it’s the other’s job.

The Stop signal: the owner is “the project team.” Projects end. Teams get reassigned. Pipelines keep running — until they quietly break and nobody notices.

[Optional: add a quick story here about an integration or model that lost its owner after go-live, and what happened.]

For sepsis: the interface team owns the Mirth channel, the ML owner owns the model, the ED or ICU nurse manager owns the alert. Three names. That’s a Go.

## Slide 11 — How will we know it worked?

Question five: how will we know it worked?

This is the question I care about most, because evaluation is what I do every day at EvalTrust — and it’s the one teams skip most often.

You need four things, written down before you build.

One primary metric, tied directly to the decision from question one. Not model AUC — that tells you the model ranks patients well, not that anything changed for them. The metric is about the action: did the nurse escalate sooner?

A baseline, measured before go-live. Without it, you can’t show improvement, and you can’t defend the project when the budget review comes.

Guardrails: the things that tell you it’s doing harm. For alerts, that’s the false-alert rate and the override rate. If nurses override almost every alert, you’re creating alert fatigue, and you’re making things worse.

And kill criteria with a review date: “if the primary metric hasn’t moved by this date, or overrides stay above this level, we turn it off.” Deciding that in advance is what makes it a real decision.

The Stop signal: “we’ll figure out how to measure it after launch.” You won’t — and by then nobody will want to.

For sepsis: the primary metric is time from first warning signs to escalation. The guardrail is the alert override rate. And we review at [__] days. That’s a Go.

## Slide 12 — Put both sides in dollars

Before you make the call, put both sides in dollars. Leaders understand this language, and it turns an opinion into a discussion you can actually have.

On the left: what the problem costs per year. Count how often it happens per day, how many minutes each occurrence wastes, multiply by 365, convert to hours and multiply by the loaded hourly cost of the person doing the work.

Here’s an example with made-up inputs, just to show the arithmetic. Say it happens 40 times a day and costs 6 minutes each time. That’s 40 times 6 times 365, divided by 60: 1,460 hours a year. At 60 dollars an hour, that’s 87,600 dollars a year. Use your own inputs — measure them, don’t guess.

On the right: what the integration costs over five years. The build, plus five times the yearly run cost — remember the iceberg. Ask your interface team and your own team for real estimates.

Then compare five years of the problem with five years of the integration.

One important caveat. Not everything fits in hours. A missed deterioration, a compliance finding, a reportable event — those don’t reduce to a nice number. Don’t force them into the formula. List them next to the number, explicitly, so the decision-makers see both.

[Optional: share the real numbers from a project you worked on, if you can.]

## Slide 13 — From five scores to one decision

Now we turn five scores into one decision. The rule is simple on purpose.

Build: every question is a Go — or you have a Caution, and you’ve written down exactly how you’ll handle it.

Pilot: two or more Cautions. Too much uncertainty to commit fully, but enough promise to test. Keep a pilot honest: one unit, a small scope, and a fixed end date with the metrics from question five. A pilot without an end date is just a build without a budget.

Don’t build — yet: any Stop. A Stop doesn’t mean the problem isn’t real. It means something has to change first: find the decision owner, fix the data timing, name a run owner, define the metric — or take a lighter path from the ladder.

What about must-haves — a regulatory requirement, a safety mandate? Run the check anyway. You won’t decide whether to build, but the check tells you how to build it so it survives: who owns it, what pattern, how you’ll prove it works.

For our sepsis pipeline: Go, Caution, Go, Go, Go. That’s a Build — with handling missing lactate values written in as a requirement.

And one more thing: this is not a decision you make alone. Make it with the clinical owner and the interface lead, and have them sign the record.

## Slide 14 — A “no” is a deliverable too

Whatever the verdict, you write it down in a Build Decision Record. One page, eight fields.

One: the request, and who asked.
Two: the decision it’s meant to change — the person and the moment.
Three: the five Build Check scores, each with a one-line reason.
Four: the cost of the problem next to the five-year cost of the integration.
Five: the verdict — Build, Pilot, or Don’t build yet.
Six: if it’s not a full build, the alternative you’re offering instead. A report, a workflow change, a pilot, a lighter pattern.
Seven: the trigger or the date to look at it again. “We’ll revisit when the lab moves to the new instrument,” or “in six months.”
Eight: signatures — the clinical owner, the interface lead, and you.

I want to spend a moment on the “no.” Saying no to an integration request is uncomfortable, especially when it comes from a senior clinician. But a well-documented no is one of the most valuable things you can deliver. It protects your team’s time for the projects that matter, and it’s not a dead end: fields six and seven tell the requester exactly what they get instead, and what would change the answer.

You’re not a gatekeeper. You’re looking after limited engineering time — yours included.

[Optional: share a time you said no — or wish you had — and what it saved or cost.]

## Slide 15 — Run the Build Check on a real request

Now it’s your turn.

Step one: pick a real integration request. If you work in healthcare, use one from your own backlog — that’s where you’ll learn the most. If you don’t, use the readmission-risk scenario in the resources for this lecture.

Step two: run the Build Check. Score all five questions — Go, Caution or Stop — with a one-line reason for each, and do the math for both sides.

Step three: fill in the Build Decision Record template. You’ll find the template and my completed example for the sepsis pipeline in the resources. Do yours first, then compare.

Budget about an hour. If you finish in ten minutes, you probably wrote “clinicians will find it useful” somewhere — go back to question one.

Post your verdict in the Q&A if you want feedback. I’m especially interested in the ones that came out as “Don’t build.”

In the next lecture, we’ll take the requests that passed and answer the next question: which pattern? HL7 v2, FHIR, a plain API, or a CDS Hook. See you there.
