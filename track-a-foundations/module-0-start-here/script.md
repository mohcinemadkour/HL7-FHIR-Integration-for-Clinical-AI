# Module 0 — Start here: This is not a passive course

Recording script — the speaker notes from each slide, in order.
About 1656 words, roughly 12 minutes at a natural pace.


## Slide 1 — HL7 FHIR Integration for Clinical AI

Hi, and welcome to HL7 FHIR Integration for Clinical AI.

My name is Mohcine Madkour. I’m an AI and machine learning engineer and architect, and for more than a decade I’ve been building AI systems on top of real hospital data — not clean CSV files, but live feeds coming out of interface engines and EHRs.

This first lecture is short. I want to do three things: tell you why I built this course, show you exactly how it’s going to work, and set expectations — because this course asks more of you than most courses on Udemy.

So grab a coffee, and let’s get into it.

## Slide 2 — Most clinical AI projects don’t fail at the model. They fail at the integration layer.

Let me start with the reason this course exists.

Over the years, I’ve watched a lot of clinical AI projects stall. And almost never because the model was bad. The model is usually the easy part. Where they get stuck is the integration layer — getting reliable, timely data out of the hospital and getting the prediction back into the clinician’s workflow.

What you see on screen is a raw HL7 v2 message: an ADT update, a patient segment, and a creatinine result. This is what hospital data actually looks like before anyone cleans it up. If you’re an ML engineer, you’ve probably never been taught to read this — and yet your model lives or dies on it.

[Optional: add a 20-second story of your own here — for example, a feed or mapping problem you hit on MySurgeryRisk or another project, and how long it took to fix.]

So this course is about that missing layer: HL7 v2, FHIR R4, Mirth Connect, Epic — and how to wire them to an inference engine.

## Slide 3 — Built on real hospital data

A quick word about me, so you know where this content comes from.

I hold a PhD in computer science, and I’ve spent my career between research and production. At UF Health I worked on MySurgeryRisk, a surgical risk platform running on real hospital data. Before that I did biomedical informatics research at UTHealth in Houston. In industry, I built predictive-maintenance MLOps for the da Vinci surgical robot fleet at Intuitive Surgical. And today I run EvalTrust, where we evaluate and monitor AI systems for regulated industries like healthcare.

I’m also Mirth Connect certified — and honestly, a lot of what I’ll teach you comes from writing Mirth transformers, debugging HL7 feeds late at night, and sitting in meetings with Epic interface teams.

I’ll put my LinkedIn in the course resources if you want the details.

## Slide 4 — Four kinds of builders

Who is this course for?

If you’re an ML engineer or an AI architect moving into healthcare, this is for you — you know models, and I’ll teach you the data plumbing.

If you’re a software engineer who just got handed an Epic integration or a FHIR project, this is for you too.

If you’re a clinical informaticist, you already know the clinical side — this course gives you the pipeline and ML skills.

And if you’re a researcher with a model that works in a notebook, this is the course that shows you what it takes to run it inside a hospital.

What you don’t need: you don’t need to be an HL7 expert. You do need to be comfortable with Python and willing to open a terminal.

## Slide 5 — This is not a passive course.

Now, an honest warning before we go any further.

This is not a course you watch at 2x speed while answering email. If that’s what you’re looking for, there are plenty of free videos out there, and I won’t be offended.

In this course, you’ll be running code. You’ll stand up a HAPI FHIR server, build Mirth channels, push real HL7 messages through them, and watch them fail. Then you’ll fix them. That’s the point.

Every module ends with something that runs — not a quiz, not a certificate screen, but a working piece of a clinical data pipeline that you can show to a hiring manager or reuse on your next project.

If that sounds like the kind of learning you want, you’re in the right place.

## Slide 6 — What AI can and can’t do for you

Let’s talk about AI for a second, because it changes how you should learn this material.

Tools like Claude or ChatGPT are genuinely good at explaining HL7 and FHIR. Ask one what an OBX segment is, or what fields a FHIR Observation has, and you’ll get a solid answer. It can even draft a first version of a Mirth transformer for you. I use these tools every day, and you should too.

But here’s what they can’t give you. They can’t tell you why your ADT A08 updates are creating duplicate patients in your feature store. They can’t tell you which mapping choice will break when the hospital upgrades Epic next year. And they can’t give you the instinct you only get from having fixed these things in production.

That gap — between knowing the definition and making the right call on a real interface — is exactly what this course is designed to close.

## Slide 7 — Three rules for this course

So here are the three rules I followed when I built this course.

First: pipelines over slides. I’ll use slides to frame ideas, but every module ends with something that actually runs on your machine.

Second: code over definitions. You won’t memorize the HL7 segment list. You’ll parse real messages, and the segments will stick because you needed them.

Third: judgment over lookup. Anything you can look up, I’ll keep short. Where I’ll slow down is on the decisions: HL7 v2 or FHIR for this use case, where to put the transformation logic, when to say no to an interface request. That’s where experience matters, and that’s what I want to pass on to you.

## Slide 8 — Four tracks, ten modules

Here’s the map of the whole course: four tracks, ten modules.

Track A is foundations and scoping. You’re in Module 0 right now — this orientation. Module 1 comes before any code, on purpose. We’ll ask the questions that should come first on any integration project: should you build this interface at all? Is HL7 v2, FHIR or an API the right pattern? And you’ll write your first Interface Design Document.

Track B gives you the fundamentals, Modules 2 to 4: HL7 v2 messaging, FHIR R4, and Mirth Connect channel engineering. This is where you build your first pipeline, from HL7 v2 to FHIR.

Track C, Modules 5 to 7, takes you into production integration: SMART on FHIR and CDS Hooks with Epic, building features from FHIR resources, and running real-time inference. That’s where the sepsis pipeline comes together.

And Track D, Modules 8 and 9, covers clinical NLP, compliance and MLOps — de-identification, the model registry, drift monitoring and FDA software-as-a-medical-device considerations.

You can go straight through. If you already know HL7 v2 well, feel free to move faster through Track B — but don’t skip Track A.

## Slide 9 — Three working pipelines

By the end of the course, you’ll have built three pipelines.

Number one: an HL7-to-FHIR integration channel. A Mirth Connect channel that takes live HL7 v2 ADT and ORU messages, parses the clinical observations, and posts them as FHIR R4 Patient and Observation resources to a local HAPI FHIR server.

Number two: a real-time sepsis risk pipeline. You’ll extract features from FHIR, run them through an XGBoost model, surface the result as a CDS Hooks alert card in the clinician’s workflow, and store the score as a FHIR RiskAssessment.

Number three: a clinical NLP pipeline. You’ll pull notes through FHIR DocumentReference, extract medications and diagnoses with scispaCy, and write structured Observations back.

These are portfolio pieces. Put them on GitHub, show them in interviews, or use them as the starting point for real work.

## Slide 10 — How every lesson works

Every lesson follows the same loop, so you always know what’s next.

One: watch a short lecture. I keep them focused on one idea.

Two: run the lab. You’ll get starter code, Docker setups and sample HL7 messages in the course resources.

Three: compare your result with my reference solution.

Four: build your own version — I’ll give you a slightly different use case so you can’t just copy mine.

And five, my favorite: break it. Send it a malformed message, a missing field, a unit it doesn’t expect. Hospitals send you messy data every day, and the engineers people trust are the ones whose pipelines fail safely.

You’ll pause these videos a lot. You’ll get stuck. That’s normal — and that’s when you’re actually learning. Use the Q&A section; I read it.

## Slide 11 — By the end, you can…

So how will you know this course worked for you?

Not by the completion certificate. You’ll know it worked when you can look at a raw HL7 message and immediately spot the problem — the wrong encoding, the missing segment, the unit that will break your model.

You’ll know it worked when you can sit across from a hospital interface team and defend your design: why FHIR here, why HL7 v2 there, why this mapping and not that one.

And you’ll know it worked when you can take a model from a notebook all the way to an alert in front of a clinician, end to end.

And if you disagree with how I did something in this course — good. Tell me in the Q&A. Some of the best improvements to this course will come from students who pushed back.

## Slide 12 — Let’s build.

That’s it for the introduction.

Before you move on, do two things. First, go to the resources for this lecture and set up your environment — Docker, Python, and the course repository. It takes about [__ minutes], and you’ll need it from Module 1 on.

Second, introduce yourself in the Q&A: tell me your role and what you want to build with HL7 and FHIR. It helps me point you to the right parts of the course.

In the next module, before we write a single line of code, we’ll answer the most important question in any integration project: should you build this interface at all — and if so, how?

See you there.
