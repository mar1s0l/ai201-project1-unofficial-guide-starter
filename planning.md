# Project 1 Planning: The Unofficial Guide

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
all-MiniLM-L6-v2 via SentenceTransformers

**Top-k:**
5

**Production tradeoff reflection:**
If cost wasn't a constraint, I would consider a model trained on specialized data rather than just general English internet text. This current model can miss campus-specific slang and struggle with other languages. Additionally, students frequently post similar topics on Reddit. An upgraded pipeline with higher throughput would allow us to ingest and embed those massive message threads efficiently, giving us a denser pool of redundant student discussions to draw from rather than just filtering for highly unique sources.

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
 └── all-MiniLM-L6-v2 (via SentenceTransformers) + ChromaDB
       │
       ▼
[4. Retrieval] 
 └── Hybrid Search (BM25 + Vector Search)
       │
       ▼
[5. Generation] 
 └── Groq (llama-3.3-70b-versatile)

**Stretch Features**
1. Hybrid Search
2. Multi-turn queries
---

## AI Tool Plan

1. I will ask Claude to help me clean the Reddit sources with a Python script utilizing the requests library. I will ask it to help me clean data after it is parsed from JSON if needed. I will give it the documents section of this planning.md. I expect the output to be cleaned up documents ready for chunking. I will look over these myself.

2. I'll give Claude my Chunking Strategy section and ask it to implement chunk_text() with LangChain with my specified chunk size and overlap. I will give it the chunking section of this planning.md. I expect a method that will return chunks of my ingested resources. I will scan to make sure chunks make sense. 

3. I will ask Claude to help me call the embedder on my chunks as well as append context headers to chunks before running them through the embedder for attributions. Then to make sure the results are stored in my ChromaDB.

4. I will ask Claude to help me write hybrid_search() to blend BM25 and Vector Search scores to return the top k matching chunks based on my specified query and k value which I previously set to 5.

5. I will use Claude for a Groq interface to input the 5 test questions I wrote above requiring it to answer questions as a helpful campus dining assistance, asking it to cite its sources and respond with "I don't have that information" if it can't find references for a query.

For multi-turn queries, I asked Claude to create a data structure to keep track of chat history. I asked it to help me cap the history length to avoid sending a lot of tokens to Groq. 

**Milestone 3 — Ingestion and chunking:**

5 representative chunks:

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

## Total Chunks: 162

**Milestone 4 — Embedding and retrieval:**

Query: 'What options are there for vegetarian students?'
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

**Milestone 5 — Generation and interface:**

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
