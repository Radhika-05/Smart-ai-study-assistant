"""
Image preprocessing utilities for improving OCR accuracy.
Isolated module — easily reusable outside Streamlit context.
"""

import io
from PIL import Image, ImageFilter, ImageOps
import numpy as np


def fix_exif_orientation(image: Image.Image) -> Image.Image:
    """Correct image rotation based on EXIF data."""
    try:
        exif = image._getexif()
        if exif:
            orientation_key = 274  # EXIF orientation tag
            if orientation_key in exif:
                orientation = exif[orientation_key]
                rotations = {3: 180, 6: 270, 8: 90}
                if orientation in rotations:
                    image = image.rotate(rotations[orientation], expand=True)
    except (AttributeError, Exception):
        pass
    return image


def convert_to_rgb(image: Image.Image) -> Image.Image:
    """Ensure image is in RGB mode."""
    if image.mode in ("RGBA", "P", "LA"):
        background = Image.new("RGB", image.size, (255, 255, 255))
        if image.mode in ("RGBA", "LA"):
            background.paste(image, mask=image.split()[-1])
        else:
            background.paste(image)
        return background
    return image.convert("RGB")


def convert_to_grayscale(image: Image.Image) -> Image.Image:
    """Convert image to grayscale."""
    return image.convert("L")


def apply_autocontrast(image: Image.Image) -> Image.Image:
    """Stretch contrast to full range for better text visibility."""
    return ImageOps.autocontrast(image, cutoff=1)


def apply_median_filter(image: Image.Image, size: int = 3) -> Image.Image:
    """Reduce salt-and-pepper noise with median filter."""
    return image.filter(ImageFilter.MedianFilter(size=size))


def apply_threshold(image: Image.Image, threshold: int = 160) -> Image.Image:
    """
    Binarize image using a simple global threshold.
    Works well for most handwritten notes on white paper.
    """
    img_array = np.array(image)
    binary = (img_array > threshold).astype(np.uint8) * 255
    return Image.fromarray(binary)


def preprocess_for_ocr(image: Image.Image) -> Image.Image:
    """
    Full preprocessing pipeline for handwritten note images.
    Returns a clean, high-contrast grayscale image suitable for GLM-OCR.
    """
    image = fix_exif_orientation(image)
    image = convert_to_rgb(image)
    image = convert_to_grayscale(image)
    image = apply_autocontrast(image)
    image = apply_median_filter(image)
    image = apply_threshold(image)
    return image


def image_to_bytes(image: Image.Image, fmt: str = "PNG") -> bytes:
    """Convert PIL image to bytes for display or saving."""
    buffer = io.BytesIO()
    image.save(buffer, format=fmt)
    return buffer.getvalue()
