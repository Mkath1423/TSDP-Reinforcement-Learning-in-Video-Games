import torch

import torch.nn as nn
import torch.nn.functional as F

import torch.optim as optim
from random import random

from ai.building_blocks import BNDoubleConv

class QLearningPolicy(nn.Module):

    def __init__(self, h, w, num_additional_features, outputs):
        super().__init__()

        self.conv1 = BNDoubleConv(1, 16)
        self.conv2 = BNDoubleConv(16, 16)

        #https://pytorch.org/tutorials/intermediate/reinforcement_q_learning.html
        def conv2d_size_out(size, kernel_size=3, stride=1):
            return (size - (kernel_size - 1) - 1) // stride + 1

        convw = conv2d_size_out(conv2d_size_out(conv2d_size_out(w)))
        convh = conv2d_size_out(conv2d_size_out(conv2d_size_out(h)))
        linear_input_size = convw * convh * 16
        self.fc1 = nn.Linear(linear_input_size + num_additional_features, 256)
        self.fc2 = nn.Linear(256, outputs)

    def forward(self, image, features):
        x = self.conv1(image)
        print(x.shape)
        x = self.conv2(x)
        print(x.shape)
        x = self.conv3(x)
        print(x.shape)
        print(x.flatten().shape)

        return x

class QTrainer:
    def __init__(self, model, lr, gamma):
        self.lr = lr
        self.gamma = gamma
        self.model = model
        self.optimizer = optim.Adam(model.parameters(), lr=self.lr)
        self.criterion = nn.MSELoss()

    # 'w'=0, 'a'=1, 's'=2, 'd'=3, rest=4, TODO shoot=5
    # state is the processed image data?
    def get_move(self,image,state):
        
        # TODO better epsilon choice for exploration tradeoff
        if random.randint(0, 200) < 80:
            move = random.randint(0, 4)
        else:
            state0 = torch.tensor([image,state], dtype=torch.float)
            prediction = self.model(state0) # need self.model
            move = torch.argmax(prediction).item()

        return move
    
    def train_step(self, state, action, reward, next_state, done):
        state = torch.tensor(state, dtype=torch.float)
        next_state = torch.tensor(next_state, dtype=torch.float)
        action = torch.tensor(action, dtype=torch.long)
        reward = torch.tensor(reward, dtype=torch.float)
        
        # dealing with 1d
        if len(state.shape) == 1:
            state = torch.unsqueeze(state, 0)
            next_state = torch.unsqueeze(next_state, 0)
            action = torch.unsqueeze(action, 0)
            reward = torch.unsqueeze(reward, 0)
            done = (done, )

        # 1: predicted Q values with current state
        pred = self.model(state)

        target = pred.clone()
        for idx in range(len(done)):
            Q_new = reward[idx]
            if not done[idx]:
                Q_new = reward[idx] + self.gamma * torch.max(self.model(next_state[idx]))

            target[idx][torch.argmax(action[idx]).item()] = Q_new
    
        # 2: Q_new = r + y * max(next_predicted Q value) -> only do this if not done
        # pred.clone()
        # preds[argmax(action)] = Q_new
        self.optimizer.zero_grad()
        loss = self.criterion(target, pred)
        loss.backward()

        self.optimizer.step()


if __name__ == "__main__":
    print("making_model")
    model = QLearningPolicy(640, 640, 0, 6)

    print("making_inputs")
    inputs = torch.randn((1, 1, 640, 640))

    model(inputs, None)