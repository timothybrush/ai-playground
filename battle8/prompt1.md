# Sprite rotation script

Your task is to write a Python script that will take a single 2D sprite image in PNG format and rotate it 359 times in one degree increments.
The output files will be written to a temporary directory, and then combined into a single wide sprite sheet image, which is then saved
in PNG format to the given output file. Transparency must be honored! The script will be called `SpriteRotater.py`.

## Example usage

`python3 SpriteRotater.py Sprite.png SpriteSheet.png`

- `Sprite.png` is the input file
  - if the input file does not exist or cannot be read: write "Input image can't be read." to stderr and exit.
  - the input format is always PNG; script should error on other formats
  - the input file is a parseable PNG image; script should error on invalid images
  - the input image is always square; script should error on other aspect ratios
- `SpriteSheet.png` is the desired output location
  - it is not an error if this file exists; prompt to confirm overwrite
  - it IS an error if the output file equals the input file (resolved absolute paths
    are the same - resolve these paths before doing any work). Exit with
    error message on stderr: "Output cannot overwrite input."
  - it IS an error if the parent directory of the target file does not exist.
    Do NOT automatically create the output directory. Exit with error message
    on stderr: "Output directory does not exist; will not create it."
  - expected output dimensions for sprite sheet:
    - height: equal to input image height
    - width: input image width times 360

Temporary image files created during the script run should be deleted before the script exits.

## Example scenario

`python3 SpriteRotater.py Sprite.png SpriteSheet.png`

- `Sprite.png` is a valid PNG image, 100px width and 100px height
  - is valid, loadable image? yes.
  - is PNG format? yes.
  - is square? yes.
- `SpriteSheet.png` does not exist
  - no need to prompt for overwrite confirmation
- Write "Rotating Sprite.png" to stdout with no trailing newline
- Create a temporary directory (within system temp dir, use `tempfile.mkdtemp`)
- for each degree between 1 and 359, inclusive:
  - rotate input image by N degrees
  - save results to temporary directory
  - filename should match the input filename but with a numeric suffix indicating degrees of rotation
  - for example: `Sprite1.png`, `Sprite2.png`, and so on, up to `Sprite359.png`
  - if any temp image fails to save, exit with stderr message "Unable to save temporary rotated image(s)!"
  - Write "." to stdout with no trailing newline
- Create a new PNG output image, 100px tall by 36000px wide
  - fill with transparency (RGBA: 0,0,0,0)
- Write a newline to stdout
- Write "Generating SpriteSheet.png" with no trailing newline to stdout
- The input image `Sprite.png` is drawn into output image at (0,0)
- for each N of the generated temporary images:
  - draw into output image at (N times input image width, 0)
  - transparency must be honored! Composite each frame so its transparent pixels
    don't overwrite the output image's pixels.
  - Write "." to stdout with no trailing newline
- Save output image to `SpriteSheet.png`
- Write a newline to stdout
- Write "Cleaning up..." to stdout
- delete temporary directory
- successful exit

## Overwrite confirmation

If the given target output file already exists, a simple confirmation message should
be printed on stdout: "Overwrite existing output file (y/N)?".

If stdout is closed (EOF), assume "N" and exit with message on stderr: "Won't overwrite
existing output."

If the user enters anything but "Y" or "y", exit with message on stderr: "Won't overwrite
existing output."

If the user enters "y" or "Y", delete the existing output file before proceeding.
Output "Overwriting existing output file" on stdout.

## Rotating images

The `pillow` library (Python Imaging Library) is installed and can be used to rotate
images around the image center, without changing the size of the image.

- use `expand=False` to keep the rotated image dimensions equal to the input image dimensions
- use `BICUBIC` for smooth rotations (default is `NEAREST` which is insufficient).
- use `rotate(-N)` for clockwise rotation (pillow default to counter-clockwise rotation).

## Compositing the output image

`pillow` (the Python Imaging Library) is installed and can be used for creating/drawing the output image.

## Script exit codes

- exit code 0 if no errors were encountered
- exit code 1 for all error conditions

Temp files must be deleted by the script even on the error paths!

