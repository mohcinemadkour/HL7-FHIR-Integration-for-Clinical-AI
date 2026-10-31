# Track A Hands-on — Reference Solution

Finish your own version first. This is one defensible answer; others exist. What matters is that each score and choice has a reason.

## The short version

**Verdict: Don't build yet** — question 4 (ownership) is a Stop. Once a model owner is named, run a **pilot**: a nightly ranked call list for the transition nurses, built from a batch extract. Nothing goes into Epic in version 1.

The lesson: the request said “plug it into Epic,” but the nurses work from a spreadsheet, once a day. The lightest path that fits the workflow is a list, not an EHR integration.

## Deliverable 1 — Build Decision Record

**Decision:** the transition nurses choose which ~25 of ~120 daily discharges to call within 48 hours. The model ranks the list so they call the highest-risk patients first.

| Question | Score | Reason |
| --- | --- | --- |
| 1. Decision | Go | Named role, moment (daily call-list prep) and action (who gets called); every day |
| 2. Data | Go | Prior admissions, diagnoses and discharge labs are in the EHR; a daily decision tolerates overnight data |
| 3. Lightest path | Caution | The request asks for Epic integration, but the workflow runs on a list; a nightly batch is enough |
| 4. Ownership | **Stop** | Nobody owns the model after go-live |
| 5. Proof | Caution | No baseline yet: today's readmission rate for called vs. not-called patients must be measured first |

**The math:** the scenario gives no minutes lost; the value is readmissions avoided, not time saved. Ask the director for (1) the current 30-day readmission rate, (2) the penalty exposure leadership worries about, (3) how long the nurses spend building the list each day.

**Verdict:** Don't build yet. **What must change:** name a model owner. **Alternative now:** sort the existing discharge report by a simple rule (for example, number of admissions in the last 12 months) so the nurses get value this month. **Revisit:** when an owner is named → pilot.

## Deliverable 2 — Pattern map

| Data flow | Trigger | Who's in the loop | How many patients | Pattern | Why |
| --- | --- | --- | --- | --- | --- |
| Training data (history) | Schedule (one-off, then monthly) | System | Whole population | Bulk $export | Population-scale, not time-critical |
| Daily discharges to score | Schedule (nightly) | System | ~120 a day | Nightly batch: Bulk $export with `_since`, or a report extract | The decision is daily; real time adds cost and nothing else |
| Discharge events (later, optional) | Event (ADT^A03) | System | Every discharge | HL7 v2 feed | Only if the list must update during the day — not in version 1 |
| Ranked list to nurses | Schedule (each morning) | Person reads a list | ~120 a day | No EHR pattern: a file or report in their current tool | They don't work in the chart, so CDS Hooks and SMART add nothing |

Not used: **CDS Hooks** (no clinician-in-chart moment), **SMART App Launch** (nobody opens an app), **C-CDA** (outbound summaries aren't needed to rank patients).

## Deliverable 3 — Interface Design Document (pilot version, condensed)

1. **Purpose and workflow:** rank yesterday's discharges each morning so the transition nurses call the highest-risk patients first. EHR → nightly extract → scoring job → ranked CSV in the nurses' shared folder by 7 a.m.
2. **Pattern, standard and security:** FHIR Bulk Data `$export` (FHIR R4) with `_since` and `_type=Patient,Encounter,Condition,Observation`; SMART Backend Services, `system/*.read` limited to those types; HTTPS, TLS 1.2+. Output file stored on the hospital network only.
3. **Data scope:** *Must* — discharge encounter, prior admissions (12 months), active diagnoses, discharge labs (sodium, hemoglobin), length of stay, disposition. *Later* — medications, social factors. *Out* — notes, imaging, outside-hospital data.
4. **Identity and matching:** shared MRN (single health system). Encounters with no MRN are excluded from scoring and listed separately for review.
5. **Errors and monitoring:** see the feed review below. Freshness alert: no extract by 5 a.m. → page the job owner; nurses fall back to the unsorted report.
6. **Constraints and assumptions:** constraint — interface team backlog ~3 months, so no new interface in version 1. Assumptions — the extract finishes before 7 a.m. (test: 2 weeks of dry runs); nurses use the ranked list (test: shadow two mornings); disposition codes are standard (test: profile one month of data — the feed review already shows they aren't).
7. **Success metrics:** *works* — list delivered by 7 a.m. on ≥ [X]% of days; *used* — share of calls made from the top 25 of the list; *outcome* — 30-day readmission rate for called patients vs. the measured baseline.
8. **Owners:** extract and job — [named model owner]; list and workflow — transition nursing lead; security review — information security.

## Deliverable 4 — Feed review

| # | Message | Problem | IDD section 5 row | IDD section 6 assumption |
| --- | --- | --- | --- | --- |
| 1 | MSG0002 | PID-3 is empty — no MRN | Business rule: hold, retry, then review; interface analyst | “Every discharge carries an MRN” — measure the rate |
| 2 | MSG0003 | PV1-45 is empty — no discharge time | Validation: reject to error queue; daily review | “Discharge time is always present” — measure the rate |
| 3 | MSG0004 | PV1-36 is `HOME2`, a local code, not a standard disposition | Validation: map local codes, or route unknown codes to review | “Disposition codes are standard” — profile a month of data |
| 4 | Message 5 | Same control ID as message 1 (`MSG0001`) — a duplicate | Deduplicate on MSH-10 plus visit number; log the duplicate | “The feed never resends” — it does; design for it |

Message MSG0003 also has disposition `06` (home with home health). That's valid, but worth a feature: those patients already have follow-up care.

Finding all four is excellent. Three is the bar for moving on.
