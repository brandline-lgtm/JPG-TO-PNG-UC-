import argparse
import os
from io import BytesIO
from typing import Tuple

from PIL import Image

# Optional AI-based upscaling
try:
    from realesrgan import RealESRGAN
    import torch
    _REAL_ESRGAN_AVAILABLE = True
except Exception:  # pragma: no cover - handled gracefully in runtime
    _REAL_ESRGAN_AVAILABLE = False

TARGET_WIDTH = 1620
TARGET_HEIGHT = 2880
TARGET_RATIO = TARGET_WIDTH / TARGET_HEIGHT
MIN_BYTES = 2 * 1024 * 1024
MAX_BYTES = 8 * 1024 * 1024
MAX_PIXELS = 25_000_000


def _crop_to_ratio(image: Image.Image) -> Image.Image:
    """Crop the image to match the target aspect ratio."""
    width, height = image.size
    current_ratio = width / height
    if abs(current_ratio - TARGET_RATIO) < 1e-3:
        return image
    if current_ratio > TARGET_RATIO:
        new_width = int(height * TARGET_RATIO)
        left = (width - new_width) // 2
        return image.crop((left, 0, left + new_width, height))
    else:
        new_height = int(width / TARGET_RATIO)
        top = (height - new_height) // 2
        return image.crop((0, top, width, top + new_height))


def _upscale_with_ai(image: Image.Image) -> Image.Image:
    """Upscale the image using Real-ESRGAN if available."""
    if not _REAL_ESRGAN_AVAILABLE:
        raise RuntimeError(
            "Real-ESRGAN is required for upscaling but is not installed.\n"
            "Install with 'pip install torch realesrgan'."
        )
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = RealESRGAN(device, scale=4)
    model.load_weights('RealESRGAN_x4plus.pth', download=True)
    return model.predict(image)


def _resize_exact(image: Image.Image) -> Image.Image:
    return image.resize((TARGET_WIDTH, TARGET_HEIGHT), Image.LANCZOS)


def _save_with_size_limits(image: Image.Image, output_path: str) -> Tuple[int, int]:
    """Save the image as JPEG ensuring file size within constraints.

    Returns the file size (bytes) and quality used.
    """
    quality_low, quality_high = 30, 95
    best_quality = quality_high
    best_bytes = None
    while quality_low <= quality_high:
        q = (quality_low + quality_high) // 2
        buffer = BytesIO()
        image.save(buffer, format='JPEG', quality=q)
        size = buffer.tell()
        if size > MAX_BYTES:
            quality_high = q - 1
        else:
            best_quality = q
            best_bytes = size
            if size < MIN_BYTES:
                quality_low = q + 1
            else:
                break
    if best_bytes is None:
        buffer = BytesIO()
        image.save(buffer, format='JPEG', quality=best_quality)
        best_bytes = buffer.tell()
    with open(output_path, 'wb') as f:
        f.write(buffer.getvalue())
    return best_bytes, best_quality


def convert_image(input_path: str, output_path: str) -> None:
    """Convert PNG to JPEG with given constraints."""
    image = Image.open(input_path).convert('RGB')
    image = _crop_to_ratio(image)
    width, height = image.size
    if width < TARGET_WIDTH or height < TARGET_HEIGHT:
        image = _upscale_with_ai(image)
    image = _resize_exact(image)
    if image.width * image.height > MAX_PIXELS:
        raise ValueError('Output image has more than 25M pixels.')
    size, quality = _save_with_size_limits(image, output_path)
    print(
        f'Saved {output_path} at {image.size[0]}x{image.size[1]} '
        f'with quality {quality} and size {size/1024/1024:.2f} MB'
    )


def main() -> None:
    parser = argparse.ArgumentParser(description='Convert PNG to JPG with upscaling.')
    parser.add_argument('input', help='Input PNG file')
    parser.add_argument('output', help='Output JPG file')
    args = parser.parse_args()
    convert_image(args.input, args.output)


if __name__ == '__main__':
    main()
