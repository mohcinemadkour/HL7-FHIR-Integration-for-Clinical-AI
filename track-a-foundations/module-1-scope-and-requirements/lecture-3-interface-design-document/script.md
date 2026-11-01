# Module 1 · Lecture 3 — Write the Interface Design Document

Recording script — the speaker notes from each slide, in order.
About 943 words, roughly 7 minutes at a natural pace.


## Slide 1 — Write the Interface Design Document

- The last lecture of Module 1.
- You've decided whether to build and picked your patterns.
- Now you write it down: the Interface Design Document, or IDD.
- It's the one document the interface team, the clinical owner and you all work from.
- First the scoping decisions: data, codes, patient matching.
- Then the IDD, section by section, on our sepsis pipeline.
- Template and sepsis example are in the resources.

## Slide 2 — “It works” is only the bottom layer

- Define “done” before you scope anything.
- Layer 1: it works. Delivery, completeness, latency, uptime.
- Layer 2: people use it. Cards seen, acted on, override rate.
- Layer 3: it changes the outcome. For sepsis: time to escalation.
- Each layer stands on the one below.
- Put at least one metric per layer in the IDD.
- Only layer 1? You can prove it works — not that it was worth building.

## Slide 3 — Move the minimum. Write down what’s out.

- How much data should move? The minimum.
- Every extra field means more mapping, testing, maintenance and PHI to secure.
- ML engineers: more features feel better. Add them later, with evidence.
- Must, version 1: core vitals, three labs, admit and transfer events.
- Later, version 2: antibiotic orders, problem list, note text.
- Out of scope: imaging, billing codes, full history.
- The out-of-scope list protects you when someone asks in month three.

## Slide 4 — Local codes in, standard codes out

- Moving data is easy. Making it mean the same thing is hard.
- Hospitals send local codes: LACT, LACTIC, or a number.
- A model trained on one site's codes gets nothing at another site.
- Map every concept to a standard code.
- LOINC for labs and vitals. SNOMED CT for problems. RxNorm for meds.
- ICD-10 for billing diagnoses. UCUM for units.
- Wrong mapping = wrong model, with no error message.
- The mapping table goes in the IDD.

## Slide 5 — Is this the same patient?

- Is this the same patient?
- Shared identifier: same MRN in both systems. Cleanest.
- Deterministic: exact match on MRN, name, date of birth.
- Probabilistic: a score across fields, with human review.
- Too strict → real matches dropped → missing features.
- Too loose → another patient's data → wrong prediction. A safety issue.
- Write the rule and the owner in the IDD.
- Sepsis: one hospital, match on the MRN in PID-3.

## Slide 6 — Eight sections, one source of truth

- The IDD has eight sections.
- 1 · Purpose and workflow.
- 2 · Pattern, standard and security.
- 3 · Data scope and mapping.
- 4 · Identity and matching.
- 5 · Errors and monitoring.
- 6 · Constraints and assumptions.
- 7 · Success metrics.
- 8 · Owners and sign-off.
- Teal sections come from your Build Decision Record. Dark ones you write with the interface team.
- Keep it to a few pages. If nobody reads it, it's not a source of truth.

## Slide 7 — “We support FHIR” is not a spec

- Section 2 is where vague words cause rework.
- “FHIR” → FHIR R4, US Core, and the exact version.
- “HL7 feed” → v2.5.1, ADT A01/A02/A03 and ORU R01, over MLLP.
- “Secure” → SMART Backend Services, signed JWT, narrowest scopes.
- “Encrypted” → TLS 1.2+, VPN for MLLP, IP allow-list.
- “Alert in Epic” → CDS Hooks 2.0, patient-view, one card.
- Cloud engineers: this decides your network, secrets and security review.
- Check every value against what the site supports.

## Slide 8 — One lab result: HL7 v2 → FHIR

- Section 3: one lab result, HL7 v2 to FHIR.
- PID-3 → subject. Look up the patient by MRN.
- OBX-3 → code. Local code to LOINC.
- OBX-5 → value. Numeric; reject if empty.
- OBX-6 → units, as UCUM.
- OBX-11 → status. Corrected results must update your features.
- OBX-14 → time, with time zone. Wrong zone = features off by hours.
- Interface team owns it. You review it with your features in mind.
- You'll build this mapping in Mirth in Track B.

## Slide 9 — Design the unhappy path

- Section 5: what happens when it fails. It will.
- Validation error: the message is wrong. Reject to an error queue; review daily.
- Business-rule error: valid, but breaks a rule — unknown MRN. Hold, retry, review.
- System error: the other side is down. Retry with backoff; page if it persists.
- For each: what happens, who's alerted, how it's resolved.
- Log everything, success and failure.
- The AI-specific failure: the feed stops quietly, the model scores stale data.
- Alert on data freshness, not just errors.

## Slide 10 — Constraints you accept. Assumptions you test.

- Section 6: constraints vs. assumptions.
- Constraints are fixed. HIPAA, TLS, what the EHR supports, budget.
- Assumptions look like facts until go-live.
- Sepsis: vitals arrive within minutes. Lactate is usually there. Nurses see the card.
- Any one wrong, and the project fails with perfect code.
- Give every assumption an owner and a test.
- Test the riskiest first — before you build.

## Slide 11 — Three decisions, three artifacts

- That wraps up Module 1 — and Track A.
- Lecture 1: should we build? → Build Decision Record.
- Lecture 2: which pattern? → a pattern per data flow.
- Lecture 3: what exactly? → Interface Design Document.
- These three separate integrations that survive from ones that get abandoned.
- No code yet, on purpose. From Track B on, every line has a reason.

## Slide 12 — Draft your first IDD

- Your assignment.
- Take the request that passed your Build Check — or the readmission scenario.
- Fill in all eight IDD sections. Keep it short.
- Unknowns stay as placeholders. They're your questions for the interface team.
- Then compare with my sepsis IDD and revise.
- Budget two to three hours. It's the document you'll reuse at work.
- Next: Track B, Module 2 — HL7 v2, segment by segment.
