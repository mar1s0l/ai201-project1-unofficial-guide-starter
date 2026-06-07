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
It wanted to make requests to the Reddit API directly, but I had manually downloaded the files since there were only 5 Reddit pages. I changed how it consumed the documents for ingestion.

**Instance 2**

- *What I gave the AI:*
I asked Claude to help me write an embedding script to store vectors in ChromeDB, telling it to use all-MiniLM-L6-v2 via SentenceTransformers 
and a value of 5 for k as well as my pipeline. 
- *What it produced:*
A file containing embedding code that connected to ChromaDB and used the model to compute embeddings that were then stored in the vector DB.
- *What I changed or overrode:*
I changed the batch size to 64 from 60 so the processing could be slighly faster (I also wanted to make it a power of 2).


## Stretch Features

1. Hybrid Search

   - implemented from the start
   - BM25 and semantic scores are combined via Reciprocal Rank Fusion

Queries and comparisons: 

The Harry Potter query shows Semantic as better than BM25 and Hybrid. It returned chunks about themed dinners while the other two strategies missed those chunks. The dietary restrictions query shows BM25 as better than Semantic and Hybrid as the vocabulary used for accommodations and restrictions seems to be similar across posts so key word matching works well. The commuter meal plan query shows the value of Hybrid search, since it needs both the keyword "commuter" and semantic understanding of meal plan context to provide better context chunks.


Query: 'Which dining hall hosted the Harry Potter dinner?'

--- Semantic ---
  [1] SpoonUniversity — Why themed dinners made UCLA dining halls great
       score: 0.3102
       text:  The Potter fans definitely came through that night because it was by far the most crowded dining hal…
  [2] DailyBruin — Opinion: dietary restrictions deserve accurate info
       score: 0.4563
       text:  After her recent meal plan downgrade to the 14 Premier plan, Wang said she cannot waste a dining hal…
  [3] SpoonUniversity — Why themed dinners made UCLA dining halls great
       score: 0.4710
       text:  . These special meals popped up a couple of times each quarter at all four dining halls. The themes …
  [4] Reddit — Comprehensive dining hall ranking
       score: 0.4715
       text:  Comprehensive dining hall ranking

Alright, I want to ask how you guys would rank the dining halls?
…
  [5] SpoonUniversity — Why themed dinners made UCLA dining halls great
       score: 0.4833
       text:  . The menu included some Potter-specific dishes as well as familiar British bites: toad-in-the-hole,…

--- BM25 ---
  [1] Reddit — How's the food at UCLA?
       score: 8.3662
       text:  It's true pre Covid dining hall here was peak

I swear the food just hit different man. The Feast wa…
  [2] Reddit — How's the food at UCLA?
       score: 7.4699
       text:  Viruses are often the culprit from having some many shared touch points at the dining hall, not the …
  [3] Reddit — UCLA Dining wiki
       score: 6.0738
       text:  * De Neve has a bathroom in the back, B-plate has bathrooms on the left of the entrance, Covel’s bat…
  [4] BruinLife — Top 5 best and worst foods at UCLA dining halls
       score: 6.0478
       text:  . The smoky flavor is definite but not overpowering and the dip itself is light, fresh and creamy. A…
  [5] DailyBruin — Schedule changes to strikes - student dining experiences
       score: 6.0022
       text:  This year, the American Federation of State, County and Municipal Employees Local 3299 – which repre…

--- HYBRID ---
  [1] Reddit — How's the food at UCLA?
       score: 0.0311
       text:  It's true pre Covid dining hall here was peak

I swear the food just hit different man. The Feast wa…
  [2] Reddit — UCLA Dining wiki
       score: 0.0304
       text:  * De Neve has a bathroom in the back, B-plate has bathrooms on the left of the entrance, Covel’s bat…
  [3] DailyBruin — Opinion: dietary restrictions deserve accurate info
       score: 0.0300
       text:  After her recent meal plan downgrade to the 14 Premier plan, Wang said she cannot waste a dining hal…
  [4] Reddit — Comprehensive dining hall ranking
       score: 0.0291
       text:  Comprehensive dining hall ranking

Alright, I want to ask how you guys would rank the dining halls?
…
  [5] DailyBruin — Opinion: dietary restrictions deserve accurate info
       score: 0.0277
       text:  “We encourage students to be proactive by consulting dining room staff for assistance and avoiding s…
────────────────────────────────────────────────────────────

Query: 'What are good options for students with dietary restrictions?'

--- Semantic ---
  [1] DailyBruin — Opinion: dietary restrictions deserve accurate info
       score: 0.3420
       text:  Despite these upsetting anecdotes, UCLA Dining seems indifferent to the daily struggle of being a st…
  [2] DailyBruin — Opinion: dietary restrictions deserve accurate info
       score: 0.4226
       text:  It’s crucial that our university takes more rigorous measures to protect the safety of students with…
  [3] DailyBruin — Opinion: dietary restrictions deserve accurate info
       score: 0.4279
       text:  Daily Bruin Log
Opinion, Opinion Columns
Opinion: Students with dietary restrictions deserve accurat…
  [4] Reddit — Gluten intolerant dining
       score: 0.4336
       text:  vegetarian at ucla is amazing they accommodate really well. i can’t speak for gluten intolerance but…
  [5] Reddit — UCLA Dining wiki
       score: 0.4434
       text:  BPlate: “Healthy” food. People either love it or hate it. Portions are generally smaller with lo…

--- BM25 ---
  [1] Reddit — How's the food at UCLA?
       score: 9.9496
       text:  I agree with everyone who says your experience depends on your dietary restrictions. It's generally …
  [2] DailyBruin — Opinion: dietary restrictions deserve accurate info
       score: 8.7412
       text:  It’s crucial that our university takes more rigorous measures to protect the safety of students with…
  [3] DailyBruin — Opinion: dietary restrictions deserve accurate info
       score: 8.5621
       text:  Despite these upsetting anecdotes, UCLA Dining seems indifferent to the daily struggle of being a st…
  [4] DailyBruin — Opinion: dietary restrictions deserve accurate info
       score: 8.2174
       text:  When labels include allergens that are not actually present, it is up to students with dietary restr…
  [5] DailyBruin — Opinion: dietary restrictions deserve accurate info
       score: 7.0743
       text:  UCLA Dining recommends that students with allergies review nutritional information on its website. C…

--- HYBRID ---
  [1] DailyBruin — Opinion: dietary restrictions deserve accurate info
       score: 0.0323
       text:  Despite these upsetting anecdotes, UCLA Dining seems indifferent to the daily struggle of being a st…
  [2] DailyBruin — Opinion: dietary restrictions deserve accurate info
       score: 0.0323
       text:  It’s crucial that our university takes more rigorous measures to protect the safety of students with…
  [3] Reddit — How's the food at UCLA?
       score: 0.0307
       text:  I agree with everyone who says your experience depends on your dietary restrictions. It's generally …
  [4] DailyBruin — Opinion: dietary restrictions deserve accurate info
       score: 0.0296
       text:  Daily Bruin Log
Opinion, Opinion Columns
Opinion: Students with dietary restrictions deserve accurat…
  [5] Reddit — UCLA Dining wiki
       score: 0.0293
       text:  BPlate: “Healthy” food. People either love it or hate it. Portions are generally smaller with lo…
────────────────────────────────────────────────────────────

Query: 'How do meal plans work for commuters?'

--- Semantic ---
  [1] Reddit — Meals as a commuter
       score: 0.3677
       text:  Meals as a Commuter

Hey guys, recently admitted transfer student who will be commuting and won't sp…
  [2] BruinLife — Where to eat at UCLA - meal plans & dining halls
       score: 0.3719
       text:  Regular Plans, or 19 Regular, 14 Regular or 11 Regular: These plans give you a fixed number of meals…
  [3] Reddit — Meals as a commuter
       score: 0.4060
       text:  Occasionally Ill get friends to swipe me in but we have different majors and very different schedule…
  [4] Reddit — UCLA Dining wiki
       score: 0.4151
       text:  ## Meal plan information

You can’t select a housing plan without a meal plan. The number means how …
  [5] Reddit — UCLA Dining wiki
       score: 0.4280
       text:  * 12am-2am: Late late night

Weekends

* 7am-9am: Continental breakfast

* 9am-5pm: Brunch

* 5p…

--- BM25 ---
  [1] BruinLife — Where to eat at UCLA - meal plans & dining halls
       score: 9.9264
       text:  BruinLife

Image via Daily Bruin Archives
New Student Guide
Where to eat at UCLA: Meal plans, dining…
  [2] BruinLife — Where to eat at UCLA - meal plans & dining halls
       score: 7.0675
       text:  Premier Plans, or 19 Premier, 14 Premier or 11 Premier: These plans are more flexible. You get a set…
  [3] Reddit — UCLA Dining wiki
       score: 6.8813
       text:  You are able to change your meal plan at the end of a quarter. There is a fee. You will lose more mo…
  [4] BruinLife — Where to eat at UCLA - meal plans & dining halls
       score: 5.7782
       text:  Regular Plans, or 19 Regular, 14 Regular or 11 Regular: These plans give you a fixed number of meals…
  [5] Reddit — UCLA Dining wiki
       score: 5.7761
       text:  ## Useful Sites

* UCLA Live Menus
* Plans and Pricing
* Hours of Operation
* Meal Plan Balance…

--- HYBRID ---
  [1] BruinLife — Where to eat at UCLA - meal plans & dining halls
       score: 0.0318
       text:  Regular Plans, or 19 Regular, 14 Regular or 11 Regular: These plans give you a fixed number of meals…
  [2] BruinLife — Where to eat at UCLA - meal plans & dining halls
       score: 0.0303
       text:  Understanding meal plans and swipes
If you live on campus, you’ll select a meal plan that fits your …
  [3] Reddit — UCLA Dining wiki
       score: 0.0300
       text:  You are able to change your meal plan at the end of a quarter. There is a fee. You will lose more mo…
  [4] Reddit — UCLA Dining wiki
       score: 0.0297
       text:  ## Meal plan information

You can’t select a housing plan without a meal plan. The number means how …
  [5] Reddit — Meals as a commuter
       score: 0.0296
       text:  Occasionally Ill get friends to swipe me in but we have different majors and very different schedule…


2. Multi-turn queries

   - maintain a conversation history limited to 4 history tokens


## Sample Chunks

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

## Retrieval Test Examples


Query: 'What options are there for vegetarian students?'
The chunks returned all mention key words vegetarian, and include references to specific food offerings, be they good or bad.

Top 5 results (hybrid BM25 + ChromaDB):

  [1] Reddit — UCLA Dining wiki  (rrf=0.0325)
       url:  https://www.reddit.com/r/ucla/wiki/ucladining/
       text: BPlate: “Healthy” food. People either love it or hate it. Portions are generally smaller with lots of vegan/vegetarian options. Many like the kale vinaigrette, zucchini brownies, and salmon. Some people bash it for being too healthy but you gotta experiment with dressings, seasonings, etc to really get the good stuff. They have the best quality salmon and some top tier meats. Popular for weekend brunch with usually the longest omelet line. Allergen-friendly pantry at the back for students who need it.



To-Go Options

  [2] Reddit — Comprehensive dining hall ranking  (rrf=0.0310)
       url:  https://www.reddit.com/r/ucla/comments/rvo8oo/comprehensive_dining_hall_ranking/
       text: Wow this was long, but I'm curious if/why you disagree, and what your favorite places are.

I mean ur vegetarian so u really don’t get to experience half the dishes. The difference between bplate quality meat dishes and De neve quality is absurd. Bplate wins by a landslide in that department

I'm actually transitioning out of being vegetarian, but I haven't tried any meat at bplate, so I'll have to do that. I've had brisket at de Neve, chicken tacos at de Neve, a sandwich at the study, and a few things at epicuria

  [3] Reddit — Gluten intolerant dining  (rrf=0.0310)
       url:  https://www.reddit.com/r/ucla/comments/15v0jh7/how_rough_is_dining_if_you_are_gluten_intolerant/
       text: As a vegetarian who doesn't eat eggs (comes as a surprise to Americans because eggs aren't considered vegetarian where I'm from), it was a bit of a nightmare. From going to dining halls daily in the fall last year to like twice this spring, you'll get bored very quickly by the lack of options. They do have a bunch of salad options but the dressings might have eggs

There’s locked gluten free rooms in the dining halls. You have to set it up with ResLife because they’ll add your student ID to be able to open the door.

  [4] Reddit — Comprehensive dining hall ranking  (rrf=0.0303)
       url:  https://www.reddit.com/r/ucla/comments/rvo8oo/comprehensive_dining_hall_ranking/
       text: most people i know think epicuria is the best so that's def a popular opinion

personally i think bplate is the most unique, interesting, and worth it heheh

what is the vegetarian version of the sausage sandwich? :0 I’ve never seen that there

they have a vegan sausage and if you put cheese on it, it's vegetarian haha

wow I’ve never tried that! thank u!!

which ones are bufet style?

  [5] Reddit — UCLA Dining wiki  (rrf=0.0296)
       url:  https://www.reddit.com/r/ucla/wiki/ucladining/
       text: **Feast**: Asian-inspired food. A bit on the smaller side and always crowded. The meals they serve at lunch are generally better than dinner. Salad bar includes hot white and brown rice daily. Not too many desserts, but the green tea soft serve and pineapple dole whip are to die for. Vegetarian options here are okay.

────────────────────────────────────────────────────────────

Query: 'Is 14P plan good for the semester?'
Chunks 1, 4, and 5 returned all mention dining plans and include personal anecdotes on whether the plan was liked by the students. Chunks 2 and 3 are not as relevant since they primarily display meal periods but not lines during them.

Top 5 results (hybrid BM25 + ChromaDB):

  [1] Reddit — Gluten intolerant dining  (rrf=0.0328)
       url:  https://www.reddit.com/r/ucla/comments/15v0jh7/how_rough_is_dining_if_you_are_gluten_intolerant/
       text: 19P meant that I always had 40-50 swipes extra every quarter which included swiping friends in everyday and eating all I could (and more). That 40-50 meal difference is the difference between 14P and 19P mathematically speaking so 14P should be more than enough. However for a couple hundred bucks more you do have assurance that you’ll have lots of extra meals and given that you can use swipes in Ackerman now you can easily sell each ticket for $5-7 which means the cost evens out either way

I had 19p as a vego and it was great would, recommend!

14p is the way to go

  [2] Reddit — UCLA Dining wiki  (rrf=0.0304)
       url:  https://www.reddit.com/r/ucla/wiki/ucladining/
       text: ## Meal plan information

You can’t select a housing plan without a meal plan. The number means how many meals you get per week. “P” is a premier meal plan. You can swipe for a meal more than once in the designated meal time if you have a “P” plan. There are 5 meal periods each day. If you have an “R” (for regular) plan, then you can only swipe once per meal period.



Meal periods

Weekdays

* 7am-11am: Breakfast

* 11am-5pm: Lunch

* 5pm-9pm: Dinner

* 9pm-12am: Late night

* 12am-2am: Late late night

Weekends

* 7am-9am: Continental breakfast

* 9am-5pm: Brunch

  [3] Reddit — UCLA Dining wiki  (rrf=0.0303)
       url:  https://www.reddit.com/r/ucla/wiki/ucladining/
       text: * 12am-2am: Late late night

Weekends

* 7am-9am: Continental breakfast

* 9am-5pm: Brunch

* 5pm-9pm: Dinner

* 9pm-12am: Late night

* 12am-2am: Late late night



Meal plan options
*Listed by decreasing cost*

19P → 19 meals per week for you to use however. They roll over each week, but not each quarter

14P → 14 meals per week for you to use however. They roll over each week, but not each quarter

19R →  19 meals per week. The meals reset each week and the unused swipes are lost

  [4] Reddit — Gluten intolerant dining  (rrf=0.0303)
       url:  https://www.reddit.com/r/ucla/comments/15v0jh7/how_rough_is_dining_if_you_are_gluten_intolerant/
       text: vegetarian at ucla is amazing they accommodate really well. i can’t speak for gluten intolerance but i know that some dining halls have gluten-free pantries that you can ask for access for

Lots of restaurants on campus like Rende for example will make your food for you gluten free if you let them know and will make sure there isn’t cross contamination, also dining halls and pretty good veg options, but 14p is definitely the way to go unless u eat a lot

As someone who had 19p and eat all my swipes.... It not worth it unless you're some kind of athlete

  [5] Reddit — Gluten intolerant dining  (rrf=0.0301)
       url:  https://www.reddit.com/r/ucla/comments/15v0jh7/how_rough_is_dining_if_you_are_gluten_intolerant/
       text: I had 19p as a vego and it was great would, recommend!

14p is the way to go

You need to reach out to the CAE to let them know about being GF if you want access to the GF pantries. Annoyingly, you may have to prove medical necessity. Here is the link to what’s inside the pantry.

You can also look through the menu to see what’s being offered each day and what allergens/dietary restrictions they have.

in general u should be able to piece together a meal at every dining hall, some nights the entrees are better than others but there’s always sides you can eat to form a meal

────────────────────────────────────────────────────────────

Query: 'Which places have long lines usually?'
The chunks returned all mention key words long lines, and include references to specific restaurants.

Top 5 results (hybrid BM25 + ChromaDB):

  [1] Reddit — Comprehensive dining hall ranking  (rrf=0.0328)
       url:  https://www.reddit.com/r/ucla/comments/rvo8oo/comprehensive_dining_hall_ranking/
       text: when are u going to epicuria bc the lines inside are always so long HAHA esp the pizzas and dessert lines

okay i should have mentioned, last quarter I  usually ate lunch at 11 and dinner at 5, so it was usually right when it opened, and the only line was waiting for them to open the doors. I do remember the dessert line being long at times, though.  I also rarely got the pizza.

Lol in that case lines aren't to long anywhere...I eat dinner at 5 usually also!

most people i know think epicuria is the best so that's def a popular opinion

  [2] Reddit — UCLA Dining wiki  (rrf=0.0313)
       url:  https://www.reddit.com/r/ucla/wiki/ucladining/
       text: ### Menus for To-Go Options

Rende: Rende East is East Asian fast food while Rende West is Mexican fast food. West has the best burritos ever, there are customizable ones or you can choose from a menu. And there’s impossible meat for the vegetarians out there. There's usually a super long line but overall it doesn’t take too long. East is basically panda express. It offers boba, though it can be a bit hard. DO NOT get the pad thai, it's just an orange glob.

  [3] DailyBruin — Schedule changes to strikes - student dining experiences  (rrf=0.0311)
       url:  https://dailybruin.com/2025/06/08/from-schedule-changes-to-strikes-students-discuss-ucla-dining-experiences
       text: “Usually, the lines would be shorter because people aren’t willing to walk all the way up and order and get it (food),” Jung said. “Sometimes it’s faster if there’s no mobile ordering.”

UCLA Dining also changed its website at the beginning of spring quarter. UCLA Housing said in an emailed statement that the update was meant to align the design with other university web pages, increase compatibility with a new food management system and improve user experience.

  [4] Reddit — UCLA Dining wiki  (rrf=0.0302)
       url:  https://www.reddit.com/r/ucla/wiki/ucladining/
       text: ## To-Go Options

General Notes
* All To-Go Places have “meal combos” that equal one swipe. Typically, this includes one entree (i.e. sandwich, mini pizza, etc), one side (chips, whole fruit), and a drink.
* Specialty beverages (i.e. specialty coffee beverages, smoothies) usually include a pastry for one swipe (not always though).
* Most To-Go Places have tables within the restaurant that allow you to eat there. As the name suggests, you can also take your food out of the restaurant and eat at other places.

  [5] Reddit — Comprehensive dining hall ranking  (rrf=0.0294)
       url:  https://www.reddit.com/r/ucla/comments/rvo8oo/comprehensive_dining_hall_ranking/
       text: 6. B CAFE
Okay, so it's not that I dislike b cafe....I want to like it. But I wish the sandwiches were a little more customizable. There's only one vegetarian sandwich, and I personally don't love the cookies as of late. I also don't like how much sauce goes into them sometimes, although I know most people aren't bothered by sauce on their food. The lines are often too long for what you get, but it's good for the occasional sandwich craving.

## Example System Responses

Loading embedding model: all-MiniLM-L6-v2
Connecting to ChromaDB at: data/chroma_db
Loading BM25 index from data/bm25_index.pkl
✓ HybridRetriever ready

"Are dishes properly labeled for food allergens?"
('No', '• DailyBruin — Opinion: dietary restrictions deserve accurate info (https://dailybruin.com/2026/01/20/opinion-students-with-dietary-restrictions-deserve-accurate-information-from-ucla-dining)\n• BruinLife — Top 5 best and worst foods at UCLA dining halls (https://bruinlife.com/top-5-best-and-worst-foods-at-the-ucla-dining-halls/)\n• Reddit — Gluten intolerant dining (https://www.reddit.com/r/ucla/comments/15v0jh7/how_rough_is_dining_if_you_are_gluten_intolerant/)')

"Can I take food to go from the dining halls?"
('No, all food must be consumed within the dining hall, although you are allowed to take out one whole fruit or dessert.', '• Reddit — UCLA Dining wiki (https://www.reddit.com/r/ucla/wiki/ucladining/)\n• Reddit — Meals as a commuter (https://www.reddit.com/r/ucla/comments/1kl3qwz/meals_as_a_commuter/)')

"What is the cost of a salad?"
("I don't have enough information to answer that.", '• BruinLife — Top 5 best and worst foods at UCLA dining halls (https://bruinlife.com/top-5-best-and-worst-foods-at-the-ucla-dining-halls/)\n• Reddit — Meals as a commuter (https://www.reddit.com/r/ucla/comments/1kl3qwz/meals_as_a_commuter/)\n• Reddit — Gluten intolerant dining (https://www.reddit.com/r/ucla/comments/15v0jh7/how_rough_is_dining_if_you_are_gluten_intolerant/)')

## Interface Details

There is a box at the top for the user query followed by two buttons: one submit the query, and the other resets the multi-turn conversation with the assistant. Below the buttons, there are two boxes: one for the assistant's response, and another for the sources used to answer the query. For example:

🍽️ UCLA Dining Assistant
Ask anything about UCLA dining halls, meal plans, food options, or dietary restrictions. Answers are grounded in student reviews and campus resources only.

Your question
[ Which dining hall has the best vegan options? ]

Ask
Reset conversation 

Answer
[ B-Plate                                       ]
Retrieved from  
[  • BruinLife — Top 5 best and worst foods at UCLA dining halls (https://bruinlife.com/top-5-best-and-worst-foods-at-the-ucla-dining-halls/)
• DailyBruin — Schedule changes to strikes - student dining experiences (https://dailybruin.com/2025/06/08/from-schedule-changes-to-strikes-students-discuss-ucla-dining-experiences)
• Reddit — Gluten intolerant dining (https://www.reddit.com/r/ucla/comments/15v0jh7/how_rough_is_dining_if_you_are_gluten_intolerant/) ]
