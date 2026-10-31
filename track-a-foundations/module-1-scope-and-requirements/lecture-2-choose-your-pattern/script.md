# Module 1 · Lecture 2 — Choose your pattern

Recording script — the speaker notes from each slide, in order.
About 2108 words, roughly 15 minutes at a natural pace.


## Slide 1 — Choose your pattern

Welcome to lecture 2.

In the last lecture, you decided whether to build. Now, for the requests that passed the Build Check, we answer the next question: which pattern?

Here’s the mistake I see most often. A team says “we’re doing a FHIR integration” before anyone has described the workflow. FHIR is a great standard, but it isn’t one thing — and it isn’t always the answer. Inside most hospitals, a lot of the real-time clinical data still moves as HL7 v2 messages.

In this lecture, you’ll learn the six patterns you’ll meet in clinical AI work, a quick way to pick between them, and how one real pipeline — our sepsis project — uses several of them together.

It’s about fifteen minutes. There’s a short exercise at the end, so keep a notepad close.

## Slide 2 — Three questions pick the pattern

Before we look at any standard, here are the three questions that pick the pattern for you.

One: what triggers the data movement? Is it an event — a patient is admitted, a lab result is finalized? Is it a request — your app asks for data when it needs it? Is it a schedule — every night? Or is it a specific moment in the clinician’s workflow, like opening a chart or signing an order?

Two: who’s in the loop? Is it a system talking to a system with no human involved, or is there a person who logs in and looks at the data?

Three: how many patients per request? One patient right now, or thousands of patients at once?

Notice that none of these questions mentions HL7 or FHIR. They’re about the workflow. You answered most of them already in the Build Check last lecture — the decision, the person and the moment. Now those answers pick the technology.

## Slide 3 — Where each pattern lives

Here are the six patterns you’ll meet, placed on one map.

The vertical axis is freshness: real-time at the top, on demand in the middle, periodic at the bottom. The horizontal axis is scope: one patient on the left, the whole population on the right.

Top left, in orange: CDS Hooks. Real-time, one patient, right inside the clinician’s workflow. For clinical AI, this is where your prediction meets a human decision.

Top, toward the middle: the HL7 v2 feed. Real-time events — admissions, transfers, lab results — streaming for every patient in the hospital as they happen.

On the left, in teal: the SMART on FHIR app. A person opens it, for one patient, when they need it.

In the middle: the plain FHIR query. Your system asks for one patient’s data on demand.

Lower left: the C-CDA document — a snapshot of one patient at one moment, usually sent between organizations.

And bottom right: FHIR Bulk Data export. Thousands of patients, on a schedule. That’s your training and monitoring data.

Keep this map in mind. Every pattern we discuss today has a place on it.

## Slide 4 — HL7 v2 pushes. FHIR waits to be asked.

If you remember one technical idea from this lecture, make it this one.

On the left: HL7 v2 is push. Something happens in the hospital — a patient is admitted — and the EHR sends an ADT A01 message. It goes over MLLP to an interface engine like Mirth, which can transform it, for example into FHIR, and pass it to your model. You don’t ask. The hospital tells you, in real time, every time.

That makes HL7 v2 the workhorse for event-driven workflows. It’s mature and very reliable. The downside: the message formats are rigid and vary from site to site, so every change — a new field, a new site — means mapping work.

On the right: FHIR REST is pull. Your app sends a request — GET Observation for this patient — and the FHIR server sends back a Bundle in JSON. Nothing moves until you ask.

That’s ideal for on-demand access and modern apps, but it means you don’t automatically know when something changed. FHIR does have a subscription mechanism for notifications, but support varies a lot between EHRs, so check what your site actually supports before you design around it.

Push for events. Pull for questions. Most real pipelines need both.

## Slide 5 — Six patterns at a glance

Here’s the whole lecture on one slide. Screenshot it — it’s also in the resources as a PDF.

HL7 v2 feed: triggered by events like admissions and results, streaming for every patient. In clinical AI, that’s your source of real-time features. Watch out: the format varies from site to site, so every new hospital means new mapping work.

FHIR query: triggered by your request, for one or a few patients. Great for pulling features on demand. Watch out for rate limits and paging on large result sets.

Bulk export: runs on a schedule, for the whole population. That’s your training data and your drift monitoring. It runs asynchronously — you start the export and collect the files later — so it’s never real-time.

SMART app: triggered when a person opens it, with a patient in context. That’s how you build clinician-facing or patient-facing apps. Expect app registration and a security review with each EHR.

CDS Hooks: triggered at a moment in the workflow — opening a chart, signing an order. That’s where AI alerts and advice live. Watch out: you have a tight latency budget, and a badly tuned alert creates alert fatigue fast.

And C-CDA documents: a snapshot sent at a transition of care, like a discharge. Useful as input for NLP. But it’s static — it doesn’t update — and matching it to the right patient takes care.

## Slide 6 — Does a person log in?

Now the distinction that confuses more teams than any other.

Someone says “we’re building a FHIR integration.” That sentence is incomplete, because there are two very different ways to authorize access to FHIR — and you need to know which one before you design anything.

The question is simple: does a person log in?

If no — it’s system to system — you use SMART Backend Services. Your service signs a JSON Web Token with its private key, the authorization server returns an access token, and your service calls the FHIR API. No human is involved. That’s how your pipelines, your feature jobs and your bulk exports work. You’ll implement exactly this with JWT client assertion in Track C.

If yes — a person logs in — you use SMART App Launch. A clinician opens your app from inside the EHR, or a patient opens it on their phone. They log in with OAuth 2.0, and your app receives a token plus the context: which user, and which patient. Then it calls FHIR on that user’s behalf, limited to what they’re allowed to see.

Same FHIR API underneath. Completely different security model, registration process and testing.

Answer this question early. Teams that find out halfway through a build lose weeks re-doing their auth.

## Slide 7 — How a prediction reaches the clinician

For clinical AI, CDS Hooks is the pattern that matters most, because it’s where your model meets a human decision. So let’s walk through how it works.

Step one: a clinician does something in the EHR — opens a patient’s chart, or starts signing an order. Those moments are called hooks; patient-view and order-sign are two common ones.

Step two: the EHR calls your CDS service over HTTPS. It can send prefetched FHIR data with the call — recent vitals, labs — so your service doesn’t have to query for them.

Step three: your model scores the patient. And this has to be fast. The clinician is waiting, so your latency budget is tight.

Step four: your service returns a card, and the EHR displays it. Below is a mockup of what that can look like: a short message, where the score came from, a link to explain it, and actions — open an order set, or dismiss with a reason.

That “dismiss with a reason” button is your evaluation data. Every override tells you something about your model or your alert design. Remember question five from the Build Check: the override rate is your guardrail metric. You’ll build this full flow in Track C.

## Slide 8 — Ask in this order. Stop at the first yes.

Here’s how to turn all of this into a decision in under a minute. Ask these questions in this order, and stop at the first yes.

One: is this an alert or a piece of advice at a specific moment in the clinician’s workflow? Then it’s CDS Hooks.

Two: does a person open an app and log in? Then it’s a SMART App Launch.

Three: do you need thousands of patients at once — for training, research, or monitoring? Then it’s Bulk export.

Four: is it a fixed snapshot sent to another organization — a referral, a discharge summary? Then it’s a C-CDA document.

Five: do you need to react the moment something happens — an admission, a lab result? Then it’s an HL7 v2 feed. If your EHR supports FHIR subscriptions well, that can be an alternative, but at most sites today, events still flow as HL7 v2.

And if none of these apply: a plain FHIR query, using backend services, is usually the right default.

Why this order? The first questions are about people and scale, and they’re the hardest constraints to change later. The last ones are about timing, and you have more flexibility there.

One warning: this tree gives you the main pattern for each data flow. A real product usually has several data flows. That’s exactly what the next slide shows.

## Slide 9 — One product, four patterns

Let’s put it all together with the pipeline you’ll build in this course: the real-time sepsis risk pipeline.

Look at the top row — the real-time path. The EHR pushes HL7 v2 messages, admissions and lab results, to Mirth. That’s pattern one, push. Mirth transforms them into FHIR resources and writes them to our FHIR server. The sepsis model queries that FHIR server for the features it needs — that’s the FHIR query pattern, using backend services, because no human logs in. And the result reaches the clinician as a CDS Hooks card in the EHR.

Now the bottom row — the batch path. Every night, we run a Bulk export to pull the population-level data we need for training and for drift monitoring. When we see drift, we revalidate and update the model.

So that’s four patterns in one product: HL7 v2, FHIR query, CDS Hooks, and Bulk export. Each one was picked by the three questions: what triggers it, who’s in the loop, and how many patients.

This is the normal case. When someone asks you “is it HL7 or FHIR?”, the honest answer is usually “both — for different flows.” Your job is to pick the right pattern for each flow, and document it in the Interface Design Document, which is our next lecture.

## Slide 10 — Pick the pattern for each case

Your turn. Pause the video now, and for each of these four cases, write down the pattern you’d use — and one sentence on why.

Case A: you need to update a patient’s features the moment they’re transferred to the ICU.

Case B: a nurse opens an app from the patient’s chart to see that patient’s risk trend over the last 48 hours.

Case C: you need to retrain your readmission model on two years of encounters for the whole hospital.

Case D: you want to warn a physician about a drug interaction while they’re signing an order.

Use the decision tree. Ask the questions in order and stop at the first yes.

Pause now. The answers are on the next slide.

## Slide 11 — How did you do?

Let’s check your answers.

Case A, the ICU transfer: an HL7 v2 feed. It’s an event, and you need to react the moment it happens. Specifically, it’s an ADT A02 — a patient transfer message.

Case B, the risk-trend app: SMART App Launch. A nurse opens it from the chart, logs in, and the app gets the patient context from the EHR.

Case C, retraining: Bulk export. Two years of encounters for the whole hospital is a population-level job, run with backend services. Please don’t try this with thousands of individual FHIR queries — you’ll hit rate limits, and the interface team will not be happy with you.

Case D, the drug interaction warning: CDS Hooks, on the order-sign hook. It’s advice at a specific moment in the workflow, before the order is final.

If you got all four, great. If you missed one, go back to the decision tree and see which question you skipped.

Post your answers — and any case from your own work you’re unsure about — in the Q&A.

In the next lecture, we take everything from this module — the Build Decision Record and the patterns you chose — and turn it into the Interface Design Document. See you there.
