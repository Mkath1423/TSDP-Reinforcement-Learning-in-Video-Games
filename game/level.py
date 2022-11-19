import pygame
from gameobject import GameObject, GameObjectGroup
from agent import Agent
from bullet import Bullet

class Level():
    def __init__(self):
        self.agents = GameObjectGroup("agents")
        self.bullets = GameObjectGroup("bullets")
        self.render_on = False

    def toggle_render(self, render_on):
        self.render_on = render_on

    def add_agent(self, name, state, color=(255,0,0)):
        self.agents.add(Agent(name, state, color))

    def add_bullet(self, name, state):
        self.bullets.add(Bullet(name, state))

    def collision(self):
        agent_states = self.agents.get_state()
        bullet_states = self.bullets.get_state()

        for a in agent_states:
            a_pos = agent_states[a]['position']
            for b in bullet_states:
                if bullet_states[b] == None:
                    continue
                b_pos = bullet_states[b]['position']
                if (a_pos[0] < b_pos[0] + 5 and a_pos[0] + 50 > b_pos[0] and
                    a_pos[1] < b_pos[1] + 5 and a_pos[1] + 50 > b_pos[1]):
                    
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

        agent_states = self.agents.get_state()
        bullet_states = self.bullets.get_state()
        cur_states = {"agents":agent_states, "bullets":bullet_states}
        agent_moves = self.agents.get_moves(cur_states)

        for i in agent_states:
            move = move_set[agent_moves[i]]
            pos = agent_states[i]['position']
            new_pos = pos

            if(move == 'w'):
                new_pos = (pos[0], pos[1]-5)
            elif(move == 'a'):
                new_pos = (pos[0]-5, pos[1])
            elif(move == 's'):
                new_pos = (pos[0], pos[1]+5)
            elif(move == 'd'):
                new_pos = (pos[0]+5, pos[1])
            elif(move == 'rest'):
                new_pos = pos
            # TODO new position sanity check
            # collision
            # game config file?

            agent_states[i]['position'] = new_pos

        self.agents.update_state(agent_states)
            

        for i in bullet_states:
            pos = bullet_states[i]['position']
            vel = bullet_states[i]['velocity']
            new_pos = (pos[0]+vel[0], pos[1]+vel[1])
            bullet_states[i]['position'] = new_pos
        
        self.bullets.update_state(bullet_states)
    

    def render(self, screen):
        assert(self.render_on)
        self.agents.update()
        self.agents.draw(screen)
        self.bullets.update()
        self.bullets.draw(screen)

    def __repr__(self):
        return f'agents:{self.agents_states}, bullets:{self.bullets_states}'