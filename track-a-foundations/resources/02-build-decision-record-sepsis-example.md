# Resource 2 — Build Decision Record (sepsis example)

**Track A · Module 1 · Lecture 1 — Should you build this integration?**

Verdict: **Build**, with handling of a missing lactate written in as a requirement. The hospital, names and figures are fictional.

## 1. Request

“Warn us earlier when a ward patient is deteriorating toward sepsis.” Requested by the ED and medical-ward nursing director.

## 2. Decision this changes

- Person who acts: rapid response nurse
- Moment: the routine vitals check on adult inpatient wards
- Action: escalates to the physician and starts the sepsis workup earlier
- Frequency: every patient, every vitals round
- Stakes: patient safety

## 3. Build Check scores

| Question | Score | Reason |
| --- | --- | --- |
| 1. Decision | Go | Named role, moment and action; daily, safety-critical |
| 2. Data | Caution | Vitals are timely; lactate turnaround varies, so it is often missing at scoring time |
| 3. Lightest path | Go | Decision window is hours and the action happens in the EHR: HL7 v2 feed plus CDS Hooks justified |
| 4. Ownership | Go | Interface team owns the Mirth channel, ML owner owns the model, ward nurse manager owns the alert |
| 5. Proof | Go | Primary: time to escalation. Guardrail: alert override rate. Review at [N] days |

## 4. The math

- Cost of the problem: not reducible to hours; the main risk is delayed recognition of deterioration (safety)
- Five-year cost of the integration: [build cost] + 5 × [yearly run cost] = [total]

## 5. Verdict

**Build.** The Caution on question 2 is fixed by a requirement: the model must score with lactate missing and flag it on the card.

## 6. Alternative offered

Not needed.

## 7. Revisit

At the [N]-day review, or if the override rate stays above [X]%.

## 8. Sign-off

Ward nurse manager, interface lead, ML owner.
