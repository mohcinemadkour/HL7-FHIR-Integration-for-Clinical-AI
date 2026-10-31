# Resource 6 — Interface Design Document (sepsis example)

**Track A · Module 1 · Lecture 3 — Write the Interface Design Document**

Sepsis Risk Pipeline, version 0.9 draft. This is the pipeline learners build in Tracks B and C. The site is fictional; bracketed values must be confirmed with the real interface team.

## 1. Purpose and workflow

- **Decision:** the rapid response nurse escalates earlier when a ward patient shows early signs of sepsis.
- **Moment:** the routine vitals check; the card shows when the chart is opened.
- **Trigger events:** admission, transfer, discharge, new vitals and lab results.
- **Workflow:** EHR → HL7 v2 → Mirth → FHIR R4 server (HAPI) → sepsis model → CDS Hooks card in the EHR. Nightly: Bulk $export → training and drift monitoring.

## 2. Pattern, standard and security

| Data flow | Pattern | Standard and version | Profiles or message types | Auth and scopes | Transport |
| --- | --- | --- | --- | --- | --- |
| Events and results in | HL7 v2 feed | HL7 v2.5.1 | ADT^A01, A02, A03; ORU^R01 | Network-level (VPN, IP allow-list) | MLLP over VPN |
| Features for scoring | FHIR query | FHIR R4 | US Core Observation, Patient | SMART Backend Services, `system/Observation.read` | HTTPS, TLS 1.2+ |
| Alert out | CDS Hooks | CDS Hooks 2.0 | patient-view hook, one card | JWT from the EHR, verified by the service | HTTPS, TLS 1.2+ |
| Training data | Bulk $export | FHIR Bulk Data | Patient, Encounter, Observation | SMART Backend Services, `system/*.read` | HTTPS, TLS 1.2+ |

## 3. Data scope and mapping

- **Must (version 1):** heart rate, respiratory rate, temperature, blood pressure; WBC, lactate, creatinine; admit and transfer events.
- **Later (version 2):** antibiotic orders, problem list, note text for NLP.
- **Out of scope:** imaging, billing codes, full chart history.

| Source field | Destination field | Rule or transformation | Code system |
| --- | --- | --- | --- |
| PID-3 | Observation.subject | Look up Patient by MRN | Hospital MRN |
| OBX-3 | Observation.code | Local code to LOINC (for example LACT → 2524-7) | LOINC |
| OBX-5 | Observation.valueQuantity.value | Numeric; reject if empty | — |
| OBX-6 | Observation.valueQuantity.code | Map to UCUM | UCUM |
| OBX-11 | Observation.status | P → preliminary, F → final, C → corrected | FHIR ObservationStatus |
| OBX-14 | Observation.effectiveDateTime | ISO 8601 with time zone | — |

## 4. Identity and matching

- **Approach:** shared identifier (single health system).
- **Field:** MRN in PID-3, matched to Patient.identifier.
- **No match:** hold the message and retry; send it for review if it still fails.
- **Owner:** interface analyst.

## 5. Errors and monitoring

| Error type | Example | What happens to the message | Who is alerted | How it's resolved |
| --- | --- | --- | --- | --- |
| Validation | OBX-5 empty | Rejected to error queue, negative ACK | Interface analyst | Daily queue review |
| Business rule | MRN not found | Held, retried, then sent for review | Interface analyst | Fix the patient link, replay the message |
| System | FHIR server timeout | Retried with backoff | On-call engineer, if it persists | Restore the service, replay the queue |

- **Data freshness alert:** no ORU message for longer than [N] minutes during the day.
- **Audit log:** every message, success or failure, kept for [retention period].

## 6. Constraints and assumptions

**Constraints:** HIPAA; TLS everywhere; CDS Hooks supported on patient-view only; no budget for a new interface engine.

| Assumption | Owner | How we test it | By when |
| --- | --- | --- | --- |
| Vitals reach Mirth within [N] minutes | Interface lead | Measure 30 days of feed timestamps | Before build |
| Lactate is present at scoring time for most patients | ML owner | Check a de-identified sample | Before build |
| Nurses see the card at the vitals check | Nurse manager | Shadow one shift | Before pilot |

## 7. Success metrics

| Layer | Metric | Baseline | Target | Review date |
| --- | --- | --- | --- | --- |
| It works | Messages delivered within [N] minutes | To measure | [target] | [date] |
| People use it | Alert override rate | Not applicable before launch | Below [X]% | [date] |
| It changes the outcome | Time from first warning signs to escalation | To measure | [target] | [date] |

## 8. Owners and sign-off

| Part | Owner | Signed | Date |
| --- | --- | --- | --- |
| Feed and channel | Interface lead | Pending | [date] |
| Model and monitoring | ML owner | Pending | [date] |
| Alert and clinical workflow | Ward nurse manager | Pending | [date] |
| Security review | Information security | Pending | [date] |
