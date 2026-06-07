# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

My system will cover student reviews, and food rankings for UCLA dining halls. This knowledge is valuable because it teaches students how to get the best food for their dietary needs and get their money’s worth out of expensive meal plans. Official university websites only post basic menus and hours, leaving out the honest student reviews, complaints, and tips needed to navigate the dining system.

---

## Documents

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
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

**Reasoning:**
I believe a recursive chunking strategy makes the most sense due to the format of my sources. Reddit pages and student articles are structured in a predictable way, so chunking from natural structure makes sense. A good chunk size is 600 characters as that covers students' posts/answers on Reddit that are shorter or longer. It's also appropriate for the articles I am sourcing since those are longer but each paragraph is not significantly long. I believe an appropriate overlap is 100 characters, as this should cover any thoughts carrying over in both forum and article sources.

---

## Retrieval Approach

**Embedding model:**
bge-small-en-v1.5 via SentenceTransformers

**Top-k:**
5

**Production tradeoff reflection:**
If cost wasn't a constraint, I would consider a model that was not just trained on general internet data as well as model not strictly optimized for English text. Students' slang which is different across campuses and is worth considering in other languages is not really considered by this model as far as I'm aware. Additionally, students make similar posts on Reddit all the time, so being able to embed all those threads with lower latency would help round out responses rather than focusing on selecting sources that are more unique.

---

## Evaluation Plan

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | What options are there for vegetarian students? | The Study, B Plate, Rende West, and B Cafe. |
| 2 | Is 14P plan good for the semester? | It is the way to go unless you eat a lot as it gives two meals per day. |
| 3 | Which places have long lines usually? | The Study, B Cafe, B Plate, and food trucks.  |
| 4 | Are dishes properly labeled for food allergens? | Some dishes are mislabeled on in-house signs that are properly labeled on the dining website. |
| 5 | Can I take food to go from the dining halls? | All food must be consumed within the dining halls except for one whole fruit or dessert. |

---

## Anticipated Challenges

1. I have some concerns about chunk size since some parts of the documents are for sure a lot longer than 600 characters and I can't guarantee that 100 characters overlap is enough, especially when considering misformatted helpful information.

2. Since my sources are from forums and articles written by students and their opinions are completely subjective, there might be problems with missing attributions and there might be some hallucinations.

---

## Architecture

[1. Document Ingestion] 
 └── Python requests / URL manipulation + copy/paste
       │
       ▼
[2. Chunking]
 └── LangChain (RecursiveCharacterTextSplitter)
       │
       ▼
[3. Embedding + Vector Store] 
 └── BAAI/bge-small-en-v1.5 (via SentenceTransformers) + ChromaDB
       │
       ▼
[4. Retrieval] 
 └── Hybrid Search
       │
       ▼
[5. Generation] 
 └── Groq

---

## AI Tool Plan

1. I will ask Claude to help me clean the Reddit sources with a Python script utilizing the requests library. I will ask it to help me clean data after it is parsed from JSON if needed. I will give it the documents section of this planning.md. I expect the output to be cleaned up documents ready for chunking. I will look over these myself.

2. I'll give Claude my Chunking Strategy section and ask it to implement chunk_text() with LangChain with my specified chunk size and overlap. I will give it the chunking section of this planning.md. I expect a method that will return chunks of my ingested resources. I will scan to make sure chunks make sense. 

3. I will ask Claude to help me call the embedder on my chunks as well as append context headers to chunks before running them through the embedder to add useful context. Then to make sure the results are stored in my ChromaDB. I will then ask it to provide a small script to display what is in the database so I can take a look at the embeddings.

4. I will ask Claude to help me write hybrid_search() to blend BM25 and Vector Search scores to return the top k matching chunks based on my specified query and k value which I previously set to 5.

5. I will use Groq to input the 5 test questions I wrote above requiring it to answer questions as a helpful campus dining assistance, asking it to cite its sources and respond with "I don't have that information" if it can't find references for a query.

**Milestone 3 — Ingestion and chunking:**
# 5 representative chunks:

[7_24] BruinLife — Top 5 best and worst foods at UCLA dining halls
  . Once you take your first bite, the entire pizza – if you can even call it that – crumbles to dust while the toppings fall onto either your plate, yourself or the floor. The tortilla pizzas are a mess to eat and are never satisfying — that is why they are the worst dish the dining halls have to offer.

[6_0] BruinLife — Where to eat at UCLA - meal plans & dining halls
  BruinLife

Image via Daily Bruin Archives
New Student Guide
Where to eat at UCLA: Meal plans, dining halls and campus spots
written by Victoria Sitter September 24, 2025
Starting college means one big question: Where and how do I eat? Luckily, UCLA offers a variety of meal plans designed to fit different lifestyles and appetites, so you won’t have to worry about going hungry between classes.

[6_14] BruinLife — Where to eat at UCLA - meal plans & dining halls
  Making eating at UCLA work for you
With so many options available, finding your favorite spots and meal rhythm might take a little time, and that’s totally okay! Whether you’re fueling up for a big study session or grabbing a quick snack between classes, UCLA’s diverse dining scene has something for every appetite and schedule. Don’t hesitate to explore different dining halls and cafés to discover what fits your taste and lifestyle best.

[1_3] Reddit — UCLA Dining wiki
  You are able to change your meal plan at the end of a quarter. There is a fee. You will lose more money if you downgrade than if you upgrade.

Selling Swipes

Students who live off campus do not have meal plans but may want to eat in the dining halls. As such, you will often find people outside dining halls asking if anyone is selling swipes. There is also a Facebook Group (UCLA Swipe Swap) for this same purpose.

Students with premier meal plans may choose to swipe in these people in exchange for payment.

[2_6] Reddit — How's the food at UCLA?
  Viruses are often the culprit from having some many shared touch points at the dining hall, not the food. It happened at my work and the health department did a thorough investigation. Also, even a little soap left on a cup gives you the runs, so people often blame the food when it could have been 100 other things

The dining hall food is amazing

My family/cousin’s Wouks visit me just so I can swipe them for Sunday lunch/dinner

Used to be excellent before COVID I hear, but it's kinda mid now imo

## Total Chunks: 141

**Milestone 4 — Embedding and retrieval:**

**Milestone 5 — Generation and interface:**
