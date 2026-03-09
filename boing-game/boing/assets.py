"""Global asset stores and loader.

``images`` and ``sounds`` are plain dicts populated by :func:`load_assets`
after the pygame display has been initialised.

``current_keys`` is reassigned every frame by the main loop; code that needs
it should import this module and read ``assets.current_keys`` rather than
binding to it with ``from boing.assets import current_keys``.
"""

import math

import pygame

from boing.constants import WIDTH, HEIGHT, HALF_WIDTH, HALF_HEIGHT

# ---------------------------------------------------------------------------
# Global stores populated at runtime
# ---------------------------------------------------------------------------
images: dict[str, pygame.Surface] = {}
sounds: dict[str, pygame.mixer.Sound] = {}
current_keys: pygame.key.ScancodeWrapper | None = None  # refreshed every frame


# ---------------------------------------------------------------------------
# Procedural sprite generators (called from load_assets)
# ---------------------------------------------------------------------------
def _make_gear_sprite(size: int = 48) -> pygame.Surface:
    """Render a cog icon into a new SRCALPHA Surface."""
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    cx = cy = size / 2
    num_teeth = 8
    r_inner   = size * 0.18
    r_mid     = size * 0.33
    r_outer   = size * 0.46
    tooth_hw  = math.pi / num_teeth * 0.55  # half angular width of a tooth
    pts = []
    for i in range(num_teeth):
        base = 2 * math.pi * i / num_teeth
        for da, r in [(-tooth_hw * 1.6, r_mid), (-tooth_hw, r_outer),
                      ( tooth_hw,       r_outer), ( tooth_hw * 1.6, r_mid)]:
            a = base + da
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    pygame.draw.polygon(surf, (210, 210, 210, 230), pts)
    pygame.draw.circle(surf, (25, 25, 25, 255), (round(cx), round(cy)), round(r_inner))
    return surf


def _make_winner_sprite(title_text: str, line2: str = "") -> pygame.Surface:
    """Generate an 800x480 winner overlay matching the greyscale style of over.png.

    Brightest text colour sampled from over.png: ~(195, 195, 195).
    Optional *line2* is rendered centred on a second line below the title.
    """
    COL_TEXT   = (195, 195, 195)
    COL_SHADOW = ( 28,  28,  28)
    COL_RULE   = (130, 130, 130)
    COL_RAYS   = ( 65,  65,  65)
    LINE_GAP   = 8       # pixels between the two text lines

    surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

    # Vignette background
    for y in range(HEIGHT):
        edge  = abs(y - HEIGHT // 2) / (HEIGHT // 2)
        alpha = int(170 + 70 * edge)
        pygame.draw.line(surf, (0, 0, 0, alpha), (0, y), (WIDTH, y))

    # Subtle CRT scanlines
    for y in range(0, HEIGHT, 3):
        pygame.draw.line(surf, (255, 255, 255, 7), (0, y), (WIDTH, y))

    cx, cy = WIDTH // 2, HEIGHT // 2

    # Starburst rays
    for i in range(16):
        angle = math.pi * 2 * i / 16
        r = 230 if i % 2 == 0 else 160
        x2 = cx + int(math.cos(angle) * r)
        y2 = cy + int(math.sin(angle) * r)
        pygame.draw.line(surf, (*COL_RAYS, 90), (cx, cy), (x2, y2), 1)

    big_font = pygame.font.SysFont(None, 112)
    title    = big_font.render(title_text, True, COL_TEXT)
    shadow   = big_font.render(title_text, True, COL_SHADOW)

    if line2:
        sub      = big_font.render(line2, True, COL_TEXT)
        sub_shad = big_font.render(line2, True, COL_SHADOW)
        block_h  = title.get_height() + LINE_GAP + sub.get_height()
        ty       = cy - block_h // 2
        # line 1
        tx = cx - title.get_width() // 2
        surf.blit(shadow, (tx + 4, ty + 4))
        surf.blit(title,  (tx, ty))
        # line 2
        sy = ty + title.get_height() + LINE_GAP
        sx = cx - sub.get_width() // 2
        surf.blit(sub_shad, (sx + 4, sy + 4))
        surf.blit(sub,      (sx, sy))
        # decorative rules span the wider of the two lines
        rule_w = max(title.get_width(), sub.get_width()) + 32
        lx     = cx - rule_w // 2
        pygame.draw.line(surf, (*COL_RULE, 210), (lx, ty - 12),
                         (lx + rule_w, ty - 12), 2)
        pygame.draw.line(surf, (*COL_RULE, 210), (lx, sy + sub.get_height() + 8),
                         (lx + rule_w, sy + sub.get_height() + 8), 2)
    else:
        tx = cx - title.get_width() // 2
        ty = cy - title.get_height() // 2
        surf.blit(shadow, (tx + 4, ty + 4))
        surf.blit(title,  (tx, ty))
        lx = tx - 16
        lw = title.get_width() + 32
        pygame.draw.line(surf, (*COL_RULE, 210), (lx, ty - 12),
                         (lx + lw, ty - 12), 2)
        pygame.draw.line(surf, (*COL_RULE, 210), (lx, ty + title.get_height() + 8),
                         (lx + lw, ty + title.get_height() + 8), 2)
    return surf


# ---------------------------------------------------------------------------
# Asset loader
# ---------------------------------------------------------------------------
def load_assets() -> None:
    """Load all image and sound assets into the module-level dicts."""
    img_names = (
        ["ball", "blank", "table", "over", "effect0", "effect1", "menu0", "menu1"]
        + ["bat00", "bat01", "bat02", "bat10", "bat11", "bat12"]
        + [f"impact{i}" for i in range(5)]
        + [f"digit{c}{d}" for c in range(3) for d in range(10)]
    )
    for name in img_names:
        images[name] = pygame.image.load(f"images/{name}.png").convert_alpha()

    images["settings"]    = _make_gear_sprite(48)
    images["you_won"]     = _make_winner_sprite("YOU WON!")
    images["player1_won"] = _make_winner_sprite("PLAYER 1", "WON!")
    images["player2_won"] = _make_winner_sprite("PLAYER 2", "WON!")

    if not pygame.mixer.get_init():
        return

    snd_names = (
        [f"bounce{i}" for i in range(5)]
        + ["bounce_synth0"]
        + [f"hit{i}" for i in range(5)]
        + ["hit_slow0", "hit_medium0", "hit_fast0", "hit_veryfast0", "score_goal0"]
    )
    for name in snd_names:
        try:
            sounds[name] = pygame.mixer.Sound(f"sounds/{name}.ogg")
        except Exception:
            pass

    # These files have no numeric suffix on disk (up.ogg / down.ogg)
    for base in ("up", "down"):
        try:
            sounds[f"{base}0"] = pygame.mixer.Sound(f"sounds/{base}.ogg")
        except Exception:
            pass
