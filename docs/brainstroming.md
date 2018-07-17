## Thoughts

- Project sketch? project plan, 26 weeks, 

- Find out possible Action Path
  - Known clickable elements: graph (tree, forest) search, path context interpretation
    - Web: clickable element **parser** (html and js events), select parser, input parser, **choose a website**, **danger steps**
    - ~~iOS/Android: UI XML files parser~~
  - ~~Unknown clickable elements: reverse engineering of user interfaces~~
    - ~~Not possible to provide an universal solution~~
  - Integrateable SDK for application, **auto parse Action Path**
  - Solving problem from UI testing prespective, frameworks:
    - https://github.com/HuddleEng/PhantomFlow
    - If there are UI testing avaliable, then the interpreation problem is solved
  - Challenges:
    - People don't want manually write UI testing --> search for clickable button and interprete final result --> developer (product manager) defined black box testing
    - Various UI elements, enumerate all different UI instances
    - All possible Action Path may be hard
- Interprete Action path (Caption generations)
  - Application context
  - Final screen text recognization with noise text filtering: **UI changes by stages**
  - Interpreate every action stage: Navigation patterns
- Present Problem
  - Guide UI overlapping (annoying)
  - **Voice assistant (conversation flows)**
    - Generating Interaction utterances API.AI
    - Automatically perfom actions
    - **Monitoring** and **Real time guiding**
    - **User flow v.s. Action Path**
- Input simulations
  - Defining all actions of UI elements, examples
    - button: KEY UP, KEY DOWN, with action time
    - Gestures: gesture path, numbers, length
- UI Evaluations, features
  - Action Time
  - How many steps for an action path
  - Number of taps
  - **if user ask**
  - ...



## Possible outcomes

- Integratable SDK
  - for Web/Mobile
- Voice Assistant
  - Working demo for web app
- Action Path Standards
  - Entry -> Destination Definition
  - Utterance Standards for different elements
  - ...

## Questions regarding papers

- Yang et al. Planning Adaptive Mobile Experiences When Wireframing 
  - What's the algorithm and how ML involved?







- Intermidiate presentation: semester break