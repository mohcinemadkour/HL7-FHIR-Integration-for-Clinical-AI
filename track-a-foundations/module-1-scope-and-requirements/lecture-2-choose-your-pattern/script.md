# Module 1 · Lecture 2 — Choose your pattern

Recording script — the speaker notes from each slide, in order.
About 942 words, roughly 7 minutes at a natural pace.


## Slide 1 — Choose your pattern

- Welcome to lecture 2.
- Last lecture: should we build? Now: which pattern?
- Common mistake: “we're doing a FHIR integration” before anyone describes the workflow.
- FHIR isn't one thing, and it isn't always the answer.
- Inside hospitals, much real-time data still moves as HL7 v2.
- Today: six patterns, a quick way to choose, and our sepsis pipeline as an example.
- About fifteen minutes. Keep a notepad — there's an exercise at the end.

## Slide 2 — Three questions pick the pattern

- Three questions pick the pattern for you.
- One: what triggers it? An event, a request, a schedule, or a workflow moment.
- Two: who's in the loop? A system alone, or a person who logs in.
- Three: how many patients? One right now, or a whole population.
- None of these mention HL7 or FHIR. They're about the workflow.
- You already answered most of them in the Build Check.

## Slide 3 — Where each pattern lives

- Six patterns on one map.
- Up: fresher data. Right: more patients.
- Top left, orange: CDS Hooks. Real-time, one patient, inside the workflow.
- Top middle: HL7 v2 feed. Real-time events for every patient.
- Left, teal: SMART app. A person opens it for one patient.
- Middle: FHIR query. Your system asks for one patient's data.
- Lower left: C-CDA document. A one-time snapshot between organizations.
- Bottom right: Bulk export. Thousands of patients on a schedule — your training data.

## Slide 4 — HL7 v2 pushes. FHIR waits to be asked.

- The one technical idea to remember: push vs. pull.
- HL7 v2 is push. Something happens — the EHR sends a message.
- It goes over MLLP to Mirth, gets transformed, reaches your model.
- Reliable and mature. But formats are rigid and vary by site.
- FHIR REST is pull. You ask, the server answers with a Bundle.
- Great for on-demand access. But you don't know when something changed.
- FHIR Subscriptions exist, but support varies. Check your site first.
- Push for events. Pull for questions. Most pipelines need both.

## Slide 5 — Six patterns at a glance

- The whole lecture on one slide. It's in the resources too.
- HL7 v2 feed: events, every patient. Real-time features. Watch: site-specific formats.
- FHIR query: your request, one patient. On-demand features. Watch: rate limits.
- Bulk export: scheduled, whole population. Training and drift. Never real-time.
- SMART app: a person opens it. Clinician and patient apps. Watch: app review.
- CDS Hooks: a workflow moment. Alerts and advice. Watch: latency, alert fatigue.
- C-CDA: transition of care. NLP input. Watch: static, patient matching.

## Slide 6 — Does a person log in?

- The distinction that confuses most teams.
- “We're building a FHIR integration” — which kind?
- Ask: does a person log in?
- No → SMART Backend Services. Your service signs a JWT and gets a token. No human.
- Used by pipelines, feature jobs, Bulk export. You'll build it in Track C.
- Yes → SMART App Launch. User opens the app, logs in with OAuth, app gets patient context.
- Same FHIR API. Different security, registration and testing.
- Decide early. Finding out mid-build costs weeks.

## Slide 7 — How a prediction reaches the clinician

- CDS Hooks is where your model meets a human decision.
- 1 · The clinician opens a chart or signs an order. That's the hook.
- 2 · The EHR calls your service, with prefetched FHIR data.
- 3 · Your model scores the patient — fast. The clinician is waiting.
- 4 · Your service returns a card. The EHR shows it.
- The mockup: a message, the source, an explanation, actions.
- “Dismiss with a reason” is your evaluation data.
- Override rate is your guardrail metric. You'll build this in Track C.

## Slide 8 — Ask in this order. Stop at the first yes.

- Ask in this order. Stop at the first yes.
- 1 · Alert at a workflow moment? → CDS Hooks.
- 2 · A person opens an app and logs in? → SMART App Launch.
- 3 · Thousands of patients at once? → Bulk export.
- 4 · Fixed snapshot to another organization? → C-CDA.
- 5 · React the moment something happens? → HL7 v2 feed.
- None of these? → FHIR query with backend services.
- People and scale come first — they're hardest to change later.
- This gives the pattern for one data flow. Real products have several.

## Slide 9 — One product, four patterns

- Our sepsis pipeline uses four patterns.
- Top row, real time: EHR pushes HL7 v2 to Mirth.
- Mirth writes FHIR resources to our FHIR server.
- The model queries FHIR for features — backend services, no human.
- The result reaches the clinician as a CDS Hooks card.
- Bottom row, nightly: Bulk export for training and drift monitoring.
- “Is it HL7 or FHIR?” Usually: both, for different flows.
- You document each flow's pattern in the IDD — next lecture.

## Slide 10 — Pick the pattern for each case

- Your turn. Pause the video.
- For each case, write the pattern and one sentence why.
- A: update features the moment a patient moves to the ICU.
- B: a nurse opens an app from the chart to see a risk trend.
- C: retrain a readmission model on two years of encounters.
- D: warn a physician about a drug interaction while signing an order.
- Use the decision tree. Answers on the next slide.

## Slide 11 — How did you do?

- A, ICU transfer: HL7 v2 feed. It's an event — ADT A02.
- B, risk-trend app: SMART App Launch. A nurse logs in, patient in context.
- C, retraining: Bulk export. Don't send thousands of single FHIR queries.
- D, drug interaction: CDS Hooks, on order-sign.
- Missed one? Find the tree question you skipped.
- Post your answers — and your own tricky cases — in the Q&A.
- Next: the Interface Design Document.
