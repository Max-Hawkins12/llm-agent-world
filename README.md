# Project Overview

This project evaluates how different levels of environmental observability affect the performance of Large Language Model (LLM) agents in a simulated 2D grid-world environment. The goal is to compare how access to information and memory influences an agent's ability to complete tasks efficiently.

## Demo

A demonstration of the LLM project can be viewed here:
_Link to be added_

# Installation

1. Check your Python version. This project was developed with Python 3.12.

```bash
python --version
```

2. Create and activate a Python virtual environment.
3. Install dependencies:

```bash
pip  install  -r  requirements.txt
```

4. Create a copy of .env.example as .env
5. Fill `OPENAI_API_KEY` with your own API key and `MODEL_NAME` with a valid model name

# Running

Start the program with:

```bash
python  main.py
```

The agent type and game modifiers can be selected from the first menu.

Once an LLM agent has completed a run its log will be stored in `/logs/<agent_type>/<model_name>-<agent_type>-<timestamp>.log`

# Game Overview

The game consists of an 8x8 2D grid, which contains: the agent (blue circle), a goal (green square), a number of mobs (red circles), and a weapon (yellow square). The objective is to reach the goal tile. The goal remains locked while any mobs are alive. Mobs can only be defeated after the agent has collected the weapon. After every successful player move, all living mobs perform their own movements.

A few game modifiers have been provided:
Mob & Weapon Placement: Either fixed or random locations
Number of Mobs: Between 1 - 4 mobs
Mob Behaviour: Either random movements or linear movement

![Game Example](/images/Game_Grid.png)

# Agent Design

There are currently 4 agent types present, each type aims to give the LLM a differing amount of information to compare the effectiveness of each approach. Each prompt is build using the same general descrption of the world, the goal, and available actions. Along with important rules the LLM must follow when providing a response. However, imformation the LLM revieves about the current world they are in differes between agents. See the Prompt Design section for example prompts.

#### 0. Human Agent

This agent is present in order to test the game functionality works as intended.

#### 1. LLM Agent - Full Game Observability

Provides complete information about the environment and serves as the upper-bound baseline of the LLM's performance.

#### 2. LLM Agent - Local Game Observability

Only provides imformation about nearby entities, forcing the model to explore and make decisions with uncertainty.

#### 3. LLM Agent - Local Game Observability + Memory

Extends the local observability with persistant memory, allowing the model to make decisions based on previously observed entities.

# Prompt Design

Each LLM agent receices a prompt containing:

- A description of the game world
- The objective for winning the game
- A list of available actions to choose from
- Rules for how to respond
- A description of the current game state
  The prompt is constructed dynamically each turn using the agent's observation model.

## Failed Iterations

# Results

The following metrics are collected for each run:

- Total turns taken
- Successful completion status
- LLM token cost
- Invalid responses
- Failed movement attempts

# Repository Structure

src/
├── agents/ **Human and LLM agents**
├── environment/ **Game world and entities**
├── game_flow/ **Agent creation and game execution**
└── ui/ **Rendering and menus**

# Future Additions

Future additons I plan to add. Non exhaustive and in no particular order:

- [ ] Improved logging and statitastical analysis
  - [ ] A log file with only the agents responses for improved readability
  - [ ] A generated report for each agent type's results
  - [ ] Graphical analysis of the data (viewing data in the application)
- [ ] Improved UX/GUI
  - [ ] General overhaul of the renderer
    - [ ] Allow for mouse controlls on the menu
  - [ ] Improved end menu
  - [ ] Allow for restarting the application
  - [ ] Allow for automatically running multiple experiments
- [ ] Additional game settings and goal types
  - [ ] Additonal mob behaviours and pathfinding
  - [ ] More actions by agents
- [ ] Additional observation models
  - [ ] Different memory systems
- [ ] Support for additional models & LLM providers
