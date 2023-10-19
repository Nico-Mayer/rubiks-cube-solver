from unittest.mock import mock_open
import cv2
import numpy as np
from enum import Enum
from cube import Cube
from utils import euclidean_distance
from ui import UI


RECT_SIZE = 120
RECT_SPACING = 10
CAM_INDEX = 1

COLORS = {
    'B': (255, 0, 0),
    'G': (0, 255, 0),
    'W': (255, 255, 255),
    'R': (0, 0, 255),
    'O': (0, 165, 255),
    'Y': (0, 255, 255),
    '0': (0, 0, 0)
}
CALIBRATED_COLORS = {
    'B': (90, 56, 26),  
    'G': (66, 144, 7),
    'W': (136, 162, 147),
    'R': (43, 51, 174),
    'O': (49, 96, 194),
    'Y': (36, 144, 173)
}
MAPPING = {
    'W': 'F',
    'B': 'L',
    'G': 'R',
    'Y': 'B',
    'O': 'D',
    'R': 'U',
}
class mode(Enum):
    CALIBRATION = 1
    SCAN = 2

cube = Cube()
cap = cv2.VideoCapture(CAM_INDEX)
ui = UI(COLORS)
selected_side = 0
mode = mode.SCAN
    
while True:
    ret, frame = cap.read()

    if not ret:
        break
    
    height, width, _ = frame.shape
    start_x = (width - (3 * RECT_SIZE + 2 * RECT_SPACING)) // 2
    start_y = (height - (3 * RECT_SIZE + 2 * RECT_SPACING)) // 2
    pressed_key = cv2.waitKey(1)
    
    ui.render(frame, cube, selected_side, mode)

    if mode == mode.CALIBRATION:
        rect_color = (0, 0, 255)
        center_x = width // 2
        center_y = height // 2
        top_left_x = center_x - (RECT_SIZE // 2)
        top_left_y = center_y - (RECT_SIZE // 2)
        bottom_right_x = center_x + (RECT_SIZE // 2)
        bottom_right_y = center_y + (RECT_SIZE // 2)
        sub_rect = frame[top_left_y:bottom_right_y, top_left_x:bottom_right_x]
        dominant_color = np.uint8(np.mean(sub_rect, axis=(0, 1)))
        cv2.putText(frame,f"{dominant_color}", (top_left_x, top_left_y - 15),1,1,(0,255,0), 1)
        cv2.rectangle(frame, (top_left_x, top_left_y), (bottom_right_x, bottom_right_y), rect_color, thickness=2)
        if pressed_key == 13:
            print(f"Color: {dominant_color}")

    elif mode == mode.SCAN:
        for row in range(3):
            for col in range(3):
                x = start_x + col * (RECT_SIZE + RECT_SPACING)
                y = start_y + row * (RECT_SIZE + RECT_SPACING)
                sub_rect = frame[y:y + RECT_SIZE, x:x + RECT_SIZE]
                dominant_color = np.uint8(np.mean(sub_rect, axis=(0, 1)))
                closest_color = min(CALIBRATED_COLORS, key=lambda color: euclidean_distance(CALIBRATED_COLORS[color], dominant_color))

                cv2.rectangle(frame, (x, y), (x + RECT_SIZE, y + RECT_SIZE), COLORS[closest_color], 2)
                cv2.putText(frame,f"{row * 3 + col + 1}", (x + RECT_SIZE - 20, y + RECT_SIZE - 10),1,1,(0,255,0), 1)
                cv2.putText(frame,f"{closest_color}", (x + RECT_SIZE // 2, y + RECT_SIZE // 2),1,1,COLORS[closest_color],2)

                if pressed_key == 13 and selected_side <= 5:
                    cube.state[row * 3 + col + selected_side * 9] = MAPPING[closest_color] 
    

    if pressed_key == ord("q"):
        break
    if pressed_key == ord("\t") and mode == mode.SCAN:
        selected_side += 1
        if selected_side > 5:
            selected_side = 0
    if pressed_key == ord("m"):
        if mode == mode.SCAN:
            mode = mode.CALIBRATION
        else:
            mode = mode.SCAN
    if pressed_key == 13:
        if mode == mode.SCAN:
            print(f"Cube State: {cube}")
            selected_side += 1
            if selected_side > 5:
                selected_side = 0

    if pressed_key == 32 and mode == mode.SCAN:
        print(f"Solution: {cube.get_solution()}")
    
    cv2.imshow('Camera Feed', frame)    
    
cap.release()
cv2.destroyAllWindows()