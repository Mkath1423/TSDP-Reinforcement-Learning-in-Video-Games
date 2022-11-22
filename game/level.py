import pygame
from gameobject import GameObject, GameObjectGroup
from agent import Agent
from bullet import Bullet
from player import Player
import numpy


class Level():
    def __init__(self):
        self.agents = GameObjectGroup("agents")
        self.bullets = GameObjectGroup("bullets")
        self.render_on = False

    def toggle_render(self, render_on):
        self.render_on = render_on

    def add_agent(self, name, state, color=(255,0,0)):
        self.agents.add(Agent(name, state, color))

    def add_player(self, name, state):
        self.agents.add(Player(name, state))

    def add_bullet(self, name, state):
        self.bullets.add(Bullet(name, state))

    def collision(self):
        agent_states = self.agents.get_state()
        bullet_states = self.bullets.get_state()

        for a in agent_states:
            if agent_states[a] == None:
                continue
            a_pos = agent_states[a]['position']

            for b in bullet_states:
                if bullet_states[b] == None:
                    continue
                b_pos = bullet_states[b]['position']

                source = bullet_states[b]['source']
                # on collision
                if (a_pos[0] < b_pos[0] + 5 and a_pos[0] + 50 > b_pos[0] and
                    a_pos[1] < b_pos[1] + 5 and a_pos[1] + 50 > b_pos[1]):
                    if(source == a): continue # bullet comes from the agent itself, skip

                    # agent on collision
                    agent_states[a]['hp'] -= 10
                    if(agent_states[a]['hp'] <= 0):
                        agent_states[a] = None

                    # bullet on collision
                    bullet_states[b] = None

        self.agents.update_state(agent_states)
        self.bullets.update_state(bullet_states)


    def update_states(self):
        move_set = ['w','a','s','d', 'rest']
        
        v_by_dir = [
                    (-4, -4), (0, -5), (4, -4),
                    (-5, 0),            (5, 0),
                    (-4, 4),  (0, 5),  (4, 4)
                    ]

        agent_states = self.agents.get_state()
        bullet_states = self.bullets.get_state()
        cur_states = {"agents":agent_states, "bullets":bullet_states}
        agent_moves = self.agents.get_moves(cur_states)

        for i in agent_states:
            x, y = agent_states[i]['position']
            if 5 <= agent_moves[i] <= 12:
                agent_center = (x+25, y+25)
                v = v_by_dir[agent_moves[i]-5]
                self.add_bullet("bullet", {'position':agent_center, 'velocity':v, 'source':i})
                agent_states[i]['cd'] = 60
                continue
            
            move = move_set[agent_moves[i]]
            if(move == 'w'):
                y -= 5
            elif(move == 'a'):
                x -= 5
            elif(move == 's'):
                y += 5
            elif(move == 'd'):
                x += 5
            elif(move == 'rest'):
                pass

            if x < 0: # prevents the agents from going out of the screen
                x = 0
            elif x > 950:
                x = 950
            if y < 0:
                y = 0
            elif y > 750:
                y = 750

            agent_states[i]['position'] = (x, y)
            if agent_states[i]['cd'] <= 0:
                continue
            agent_states[i]['cd'] -= 1

        self.agents.update_state(agent_states)
            
        bullet_states = self.bullets.get_state() # shooting adds new bullets, need to get the updated one

        for i in bullet_states:
            x, y = bullet_states[i]['position']
            v_x, v_y = bullet_states[i]['velocity']
            x += v_x
            y += v_y
            if x < 0 or x > 1000 or y < 0 or y > 800: # delete if out of the screen
                bullet_states[i] = None
                continue
            bullet_states[i]['position'] = (x, y)
        
        self.bullets.update_state(bullet_states)
    

    def render(self, screen):
        assert(self.render_on)
        self.agents.update()
        self.agents.draw(screen)
        self.bullets.update()
        self.bullets.draw(screen)

    def generate_image(self):
        sc = numpy.zeros((800, 1000), dtype=int)

        agent_pos = self.agents.get_state()
        bullet_pos = self.bullets.get_state()

        for i in agent_pos:
            x, y = agent_pos[i]['position']
            for j in range(x, x+51):
                for k in range(y, y+51):
                    sc[j][k] = 1
        for i in bullet_pos:
            x, y = bullet_pos[i]['position']
            for j in range(x, x+6):
                for k in range(y, y+6):
                    sc[j][k] = 2

        return sc



    def __repr__(self):
        return f'agents:{self.agents}, bullets:{self.bullets}'