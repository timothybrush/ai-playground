# Sprite viewer app

Your task is to write a Python application that takes a horizontally-laid-out PNG sprite sheet,
extracts 360 frames from it, and displays the sprite in a resizable window, rotating continuously
at 45 degrees per second (8 seconds per full rotation). Transparency must be honored!
The app will be called `SpriteViewer.py`.

## Example usage

`python3 SpriteViewer.py SpriteSheet.png`

- `SpriteSheet.png` is the input file
  - if the input file does not exist or cannot be read: write "Input image can't be read." to stderr and exit.
  - the input format is always PNG; app should error on other formats
  - the input file is a parseable PNG image; app should error on invalid images
  - each sprite frame is assumed to be square. Frame dimensions are the sprite sheet's
    height in both axes.
  - the sprite sheet's width must be exactly 360 times its height (360 square frames
    side by side). Otherwise: write "Sprite sheet does not contain exactly 360 frames."
    to stderr and exit.

- The app writes nothing to stdout. All errors are written to stderr.

## Frame extraction

- The 360 frames are extracted from the sprite sheet in memory. No temporary files.
- Frame 0 (0 degrees) is the leftmost frame; frames proceed left to right in order.
- Each frame is a square whose side length equals the sprite sheet's height.

## Display

Assume the app runs on a machine with an X11 display (possibly a virtual display),
and that `pygame-ce` is installed. Use `pygame-ce` for the window and all rendering.

- the window title is "SpriteViewer".
- the initial window background is black (RGB 0,0,0).
  - left-clicking anywhere in the window toggles the window background color between black and white.
- the window is resizable.
- the window's initial size is the frame dimensions plus a 50px margin on each side.
  (for example, a 100x100 frame gives a 200x200 window with the sprite exactly centered)

### Sizing the sprite

- The displayed sprite is always a centered square.
- The displayed sprite's side length is `min(window width, window height) - 100` pixels,
  giving the sprite at least a 50px margin on every side.
- If the window's width or height is 100px or less, the sprite cannot fit with these
  margins. In that case, display only the window background until the window is made
  large enough to display the sprite again.
- The displayed sprite is scaled from the current frame using `pygame.transform.scale`.

### Rotation animation

- The sprite rotates continuously at 45 degrees per second: one frame every 1/45th of
  a second, with a full rotation taking 8 seconds.
- Frame indices advance in order 0, 1, 2, ..., 359, then wrap back to 0, so the sprite
  appears to rotate clockwise.
- When the window is resized, the sprite must be re-rendered at the new size immediately
  (do not wait for the next frame advance).

## Example scenario

`python3 SpriteViewer.py SpriteSheet.png`

- `SpriteSheet.png` is a valid PNG, 100px tall and 36000px wide
  - frame dimensions: 100x100. frame count: 36000 / 100 = 360. OK.
- Open a 200x200 window titled "SpriteViewer" with a black background
- Draw frame 0 at native 100x100, exactly centered (50px margin on all sides)
- Every 1/45th of a second, advance to the next frame (1, 2, 3, ..., 359, then back to 0)
- The user resizes the window to 500x300
  - displayed sprite: 300 - 100 = 200x200, centered
    (150px margin left/right, 50px margin top/bottom)
- The user shrinks the window to 150x150
  - displayed sprite: 150 - 100 = 50x50, centered
- The user shrinks the window to 100x100
  - sprite is not displayed; only the black background
- The user closes the window
  - clean exit, exit code 0

## App exit codes

- exit code 0 when the window is closed normally
- exit code 1 for all error conditions
