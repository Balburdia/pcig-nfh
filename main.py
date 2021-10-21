"""Generate a random panel using the available blocks."""
import argparse
import json
import os
import random
from typing import List

from PIL import Image, ImageDraw, ImageFont
from PIL.PngImagePlugin import PngImageFile


BACKGROUND_IMAGE = "images/panelBorder.png"
IMAGES_PATH = os.environ.get("IMAGES_PATH", "images/all")
BLOCKS_RANGE = (10, 612)
IGNORE_NUMBERS = [110, 111, 112, 412]
NUMBER_FONT = ImageFont.truetype(
    "fonts/NotoSansMono-Regular-Nerd-Font-Complete.ttf", 12
)


def get_numbers_list(nfh: bool = False) -> List[str]:
    """Get the number list from the given ranges."""
    # Use only NFH owned blocks.
    if nfh:
        with open("nfh_tiles.json", "r") as f:
            data = json.load(f)
            return data["nfh"]
    # Use all the blocks.
    else:
        start, end = BLOCKS_RANGE
        return [str(i) for i in range(start, end + 1) if i not in IGNORE_NUMBERS]


def create_image_grid(images: List[PngImageFile]) -> PngImageFile:
    """Assemble the images on the grid."""
    # Create an image from the background image.
    grid = Image.open(BACKGROUND_IMAGE)
    w, h = images[0].size
    offset = 20

    # Add all images on top of the background.
    for i, img in enumerate(images):
        grid.paste(img, box=((i % 3 * w) + offset, (i // 3 * h) + offset))
    return grid


def create_image_from_numbers(
    block_numbers: List[str], no_numbers: bool = True
) -> PngImageFile:
    """Create the grid image for the provided numbers."""
    images = []
    for block in block_numbers:
        # Open the block image
        img = Image.open(f"{IMAGES_PATH}/{block}.png")
        # Add a small rectangle with the block number inside to the block image.
        if not no_numbers:
            editable_image = ImageDraw.Draw(img)
            editable_image.rectangle(((12, 16), (39, 30)), fill="black")
            editable_image.text(
                (15, 15), block.zfill(3), (237, 230, 211), font=NUMBER_FONT
            )
        images.append(img)
    return create_image_grid(images)


def numbers_sanity_check(numbers_list: List[str]) -> bool:
    """Check for problems on the number list."""
    if len(numbers_list) < 9:
        print(
            "The number of provided numbers were insufficient. Please provide at "
            "least 9 numbers."
        )
        return False

    for number in numbers_list:
        # Check if the value provided is a valid integer.
        try:
            number = int(number)
        except ValueError:
            print(f"The value '{number}' not a valid number.")
            return False

        # Check if the value provided is inside the valid range.
        min_value, max_value = BLOCKS_RANGE
        if number < min_value or number > max_value:
            print(
                f"The value '{number}' is outside the blocks range. "
                f"Blocks range: {min_value}-{max_value}"
            )
            return False

        if number in IGNORE_NUMBERS:
            print(
                f"The value '{number}' is not available in the contest blocks. "
                f"Invalid numbers are: {IGNORE_NUMBERS}."
            )
            return False

    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a random art piece.")
    parser.add_argument(
        "--only-nfh",
        dest="only_nfh",
        action="store_true",
        default=False,
        help="Only uses NFH blocks.",
    )
    parser.add_argument(
        "--no-numbers",
        dest="no_numbers",
        action="store_true",
        default=False,
        help="Don't add the block numbers to the images.",
    )
    parser.add_argument(
        "--save",
        dest="save",
        action="store_true",
        default=False,
        help="Saves the resulting image.",
    )
    parser.add_argument(
        "--dont-show",
        dest="no_image",
        action="store_true",
        default=False,
        help="Don't show the image in the end. Use together with --save to only save "
             "files without opening them.",
    )
    parser.add_argument(
        "--from-numbers",
        action="store",
        dest="numbers",
        default="",
        help="Use the given block numbers to generate images, comma separated.",
    )
    parser.add_argument(
        "--samples",
        action="store",
        dest="n_samples",
        default=1,
        type=int,
        help="Number of samples to generate. Don't set this number too high or you "
             "will be flooded by images."
    )
    args = parser.parse_args()

    # Troll check
    if args.n_samples <= 0:
        print("Please, don't do this.")
        exit(69)

    for i in range(args.n_samples):
        if not args.numbers:
            # Get the numbers list.
            raw_numbers_list = get_numbers_list(nfh=args.only_nfh)
        else:
            # Check and use the numbers list provided by parameter.
            raw_numbers_list = args.numbers.split(",")

        if not numbers_sanity_check(raw_numbers_list):
            exit(1)

        # Create a random sample with the given numbers.
        numbers = random.sample(raw_numbers_list, 9)
        # Generate the image from the given numbers.
        im = create_image_from_numbers(numbers, args.no_numbers)
        # Save the file if args.save parameter was specified.
        if args.save:
            im.save(f"images/generated/{'-'.join(numbers)}.png")

        # Show the resulting image.
        if not args.no_image:
            # Show the image generated.
            im.show()

        # Close the image.
        im.close()
