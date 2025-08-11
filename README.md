# PNG to JPG Converter with AI Upscaling

This project provides a Python utility that converts PNG images to JPEG while:

- preserving the original aspect ratio,
- upscaling small images with [Real-ESRGAN](https://github.com/xinntao/Real-ESRGAN),
- ensuring the final resolution is exactly **1620×2880**, and
- saving the JPEG so that its size falls between **2 MB** and **8 MB**.

If the input image dimensions are below the required resolution, the script uses an
AI model to upscale before resizing. The output is guaranteed to contain fewer than
25 million pixels.

## Installation

```bash
pip install pillow numpy
# for AI upscaling support
pip install torch realesrgan
```

## Usage

```bash
python converter.py input.png output.jpg
```

## Simple GUI

A minimal Tkinter interface is provided for easy conversion without using the
command line:

```bash
python ui.py
```

Select the input PNG and the desired output JPG path. The repository includes a
`workspace/` directory that can be used to store your images.

## Running tests

```bash
pip install pytest pillow numpy
pytest
```
