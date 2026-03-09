"""Global asset stores and loader.

``images`` and ``sounds`` are plain dicts populated by :func:`load_assets`
after the pygame display has been initialised.

``current_keys`` is reassigned every frame — import this module and read
``assets.current_keys`` rather than binding with ``from chicken.assets import``.
"""

import pygame

# ---------------------------------------------------------------------------
# Global stores populated at runtime
# ---------------------------------------------------------------------------
images: dict[str, pygame.Surface] = {}
sounds: dict[str, pygame.mixer.Sound] = {}
current_keys: pygame.key.ScancodeWrapper | None = None  # refreshed every frame


# ---------------------------------------------------------------------------
# Asset loader
# ---------------------------------------------------------------------------
def load_assets() -> None:
    """Load all image and sound assets into the module-level dicts.

    TODO: populate img_names and snd_names once art assets are added.
    """
    img_names: list[str] = [
        # e.g. "chicken", "road", "river", "log", "car1", "truck", ...
    ]
    for name in img_names:
        images[name] = pygame.image.load(f"images/{name}.png").convert_alpha()

    if not pygame.mixer.get_init():
        return

    snd_names: list[str] = [
        # e.g. "hop", "splat", "squish", "drown", "home", "level_clear", ...
    ]
    for name in snd_names:
        try:
            sounds[name] = pygame.mixer.Sound(f"sounds/{name}.ogg")
        except Exception:
            pass
