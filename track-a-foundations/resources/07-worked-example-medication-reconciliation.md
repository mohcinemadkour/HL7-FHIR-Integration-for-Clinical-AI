# Resource 7 — Worked practice example: medication reconciliation

**Track A · Module 1 · all three lectures**

This example walks one request through every Module 1 template, step by step. After each filled-in section, a **Why** note explains the choice — the thinking you should copy, not the words.

It's chosen to differ from the other two examples:

| Example | Verdict | Main patterns |
| --- | --- | --- |
| Sepsis (Resources 2 and 6) | Build | HL7 v2 feed, FHIR query, CDS Hooks |
| Readmission (hands-on) | Don't build yet | Bulk $export, nightly list |
| **Medication reconciliation (this one)** | **Pilot** | **SMART App Launch, C-CDA documents** |

Everything here is fictional and illustrative.

---

## The request

The pharmacy director at Riverbend Medical Center writes:

> “Our pharmacists spend too long comparing the patient's home medication list with the admission orders. Can AI flag the mismatches for them?”

What you learn in a 30-minute call:

- Admission medication reconciliation is done by a pharmacist within 24 hours of admission.
- About 60 adult admissions a day; pharmacists reconcile all of them on weekdays.
- Home medications come from three places: the patient interview, the EHR's own history, and outside records received as C-CDA documents from a regional health information exchange (HIE).
- Pharmacists work inside the EHR chart while reconciling.
- Missed discrepancies are reported to the medication safety committee.
- Pharmacy informatics already maintains two other EHR apps.
- Nobody has measured how many discrepancies pharmacists currently catch or miss.

---

## Step 1 — Build Decision Record (Resource 1)

### 1. Request

- Request: flag mismatches between the home medication list and admission orders for the reconciling pharmacist.
- Requested by: pharmacy director.

> **Why:** one sentence, in the requester's terms. Don't rewrite it into a solution yet.

### 2. Decision this changes

- Person who acts: the admitting-unit pharmacist
- Moment: admission medication reconciliation, within 24 hours of admission
- Action: confirms, changes or flags each order that doesn't match the home list
- Frequency: ~60 admissions a day
- Stakes: patient safety (medication errors at transitions of care)

> **Why:** the request said “pharmacists”; we named the specific moment and action. If you can't fill this in, you stop here.

### 3. Build Check scores

| Question | Score | Reason |
| --- | --- | --- |
| 1. Decision | Go | Named role, moment and action; daily; safety-critical |
| 2. Data | Caution | Admission orders and EHR history are reliable; outside C-CDA medication lists are incomplete and sometimes out of date |
| 3. Lightest path | Go | The pharmacist is already in the chart, opening an app — a SMART app launched from the chart fits without changing the workflow |
| 4. Ownership | Go | Pharmacy informatics owns the app and the model; the pharmacy director owns the workflow |
| 5. Proof | Caution | No baseline: nobody knows how many discrepancies are caught or missed today |

> **Why:** two Cautions, no Stops. Notice that “outside data is messy” is a Caution, not a Stop: it doesn't block the decision, it limits how much to trust one source. And “no baseline” is fixable before go-live.

### 4. The math

- Cost of the problem per year = 60 reconciliations a day × [minutes spent comparing lists] × 365 ÷ 60 × [pharmacist hourly cost] = [fill in after measuring]
- Five-year cost of the integration = [build cost] + 5 × [yearly run cost]
- Risks that don't fit in hours: medication errors at admission (safety); findings from the medication safety committee (compliance)

> **Why:** we don't invent the minutes. A two-day time study is part of the pilot. Safety risk is listed next to the number, not forced into it.

### 5. Verdict: **Pilot**

Two Cautions → Pilot: the pharmacists on one ward only, for 60 days, then decide.

### 6. Alternative offered

Not needed — but if the pilot fails, a simple side-by-side list view (no AI) is the fallback.

### 7. Revisit

At day 60, or earlier if pharmacists override more than [X]% of flags.

### 8. Sign-off

Pharmacy director, interface lead, pharmacy informatics lead.

---

## Step 2 — Pattern map (Resource 4)

| Data flow | Trigger | Who's in the loop | How many patients | Pattern | Why |
| --- | --- | --- | --- | --- | --- |
| Admission orders and EHR medication history | Pharmacist opens the patient | Person logs in | One patient | **SMART App Launch** → FHIR MedicationRequest | The pharmacist is in the chart; the app gets the patient in context |
| Outside medication lists | Received from the HIE | Sender pushes | One snapshot per patient | **C-CDA document**, read via FHIR DocumentReference | It's a static snapshot from another organization |
| Discrepancy flags back to the pharmacist | Same app session | Person | One patient | Shown in the SMART app | No new data flow needed |

Not used: **CDS Hooks** (the pharmacist opens the app on purpose; no interruptive alert needed), **HL7 v2 feed** (nothing has to happen the moment an order is placed), **Bulk $export** (only for later model evaluation).

> **Why:** we walked the decision tree for each flow and stopped at the first yes. Question 2 — “a person opens an app and logs in?” — answered the main flow.

---

## Step 3 — Interface Design Document (Resource 5), pilot version

### 1. Purpose and workflow

- Decision: the pharmacist confirms or changes each admission order that doesn't match the home medication list.
- Workflow: pharmacist opens the patient → launches the app from the chart → app reads orders, EHR history and outside lists → shows matched, mismatched and missing medications → pharmacist acts in the EHR as usual.

### 2. Pattern, standard and security

| Data flow | Pattern | Standard and version | Profiles or message types | Auth and scopes | Transport |
| --- | --- | --- | --- | --- | --- |
| Orders and history | SMART App Launch | FHIR R4 | US Core MedicationRequest (active orders and reported home medications) | OAuth 2.0, `patient/MedicationRequest.read` | HTTPS, TLS 1.2+ |
| Outside lists | C-CDA via FHIR | FHIR R4 DocumentReference; C-CDA R2.1 | Medications section | `patient/DocumentReference.read` | HTTPS, TLS 1.2+ |

> **Why:** “SMART app” isn't a spec. Version, profiles and exact scopes are — and the scopes are the narrowest that work (read-only, this patient only).

### 3. Data scope and mapping

- Must (pilot): active orders, EHR medication history, outside medication lists from the last 12 months.
- Later: allergies, renal function for dose checks.
- Out of scope: writing orders back to the EHR, discharge reconciliation.

| Source | Destination | Rule | Code system |
| --- | --- | --- | --- |
| MedicationRequest.medicationCodeableConcept | Comparison key | Normalize to ingredient level | RxNorm |
| C-CDA medication entry | Comparison key | Map local or NDC codes to RxNorm; unmapped → shown as “unmatched source” | RxNorm |
| Dose and frequency | Comparison detail | Compare after unit normalization | UCUM |

> **Why:** comparing medications only works at a shared level — RxNorm ingredients. Without that, “metoprolol tartrate 25 mg” and a local code look different.

### 4. Identity and matching

- Inside the EHR: the SMART launch context gives the patient — no matching needed.
- Outside C-CDA documents: already matched by the HIE; the app shows the source and date of every outside list.
- No match or doubtful match: the outside list isn't shown; the pharmacist sees “outside records unavailable.”

> **Why:** the safe failure is to show less, not to show another patient's medications.

### 5. Errors and monitoring

| Error type | Example | What happens | Who is alerted | How it's resolved |
| --- | --- | --- | --- | --- |
| Validation | C-CDA with no medication section | Skip that document; tell the pharmacist | Nobody | Logged for weekly review |
| Business rule | Code that can't map to RxNorm | Show as “unmatched source” | Pharmacy informatics (weekly report) | Add the mapping |
| System | FHIR server timeout | Retry once; then show “try again” | On-call informatics, if repeated | Restore service |

- Freshness: outside lists older than 12 months are marked as old.
- Audit: every launch, flag shown and pharmacist action logged.

### 6. Constraints and assumptions

- Constraints: app must pass the EHR vendor's app review; read-only access; HIPAA.

| Assumption | Owner | How we test it | By when |
| --- | --- | --- | --- |
| Most admissions have at least one outside list | Pharmacy informatics | Count on 2 weeks of admissions | Before build |
| Most medication codes map to RxNorm | Interface lead | Map a 1-month sample | Before build |
| Pharmacists will launch the app every time | Pharmacy director | Shadow two shifts during the pilot | Week 2 of pilot |

### 7. Success metrics

| Layer | Metric | Baseline | Target | Review date |
| --- | --- | --- | --- | --- |
| It works | App loads within [N] seconds | To measure | [target] | Day 30 |
| People use it | Share of reconciliations where the app was opened | 0 | [target] | Day 30 |
| It changes the outcome | Discrepancies found per reconciliation; time per reconciliation | Two-day time study before the pilot | [target] | Day 60 |

> **Why:** the two Cautions from the Build Check became concrete work: an assumption test for outside data, and a baseline study for proof.

### 8. Owners and sign-off

| Part | Owner |
| --- | --- |
| App, model and monitoring | Pharmacy informatics lead |
| Workflow | Pharmacy director |
| FHIR access and app registration | Interface lead |
| Security review | Information security |

---

## What to notice

- **Cautions turn into requirements and tests,** not into reasons to stop.
- **The pattern came from the workflow:** the pharmacist is already in the chart, so a SMART app beats a background feed.
- **Every unknown stays visible** as a bracket or an assumption with an owner.

Now try the same steps on your own request, or on the readmission scenario in [Resource 3](03-readmission-practice-scenario.md).
