# Python ACT-R

A Python implementation of the ACT-R cognitive Architecture

Please note that this version of Python ACT-R does not run on Python 3.11 or higher

Install Python ACT-R from the command line using either `pip` or `pip3` as follows:

```bash
pip install python_actr
```

For details, visit the wiki page: https://github.com/CarletonCognitiveModelingLab/python_actr/wiki/PythonACTRTutorials

# Vacuum Agent Simulator

This code builds a grid-like environment and creates a vacuum agent to clean up "mud". The agent is based on the ACT-R cognitive architecture and simulates the behavior of a Roomba-like robot.

### Getting Started

To run the simulation, simply run the code in your preferred Python environment. The required dependencies are:

- AgentSupport
- python_actr
- random

### How it Works

The code defines a `VacuumAgent` class, which is a subclass of python_actr.ACTR. The agent has a `goal` buffer, a body object, and two modules: a motor module and a clean sensor module. The agent's goal is to search the environment and clean all the dirty cells. The agent moves around the environment randomly until it detects dirt, at which point it cleans the cell. The agent's behavior is defined by a set of rules that specify its actions in different situations.

The code also defines a `MyCell` class that represents the cells in the environment. Each cell has a state that can be either "clean" or "dirty".

### Rules

The agent's behavior is defined by a set of rules that specify its actions in different situations. Here are the main rules:

`clean_cell`: If the clean sensor detects dirt, the agent cleans the cell.
`forward_rsearch`: If the agent is doing a random search and there is no wall ahead, the agent moves forward and updates its goal.
`left_rsearch`: If the agent is doing a random search and it reaches the end of a row, it turns left and updates its goal.
`forward_wsearch`: If the agent is doing a wall-following search and there is a wall ahead, the agent turns left and updates its goal.

### World

The code defines a grid-like world using the `grid` module from `python_actr`. The `world` is initialized with a map of cells defined in the `AgentSupport` module. The agent is added to the world at position (5,5) facing north. The world is displayed using the `display` function from python_actr.

### Logging

The code logs all the agent's actions and the state of the environment using the `log_everything` function from `python_actr`. The log is saved in the `AgentSupport` module.

### Acknowledgments

The code was originally written by Terry Stewart at the University of Waterloo and modified by Chris Dancy at Penn State in February 2023. The code uses the `python_actr` library and the `grid` module from `python_actr`. The environment map is defined in the `AgentSupport` module.
