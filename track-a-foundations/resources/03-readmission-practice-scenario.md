# Resource 3 — Readmission-risk practice scenario

**Track A · Module 1 · Lectures 1 and 3**

Use this scenario for the Lecture 1 and Lecture 3 assignments if you don't have a real request from work. The hospital and every detail are fictional.

## The request

The care-transitions director at Lakeside Regional Hospital emails you:

> “We want an AI model that flags patients at high risk of 30-day readmission, so our team can call them after discharge. Can you plug it into Epic?”

## What you learn in a 30-minute call

- Two transition nurses call high-risk patients within 48 hours of discharge.
- Today they pick patients from a daily discharge report, using their own judgment.
- They can make about 25 calls a day. The hospital discharges about 120 adult patients a day.
- They work from a call list in a spreadsheet, not from the EHR chart.
- Readmission penalties are a concern for hospital leadership.
- The interface team has a backlog of roughly three months.
- Discharge summaries are sent as C-CDA documents to outside primary-care practices.
- Nobody has said who would own the model after go-live.

## Your tasks

1. **Lecture 1:** run the Build Check, do the math and fill in a Build Decision Record.
2. **Lecture 2:** for each data flow you need, pick a pattern with the decision tree.
3. **Lecture 3:** if your verdict is Build or Pilot, draft the Interface Design Document.

## Hints — read after you try

<details>
<summary>Show hints</summary>

- The decision happens once a day, after discharge. Does it need real time?
- The nurses work from a list. What is the lightest path to put a ranked list in front of them?
- One Build Check question has no answer yet. Which one, and what does that mean for your verdict?

</details>
