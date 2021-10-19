# Panel Competition Image Generator

This project was build by a member of the NFH community and is open for everyone
that wants to try it.

## Requirements
- Python 3.7+
- pip

## Installation
Install the dependencies with:
```bash
pip install -r requirements.txt
```

## Downloading the images
To download all images, use the following command:
```bash
python download.py
```
If you want to use the images from the ones available to NFH, use:
```
python download.py --nfh-only
```

## Creating random samples

**Important: You first need to download the images in order to run the command bellow.**

To create a random sample from all available images:
```bash
python main.py
```
If you want to use only images from the ones available to NFH, use:
```bash
python main.py --nfh-only
```
If you want to remove the block numbers from the image, use:
```bash
python main.py --no-numbers
```
If you want to save the image in the end, use:
```bash
python main.py --save
```
The file will be saved on `images/generated` with the name being the block numbers.

**Example:**

Tiles used: `431, 435, 414, 443, 417, 458, 459, 427, 419`

Resulting file name: `431-435-414-443-417-458-459-427-419.png`