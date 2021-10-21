"""Download the block images."""
import argparse
import json
import os
from typing import Union

import requests


IMAGES_PATH = os.environ.get("IMAGE_PATH", "images/all")
BLOCKS_URL = "https://data.thepanels.art/blocks/{number}_ps9_nb.png"
BLOCKS_RANGE = (600, 650)


def download_block(number: Union[str, int], path: str = IMAGES_PATH) -> None:
    """Download the block image on the given path."""
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
        with open("nfh_tiles.json", "r") as f:
            data = json.load(f)
        for num in data["nfh"]:
            download_block(num)
    else:
        start, end = BLOCKS_RANGE
        for num in range(start, end + 1):
            # To download only NFH images to images/nfh, use this line.
            # download_block(num, "images/nfh")
            download_block(num)
    print("Download finished.")
