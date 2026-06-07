# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

My system will cover student reviews, and food rankings for UCLA dining halls. This knowledge is valuable because it teaches students how to get the best food for their dietary needs and get their money’s worth out of expensive meal plans. Official university websites only post basic menus and hours, leaving out the honest student reviews, complaints, and tips needed to navigate the dining system.

---

## Document Sources

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1 | Reddit | Forum | https://www.reddit.com/r/ucla/wiki/ucladining/ |
| 2 | Reddit | Forum | https://www.reddit.com/r/ucla/comments/123arn7/hows_the_food_at_ucla/ |
| 3 | Reddit | Forum | https://www.reddit.com/r/ucla/comments/15v0jh7/how_rough_is_dining_if_you_are_gluten_intolerant/ |
| 4 | Reddit | Forum | https://www.reddit.com/r/ucla/comments/rvo8oo/comprehensive_dining_hall_ranking/ |
| 5 | Reddit | Forum | https://www.reddit.com/r/ucla/comments/1kl3qwz/meals_as_a_commuter/ |
| 6 | BruinLife | Article | https://bruinlife.com/where-to-eat-at-ucla-meal-plans-dining-halls-and-campus-spots/ |
| 7 | BruinLife | Article | https://bruinlife.com/top-5-best-and-worst-foods-at-the-ucla-dining-halls/ |
| 8 | DailyBruin | Article | https://dailybruin.com/2025/06/08/from-schedule-changes-to-strikes-students-discuss-ucla-dining-experiences|
| 9 | DailyBruin | Article | https://dailybruin.com/2026/01/20/opinion-students-with-dietary-restrictions-deserve-accurate-information-from-ucla-dining |
| 10 | SpoonUniversity | Article | https://spoonuniversity.com/school/ucla/why-themed-dinners-made-ucla-s-dining-halls/ |

---

## Chunking Strategy

**Chunk size:**

**Overlap:**

**Why these choices fit your documents:**

**Final chunk count:**

---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:**

**Production tradeoff reflection:**

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:**

**How source attribution is surfaced in the response:**

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |
| 4 | | | | | |
| 5 | | | | | |

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:**

**What the system returned:**

**Root cause (tied to a specific pipeline stage):**

**What you would change to fix it:**

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:**

**One way your implementation diverged from the spec, and why:**

---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1**

- *What I gave the AI:*
- *What it produced:*
- *What I changed or overrode:*

**Instance 2**

- *What I gave the AI:*
- *What it produced:*
- *What I changed or overrode:*
