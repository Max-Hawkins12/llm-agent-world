# Project Overview

This project explores how Large Language Models can act as agents in a simple grid-world environment. The environment contains a weapon, several moving mobs, and a locked goal. To complete the task, the agent must:

1.  Acquire the weapon.
2.  Defeat all mobs.
3.  Reach the goal tile.

The project focuses on the interface design between the LLM and the game world. Multiple observation representations were tested to determine which information an LLM actually requires to reliably perform goal-directed behaviour.

The final solution uses an Objective-Oriented Observation model that provides only information relevant to the agent's current objective. This reduced navigation errors, improved task completion reliability, and demonstrated the importance of carefully designing observations rather than simply exposing the full game state.

# Installation

1. Check your Python version. This project was developed with Python 3.12.

```bash
python --version
```

2. Create and activate a Python virtual environment.
3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create a copy of .env.example as .env
5. Fill `OPENAI_API_KEY` with your own API key and `MODEL_NAME` with a valid model name

# Running

Start the program with:

```bash
python main.py
```

Once an LLM agent has completed a run, its log will be stored in `/logs/<model_name>-<timestamp>.log`

# Game Overview

The game consists of an 8x8 2D grid, which contains: the agent (blue circle), a goal (green square), a number of mobs (red circles), and a weapon (yellow square). The objective is to reach the goal tile. The goal is locked while there are mobs alive. Mobs can be defeated after the agent has collected the weapon. After every successful player move, all living mobs perform their own movements.

![Game Grid](/images/Game_Grid.png)

# Agent Design

The LLM agent is provided with an Objective-Oriented observation of the world. At each turn, the agent has a clear objective, so to reduce the need for complex reasoning and task prioritisation, the LLM is provided only with the observations required to complete its objective. This approach produced the most reliable task completion behaviour, the fewest reasoning errors, and the most consistent navigation performance.

The final prompt structure is as follows:

- A description of the world and its rules
- A list of available actions
- The action of the previous turn and its outcome
- The world observation and current objective
- An explanation of each objective's goals
- Rules for the response format

This prompt structure gave the LLM enough information about its world and current task to perform its objective, while avoiding unnecessary information that the model would need to process and prioritise. The previous action and its outcome are included to provide short-term feedback and allow the agent to react to failed moves. During testing, providing the full world state often increased the complexity of reasoning. The model had to determine its current objective, identify the relevant target, calculate relative positions, and then select an action. This frequently resulted in navigation mistakes despite all the required information being available.

## Example Logs

The logs of the 10 runs I used to evaluate the LLM can be found in: `/logs/result_logs/`

Example logs from each agent design iteration can be found in: `/logs/design_iterations/`

These logs demonstrate how the different world observations affected the agent's behaviour.

## Design Iterations

**Iteration 1 - Full Coordinate Observation**

I initially provided the LLM with the full coordinates of everything in the environment. My thought was that this mimics how the game logic works internally and provides complete information about the game state. However, this led to frequent navigational errors because the coordinates were misinterpreted. While this representation contained complete information about the environment, it required the model to repeatedly perform coordinate transformations before selecting an action.
On the second turn of log `coordinate_observation_failure.log`, the LLM reasoned "The weapon is located directly above the agent at position (1, 5)." despite the weapon actually being located **below** the agent's position. This type of navigation error was frequent and stemmed from the LLM's struggle to interpret the coordinates.

**Iteration 2 - Coordinates + Direction + Distance**

I then provided the directions and Manhattan distances of the objects, along with their coordinates. This reduced the amount of spatial reasoning required because the model no longer had to calculate relative positions itself. Navigation quality improved, but coordinate-related errors still occurred. During testing, I observed that the model often relied on the coordinate fields even when the direction fields already contained the information required to make a correct move. This suggested that the coordinate data was introducing unnecessary complexity rather than providing useful information.
It is worth noting that after I increased the timeout threshold to 100 turns, there was one test run in which the agent succeeded on this iteration (see the log `distance_direction_iteration_win.log`). This proved that moving away from the coordinates was the right approach. However, it took the agent 85 turns, far more than in improved iterations, due to inconsistent targeting and confusion about the current objective.

**Iteration 3 - Direction + Distance + Explicit Objective**

I then removed coordinates entirely and introduced an explicit current objective. Instead of forcing the model to determine which task to prioritise, the observation indicated whether the agent should acquire the weapon, hunt mobs, or move towards the goal. This significantly improved consistency. Navigation decisions were now based on simple directional information rather than coordinate calculations, and the model no longer needed to reason about task prioritisation itself.

**Iteration 4 - Objective-Oriented Observation (Final)**

The final iteration further reduced the observation to only information relevant to the current objective. When the objective was GET_WEAPON, the observation only contained information about the weapon. When hunting mobs, only information about the closest mob was provided. Exposing all mobs often led to inconsistent targeting behaviour, as the model repeatedly switched between targets. Restricting observations to the closest mob reduced this behaviour and simplified decision-making (see log `goal_oriented_all_mobs_almost_failure.log`). When all mobs were defeated, only the goal information was exposed. This reduced the amount of irrelevant information presented to the model, resulting in the highest task completion rate during testing. Rather than reasoning about every entity in the environment simultaneously, the model only needed to reason about the next step required to complete its current objective.

## Limitations

The agent occasionally becomes stuck when a mob blocks the shortest path to the weapon. Although the previous action and outcome are provided in the prompt, the model does not always use this information to revise its strategy. Future work would investigate short-term memory or stronger feedback mechanisms to improve recovery from failed actions.

# Results

The purpose of these metrics is to evaluate both task completion and agent efficiency. Successful completion demonstrates goal-directed behaviour, while token usage, invalid responses, and failed movement attempts provide insight into how effectively the observation representation supports decision making.

| Run | Success | Turns | Invalid Responses | Input Tokens | Output Tokens |
| --- | ------- | ----- | ----------------- | ------------ | ------------- |
| 1   | Yes     | 22    | 0                 | 5477         | 1127          |
| 2   | Yes     | 20    | 0                 | 4957         | 990           |
| 3   | Yes     | 26    | 0                 | 6453         | 1282          |
| 4   | Yes     | 33    | 1                 | 8194         | 1554          |
| 5   | Yes     | 27    | 3                 | 6729         | 1351          |
| 6   | Yes     | 24    | 0                 | 5966         | 1188          |
| 7   | Yes     | 21    | 1                 | 5208         | 1066          |
| 8   | Yes     | 53    | 1                 | 13211        | 2638          |
| 9   | No      | 24    | 3                 | 5985         | 1153          |
| 10  | Yes     | 36    | 2                 | 8963         | 1772          |

# Repository Structure

```
src/
├── agents/			Human and LLM agents
├── environment/	Game world and entities
├── game_flow/		Agent creation and game execution
└── ui/				Rendering and menus
```
