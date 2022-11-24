# TSDP - Reinforcement Learning in Video Games

The level object contains all game object groups, and the game loop will only interact with the level object. The game object inherits from the pygame sprite group, and includes a dictionary storing the state of each sprite within that group. On each iteration, the level gets the states of all game objects, updates their states (according to the move for agents, velocity for bullets), and checks for collisions.

Possible extensions of the game: the game can contain more features that influence the winning, which affects the strategic thinking of the model. This includes obstacles, magazine and reloading system, more weapon choice, character specific features (such as difference in speed), etc. Obviously we don’t have time to achieve all of them right now, but the idea of it can be inherited and be extended in the future.

To accomplish our goal we have chosen to use Q-Learning. This algorithm learns the expected value of taking each action in a given state. …

The model a few different techniques that are often seen in projects like this. The model has two inputs. The first is a classmap. Each type of object in the game is given a numeric representation. (ex Friendly=1, Enemy=2, Bullet=3 …). This prevents the model from specifying to certain sprites which would cause it to lose all useful training when any sprites are changed. The second inputs is a 1d tensor contain other useful information that is not represented in the image. (ex. canShoot, hp, …). The classmap is first passed through a resnet. From there it is flattened and concatenated onto the additional information and passed to a fully connected network that outputs the expected value of each possible move.


Table of Contents

## Table of Contents
[Dependencies](#dependencies)
[Project Structure](#project-structure)
[Installation](#installation)
[Features](#features)
[Team Members](#team-members)


Languages:
Python

## Dependencies
Pytorch, Torchvision, Pygame, PyYAML …

## Project Structure
…

## Installation
fork the repo 🙂 🍴
pip install -r requirements.txt
…

## Features
Configuration and logging system
Training system
The Game
Classmap rendering

## Screenshots

The game 
Training graph 

## Team members

| <a href="https://github.com/Mkath1423" target="_blank"> **Lex Stapleton**</a> | <a href="https://github.com/shiqui" target="_blank"> **Shi Qi**</a> | <a href="https://github.com/ChunxinZheng" target="_blank"> **ChunxinZheng**</a> | <a href="https://github.com/hg2006" target="_blank"> **Hexin Guo**</a> |
| :---: | :---: | :---: | :---: |
| <img src="https://avatars.githubusercontent.com/u/43355577?v=4" width="100"> | <img src="https://avatars.githubusercontent.com/u/44322197?v=4" width="100"> | <img src="https://avatars.githubusercontent.com/u/115291818?v=4" width="100"> | <img src="https://avatars.githubusercontent.com/u/116389473?v=4" width="100"> |

