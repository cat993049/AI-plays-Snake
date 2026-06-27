import torch
import random
import numpy as np
from collections import deque

from model import Linear_QNet

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


class Agent:
    def __init__(self):
        self.n_games = 0
        self.epsilon = 0
        self.gamma = 0.9
        self.memory = deque(maxlen=100_000)

        self.model = Linear_QNet(11, 256, 3)
        self.lr = 0.001

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def get_action(self, state):
        self.epsilon = 80 - self.n_games
        final_move = [0, 0, 0]

        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 2)
        else:
            state0 = torch.tensor(state, dtype=torch.float).to(device)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()

        final_move[move] = 1
        return final_move

    def train_long_memory(self):
        if len(self.memory) < 1000:
            return

        batch = random.sample(self.memory, 1000)

        states, actions, rewards, next_states, dones = zip(*batch)

        states = torch.tensor(states, dtype=torch.float).to(device)
        next_states = torch.tensor(next_states, dtype=torch.float).to(device)
        actions = torch.tensor(actions, dtype=torch.float).to(device)
        rewards = torch.tensor(rewards, dtype=torch.float).to(device)
        dones = torch.tensor(dones, dtype=torch.bool).to(device)

        # aquí no metemos optimización todavía en bruto (para mantenerlo limpio)
        # pero sí dejamos estructura de aprendizaje lista


def train():
    from snake_gameai import SnakeGameAI

    agent = Agent()
    game = SnakeGameAI()

    while True:
        state_old = game.get_state() if hasattr(game, "get_state") else [0]*11

        action = agent.get_action(state_old)

        reward, done, score = game.play_step(action)

        state_new = game.get_state() if hasattr(game, "get_state") else [0]*11

        agent.remember(state_old, action, reward, state_new, done)

        if done:
            game.reset()
            agent.n_games += 1

            print(f"Game: {agent.n_games} Score: {score}")


if __name__ == "__main__":
    train()