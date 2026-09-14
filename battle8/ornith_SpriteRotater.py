#!/usr/bin/env python3
"""SpriteRotater.py

Rotate a single 2D PNG sprite 359 times in one-degree increments and stitch the
result (plus the original 0-degree frame) into one wide sprite sheet.

Usage:
    python3 SpriteRotater.py <input.png> <output.png>

The sheet is 360 frames wide (0 degrees through 359 degrees), each frame exactly
as wide as the input. Frames are composited with transparency honoured, so the
transparent pixels of a rotated frame never paint over the sheet's background.

Exit codes:
    0 - success, no errors
    1 - any error condition
"""

import os
import sys
import tempfile

from PIL import Image, UnidentifiedImageError


def fail(message):
    """Report an unrecoverable error to stderr and exit with the error code."""
    print(message, file=sys.stderr)
    sys.exit(1)


def resolve_path(path):
    """Return an absolute, normalized path so input/output identity can be
    compared reliably before any work is done."""
    return os.path.abspath(os.path.expanduser(path))


def load_and_validate_input(input_path):
    """Open and validate the input image.

    The input must exist, be a parseable PNG, and be square. Any violation exits
    with code 1 and the canonical "Input image can't be read." message (or a
    format-specific message). Returning early keeps all failure paths from
    creating stray files.
    """
    if not os.path.isfile(input_path):
        fail("Input image can't be read.")

    try:
        image = Image.open(input_path)
        # .load() forces a full decode so a truncated or corrupt PNG is caught
        # here rather than later, after we have already done work.
        image.load()
    except (OSError, ValueError, UnidentifiedImageError):
        fail("Input image can't be read.")

    if image.format != "PNG":
        fail("Input image is not a PNG file.")

    if image.size[0] != image.size[1]:
        fail("Input image is not square.")

    return image


def confirm_overwrite(output_path):
    """Prompt for confirmation when the output file already exists.

    Returns True only when the caller may proceed. On any refusal (EOF, empty
    input, or anything other than y/Y) this exits with code 1 without deleting
    anything.
    """
    print("Overwrite existing output file (y/N)?", end="", flush=True)

    try:
        response = input()
    except EOFError:
        fail("Won't overwrite existing output.")

    if response not in ("y", "Y"):
        fail("Won't overwrite existing output.")

    # Explicitly remove the stale file so the new sheet starts from a clean
    # (transparent) canvas and does not collide with old pixels.
    os.remove(output_path)
    print("Overwriting existing output file", flush=True)
    return True


def rotate_and_build_sheet(input_image, output_path):
    """Rotate every degree 1..359 into temp files, then composite all 360 frames
    into the final sheet. The temp directory is always removed, even on error."""
    input_width, input_height = input_image.size
    input_basename = os.path.basename(input_image.filename)
    sheet_width = input_width * 360

    temp_dir = tempfile.mkdtemp()
    try:
        print("Rotating " + input_basename, end="", flush=True)

        # Keep the decoded image objects so compositing avoids re-reading files.
        rotated_frames = []
        for degree in range(1, 360):
            # rotate(-N) gives clockwise rotation, expand=False keeps the frame
            # the same size as the input, and BICUBIC keeps edges smooth.
            rotated = input_image.rotate(
                -degree, expand=False, resample=Image.BICUBIC
            )
            temp_path = os.path.join(temp_dir, "%s%d.png" % (input_basename, degree))
            try:
                rotated.save(temp_path)
            except OSError:
                fail("Unable to save temporary rotated image(s)!")
            rotated_frames.append((degree, rotated))
            print(".", end="", flush=True)

        # Transparent canvas: width is 360 frames, height matches the input.
        sheet = Image.new("RGBA", (sheet_width, input_height), (0, 0, 0, 0))
        print("", flush=True)
        print("Generating SpriteSheet.png", end="", flush=True)

        # The 0-degree frame is the original sprite, drawn first at the origin.
        sheet.paste(input_image, (0, 0))
        for degree, frame in rotated_frames:
            # Composite (masked paste) so each frame's transparent pixels do not
            # overwrite the pixels already on the sheet.
            sheet.paste(frame, (degree * input_width, 0), frame)
            print(".", end="", flush=True)

        sheet.save(output_path)
    finally:
        # Temp files must be gone before we exit, on success or failure.
        import shutil

        shutil.rmtree(temp_dir, ignore_errors=True)

    print("", flush=True)
    print("Cleaning up...", flush=True)


def main(argv):
    if len(argv) != 3:
        fail("Usage: python3 SpriteRotater.py <input.png> <output.png>")

    input_path = resolve_path(argv[1])
    output_path = resolve_path(argv[2])

    # Validate the input first, then compare resolved paths before doing work.
    input_image = load_and_validate_input(input_path)

    if output_path == input_path:
        fail("Output cannot overwrite input.")

    if not os.path.isdir(os.path.dirname(output_path)):
        fail("Output directory does not exist; will not create it.")

    if os.path.exists(output_path) and not confirm_overwrite(output_path):
        return 1

    rotate_and_build_sheet(input_image, output_path)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
