import cv2
import numpy as np
from cube import Cube
from utils import euclidean_distance

RECT_SIZE = 120
RECT_SPACING = 10
CAM_INDEX = 1

COLORS = {
    'B': (255, 0, 0),
    'G': (0, 255, 0),
    'W': (255, 255, 255),
    'R': (0, 0, 255),
    'O': (0, 165, 255),
    'Y': (0, 255, 255)
}
CALIBRATED_COLORS = {
    'B': (90, 56, 26),  
    'G': (113, 191, 81),
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
    'R': 'U'
}

cube = Cube()
cap = cv2.VideoCapture(CAM_INDEX)
enter_pressed = False
scanned_sides = 0

def render_side(frame, index):
    cell_size = 20
    spacing = 2
    # Up
    if index == 0:
        start_x = 80
        start_y = 15
    # Right
    elif index == 1:
        start_x = 150
        start_y = 85
    # Front
    elif index == 2:
        start_x = 80
        start_y = 85
    # Down
    elif index == 3:
        start_x = 80
        start_y = 155
    # Left
    elif index == 4:
        start_x = 10
        start_y = 85
    # Back
    elif index == 5:
        start_x = 220
        start_y = 85
        
    for row in range(3):
        for col in range(3):
            x = start_x + col * (cell_size + spacing)
            y = start_y + row * (cell_size + spacing)
            val = cube.get_color_string()[index * 9 + row * 3 + col] 
            if val == "B":
                color = (255,0,0)
            elif val == "R":
                color = (0,0,255)
            elif val == "G":
                color=(0,255, 0)
            elif val == "Y":
                color=(0,255,255)
            elif val == "O":
                color=(0,165,255)
            elif val == "W":
                color=(255,255,255)
            else:
                color=(0,0,0)
                
            cv2.rectangle(frame, (x, y), (x + cell_size, y + cell_size), color, -1)         
    if index == scanned_sides:
        cv2.rectangle(frame, (start_x - 2 , start_y - 2), (start_x + 65, start_y + 65), (0, 255, 0), 2)  

def render_cube(frame):
    for i in range(6):
        render_side(frame, i)
    

def render_ui(frame):
    height, width, _ = frame.shape
    if scanned_sides <= 5:
        cv2.putText(frame,f"Scan side ({scanned_sides}/6): ", (15, height - 15),2,1.0,(0,255,0))
    else:
        cv2.putText(frame,f"Scan complete", (15, height - 15),2,1.0,(0,255,0))
    
    render_cube(frame)
    
while True:
    ret, frame = cap.read()

    if not ret:
        break
    
    height, width, _ = frame.shape

    start_x = (width - (3 * RECT_SIZE + 2 * RECT_SPACING)) // 2
    start_y = (height - (3 * RECT_SIZE + 2 * RECT_SPACING)) // 2
    
    render_ui(frame)

    for row in range(3):
        for col in range(3):
            x = start_x + col * (RECT_SIZE + RECT_SPACING)
            y = start_y + row * (RECT_SIZE + RECT_SPACING)
            sub_rect = frame[y:y + RECT_SIZE, x:x + RECT_SIZE]
            dominant_color = np.uint8(np.mean(sub_rect, axis=(0, 1)))
            closest_color = min(CALIBRATED_COLORS, key=lambda color: euclidean_distance(CALIBRATED_COLORS[color], dominant_color))

            cv2.rectangle(frame, (x, y), (x + RECT_SIZE, y + RECT_SIZE), (0, 255, 0), 2)
            cv2.putText(frame,f"{row * 3 + col + 1}", (x + RECT_SIZE - 15, y + RECT_SIZE - 5),1,1.5,(0,255,0))
            cv2.putText(frame,f"{closest_color}", (x + RECT_SIZE // 2, y + RECT_SIZE // 2),1,1.5,COLORS[closest_color],2)

            if enter_pressed and scanned_sides <= 5:
                cube.state[row * 3 + col + scanned_sides * 9] = MAPPING[closest_color]

    if enter_pressed:
        print(cube)
        if scanned_sides <= 5:
            scanned_sides += 1
    enter_pressed = False
    
    cv2.imshow('Camera Feed', frame)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break
    elif key == 13:  
        print(" ")
        enter_pressed = True
    
cap.release()
cv2.destroyAllWindows()