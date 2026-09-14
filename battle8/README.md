# LLM Battle 8 - Battle of the mini-models

## Overview

Take a bunch of small (sub-10B parameter) LLMs and get them to perform
a series of easy to moderately difficult tasks. Time them, and measure
success or failure of each model based on their output.

## The contenders

- Ornith 1.5 9B
- IBM Granite 4.2 8B
- Spark X2.5 4B

All models will be tested at Q8.

## The challenge

We'll break the challenge down into stages, with progressive difficulty.
The challenges will range from "easy" to "moderate", on the assumption
that truly hard coding tasks are probably out of reach for a small model.

### Challenge 1 - easy

Given a square 2D sprite image in PNG format, write a Python script to rotate
it in 1-degree increments 359 times (this gives us 360 total images, including
the input image). Save the results as one new image per degree of rotation
in a separate PNG file to a temporary directory. The output temp
directory should contain 359 files in total. Combined with the input
file, this gives us a total of 360 image files.

Now, take the 360 separate PNG images and assemble
them into one PNG sprite sheet:

- the height of the sprite sheet is the height of the input image
- the width of the sprite sheet is the width of input image X image count.
- (for example, image width 100px, 360 frames = 36000px wide sprite sheet)

Save the resulting sprite sheet as a PNG image. Transparency must be honored!

### Challenge 2 - moderate

Write a Python app that takes a horizontally-laid-out PNG sprite sheet,
extracts 360 frames from it (error on unexpected sprite count), and
displays the sprite in a resizable window, rotating at the rate
of 45 degrees per second (8 seconds per full rotation).

We can assume that each sprite frame is square. Therefore, the sprite
dimensions can be computed from the sprite sheet height. For example,
if the sprite sheet image is 100px tall, we can assume that each sprite
is 100px wide. Error if the sprite sheet width does not match this
assumption.

Transparency must be honored!

The window's initial size should be the sprite dimensions plus a margin
of 50px per side. For example, if the sprite dimensions are 100x100, then
the window size should be 200x200, with the sprite exactly centered.
Resizing the window scales the sprite such that it always occupies the
window dimensions with at least a 50x margin on each side. If the window
is made too small to fit the sprite with this margin, stop displaying
the sprite until the window is made larger.
