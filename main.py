from os import name
from tracemalloc import start
import cv2
import numpy as np

RECT_SIZE = 120
RECT_SPACING = 10
CAM_INDEX = 0
COLORS = {
    'blue': (90, 56, 26),  
    'green': (113, 191, 81),
    'white': (136, 162, 147),
    'red': (43, 51, 174),
    'orange': (49, 96, 194),
    'yellow': (36, 144, 173)
}

cap = cv2.VideoCapture(CAM_INDEX)
enter_pressed = False
average = [0,0,0]
scanned_sides = 0

blue_side = np.empty((3, 3), dtype=object)
white_side = np.empty((3, 3), dtype=object)
green_side = np.empty((3, 3), dtype=object)
yellow_side = np.empty((3, 3), dtype=object)
orange_side = np.empty((3, 3), dtype=object)
red_side = np.empty((3, 3), dtype=object)

def euclidean_distance(color1, color2):
    return np.linalg.norm(np.array(color1) - np.array(color2))

def calc_average(color):
    average[0] += color[0]
    average[1] += color[1]
    average[2] += color[2]


def render_side(frame, index):
    start_x = 75
    start_y = 10 + (index * 72)
    cell_size = 20
    spacing = 2
    side, name = get_side(index)

    if index == 4:
        start_x =  147
        start_y = 82
    if index == 5:
        start_x =  5
        start_y = 82

    for row in range(3):
        for col in range(3):
            x = start_x + col * (cell_size + spacing)
            y = start_y + row * (cell_size + spacing)
            val = side[row][col]
            color = (0,0,0)
            if val == "blue":
                color = (255,0,0)
            elif val == "red":
                color = (0,0,255)
            elif val == "green":
                color=(0,255, 0)
            elif val == "yellow":
                color=(0,255,255)
            elif val == "orange":
                color=(0,165,255)
            elif val == "white":
                color=(255,255,255)
                
            cv2.rectangle(frame, (x, y), (x + cell_size, y + cell_size), color, -1)           

def render_cube(frame):
    for i in range(6):
        render_side(frame, i)
    

def render_ui(frame):
    height, width, _ = frame.shape
    side, name = get_side(scanned_sides)
    if scanned_sides <= 5:
        cv2.putText(frame,f"Scan {name} Side ({scanned_sides}/6): ", (15, height - 15),2,1.0,(0,255,0))
    else:
        cv2.putText(frame,f"Scan complete", (15, height - 15),2,1.0,(0,255,0))
    
    render_cube(frame)
    
def get_side(index):
    if index == 0:
        return blue_side, "blue"
    elif index == 1:
        return white_side, "white"
    elif index == 2:
        return green_side, "green"
    elif index == 3:
        return yellow_side, "yellow"
    elif index == 4:
        return orange_side, "orange"
    elif index == 5:
        return red_side, "red"
    else:
        return None, "None"

def fill_side(color, row, col):
    side, name = get_side(scanned_sides)
    side[row][col] = color
    
def print_cube():
    print(f"Blue Side:\n {blue_side}")
    print(f"White Side:\n {white_side}")
    print(f"Green Side:\n {green_side}")
    print(f"Yellow Side:\n {yellow_side}")
    print(f"Orange Side:\n {orange_side}")
    print(f"Red Side:\n {red_side}")

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
            cv2.rectangle(frame, (x, y), (x + RECT_SIZE, y + RECT_SIZE), (0, 255, 0), 2)
            cv2.putText(frame,f"{row * 3 + col + 1}", (x + RECT_SIZE - 15, y + RECT_SIZE - 5),1,1.5,(0,255,0))
            if enter_pressed and scanned_sides <= 5:
                sub_rect = frame[y:y + RECT_SIZE, x:x + RECT_SIZE]
                dominant_color = np.uint8(np.mean(sub_rect, axis=(0, 1)))
                closest_color = min(COLORS, key=lambda color: euclidean_distance(COLORS[color], dominant_color))
                calc_average(dominant_color)
                fill_side(closest_color, row, col)
                # print(f"Rectangle {row * 3 + col + 1}: Dominant Color (BGR): {dominant_color},{closest_color}")
    if enter_pressed:
        print(f"Average: {average[0]//9},{average[1]//9},{average[2]//9}")
        if scanned_sides == 6:
            print_cube()
        elif scanned_sides <= 5:
            scanned_sides += 1
        average = [0,0,0]
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