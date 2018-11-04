## Fixed Browsing Tasks

You can perform the task in any order you like, but you have to achieve the goal of the task.

| Task | Website Domain | Task Description | Expected Intention Change Point | Entrypoint | Type |
|:--------:|:-------------------:|:--------------------|----------|----------|----------|
| 1 |amazon.de|| 1. looking for iphone; 2. looking for iphone case; 3. looking for wireless charging dock for iphone. | do not remove a feature / **complete open task** / |  |
| 2 |amazon.de||  |  |  |
| 2 |github.com|| 1. looking for trends of javascript; 2. looking for backend framekworks; 3.  select a language from thesis frameworks. |  |  |
| 3 |facebook.com|You are a facebook user, and you have a wide social. However you don't wants to see parenting information in your timeline, you wish to turn them off for a year from your timeline; then recently you start interested in ping pong, you want to join a related local group.| 1. looking for ad settings; 2. find |  |  |
| 4 |twitter.com|You lost your phone and phone number, and you bought a new one. However the old phone number was registered in your twitter account, you want to change it for your account safety. Please find the entrace to change your phone number and password. Then you becomes curious on twitter's settings. You want to know how twitter use your data and prevent twitter collect your data.| 1. Change phone number; 2. change password; 3. find personality settings; |  |  |
| 5 |medium.com|| 1. find tech related articles; 2. looking for websocket related articles; 3. find shared github repository |  |  |
| 6 |bloomberg.com|                                                              | 1. Find out the original article; 2. check related articles; 3. Find the latest article |  |  |
| 7 |ifi.lmu.de|| 1. Official provided study plan; 2. Current offered courses in the upcoming semester; 3. Find out |  |  |
| 8 |quora.com|???|  |  |  |
| 9 |dribbble.com|Assume you were an UX designer, you like Dribbble because its a fantastic to get inspiration from there. Now, you are consiering looking for part-time freelance on Dribbble. The resiponsibility of the job should match for "educational product UX design"| 1. jobs list; 2. reading job descriptions; 3. focus on educational products |  |  |
| 10 |arxiv.org|??? specific paper / specific topic / mobile health / explosive task / give topic / find five papers|  |  |  |
| 11 |youtube.com|You want to be a Youtuber. You wants to know how to earn money from making videos, and what should you concern when you publishing a video.| 1. youtube profits guide; 2. youtube video making tutorial; 3. youtube copyright guide |  |  |
| 11' |youtube.com|looking for videos / consider mainstream study (video) / find funny video send to your friend / find menu resipy videos /|  | | |
| 12 |reddit.com|| ??? |  |  |
| 13 |google.com|| 1. find your settings 2. find your personality settings. 3. find ad recomendation personality settings |  |  |
| 14 |google.com|You can't access your gmail. You want to findout whether gmail are current malfuntioning or not. Contact  instance messaging support.| 1. go to gmail; 2. find google service status monitoring; 3. looking for technical support. |  |  |
| 15 |ielts.org|You want to register ielts test. Your task is to findout is your city has a place  for examination that close to you.  You want to know the requirements for the test and the registration entrace of IELTS test.| 1. find local authority; 2. find requirements; 3. find entrace of registration |  |  |
| 16 |||  |  |  |
| 17 |||  |  |  |
| 18 |||  |  |  |
| 19 |||  |  |  |
| 20 |goal directed task|few website, virous types of tasks| dummy accuont: **control** what can be showed on the website |  |  |
|  |browsing directed task||  |  |  |

## Measurement

1. There are six designed tasks, each task contains three major intent. The participant should be able to finish each task within 5 minutes (record finished/unfinished, **pilot study**). Finish same task with search engine again. 

   - Latin square erase learning effect --> User i: with search engine / without search engine; User i+1: without search engine / with search engine;

     ```
     User i            User i+1
     
     Task1 wSE       Task1 w/oSE
     Task2 wSE       Task2 w/oSE
     Task3 wSE         ...
     Task4 wSE
     Task5 wSE
     Task6 wSE
     ----------------------------
     Task1 w/oSE     Task1 wSE
     Task2 w/oSE     Task2 wSE
     Task3 w/oSE       ...
     Task4 w/oSE
     Task5 w/oSE
     Task6 w/oSE
     
     
     - do not do search engine
     - future work for search engine
     ```

      - Is there a learning effect? Is the second round of perform same task always better than first round?

   - Complete task without search engine / with search engine
     - How search engine influences the result? How much the search engine improve user clickstream? (length and time)
     - Does "with Search Engine" significantly improve user clickstream for all tasks? Which significant test should be used in this case? should based on the first question.
   - Task complete / Task incomplete
     - Is the task description too fuzzy and the user doesn't understand the task properly?
     - Where did the user end up?
     - How much user i clickstream differ from to the shortest clickstream that finished the task?
   - Clickstream of each task, hybrid sequence: action, time, action, time, ..., time, action;
     - Measuring `URLi -> URLj`, `Ti` for time stay on `URLi`;
     - Use the shortest clickstream as ground truth;

2. **Collection purpose**: Two tracks for the first study:

   - Offline group: 20 person

     - Finish 6 tasks, record all clickstreams
   - Online group: people who in offline group: Require all participants install the chrome browser plugin for 1 week (do not say restrict in 10min), measures every day at least 10min. --> **change point study? others??**
   - **Approaches**:

     - **Change point detection**: Hidden markov chain

     - **Productivity**: distance between two change point, shorter means productive; --> Use the shortest path from a participant, mark the path as ground truth. When analyse other user clickstream, compute the shortest path between Dijkstra

       ```
          +--- click k ---+
          |               v 
       click i -----> click j
       ```

     - URL embeddings: next possible click prediction ("network action sequence prediction")

3. **Evaluation** (with trained model), same tasks (PP: Plugin Prediction), two tracks:

   - Use nothing (vanilla, V), use search engine (SE), use plugin (P).

   - vanilla

   - vanilla + SE

   - vanilla + P

   - vanilla + SE + P

     ```
     User i
     ----
     Task 1 V
     Task 2 V
     ----
     Task 1 V + SE
     Task 2 V + SE
     ----
     Task 1 V + P
     Task 2 V + P
     ----
     Task 1 V + SE + P
     Task 2 V + SE + P
     
     User i+1
     ----
     Task 1 V + SE + P
     Task 2 V + SE + P
     ----
     Task 1 V
     Task 2 V
     ----
     Task 1 V + SE
     Task 2 V + SE
     ----
     Task 1 V + P
     Task 2 V + P
     
     User i+2
     ----
     Task 1 V + P
     Task 2 V + P
     ----
     Task 1 V + SE + P
     Task 2 V + SE + P
     ----
     Task 1 V
     Task 2 V
     ----
     Task 1 V + SE
     Task 2 V + SE
     
     User i+3
     ----
     Task 1 V + SE
     Task 2 V + SE
     ----
     Task 1 V + P
     Task 2 V + P
     ----
     Task 1 V + SE + P
     Task 2 V + SE + P
     ----
     Task 1 V
     Task 2 V
     ```

     - Same group of user in evaluation stage, install plugin with trained model. Use about one week, at lease 10min every day.

     - Metrics:

       - `#total_clicks`

       - `#plugin_clicks`

       - `len(clickstream_{ij})`

       - `dist(clickstream_{ij}, clickstream_{kj})`, `dist: manhattan distance`

       - `dist(clickstream_{ij}, clickstream'_{ij})`，`': wSE,w/oSE,V,P`

       - `t-test(clickstream_{i*}, clickstream'_{i*})`: compare two task groups, same user, 

         | Dependent Variable                        | Independent Variable | Control Variable |
         | ----------------------------------------- | -------------------- | ---------------- |
         | `User i`'s clickstream `clickstream_{i*}` | `Task j V`           | `w/oSE, wSE, P`  |

         Task specific? Best control conditions? Best: shortest clickstream

       - `t-test(clickstream_{*j}, clickstream'_{*j})`: compare  two user groups, same task, idependent variables: `user,wSE,w/oSE,V,P`

         | Dependent Variable                          | Independent Variable | Control Variable |
         | ------------------------------------------- | -------------------- | ---------------- |
         | `Task j V`'s clickstream `clickstream_{*j}` | `User i`             | `w/oSE, wSE, P`  |

         User specific? Best control conditions? Best: shortest clickstream

         - how changes the behavior / cyclers , measure changes havior when use the plugin, how they reflect the plugin. qualidative / think cloud / (super) equivelant task for same user. 

     - Method:
       - Accuracy - ratio of usage: `#click_plugin_provided_links / # total_clicks`
       - Optimization Rate: `len(clickstream_i)`
       - Similarity measurement: Pairwise `dist(clickstream_{i}, clickstream_{j})` matrix between participants: similarity between users. / same, similarity between tasks


- Speed up Google Chrome https://support.google.com/chrome/answer/1385029?co=GENIE.Platform%3DDesktop&hl=en (network action predictions ("page prefetch"))
- How does 'Predict Network Actions' work? https://productforums.google.com/forum/#!msg/chrome/GGNrg-qnprE/rDqmu8EGvPwJ



## Questionnaire

1. General questions: age, study program/occupation, male/female, ...
2. What are the top-5 (max to 5, seen pattern) websites that you accessed most during the week? List all of them. (include private use): **indication for people different groups productive use group, compaire user groups** general indications both kind of use, kinf of indications.
3. Explain what is your purpose to acessing the website? For work/study or information browsering/amusing?
4. Do you have a clear purpose when you actually access your top-5 websites? For example, when you login to youtube, are you looking for a specific video or just browsing. Answer the question for all of your top-10 websites. **(two conditions, sometimes just browsing, sometimes looking for specific, motivations to go to the website, cook, just look cat video, both cases, report own, question, description situation why you use it, how, purpose? browsing behavior)**
5. When you use search engine, do you save the website of result to your bookmarks? Why?
6. Do you use browser plugin? What is your major browser? chrome/safari/ie or else?













Video / record participant / record desktop screen / for safety why user spend so much time

record mouse / record click / view / elements that user clicked



Argument: why we dont' record others? find things use







Wild study, pop up ask: "what are you doing?" are you productive, are you browsing for fun.





1. amazon task
2. pilot study
3. ask people in median group





```py
networkx
```



























**Note: **

- **You are not allowed to input URL on browser directly.**
- **Keep pages open if they are required in the task, close the irrelevant pages when you don't need it.**
- You are allowed to do anything, such as open multiple pages, use search engine and etc.
- Close the browser when you finished the task and accomplished the requirement



| ID   | Determined Goal Oriented Task                                | Fuzzy Goal Browsing Task                                     | Aimless Browsing Task                                        | Requirement                                                  | Starting page                             | Category                                 |
| ---- | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ | ----------------------------------------- | ---------------------------------------- |
| 1    | Assume your smartphone was broken, you have 1200 euros as budget. You wants to buy an iPhone, a smart phone case, and a wireless charging dock. Adding them to your cart. | You want to buy three gifts for your best friend and give them to your firends to the birthday party. Add three items to the cart, open the cart when you finished. | Check your interested category, browsing items, add three items to cart within 5 min. | Keep the cart window open and close the others.              | www.amazon.com                            | shopping                                 |
| 2    | You are comparing three most popular frontend desktop frameworks: Electron / NW.js / ReactNative Desktop. Your goal is to find out the latest release download link. | You were a senior developer. Your boss wants you write a report regarding the tends of current development techniques. You want to find the most three popular (top-3 stars) web backend Go frameworks and access their repository,  write their name down on a paper when you decided. | Browsing github and select three github repository your most interested in. | Keep the release download link page open and close the others. | www.github.com                            | development / productivity               |
| 3    | You are looking for a copyleft **logo** for your cloud computing startup, find three candidate logo. | Find **three images** you like the most for these three animals: gopher, cat and dog. | Browsing on dribbble, select three images you like the most while you browsing dribbble. | Keep the selected image window open, and close the others.   | www.dribbble.com                          | information retrieve / productivity      |
| 4    | You are a fresh medieninformatik student major in HCI program. You wants to find out recommended first semester study plan provided by the program, then select "Human-Computer Interaction II" opened in WS18/19 and check previous "Human-Computer Interaction I" opened in SS18 and SS17. | You are a fresh medieninformatik student. You wants to select three lectures, one seminar and one practicum for your study in WS18/19. | Browsing the website for 5 min.                              | Keep the study plan pages open and close the others.         | www.medien.ifi.lmu.de                     | information retrieve / reference / study |
| 5    | You are a international student who want to apply economics program  for your master study at LMU. Find the page for application requirement . |                                                              | Browsing for 5 min.                                          |                                                              | https://www.en.uni-muenchen.de/index.html | information retrieve / reference / study |
| 6    |                                                              |                                                              | Browsing on youtube for 5 min.                               |                                                              | www.youtube.com                           |                                          |
| 7    |                                                              | Find the most recent published a overview paper for these three topics respectively: affective computing, convolutional neural networks, distributed consistency algorithm. | Browsing arxiv for 5 min.                                    |                                                              | www.arxiv.org                             |                                          |
| 8    |                                                              | You want to know how google profiling you based on your history. Find your personality profile that created by Google. | Browsing google for 5 min.                                   |                                                              | google.com                                |                                          |
| 9    | You live in Munich, you want to participate to IELTS test next year on Feburary. Looking for the entrace to register the examination. You must keep seeking and stop when you selected the first track of Feburary test. |                                                              | Browsing IELTS website for 5 min                             |                                                              | ielts.org                                 |                                          |
| 10   | You realized medium.com is a nice place to post blog knowledge. Your boss want you develop a websocket based application via programming language Go, and you want to see how people share their knowledge on medium, your task is to find the most popular github repository relates to websocket that people shared on medium. |                                                              | Browsing posts on medium for 5 min.                          |                                                              | medium.com                                |                                          |
| 11   | ????                                                         | ????                                                         | Browsing facebook for 5 min.                                 |                                                              | www.facebook.com                          |                                          |
| 12   | ????                                                         | ????                                                         | Browsing twitter for 5 min.                                  |                                                              | twitter.com                               |                                          |
|      | You somehow heared about Bloomberg reported a news about China use tiny chips infiltrate U.S companies. You wants to find the article | You want to find the relevant news regarding the progress of China use tiny chips infiltrate U.S companies. | Browsing news on bloomberg in 5 min.                         | Keep news window open if you like, close the others.         | https://www.bloomberg.com/europe          |                                          |
| 13   | You are a fan of Marvel comics, you want to view some spoilers regarding a comming moive "The Avengers 4". Find latest three post that spoilers The Avengers 4. |                                                              | Browsing on reddit in 5 min                                  |                                                              | www.reddit.com                            |                                          |
|      |                                                              |                                                              |                                                              |                                                              |                                           |                                          |
|      |                                                              |                                                              |                                                              |                                                              |                                           |                                          |
|      |                                                              |                                                              |                                                              |                                                              |                                           |                                          |
|      |                                                              |                                                              |                                                              |                                                              |                                           |                                          |
|      |                                                              |                                                              |                                                              |                                                              |                                           |                                          |







# Pilot study

## User 1

| Task ID | Timing | Difficulty (1-5) 1 very easy, 5 very difficult |
| ------- | ------ | ---------------------------------------------- |
| 1-1     |        |                                                |
| 1-2     |        |                                                |
| 1-3     |        |                                                |
| 2-1     |        |                                                |
| 2-2     |        |                                                |
| 2-3     |        |                                                |
| 3-1     |        |                                                |
| 3-2     |        |                                                |
| 3-3     |        |                                                |
| 4-1     |        |                                                |
| 4-2     |        |                                                |
| 4-3     |        |                                                |
| 5-1     |        |                                                |
| 5-2     |        |                                                |
| 5-3     |        |                                                |
|         |        |                                                |
|         |        |                                                |
|         |        |                                                |
|         |        |                                                |

## Questionnaire

- General questions: age, study program/occupation, male/female



- What are the top-5 (max to 5, seen pattern) websites that you accessed most during the week? List all of them. (include private use): **indication for people different groups productive use group, compaire user groups** general indications both kind of use, kinf of indications.



- What is your most common purpose or motivation to acessing the website? Answer in one sentence for each of your top-5 websites.



- Do you have a clear purpose when you access your top-5 websites? For example, when you login to youtube, are you looking for a specific video or just browsing. Answer the question for all of your top-10 websites, answer the most often case.



- When you use search engine seeking for information you want, do you save the website of result to your bookmarks? Why? Answer your most common case.



- What is your major browser? Do you use browser plugin? chrome/safari/ie or else?



- Do you have feedbacks regarding the study? If so, write down bellow.

