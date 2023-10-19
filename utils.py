import numpy as np
import cv2

def euclidean_distance(color1, color2):
    return np.linalg.norm(np.array(color1) - np.array(color2))

def render_text(frame, text, pos, color=(0, 255, 0), scale=0.5, thickness=1, line_type=cv2.LINE_AA):
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame, text, pos, font, scale, color, thickness, line_type)

def render_rect(frame, pos, w, h, color=(0, 255, 0), thickness=1):
    cv2.rectangle(frame, pos, (pos[0] + w, pos[1] + h), color, thickness)
