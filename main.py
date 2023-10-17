import cv2
import numpy as np

RECT_SIZE = 80
RECT_SPACING = 10
CAM_INDEX = 1
COLORS = {
    'blue': (0, 0, 255),  
    'green': (0, 255, 0),
    'white': (255, 255, 255),
    'red': (0, 0, 255),
    'orange': (0, 165, 255),
    'yellow': (0, 255, 255)
}

cap = cv2.VideoCapture(CAM_INDEX)
enter_pressed = False

def euclidean_distance(color1, color2):
    return np.linalg.norm(np.array(color1) - np.array(color2))

while True:
    ret, frame = cap.read()

    if not ret:
        break
    
    height, width, _ = frame.shape

    start_x = (width - (3 * RECT_SIZE + 2 * RECT_SPACING)) // 2
    start_y = (height - (3 * RECT_SIZE + 2 * RECT_SPACING)) // 2

    for row in range(3):
        for col in range(3):
            x = start_x + col * (RECT_SIZE + RECT_SPACING)
            y = start_y + row * (RECT_SIZE + RECT_SPACING)
            cv2.rectangle(frame, (x, y), (x + RECT_SIZE, y + RECT_SIZE), (0, 255, 0), 2)
            cv2.putText(frame,f"{row * 3 + col + 1}", (x + RECT_SIZE - 15, y + RECT_SIZE - 5),1,1.0,(0,255,0))
            if enter_pressed:
                sub_rect = frame[y:y + RECT_SIZE, x:x + RECT_SIZE]
                dominant_color = np.uint8(np.mean(sub_rect, axis=(0, 1)))
                closest_color = min(COLORS, key=lambda color: euclidean_distance(COLORS[color], dominant_color))
                print(f"Rectangle {row * 3 + col + 1}: Dominant Color (BGR): {dominant_color},{closest_color}")
                
    enter_pressed = False
    cv2.imshow('Camera Feed', frame)
	

    key = cv2.waitKey(1)
    if key == ord('q'):
        break
    elif key == 13:  
        enter_pressed = True

    
cap.release()
cv2.destroyAllWindows()

