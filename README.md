# HL7 FHIR Integration for Clinical AI: A Practitioner's Guide

Course materials for the Udemy course by **Mohcine Madkour, PhD**. The course takes clinical data from raw HL7 v2 hospital feeds, through FHIR R4 APIs, Mirth Connect and Epic, into real-time AI inference.

Clinical AI projects rarely fail at the model. They fail at the integration layer. This course teaches the standards, tools and decisions that connect live hospital systems to inference engines.

**Who it's for:** ML engineers and AI architects moving into healthcare, software and cloud engineers handling EHR integration, clinical informaticists, and product managers working on health data products.

## Course plan — 4 tracks, 10 modules

| Track | Module | Title | Length |
| --- | --- | --- | --- |
| **A · Foundations & Scoping** | M0 | Start here: This is not a passive course | ~12 min |
| | M1 | Scope & requirements: should you build it, choose your pattern, the Interface Design Document | ~50 min |
| **B · Healthcare Data Fundamentals** | M2 | HL7 v2 messaging deep dive | ~90 min |
| | M3 | FHIR R4 for clinical AI practitioners | ~110 min |
| | M4 | Mirth Connect channel engineering | ~130 min |
| **C · Production Integration** | M5 | Epic EHR integration: SMART on FHIR & CDS Hooks | ~120 min |
| | M6 | FHIR feature extraction for AI models | ~100 min |
| | M7 | Clinical AI inference & CDS Hooks | ~120 min |
| **D · AI Integration & Deployment** | M8 | Document extraction & NLP | ~90 min |
| | M9 | Production, compliance & MLOps | ~100 min |

The full plan, with content and editable lengths, is in [`course-plan/FHIR_Course_Plan.xlsx`](course-plan/FHIR_Course_Plan.xlsx).

## What you build

| Project | Built in | What it does |
| --- | --- | --- |
| Readmission integration scope (hands-on) | Track A | Build Decision Record, pattern map, Interface Design Document and HL7 feed review for one request |
| HL7 → FHIR integration channel | Track B | Mirth ingests ADT and ORU feeds and posts FHIR Patient and Observation resources to HAPI FHIR |
| Real-time sepsis risk pipeline | Track C | FHIR features → XGBoost model → CDS Hooks card, scores saved as FHIR RiskAssessment |
| Clinical NLP pipeline | Track D | DocumentReference notes → scispaCy extraction → structured Observations |

## Repository layout

```
course-plan/                     Course plan spreadsheet
track-a-foundations/
  module-0-start-here/           Recording script + slide source
  module-1-scope-and-requirements/
    lecture-1-should-you-build/
    lecture-2-choose-your-pattern/
    lecture-3-interface-design-document/
  resources/                     Learner downloads (templates, examples, scenario, cheat sheet)
  hands-on/                      Track A exercise: brief, sample HL7 feed, reference solution, deck
track-b-healthcare-data-fundamentals/
track-c-production-integration/
track-d-ai-integration-deployment/
```

Each lecture folder has:

- `script.md` — the recording script: the speaker notes for every slide, in order.
- `deck-source/` — the slide source (`deck.json` plus one HTML file per slide). The presentable decks live as Claude Slides artifacts and export to PowerPoint or PDF. Images in the source point to artifact storage and don't render on GitHub.

## Track A learner resources

| # | Resource | Lecture |
| --- | --- | --- |
| 1 | [Build Decision Record — template](track-a-foundations/resources/01-build-decision-record-template.md) | M1 · L1 |
| 2 | [Build Decision Record — sepsis example](track-a-foundations/resources/02-build-decision-record-sepsis-example.md) | M1 · L1 |
| 3 | [Readmission-risk practice scenario](track-a-foundations/resources/03-readmission-practice-scenario.md) | M1 · L1 and L3 |
| 4 | [Pattern cheat sheet and decision tree](track-a-foundations/resources/04-pattern-cheat-sheet.md) | M1 · L2 |
| 5 | [Interface Design Document — template](track-a-foundations/resources/05-interface-design-document-template.md) | M1 · L3 |
| 6 | [Interface Design Document — sepsis example](track-a-foundations/resources/06-interface-design-document-sepsis-example.md) | M1 · L3 |
| 7 | [Worked practice example — medication reconciliation](track-a-foundations/resources/07-worked-example-medication-reconciliation.md) | M1 · all lectures |

How to use each one: [resources/README.md](track-a-foundations/resources/README.md).

**Track A hands-on:** [Scope the readmission integration](track-a-foundations/hands-on/README.md) — four deliverables, about four hours, ending with a review of a synthetic HL7 v2 discharge feed.

All hospitals, names and figures in the examples are fictional and illustrative.

## Presentations (PowerPoint)

PowerPoint files are not stored in this repo. To build them locally from the slide sources: `python tools/build_pptx.py` (needs `python-pptx` and Playwright with Chromium).

## Status

| Track | Status |
| --- | --- |
| A | Scripts, slides, resources and hands-on ready. M0 recorded. |
| B, C, D | Planned — see each track's README |

## Instructor

Mohcine Madkour, PhD — Senior AI/ML Engineer & Architect, founder of EvalTrust. [LinkedIn](https://www.linkedin.com/in/mohcine-madkour-83a642b2) · [Course site](https://mohcinemadkour.github.io/fhir-course/)
