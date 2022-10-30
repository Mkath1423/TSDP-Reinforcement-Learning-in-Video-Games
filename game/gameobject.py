from pygame.sprite import Sprite, Group, AbstractGroup

from abc import ABC, abstractmethod

import itertools

#from game import log


class GameObject(Sprite, ABC):
    gen_id = itertools.count()#.next

    def __init__(self, name, *groups: AbstractGroup):
        super().__init__(*groups)
        self.id = GameObject.gen_id()
        self.name = name

    @property
    def get_id(self):
        return self.id

    @property
    @abstractmethod
    def get_name(self):
        return self.name

    @abstractmethod
    def get_state(self):
        pass

    @abstractmethod
    def update_state(self, new_state):
        pass

    def __repr__(self):
        return f"GameObject(name={self.name}, id={self.id})"


class GameObjectGroup(Group):
    gen_id = itertools.count()#.next

    def __init__(self, name, *groups: AbstractGroup, suppress_warnings=False):
        super().__init__(*groups)
        self.id = GameObject.gen_id()
        self.name = name

        self.suppress_warnings = suppress_warnings
        self.warned_duplicates = []


    @property
    def get_id(self):
        return self.id

    @property
    def get_name(self):
        return self.name

    def get_state(self):
        out = {}

        for obj in self.sprites():
            if not isinstance(obj, GameObject):
                continue

            if out.__contains__(obj.id):
                if obj.id not in self.warned_duplicates and not self.suppress_warnings:
                    log.warning(f"Group {self.id} contains duplicate object {repr(obj)}")
                    self.warned_duplicates.append(obj.id)
                    continue

            out[obj.id] = (obj.name, obj.get_state())

        return out

    def update_state(self, new_state: dict):
        to_remove: list[Sprite] = []
        for sprite in self.sprites():
            if not isinstance(sprite, GameObject):
                continue

            # if the new state is None then remove the sprite
            val = new_state.get(sprite.get_id(), default=None)
            if val is None:
                to_remove.append(sprite.get_id())

            else:
                sprite.update(val)

        self.remove(to_remove)

