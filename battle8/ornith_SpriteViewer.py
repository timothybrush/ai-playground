#!/usr/bin/env python3
"""SpriteViewer: animate a single frame of a rotation sprite sheet.

Usage:
    python3 SpriteViewer.py SpriteSheet.png

The input is a horizontally-laid-out PNG sprite sheet whose width is exactly
360 times its height, so it contains 360 square frames side by side. The app
extracts those frames in memory and displays the current one in a resizable
window, rotating one frame every 1/45th of a second (45 degrees per second).

All diagnostics are written to stderr; nothing is ever written to stdout.
"""

import os
import sys

import pygame

# Exit codes: 0 for a clean window close, 1 for any error condition.
EXIT_OK = 0
EXIT_ERROR = 1

# Number of square frames the sprite sheet must contain.
FRAMES_PER_ROTATION = 360

# Sprite sheet width must equal the number of frames times the frame size.
SPRITES_PER_ROW = FRAMES_PER_ROTATION

# Window margin (in pixels) added around the sprite on all four sides.
MARGIN = 50

# Sprite inset (in pixels) subtracted from the smaller window dimension. This
# yields the sprite side length and guarantees at least a 50px margin per side.
SPRITE_INSET = 2 * MARGIN

# Rotation speed in degrees per second (one frame every 1/45th of a second).
ROTATION_SPEED_DEGREES_PER_SECOND = 45.0

# Degrees added to the sprite per frame advance. Derived from the spec: a full
# 360-degree rotation must take 8 seconds at 45 degrees per second, so the loop
# runs 45 frames per second and each frame is exactly 1 degree.
DEGREES_PER_FRAME = 360.0 / (ROTATION_SPEED_DEGREES_PER_SECOND * 8.0)

# Background color toggled on left-click.
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Frame indices advance clockwise, so we rotate the surface by the negative
# angle (pygame.transform.rotate is counter-clockwise for positive angles).
ROTATION_SIGN = -1.0


def load_sprite_sheet(path):
    """Load and validate the sprite sheet, returning the loaded Surface.

    Raises ValueError with a stderr-ready message when the sheet cannot be
    read or does not contain exactly 360 frames.
    """
    # The format must be PNG. Relying on pygame alone is unsafe because it will
    # happily decode other raster formats, so gate on the extension explicitly.
    if not _is_png(path):
        raise ValueError("Input image can't be read.")

    try:
        sheet = pygame.image.load(path)
    except pygame.error as exc:
        # Covers missing files, unreadable files, and malformed images alike.
        raise ValueError(f"Input image can't be read: {exc}") from exc

    # Each frame is square with a side length equal to the sheet's height.
    frame_size = sheet.get_height()
    sheet_width = sheet.get_width()
    if sheet_width != SPRITES_PER_ROW * frame_size:
        raise ValueError("Sprite sheet does not contain exactly 360 frames.")

    return sheet


def _is_png(path):
    """Return True when *path* is a regular file with a .png extension."""
    return path.lower().endswith(".png") and os.path.isfile(path)


def extract_frame(sheet, frame_size):
    """Return an independent surface holding the leftmost frame (frame 0).

    Frames are laid out left to right, each a square of side *frame_size*. The
    returned surface is a private copy, so later modifications to the source
    sheet do not affect it.
    """
    frame = pygame.Surface((frame_size, frame_size), pygame.SRCALPHA)
    frame.blit(
        sheet.subsurface(pygame.Rect(0, 0, frame_size, frame_size)),
        pygame.Rect(0, 0, frame_size, frame_size),
    )
    return frame


def compute_sprite_side(window_size):
    """Return the displayed sprite side length for the current window size.

    The side is the smaller window dimension minus the inset. Returns 0 when
    the window is too small to fit the sprite with the required margins, in
    which case only the background should be shown.
    """
    smaller_dimension = min(window_size[0], window_size[1])
    return max(0, smaller_dimension - SPRITE_INSET)


def render_frame(screen, sprite, window_size, sprite_side, angle):
    """Draw the current rotated, scaled sprite onto *screen*.

    The background is painted by the caller before this is invoked, so this
    function only draws the sprite. When the window is too small to fit the
    sprite, nothing is drawn and the caller's background remains visible.
    """
    if sprite_side <= 0:
        return

    scaled = pygame.transform.scale(sprite, (sprite_side, sprite_side))
    rotated = pygame.transform.rotate(scaled, ROTATION_SIGN * angle)
    rect = rotated.get_rect(center=(window_size[0] / 2, window_size[1] / 2))
    screen.blit(rotated, rect)


def run(frame, frame_size):
    """Run the animation loop until the window is closed."""
    # A pygame.Rect (rather than a size tuple) makes the window resizable.
    window_size = pygame.Rect(0, 0, frame_size + MARGIN * 2, frame_size + MARGIN * 2)
    screen = pygame.display.set_mode((frame_size + MARGIN * 2, frame_size + MARGIN * 2), pygame.RESIZABLE)
    pygame.display.set_caption("SpriteViewer")

    clock = pygame.time.Clock()
    background = BLACK
    frame_index = 0
    angle = 0.0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Toggle between black and white on any left-click.
                background = WHITE if background == BLACK else BLACK

        # clock.tick caps the loop at 45 fps, so one frame is shown every 1/45th
        # of a second; advancing the angle by one degree per frame then yields
        # exactly 45 degrees per second and an 8-second full rotation.
        clock.tick(ROTATION_SPEED_DEGREES_PER_SECOND)
        frame_index = (frame_index + 1) % SPRITES_PER_ROW
        angle += DEGREES_PER_FRAME

        # Paint the current background (black or white) before drawing the
        # sprite, so a toggled white background is actually visible.
        screen.fill(background)

        window_size = screen.get_size()
        sprite_side = compute_sprite_side(window_size)
        render_frame(screen, frame, window_size, sprite_side, angle)

        pygame.display.flip()


def main(argv):
    """Entry point. Returns the process exit code."""
    if len(argv) != 2:
        print(f"Usage: python3 SpriteViewer.py SpriteSheet.png", file=sys.stderr)
        return EXIT_ERROR

    path = argv[1]
    try:
        sheet = load_sprite_sheet(path)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return EXIT_ERROR

    frame_size = sheet.get_height()
    frame = extract_frame(sheet, frame_size)

    pygame.init()
    try:
        run(frame, frame_size)
    finally:
        pygame.quit()
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main(sys.argv))
