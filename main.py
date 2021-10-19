import argparse
import os
import random

from PIL import Image, ImageFont, ImageDraw


BACKGROUND_IMAGE = "images/panelBorder.png"
IMAGES_PATH = os.environ.get("IMAGES_PATH", "images/all")
NFH_IMAGES_RANGE = (413, 462)
BLOCKS_RANGE = (10, 612)
IGNORE_NUMBERS = [110, 111, 112, 412]
NUMBER_FONT = ImageFont.truetype(
    "fonts/NotoSansMono-Regular-Nerd-Font-Complete.ttf", 12
)


def get_numbers_list(nfh=False):
    if nfh:
        start, end = NFH_IMAGES_RANGE
    else:
        start, end = BLOCKS_RANGE
    return [str(i) for i in range(start, end + 1) if i not in IGNORE_NUMBERS]


def create_image_grid(images):
    grid = Image.open(BACKGROUND_IMAGE)
    w, h = images[0].size
    offset = 20

    for i, img in enumerate(images):
        grid.paste(img, box=((i % 3 * w) + offset, (i // 3 * h) + offset))
    return grid


def create_image_from_numbers(block_numbers, add_number=True):

    images = []
    for block in block_numbers:
        img = Image.open(f"{IMAGES_PATH}/{block}.png")
        if add_number:
            editable_image = ImageDraw.Draw(img)
            editable_image.rectangle(((12, 16), (39, 30)), fill="black")
            editable_image.text(
                (15, 15), block.zfill(3), (237, 230, 211), font=NUMBER_FONT
            )
        images.append(img)
    return create_image_grid(images)


def show_image(image):
    image.show()


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
    args = parser.parse_args()

    numbers = random.sample(get_numbers_list(nfh=args.only_nfh), 9)
    im = create_image_from_numbers(numbers, args.no_numbers)
    if args.save:
        im.save(f"images/generated/{'-'.join(numbers)}.png")
    show_image(im)
    im.close()
