import argparse

import requests
import os

IMAGES_PATH = os.environ.get("IMAGE_PATH", "images/all")
BLOCKS_URL = "https://data.thepanels.art/blocks/{number}_ps9_nb.png"
NFH_BLOCKS_RANGE = (413, 462)
BLOCKS_RANGE = (10, 612)
IGNORE_NUMBERS = [110, 111, 112, 412]


def download_block(number: int, path: str = IMAGES_PATH):
    """Download the block image on the given path."""
    if number in IGNORE_NUMBERS:
        return None
    response = requests.get(BLOCKS_URL.format(number=number))
    if response.status_code == 200:
        with open(f"{path}/{number}.png", "wb") as f:
            f.write(response.content)
    else:
        print(f"Block number {number} failed to download.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download blocks.")
    parser.add_argument(
        "--only-nfh",
        dest="only_nfh",
        action="store_true",
        default=False,
        help="Only downloads NFH blocks.",
    )
    args = parser.parse_args()

    print("Downloading block images.")
    if args.only_nfh:
        start, end = NFH_BLOCKS_RANGE
    else:
        start, end = BLOCKS_RANGE
    for num in range(start, end + 1):
        # To download only NFH images to images/nfh, use this line.
        # download_block(num, "images/nfh")
        # To download all images, use this line.
        download_block(num)
    print("Download finished.")
