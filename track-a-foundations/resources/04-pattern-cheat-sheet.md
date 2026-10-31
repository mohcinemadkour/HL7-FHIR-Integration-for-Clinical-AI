# Resource 4 — Pattern cheat sheet

**Track A · Module 1 · Lecture 2 — Choose your pattern**

Pick one pattern per data flow. Most real products combine two to four patterns.

| Pattern | Trigger | Who's in the loop | Scope | Clinical AI use | Watch out |
| --- | --- | --- | --- | --- | --- |
| HL7 v2 feed | Event: admit, transfer, result | System (push over MLLP) | Every event, streaming | Real-time features | Formats vary by site |
| FHIR query | Your request | System (SMART Backend Services) | One or a few patients | On-demand features | Rate limits, paging |
| Bulk $export | Schedule | System (SMART Backend Services) | Whole population | Training, drift monitoring | Asynchronous, not real-time |
| SMART App Launch | A person opens the app | Person logs in (OAuth 2.0) | Patient in context | Clinician and patient apps | App registration, security review |
| CDS Hooks | Workflow moment: patient-view, order-sign | EHR calls your service | Current patient | Alerts and advice | Latency budget, alert fatigue |
| C-CDA document | Transition of care | Sender pushes | One snapshot | Notes and summaries as NLP input | Static, patient matching |

## Decision tree — ask in order, stop at the first yes

1. An alert or advice at a moment in the clinician's workflow? → **CDS Hooks**
2. A person opens an app and logs in? → **SMART App Launch**
3. Thousands of patients at once? → **Bulk $export**
4. A fixed snapshot sent to another organization? → **C-CDA document**
5. React the moment something happens? → **HL7 v2 feed** (or FHIR Subscriptions, where the EHR supports them well)
6. None of the above → **FHIR query** with SMART Backend Services

## Push vs. pull in one line

HL7 v2 tells you when something happens; FHIR answers when you ask.
