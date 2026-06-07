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
600 characters

**Overlap:**
100 characters

**Why these choices fit your documents:**
I believe a recursive chunking strategy makes the most sense due to the format of my sources. Reddit pages and student articles are structured in a predictable way, so chunking from natural structure makes sense. A good chunk size is 600 characters as that covers students' posts/answers on Reddit that are shorter or longer. It's also appropriate for the articles I am sourcing since those are longer but each paragraph is not significantly long. I believe an appropriate overlap is 100 characters, as this should cover any thoughts carrying over in both forum and article sources.

**Final chunk count:**
162

---

## Embedding Model

**Model used:** 
all-MiniLM-L6-v2 via SentenceTransformers

**Production tradeoff reflection:**
If cost wasn't a constraint, I would consider a model trained on specialized data rather than just general English internet text. This current model can miss campus-specific slang and struggle with other languages. Additionally, students frequently post similar topics on Reddit. An upgraded pipeline with higher throughput would allow us to ingest and embed those massive message threads efficiently, giving us a denser pool of redundant student discussions to draw from rather than just filtering for highly unique sources.

---

## Grounded Generation

**System prompt grounding instruction:**
You are a helpful assistant that answers questions about UCLA dining.
You must answer using ONLY the context chunks provided below.
If the answer cannot be found in the context, say "I don't have enough information to answer that."
Do not use any outside knowledge. Do not make anything up.
Be concise and direct.

**How source attribution is surfaced in the response:**
I add the following to the prompt to make sure all sources are attributed:
"Answer the question using only the context above. "
"Format your response as:\n"
"Answer: <your answer>\n"
"Sources: <comma-separated list of source names and URLs you used>"
I also make sure that if no relevant chunks are retrieved via hybrid search, the query returns  {"answer": "I don't have enough information to answer that.", "sources": []}.

---

## Evaluation Report

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | What options are there for vegetarian students? | The Study, B Plate, Rende West, and B Cafe.| There are vegetarian options at BPlate, with many liking the kale vinaigrette, zucchini brownies, and they have a vegan sausage that can be made vegetarian by adding cheese. Feast also has okay vegetarian options. Additionally, salad options are available, but dressings might have eggs. | Relevant | Accurate |
| 2 | Is 14P plan good for the semester? | It is the way to go unless you eat a lot as it gives two meals per day. | Yes, 14P is recommended by multiple users. | Relevant | Accurate |
| 3 | Which places have long lines usually? | The Study, B Cafe, B Plate, and food trucks. | Epicuria, Rende, and B Cafe usually have long lines. | Relevant | Partiall accurate |
| 4 | Are dishes properly labeled for food allergens? | Some dishes are mislabeled on in-house signs that are properly labeled on the dining website. | No | Relevant | Partiall accurate |
| 5 | Can I take food to go from the dining halls? | All food must be consumed within the dining halls except for one whole fruit or dessert. | No, all food must be consumed within the dining hall, although you are allowed to take out one whole fruit or dessert. | Relevant | Accurate |

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

**Question that failed:**
Which dining hall hosted the Harry Potter dinner?

**What the system returned:**
I don't have enough information to answer that.
• Reddit — How's the food at UCLA? (https://www.reddit.com/r/ucla/comments/123arn7/hows_the_food_at_ucla/)
• Reddit — UCLA Dining wiki (https://www.reddit.com/r/ucla/wiki/ucladining/)
• DailyBruin — Opinion: dietary restrictions deserve accurate info (https://dailybruin.com/2026/01/20/opinion-students-with-dietary-restrictions-deserve-accurate-information-from-ucla-dining)
• Reddit — Comprehensive dining hall ranking (https://www.reddit.com/r/ucla/comments/rvo8oo/comprehensive_dining_hall_ranking/)

**Root cause (tied to a specific pipeline stage):**
The detail specifying that all themed dinners take place at all four dining halls was in a different chunk than the details regarding the Harry Potter dinner. Since relevant information on where the dinners were hosted and on the themes were split across different chunks, the model did not have enough context to answer correctly.

**What you would change to fix it:**
I believe the core issue is that 600 character chunks were limiting for that specific document. Information on dining halls was at the very beginning of the document while the Harry Potter dinners were mentioned towards the end. Increasing the chunk size or maybe just the overlap would fix the problem and provide more context for queries like the above.

---

## Spec Reflection

**One way the spec helped you during implementation:**
The spec was helpful in reinforcing the concepts learned in class to implement this project. It was really helpful to have the information written out clearly. I was able to easily use AI assistance using the spec document to implement features and receive helpful explanations based on what I was hoping to do with my RAG pipeline.

**One way your implementation diverged from the spec, and why:**
My implementation did not diverge from the spec aside from adding stretch features. I did begin with Hybrid Search from the start from looking at the slides. I was also going to use a different embedding model, but defaulted to the recommended for the sake of simplicty.

---

## AI Usage

**Instance 1**

- *What I gave the AI:*
I asked Claude to help me write an ingestion and a chunking method, giving it the Domain, Documents, and Chunking Strategy part of my spec as well as my pipeline. I told it to use LangChain.
- *What it produced:*
A file containing ingestion and chunking code, utilizing different ingestion methods based on the type of the source I had provided. When executed, it produced a file called chunks.json containing 162 chunks of clean text from all my sources.
- *What I changed or overrode:*
It wanted to make requests to the Reddit API directly, but I had manually downloaded the files since there were only 5 Reddit pages.

**Instance 2**

- *What I gave the AI:*
I asked Claude to help me write an embedding script to store vectors in ChromeDB, telling it to use all-MiniLM-L6-v2 via SentenceTransformers 
and a value of 5 for k as well as my pipeline. 
- *What it produced:*
A file containing embedding code that connected to ChromaDB and used the model to compute embeddings that were then stored in the vector DB.
- *What I changed or overrode:*
I changed the batch size to 64 from 60 so the processing could be slighly faster (I also wanted to make it a power of 2). 

