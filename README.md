# Snake AI with Deep Q-Learning

A simple implementation of the classic Snake game along with an AI agent that uses Deep Q-Learning (DQN) built with PyTorch.

## Features

- Classic Snake game playable with keyboard controls.
- AI version of Snake for reinforcement learning experiments.
- Deep Q-Network (DQN) implemented with PyTorch.
- Experience Replay memory.
- Epsilon-Greedy exploration strategy.
- Training visualization using Matplotlib.

## Project Structure

```
.
├── agent.py          # AI agent and training loop
├── model.py          # Deep Q-Network model
├── snake_game.py     # Manual Snake game
├── snake_gameai.py   # Snake environment for the AI
├── Helper.py         # Plotting utilities
├── LICENSE           # License for the proyect
└── README.md
```

## Requirements

Install the required dependencies:

```bash
pip install pygame torch numpy matplotlib
```

## Usage

Run the manual version of the game:

```bash
python snake_game.py
```

Run the AI training loop:

```bash
python agent.py
```

## How It Works

The agent observes an 11-dimensional state representation that includes:

- Immediate collision danger.
- Current movement direction.
- Relative position of the food.

Based on this information, the neural network predicts one of three possible actions:

- Move straight.
- Turn right.
- Turn left.

Experiences are stored in replay memory and are intended to be used for training the model through Deep Q-Learning.

## Neural Network


Input (11)
    │
    ▼
Linear (256)
    │
   ReLU
    │
    ▼
Linear (3)


## Current Status

Implemented:

- Snake game environment.
- Neural network model.
- Experience replay memory.
- State representation.
- Epsilon-Greedy action selection.

Planned:

- Complete DQN training step.
- Target Q-value optimization.
- Model checkpointing.
- Improved reward function.
- Hyperparameter tuning.

## Technologies

- Python
- PyTorch
- Pygame
- NumPy
- Matplotlib

## License

This project is dedicated to the public domain under the **Creative Commons Zero v1.0 Universal (CC0 1.0)** license.

You are free to copy, modify, distribute, and use this project for any purpose, including commercial applications, without asking for permission.

For more information, see the [CC0 1.0 Universal License](https://creativecommons.org/publicdomain/zero/1.0/).
