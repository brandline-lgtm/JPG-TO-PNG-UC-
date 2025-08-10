import os
from pathlib import Path

import numpy as np
from PIL import Image

from converter import convert_image, TARGET_WIDTH, TARGET_HEIGHT


def test_conversion(tmp_path: Path) -> None:
    # Create a random PNG image larger than target to avoid AI upscaling during test
    width, height = 2000, 3000
    arr = np.random.randint(0, 256, (height, width, 3), dtype=np.uint8)
    img = Image.fromarray(arr)
    input_path = tmp_path / 'input.png'
    output_path = tmp_path / 'output.jpg'
    img.save(input_path, format='PNG')

    convert_image(str(input_path), str(output_path))

    assert output_path.exists()
    out = Image.open(output_path)
    assert out.size == (TARGET_WIDTH, TARGET_HEIGHT)
    size = os.path.getsize(output_path)
    assert 2 * 1024 * 1024 <= size <= 8 * 1024 * 1024
