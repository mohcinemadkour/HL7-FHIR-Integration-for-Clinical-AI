# Module 1 · Lecture 3 — Write the Interface Design Document

Recording script — the speaker notes from each slide, in order.
About 1898 words, roughly 14 minutes at a natural pace.


## Slide 1 — Write the Interface Design Document

Welcome to the last lecture of Module 1.

So far you’ve decided whether to build, with the Build Check, and you’ve picked a pattern for each data flow. Now we write it down in the Interface Design Document — the IDD.

Whether you’re an AI engineer, a cloud architect or a product manager, the IDD is the one document that the interface team, the clinical owner and you all work from. When something is unclear six months from now, this is where you look.

In this lecture we’ll cover the scoping decisions that go into it — how much data, which codes, how to match patients — and then walk through the IDD section by section, using our sepsis pipeline. The template and a completed sepsis example are in the resources.

## Slide 2 — “It works” is only the bottom layer

Before we scope anything, let’s define what done means.

At go-live, the technical team usually celebrates: messages are flowing, tests passed, it works. That’s layer one, and it matters — delivery, completeness, latency, uptime.

But it’s only the bottom layer. Layer two: do people actually use it? For our sepsis alert: are cards being seen, are nurses acting on them, and what’s the override rate?

Layer three: does it change the outcome it was built for? For sepsis, that’s time to escalation — the metric you defined in the Build Check.

Each layer depends on the one below it. No reliable data, no trust. No trust, no adoption. No adoption, no outcome.

So the first thing that goes into your IDD is at least one metric for each layer. If you can only measure layer one, you can only prove that it works — not that it was worth building.

## Slide 3 — Move the minimum. Write down what’s out.

Now scope. How much data should move?

The most common failure here is scope creep. You start with a clear goal, then someone says “while we’re at it, let’s also pull the allergies, the imaging, the whole history.” Every extra field is more mapping, more testing, more to maintain, and more protected health information to secure.

ML engineers are especially prone to this, because more features feel like a better model. Resist it. Start with the minimum the model and workflow need, and add later with evidence.

Sort every field into three buckets. Must, for version one: for sepsis, the core vitals, three labs, and admit and transfer events. Later, for version two: antibiotic orders, the problem list, note text for NLP. And out of scope: imaging, billing codes, the full chart history.

The out-of-scope list is the one people skip, and it’s the one that protects you. When someone asks in month three “why don’t we have imaging?”, you point to the signed IDD.

## Slide 4 — Local codes in, standard codes out

Next: codes. Moving data is easy. Making sure it means the same thing on both sides is the hard part.

Hospitals send local codes. One site calls lactate “LACT”, another “LACTIC”, a third uses a number. If your model is trained on one site’s codes and deployed at another, it silently gets nothing — or the wrong thing.

So every clinical concept gets mapped to a standard code. Labs and vitals go to LOINC: lactate, creatinine and heart rate here. Problems and findings go to SNOMED CT. Medications go to RxNorm. ICD-10 is mainly for diagnoses on the billing side. And don’t forget units: UCUM, so that milligrams per deciliter never gets mixed up with micromoles per liter.

For AI teams this is not a detail. Your features are defined by these codes. If the mapping is wrong, your model is wrong — with no error message.

The mapping table goes in the IDD, owned by the interface team, reviewed by someone clinical.

## Slide 5 — Is this the same patient?

The next scoping decision is identity. When a message arrives, the receiving system has to answer: is this the same patient?

There are three approaches. A shared identifier — both systems use the same medical record number. That’s the cleanest, and it’s what you’ll usually have inside one health system. Deterministic matching — a set of fields must match exactly, like MRN, name and date of birth. And probabilistic matching — an algorithm scores several fields and accepts a match above a threshold, with a human reviewing the uncertain ones.

Here’s why it matters for AI. Make the rules too strict and real matches get dropped, so your model sees missing features. Make them too loose and one patient’s lab ends up in another patient’s record — and your model makes a confident prediction on the wrong person. That’s a safety issue.

So matching is not a config detail. It goes in the IDD as a decision, with the rule and the owner. For sepsis, inside one hospital, we match on the MRN in PID-3.

## Slide 6 — Eight sections, one source of truth

Here’s the IDD. Eight sections.

One: purpose and workflow — the decision, the person, the moment, and a simple workflow diagram.
Two: the pattern, the standard and security — exactly what you chose in lecture 2, made precise.
Three: data scope and mapping — your must, later and out lists, plus the field mapping.
Four: identity and matching.
Five: errors and monitoring.
Six: constraints and assumptions.
Seven: success metrics — one for each of the three layers.
Eight: owners and sign-off.

Notice the colors. The teal sections — purpose, metrics, owners — you mostly already have from your Build Decision Record. Copy them over. The dark sections are the how, and you write those together with the interface team.

Keep it short. A good IDD for one interface is a few pages, not fifty. If nobody reads it, it’s not a source of truth.

Let’s look at the sections where teams most often go wrong.

## Slide 7 — “We support FHIR” is not a spec

Section two is where vague words cause the most rework.

“We support FHIR” tells an engineer almost nothing. Which version? Which profiles? So you write: FHIR R4, US Core profiles, and the exact version the site runs.

“We’ll get an HL7 feed” — which version, which message types, which transport? HL7 v2.5.1, ADT A01, A02, A03 and ORU R01, over MLLP.

“It’s secure” — how? SMART Backend Services with a signed JWT, and the exact scopes, like system slash Observation dot read. Ask for the narrowest scopes that work.

“Encrypted” becomes TLS 1.2 or higher, a VPN for the MLLP connection, and an IP allow-list.

And “an alert in Epic” becomes CDS Hooks version 2.0, on the patient-view hook, returning a card with one action.

Cloud engineers: this is the section you’ll care most about, because it decides your network design, your secrets management and your security review. Fill it in with the interface team, and check every value against what the site actually supports.

## Slide 8 — One lab result: HL7 v2 → FHIR

Section three is the mapping. Here’s what it looks like for one lab result going from an HL7 v2 ORU message to a FHIR Observation.

PID-3, the patient identifier, becomes the subject — we look up the FHIR Patient by MRN, which is the matching rule we just decided.

OBX-3, the test code, becomes Observation dot code — mapped from the local code to LOINC with the mapping table.

OBX-5, the value, becomes valueQuantity dot value. It must be numeric, and if it’s empty, we reject the message.

OBX-6, the units, map to a UCUM code.

OBX-11, the result status: preliminary, final, corrected. Pay attention to this one. When a lab corrects a result, your features must update — otherwise your model scores the wrong value.

And OBX-14, the observation time, becomes effectiveDateTime, in ISO 8601 with a time zone. Get the time zone wrong and your time-window features are off by hours.

The interface team usually owns this table. Your job is to review it with model features in mind. You’ll build this exact mapping in Mirth in Track B.

## Slide 9 — Design the unhappy path

Section five: what happens when it fails. Because it will.

Plan for three kinds of errors.

Validation errors: the message itself is wrong — say OBX-5, the value, is empty. Reject it to an error queue, and an interface analyst reviews the queue every day.

Business-rule errors: the message is valid, but it breaks a rule — the MRN doesn’t match any patient yet, maybe because the admission hasn’t arrived. Hold it, retry, and if it still fails, send it for review.

System errors: the other side is down — the FHIR server times out. Retry with backoff, and page on-call if it keeps failing.

For each type, the IDD answers three questions: what happens to the message, who gets alerted, and how it gets resolved. And log everything, successes and failures, for audit.

Now the failure that’s specific to AI, in orange. The feed stops quietly. No errors — just no new messages. The model keeps running and keeps producing scores, on data that’s hours old. Nobody notices.

So monitor freshness: alert when you haven’t received a message in longer than normal. That one alert has saved more pipelines than any error handler.

## Slide 10 — Constraints you accept. Assumptions you test.

Section six separates two things teams often mix up.

Constraints are fixed. You accept them and design around them. HIPAA and encryption everywhere. Maybe the EHR only supports CDS Hooks on patient-view. Maybe there’s no budget for a new interface engine.

Assumptions are different. They’re things you believe are true but haven’t verified. And they look exactly like facts — until go-live.

For sepsis: we assume vitals reach Mirth within a few minutes. We assume lactate is usually present when we score. We assume nurses will see the card at the vitals check.

Any of these can be wrong, and if it is, the project fails even though every line of code is correct.

So every assumption in the IDD gets two things: an owner and a test. Measure thirty days of feed timestamps. Check a de-identified sample for lactate. Shadow one shift and watch how the nurses actually work.

Test the riskiest assumptions first — ideally before you build, not after.

## Slide 11 — Three decisions, three artifacts

Let’s wrap up Module 1 — and with it, Track A.

You made three decisions, and each one produced an artifact.

Lecture 1: should we build? You ran the Build Check and wrote a Build Decision Record.

Lecture 2: which pattern? You picked the right pattern for each data flow — HL7 v2, FHIR query, Bulk, SMART, CDS Hooks or documents.

Lecture 3: what exactly are we building? You captured it all in the Interface Design Document: scope, codes, matching, errors, assumptions, metrics and owners.

These three documents are what separate an integration that survives in a hospital from one that ends up abandoned. And notice: we haven’t written a line of code yet. That’s deliberate. From Track B on, every line of code you write will have a reason behind it.

## Slide 12 — Draft your first IDD

Your assignment for this lecture.

Take the request that passed your Build Check in lecture 1 — or the readmission scenario from the resources.

Fill in the IDD template, all eight sections. Keep it short. Use bracketed placeholders for anything you don’t know yet — those placeholders are your list of questions for the interface team.

Then open my completed IDD for the sepsis pipeline, compare, and revise yours.

Budget two to three hours. It’s the most useful document you’ll write in this course, because it’s the one you’ll actually reuse at work.

Next up is Track B, starting with Module 2, and we finally open the hood: HL7 v2 messaging, segment by segment. Bring your IDD — we’ll build against it. See you there.
