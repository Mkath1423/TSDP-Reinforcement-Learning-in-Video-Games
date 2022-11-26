# TSDP - Reinforcement Learning in Video Games

The level object contains all game object groups, and the game loop will only interact with the level object. The game object inherits from the pygame sprite group and includes a dictionary storing the state of each sprite within that group. On each iteration, the level gets the states of all game objects, updates their states (according to the move for agents, and velocity for bullets), and checks for collisions.

Possible extensions of the game: the game can contain more features that influence the winning, which affects the strategic thinking of the model. This includes obstacles, a magazine and reloading system, more weapon choices, character-specific features (such as differences in speed), etc. We don’t have time to achieve all of them right now, but the idea of it can be inherited and extended in the future.

To accomplish our goal we have chosen to use Q-Learning. This algorithm learns the expected value of taking each action in a given state and is a very common/effective method of reinforcement learning. 

The model uses a few different techniques that are often seen in projects like this. The model has two inputs, the first is a class map. Each type of object in the game is given a numeric representation (ex Friendly=1, Enemy=2, Bullet=3 …) which is then rendered onto a 1-channel image tensor. This prevents the model from specifying to certain sprites which would cause it to lose all useful training when any sprites are changed. The second input is a 1d tensor containing other useful information that is not represented in the image. (ex. hp, shoot cooldown, ability cooldown). The class map is first passed through a resnet. From there it is flattened and concatenated onto the additional information and passed to a fully connected network that outputs the expected value of each possible move.

Table of Contents

## Table of Contents
- [Dependencies](#dependencies)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Features](#features)
- [Team Members](#team-members)



## Dependencies
Languages:
- Python
Packages:
- Pytorch 
- Torchvision
- Pygame
- PyYAML
- numpy
```
## Project Structure
|─ main.py
|─ requirements.txt
|─ READMD.md
|──|─ ai
|     |─ __init__.py
|     |─ building_block.py
|     |─ model.py
|     |─ ReplayMemory.py
|──|─ game
|     |─ __init__.py
|     |─ gameobject.py
|     |─ agent.py
|     |─ AI_Agent.py
|     |─ player.py
|     |─ target.py
|     |─ bullet.py
|     |─ level.py
|──|─ utilities
|     |─ __init__.py
|     |─ args.py<br/>
|     |─ config.py
|     |─ logger.py
|     |─ checkpoints.py
|     |─ files.py
```
## Installation
fork the repo 🙂 🍴
pip install -r requirements.txt
python main.py "config/default.yaml"

## Features
- Configuration and logging system
- Training system
- 2d Topdown Shooter
- QLearning implementaion
- Classmap rendering

## Screenshots
| <img src="https://user-images.githubusercontent.com/43355577/204070062-d2577b8e-a0bb-4fec-a152-6b65aa6075cb.png" width="300">  <img src="https://user-images.githubusercontent.com/43355577/204070063-63edfc33-1da7-4cd4-bf07-6cb05a400389.png" width="300">  <img src="https://user-images.githubusercontent.com/43355577/204070083-0e37d4d3-00d9-4db0-a66e-4044dbe18308.gif" width="300"> 

## Team members

| <a href="https://github.com/Mkath1423" target="_blank"> **Lex Stapleton**</a> | <a href="https://github.com/shiqui" target="_blank"> **Shi Qi**</a> | <a href="https://github.com/ChunxinZheng" target="_blank"> **ChunxinZheng**</a> | <a href="https://github.com/hg2006" target="_blank"> **Hexin Guo**</a> |
| :---: | :---: | :---: | :---: |
| <img src="https://avatars.githubusercontent.com/u/43355577?v=4" width="100"> | <img src="https://avatars.githubusercontent.com/u/44322197?v=4" width="100"> | <img src="https://avatars.githubusercontent.com/u/115291818?v=4" width="100"> | <img src="https://avatars.githubusercontent.com/u/116389473?v=4" width="100"> |

