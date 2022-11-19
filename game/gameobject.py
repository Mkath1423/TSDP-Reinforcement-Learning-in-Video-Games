
from abc import ABC, abstractmethod

import itertools

from pygame.sprite import Sprite, AbstractGroup, Group

from game import log


class GameObject(Sprite, ABC):
    gen_id = itertools.count().__next__

    def __init__(self, name, *groups: AbstractGroup):
        super().__init__(*groups)
        self.id = GameObject.gen_id()
        self.name = name

    @property
    def get_id(self):
        return self.id

    @property
    def get_name(self):
        return self.name

    @abstractmethod
    def get_state(self):
        pass

    @abstractmethod
    def update_state(self, new_state):
        pass

    @abstractmethod
    def get_move(self, game_state):
        pass

    def __repr__(self):
        return f"GameObject(name={self.name}, id={self.id})"


class GameObjectGroup(Group):
    gen_id = itertools.count().__next__

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

            out[obj.id] = obj.get_state()

        return out

    def update_state(self, new_state: dict):
        to_remove: list[Sprite] = []
        for sprite in self.sprites():
            if not isinstance(sprite, GameObject):
                continue

            # if the new state is None then remove the sprite
            val = new_state.get(sprite.id, None)
            if val is None:

                to_remove.append(sprite)

            else:
                sprite.update_state(val)

        self.remove(to_remove)

    def get_moves(self, game_state):
        out = {}

        for obj in self.sprites():
            if not isinstance(obj, GameObject):
                continue

            if out.__contains__(obj.id):
                if obj.id not in self.warned_duplicates and not self.suppress_warnings:
                    log.warning(f"Group {self.id} contains duplicate object {repr(obj)}")
                    self.warned_duplicates.append(obj.id)
                    continue

            out[obj.id] = obj.get_move(game_state)

        return out

if __name__ == "__main__":
    class TestGO(GameObject):
        def get_state(self):
            return {"name":self.name, "id":self.id}

        def update_state(self, new_state):
            log.debug(self.id, new_state["id"])

    groupA = GameObjectGroup("A")
    groupB = GameObjectGroup("B")

    log.debug("group ids:", groupA.id, groupB.id)

    for i in range(10):
        groupA.add(TestGO(f"A{i}"))
        groupB.add(TestGO(f"B{i}"))

    groupA.update_state(groupA.get_state())
    groupB.update_state(dict([
        (k, None) for k, v in groupB.get_state().items()
    ]))

    print(len(groupA.sprites()))
    print(len(groupB.sprites()))

