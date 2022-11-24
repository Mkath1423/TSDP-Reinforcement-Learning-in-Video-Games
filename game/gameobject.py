
from abc import ABC, abstractmethod

import itertools

from pygame.sprite import Sprite, AbstractGroup, Group

from game import log


class GameObject(Sprite, ABC):
    gen_id = itertools.count().__next__

    def __init__(self, name, class_label, *groups: AbstractGroup):
        super().__init__(*groups)
        self.id = GameObject.gen_id()
        self.name = name

        self.class_label = class_label

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

    def get_by_id(self, id):
        for spr in self.sprites():
            if isinstance(spr, GameObject) and spr.id == id:
                return spr

        log.warning(f"no gameobject found with id: {id}. returning None")
        return None

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

            if new_state.__contains__(sprite.id):
                # if the new state is None then remove the sprite
                val = new_state[sprite.id]
                if val is None:
                    to_remove.append(sprite)

                else:
                    sprite.update_state(val)

        self.remove(*to_remove)

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

    def render_class_map(self, surface):
        h, w = surface.shape
        for obj in self.sprites():
            if not isinstance(obj, GameObject):
                continue

            if obj.rect.topleft == w or obj.rect.topright == h:
                continue

            surface[
                max(0, obj.rect.topleft[0]):min(obj.rect.topright[0] + 1, w),
                max(0, obj.rect.topleft[1]):min(obj.rect.bottomright[1] + 1, h)
            ] = obj.class_label

        return surface


if __name__ == "__main__":
    class TestGO(GameObject):
        def get_state(self):
            return {"name":self.name, "id":self.id}

        def update_state(self, new_state):
            log.debug(self.id, new_state["id"])

    groupA = GameObjectGroup("A")
    groupB = GameObjectGroup("B")

    log.debug("group ids:", groupA.get_id, groupB.get_id)
    log.debug("group ids:", groupA.id, groupB.id)

    for i in range(10):
        groupA.add(TestGO(f"A{i}", 0))
        groupB.add(TestGO(f"B{i}", 0))

    groupA.update_state(groupA.get_state())
    groupB.update_state(dict([
        (k, None) for k, v in groupB.get_state().items()
    ]))

    print(len(groupA.sprites()))
    print(len(groupB.sprites()))

