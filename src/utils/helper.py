import cv2
import numpy as np
from cv2.typing import MatLike, Point, Scalar


def euclidean_distance(color1: np.ndarray, color2: np.ndarray) -> float:
    difference = color1 - color2

    distance = np.linalg.norm(difference)

    return float(distance)


def render_text(
    frame: MatLike,
    text: str,
    pos: Point,
    color: Scalar = (0, 255, 0),
    scale: float = 0.5,
    thickness: int = 1,
    line_type: int = cv2.LINE_AA,
):
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame, text, pos, font, scale, color, thickness, line_type)


def render_rect(
    frame: MatLike,
    pos: Point,
    w: int,
    h: int,
    color: Scalar = (0, 255, 0),
    thickness: int = 1,
):
    cv2.rectangle(frame, pos, (pos[0] + w, pos[1] + h), color, thickness)


def calculate_dominant_color(image_region: np.ndarray) -> np.uint8:
    image_region = image_region.astype(np.float32)
    return np.uint8(np.mean(image_region, axis=(0, 1)))
