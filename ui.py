from calendar import c
import cv2
import numpy as np

class UI:
    __slots__ = ['COLORS']

    def __init__(self, COLORS):
        self.COLORS = COLORS
    
    def render(self, frame, cube, selected_side, mode):  
        render_info(frame, selected_side, mode)
        
        if mode == mode.SCAN:
            for i in range(6):
                render_side(frame, cube, self.COLORS, selected_side, i)
          
    
def render_side(frame, cube, colors, selected_side, index):
    cell_size = 20
    spacing = 2
    start_positions = [(80, 15), (150, 85), (80, 85), (80, 155), (10, 85), (220, 85)]
    if 0 <= index < len(start_positions):
        start_x, start_y = start_positions[index]
    else:
        return
    
    for row in range(3):
        for col in range(3):
            x = start_x + col * (cell_size + spacing)
            y = start_y + row * (cell_size + spacing)
            val = cube.get_color_string()[index * 9 + row * 3 + col]
            color = colors[val]
            cv2.rectangle(frame, (x, y), (x + cell_size, y + cell_size), color, -1)         
    if index == selected_side:
        cv2.rectangle(frame, (start_x - 2 , start_y - 2), (start_x + 65, start_y + 65), (0, 0, 255), 2)  

def render_info(frame, selected_side, mode):
    font = cv2.FONT_HERSHEY_SIMPLEX
    scale = 0.5
    thickness = 1
    if mode == mode.SCAN:
        color = (0, 255, 0)
    elif mode == mode.CALIBRATION:
        color = (10, 10, 255)
    line_type = cv2.LINE_AA
    height, width, _ = frame.shape
    cv2.rectangle(frame, (width, 0), (width - 200, height), (0, 0, 0), -1)
    cv2.putText(frame, "Controls:", (width - 190, 30), font, scale, color, thickness, line_type)
    cv2.putText(frame, "'Q' = Close Window", (width - 190, 60), font, scale, color, thickness, line_type)
    cv2.putText(frame, "'M' = Change Mode", (width - 190, 150), font, scale, color, thickness, line_type)
    cv2.putText(frame, f"Mode: {get_current_mode(mode)}", (width - 190, height - 60), font, scale, color, thickness, line_type)
    if mode == mode.SCAN:
        cv2.putText(frame, "'Enter' = Scan Side", (width - 190, 90), font, scale, color, thickness, line_type)
        cv2.putText(frame, "'Space' = Print Solution", (width - 190, 180), font, scale, color, thickness, line_type)
        cv2.putText(frame, "'Tab' = Change Side", (width - 190, 120), font, scale, color, thickness, line_type)
        cv2.putText(frame, f"Selected: {get_selected_side(selected_side)}", (width - 190, height - 30), font, scale, color, thickness, line_type)
    elif mode == mode.CALIBRATION:
        cv2.putText(frame, "'Enter' = Print color", (width - 190, 90), font, scale, color, thickness, line_type)


def get_current_mode(mode):
    if mode == mode.SCAN:
        return "Scan"
    elif mode == mode.CALIBRATION:
        return "Calibration"

def get_selected_side(selected_side):
    if selected_side == 0:
        return "Upper"
    elif selected_side == 1:
        return "Right"
    elif selected_side == 2:
        return "Front"
    elif selected_side == 3:
        return "Down"
    elif selected_side == 4:
        return  "Left"
    elif selected_side == 5:
        return "Back"