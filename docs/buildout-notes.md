# Collegium Alexandrinum - build-out notes

Typed from my handwritten 16-page design notes (24 Oct 2026). This is the source of truth for intent. If an agent spec and this file disagree, this file wins until Joshua says otherwise.

## p1 - How humans learn
- **Consuming** (read, watch, get it explained) "feels like learning". It's how we *think* we learn.
- **Producing** (recall, predict, explain, attempt) "feels harder". It's how we *actually* learn.
- How much people remembered:
  - Re-read 4 times: 83% at 5 minutes, 40% at 1 week.
  - Read once, tested 3 times: 71% at 5 minutes, 61% at 1 week.

## p2 - The roles AI can play (10 total roles, "agents")
| Role | Use when |
|---|---|
| Interviewer | Starting out, unsure what you need |
| Mapmaker | A subject feels shapeless |
| Explainer | You tried and are truly stuck |
| Socratic Questioner | You think you understand |
| Examiner | You've covered it once |
| Checker | You made something: summary, proof, code |
| Listener | Explain it back in your own words |
| Diagnostician | The same mistake keeps coming back |
| Sparring Partner | Practising a skill: speaking, interviewing |
| Clerk | Pure logistics: notes, formats, schedules |

## p3 - Spaced repetition
- Memory of a subject decays over time with no review.
- Reviewing at growing gaps (a week, a month, a few months) lifts it back each time.
- **AI does the busywork:** writes flash cards, keeps the schedule, turns mistakes into new cards.

## p4-5 - The Interviewer
**Purpose:**
1. Discover the TRUE reason for the learning topic: an interview, overall knowledge, to build something.
2. Create a baseline of known knowledge, to create a plan (with the Map Maker) that patches knowledge holes.

**Example:**
- Me: "Hey, I want to learn in depth everything I can about AI."
- Agent: "What is this for?"
- Me: "I want a solid, up-to-date knowledge of AI so I can help my clients automate their businesses, but also understand it deep enough that when I talk about it (public or social media) I am regarded as an industry expert."
- Agent: "What do you already know?"
- Result, your plan: Goal = help clients and be an industry expert. Skip = whatever I already know. Practice = XYZ.

**Use it when:** I am starting out and unsure what I need.

## p6 - The Map Maker
**Purpose:** create a learning plan based on the goal and current level of knowledge from the Interviewer.
- If the subject is vast (many subsets), identify the subsets that most closely relate to accomplishing the goal.
- Then map out each learning topic in a flow, explaining why each learning block is there, its objective, and how it builds on the previous.
- If there are multiple options for a learning block, list the top 3 best choices and allow the user to select one.

## p7 - The Explainer ("Professor")
Flow: Read it -> Set it up -> Solve it -> Check it. The student can read and set up but gets stuck on solve and check. AI helps solve and check. Then "redo, no help" loops back to the start.

The agent explains the concept, helps solve it, then generates similar scenarios for the user to solve on their own to confirm understanding.

**Use it when:**
1. The user has tried it and is truly stuck.
2. A new topic has been taught and the level of understanding needs to be gauged.

## p8 - The Socratic Questioner
Example: User: "I get it." Agent: "So what is the difference between X and Y?" User: "Um..." Agent: "What if X doubled?" User: "Oh! It would break."

**It never hands over the answer** (the answer is locked).

**Use it when:** the user thinks they understand; end of a training module; periodic pop quizzes; the user says "Can you make sure I understand [TOPIC]".

**Purpose:** ask the user "why/how" based questions to identify how well they learned the topic.

## p9 - The Examiner
Questions get HARDER EACH TIME. A miss steps back to an easier question, then climbs again.

**Use it when:** a topic has been covered; tests and quizzes; end of a learning module; spot quizzes; the user asks "Quiz me on [TOPIC]".

**Purpose:** create quizzes, exams, flash cards etc. of increasing difficulty to test and record the user's level of knowledge and progress.

## p10 - The Checker
Example: "My summary" with marks: "a step is missing" (it points it out, the user fixes) and "wrong term here".

**Purpose:** assesses that the logic, intermediate steps and reasoning were correct in order to get to the outcome. Similar to "show your work" in basic math.

**Use it when:**
1. The user has created something: a summary, a proof, code, a paper.
2. The same topic is incorrect on multiple exams or quizzes.

## p11 - The Listener
The user's spoken explanation is matched line by line against "the source (training material)". Ticks for covered points, "you missed this" for the gap.

**Purpose:** evaluate the user's ability to verbally explain topics learned. The user dictates an answer to a question based on the topic, and the agent reviews it, then compares it to the source to confirm accuracy.

**Use it when:**
1. Final knowledge check before moving on to the next subject.
2. As a form of pop quiz.
3. The user prompts "Can I explain in my own words [TOPIC]".

## p12 - The Diagnostician
Quiz 1, Test 2 and Pop Quiz 3 each have a miss, and they point to the same shared misunderstanding.

**Purpose:** the agent identifies recurring mistakes, finds the root knowledge gap of the mistakes, and flags that as an area needing targeted training. It uses quizzes, tests, and results from the Listener and Checker agents to identify misunderstandings.

**Use it when:**
1. The user keeps making the same mistake.
2. Run before a module is marked completed.
3. The user prompts "I keep getting [TOPIC] wrong and I don't know why."

## p13 - The Sparring Partner
**Purpose:** test the user's knowledge in a fast-paced conversation format based on the goal. Examples:
- Job interview
- Client challenging the user on a proposed idea
- Debate platform
- Sales call with a cold prospect
- Board room presentation
- Doctoral review board

The agent has a difficulty slider to simulate various levels of interaction. A timer should be set at the beginning of the round for the time the user has to answer.

**Use it when:**
1. The user has finished learning a skill.
2. The course is complete and the user is prepping for the goal.
3. The user prompts "Can you help me get prepared for [TYPE GOAL/EVENT]".

## p14 - The Clerk
**Purpose:** the backbone of the school. It takes the notes, test and quiz results, and other data from agents and:
- Organises notes and quiz/test results.
- Creates flash cards and keeps them up to date.
- Handles scheduling of alerts.
- Maintains the current "knowledge" base of the topic being trained.
- It DOES NOT add to notes. It only organises and formats them in the user's set style.

## p15 - Initiation of school
1. The Interviewer should ask enough questions to gauge the level the user is at.
2. Then explain 2-3 topics at 3 levels: (1) for a child, (2) for a beginner, (3) for an expert. This helps gauge the level of understanding and vocabulary, and confirms the findings in step 1.
3. Based on the assessment from 1 and 2, use resources to create training material written at the level decided from 1 and 2 for the beginning.

## p16 - Tools / skills
- **role-play:** job interview.
- **realistic-task:** simulate a job or task the user would encounter, where the new knowledge should be used to complete the objective.
- **practice-app:** create a simple app that drills on [TOPIC]. Questions should be based on real-world scenarios. Each wrong answer should provide the correct answer, with a final score at the end.

## Decisions made in planning (24 Oct 2026)
- The 1-3 Haiku scouts run **once**, during the curriculum build, to make sure the Map Maker's material is current. After that, agents answer from the course pack. Later: weekly freshness checks for fast-moving fields (AI changes every couple of weeks).
- Routing is "suggested, I confirm" while testing. It goes fully automatic once the logic is proven: the squad should know who to call based on quiz answers and where the student gets stuck.
- Two goals: learn AI to serve clients better, and a possible product ("college in your pocket").
