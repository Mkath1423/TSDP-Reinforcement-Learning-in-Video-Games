from ai import log

import torch

import torch.nn as nn
from torch.nn import Conv2d, BatchNorm2d, ReLU, AdaptiveAvgPool2d, Linear

import torch.optim as optim

import torchvision

import random

from ai.ReplayMemory import State


class PolicyNetwork(nn.Module):

    def __init__(self, num_additional_features, num_outputs):
        super().__init__()
        self.num_additional_features = num_additional_features
        self.num_outputs = num_outputs

        self.in_conv = Conv2d(1, 64, kernel_size=(7, 7), stride=(2, 2), padding=(3, 3), bias=False)
        self.in_bn = BatchNorm2d(64, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
        self.in_relu = ReLU(inplace=True)

        resnet = torchvision.models.resnet18()

        self.layer1 = resnet.layer1
        self.layer2 = resnet.layer2
        self.layer3 = resnet.layer3
        self.layer4 = resnet.layer4

        self.out_pool = AdaptiveAvgPool2d(output_size=(1, 1))

        self.fc = Linear(512 + num_additional_features, num_outputs)

    def forward(self, state: State):
        image, features = state.image, state.info
        # if image is None or (features is None and self.num_additional_features != 0):
        #     log.error("model got None inputs returning blank array")
        #     return torch.zeros((1, self.num_outputs)) # TODO check if this is right
        #
        # if len(image.shape) != 4:
        #     log.error(f"image must be of form [N, 1, H, W] not {image.shape}.")
        #     return None
        #
        # if features is not None and len(features.shape) != 2:
        #     log.error(f"features must be of form [N, F] not {features.shape}.")
        #     return None
        #
        # if image.shape[0] != features.shape[0]:
        #     log.error(f"image and features must have the same number of batches. image shape: {image.shape}, feature shape: {features.shape}.")
        #     return None

        x = self.in_conv(image)
        x = self.in_bn(x)
        x = self.in_relu(x)

        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        x = self.layer4(x)

        x = self.out_pool(x)
        x = torch.flatten(x, 1)

        if features is not None:
            x = torch.cat((x, features), dim=1)

        x = self.fc(x)
        return x


class QTrainer:
    def __init__(self, model, lr, gamma, epsilon, num_moves):
        self.lr = lr
        self.gamma = gamma
        self.epsilon = epsilon

        self.model: nn.Module = model
        self.optimizer = optim.Adam(model.parameters(), lr=self.lr)
        self.criterion = nn.MSELoss()
        self.num_moves = num_moves

    def get_move(self, state):
        if random.random() < self.epsilon and self.model.training:
            return random.randint(0, self.num_moves)
        else:
            prediction = self.model(state)
            # log.debug([round(e, ndigits=3) for e in prediction[0].tolist()], torch.argmax(prediction).item())
            return torch.argmax(prediction).item()

    def generate_mini_batches(self, state: State,
                              action,
                              reward,
                              next_state: State,
                              done):

        mini_state = [
            State(image, info) for image, info in zip(state.image.split(4), state.info.split(4))
        ]
        mini_action = action.split(4)
        mini_reward = reward.split(4)

        next_state = [
            State(image, info) for image, info in zip(next_state.image.split(4), next_state.info.split(4))
        ]

        mini_done = done.split(4)

        return zip(
            mini_state,
            mini_action,
            mini_reward,
            next_state,
            mini_done
        )

    def train_step(self,
                   state_: State,
                   action_,
                   reward_,
                   next_state_: State,
                   done_):
        for state, action, reward, next_state, done in self.generate_mini_batches(state_, action_, reward_, next_state_, done_):
            # 1: predicted Q values with current state
            pred = self.model(state)
            next_prediction = self.model(next_state)

            target = pred.clone()
            for idx in range(len(done)):
                Q_new = reward[idx]
                if not done[idx]:
                    Q_new = reward[idx] + self.gamma * torch.max(next_prediction[idx])

                target[idx][torch.argmax(action[idx]).item()] = Q_new

            # 2: Q_new = r + y * max(next_predicted Q value) -> only do this if not done
            # pred.clone()
            # preds[argmax(action)] = Q_new
            self.optimizer.zero_grad()
            loss = self.criterion(target, pred)
            loss.backward()

            self.optimizer.step()


if __name__ == "__main__":
    log.debug("making_model")
    _model = PolicyNetwork(6, 6)

    log.debug("making_inputs")
    _inputs = torch.randn((2, 1, 640, 640))

    log.debug("model output:", _model(_inputs, torch.randn((2, 6))))
