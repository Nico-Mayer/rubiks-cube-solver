import cv2
import numpy as np
from cv2.typing import MatLike

from colors import CALIBRATED_COLORS, COLORS, MAPPING
from cube import Cube
from system_state import Mode, Selected_Side
from ui import UI
from utils import calculate_dominant_color, euclidean_distance, render_rect, render_text

RECT_SIZE = 120
RECT_SPACING = 10
CAM_INDEX = 1


def calibrate(frame: MatLike, pressed_key: int):
    height, width, _ = frame.shape
    x = (width - RECT_SIZE) // 2
    y = (height - RECT_SIZE) // 2
    sub_rect = frame[y : y + RECT_SIZE, x : x + RECT_SIZE]
    dominant_color = calculate_dominant_color(sub_rect)
    render_text(frame, f"{dominant_color}", (x, y - 10))
    render_rect(frame, (x, y), RECT_SIZE, RECT_SIZE)
    if pressed_key == 13:
        print(f"Color: {dominant_color}")


def scan(
    frame: MatLike, cube: Cube, row: int, col: int, side_index: int, pressed_key: int
):
    height, width, _ = frame.shape
    start_x = (width - (3 * RECT_SIZE + 2 * RECT_SPACING)) // 2
    start_y = (height - (3 * RECT_SIZE + 2 * RECT_SPACING)) // 2
    x = start_x + col * (RECT_SIZE + RECT_SPACING)
    y = start_y + row * (RECT_SIZE + RECT_SPACING)
    sub_rect = frame[y : y + RECT_SIZE, x : x + RECT_SIZE]
    dominant_color = calculate_dominant_color(sub_rect)
    closest_color = min(
        CALIBRATED_COLORS,
        key=lambda color: euclidean_distance(
            CALIBRATED_COLORS[color], np.array(dominant_color)
        ),
    )

    render_rect(frame, (x, y), RECT_SIZE, RECT_SIZE, COLORS[closest_color], 2)
    render_text(frame, f"{row * 3 + col + 1}", (x + RECT_SIZE - 20, y + RECT_SIZE - 10))
    render_text(
        frame,
        f"{closest_color}",
        (x + RECT_SIZE // 2 - 5, y + RECT_SIZE // 2 + 5),
        COLORS[closest_color],
        0.7,
    )

    if pressed_key == 13 and side_index <= 5:
        cube.state[row * 3 + col + side_index * 9] = MAPPING[closest_color]


def handle_keypress(
    pressed_key: int, cube: Cube, selected_side: Selected_Side, mode: Mode
) -> bool:
    if pressed_key == ord("q"):
        return False
    elif pressed_key == ord("\t") and mode.is_scan():
        selected_side.next()
    elif pressed_key == ord("m"):
        mode.change()
    elif pressed_key == 13:
        if mode.is_scan():
            print(f"Cube State: {cube}")
            selected_side.next()
    elif pressed_key == 32 and mode.is_scan():
        print(f"Solution: {cube.get_solution()}")
    elif pressed_key == ord("r"):
        cube.reset_side(selected_side.get_index())
    return True


def main():
    cube = Cube()
    cap = cv2.VideoCapture(CAM_INDEX)
    ui = UI()
    mode = Mode()
    selected_side = Selected_Side()

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        pressed_key = cv2.waitKey(1)
        ui.render(frame, cube, selected_side, mode)

        if mode.is_calibration():
            calibrate(frame, pressed_key)
        elif mode.is_scan():
            for row in range(3):
                for col in range(3):
                    scan(frame, cube, row, col, selected_side.get_index(), pressed_key)

        if not handle_keypress(pressed_key, cube, selected_side, mode):
            break

        cv2.imshow("Camera Feed", frame)
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
