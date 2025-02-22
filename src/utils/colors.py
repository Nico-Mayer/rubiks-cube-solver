from typing import Dict, Tuple

import numpy as np

COLORS: Dict[str, Tuple[int, int, int]] = {
    "B": (255, 0, 0),
    "G": (0, 255, 0),
    "W": (255, 255, 255),
    "R": (0, 0, 255),
    "O": (0, 165, 255),
    "Y": (0, 255, 255),
    "0": (100, 100, 100),
}

CALIBRATED_COLORS: Dict[str, Tuple[int, int, int]] = {
    "B": (126, 58, 4),
    "G": (84, 137, 59),
    "W": (204, 205, 210),
    "R": (10, 9, 172),
    "O": (2, 50, 238),
    "Y": (21, 163, 248),
}

MAPPING: Dict[str, str] = {
    "W": "F",  # White maps to Front
    "B": "L",  # Blue maps to Left
    "G": "R",  # Green maps to Right
    "Y": "B",  # Yellow maps to Back
    "O": "D",  # Orange maps to Down
    "R": "U",  # Red maps to Up
}


def map_colors_to_sides(color_string: str) -> str:
    """Map the colors in the color_string to their respective sides using the MAPPING dictionary."""
    return "".join(MAPPING.get(color, color) for color in color_string)


def map_sides_to_colors(side_string: str) -> str:
    """Convert the side string back to the original color string using the MAPPING dictionary."""
    reverse_mapping = {v: k for k, v in MAPPING.items()}
    return "".join(reverse_mapping.get(side, side) for side in side_string)


def calculate_dominant_color(image_section: np.ndarray) -> np.ndarray:
    """
    Calculate the dominant color in the given image section (sub-rectangle).
    Returns an RGB value as a numpy array.

    :param image_section: A numpy array representing a portion of the image (e.g., a 2D slice of the image).
    :return: The dominant color as an RGB numpy array.
    """
    # Convert the image section to a float32 for more precision during mean calculation
    image_section = image_section.astype(np.float32)

    # Calculate the mean across the 0th and 1st axes (height and width), giving the average color
    dominant_color = np.mean(image_section, axis=(0, 1))

    # Convert the result back to np.uint8 to represent the RGB color as an 8-bit value
    return np.asarray(dominant_color, dtype=np.uint8)


def euclidean_distance(color1: np.ndarray, color2: np.ndarray) -> float:
    """
    Calculate the Euclidean distance between two RGB colors.

    :param color1: The first color as an RGB numpy array.
    :param color2: The second color as an RGB numpy array.
    :return: The Euclidean distance as a float.
    """
    return float(np.linalg.norm(color1 - color2))


def find_closest_color(
    dominant_color: np.ndarray, calibrated_colors: Dict[str, Tuple[int, int, int]]
) -> str:
    """
    Find the closest calibrated color to the dominant color based on Euclidean distance.

    :param dominant_color: The dominant color as an RGB numpy array.
    :param calibrated_colors: A dictionary mapping color names to their RGB values.
    :return: The name of the closest calibrated color.
    """
    return min(
        calibrated_colors,
        key=lambda color: euclidean_distance(
            np.array(calibrated_colors[color]), np.array(dominant_color)
        ),
    )


def process_image_section(sub_rect: np.ndarray) -> str:
    """
    Process the sub-rectangle of the image to find the closest color to its dominant color.

    :param sub_rect: A numpy array representing a sub-rectangle (section) of the image.
    :return: The name of the closest calibrated color.
    """
    dominant_color = calculate_dominant_color(sub_rect)
    closest_color = find_closest_color(dominant_color, CALIBRATED_COLORS)
    return closest_color
