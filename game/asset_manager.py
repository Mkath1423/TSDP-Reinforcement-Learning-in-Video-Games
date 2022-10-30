import pygame

from utilities.file_loading import is_file

from game import log

_sprites = {

}


def load_sprite(path, force_reload=False):
    if not is_file(path):
        return

    # if sprite was already loaded, use the loaded image
    if path in _sprites and not force_reload:
        log.info(f"found preloaded sprite: {path}")

        val = _sprites.get(path, default=None)

        if val is None:
            log.warning(f"value of preloaded sprite: {path} was None")
        return val

    # otherwise, try to load the image
    else:
        log.info(f"loading image: {path}")

        val = pygame.image.load(path)

        if val is None:
            log.error(f"failed to load image: {path}")
            return None

        else:
            _sprites[path] = val
            return val
