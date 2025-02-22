import cv2

from scene.scene import SceneManager

RECT_SIZE: int = 120
RECT_SPACING: int = 5
CAM_INDEX: int = 1


def main():
    cap = cv2.VideoCapture(CAM_INDEX)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    scene_manger = SceneManager()

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        pressed_key = cv2.waitKey(1)

        scene_manger.handle_input(frame, pressed_key)
        scene_manger.update(frame)
        scene_manger.render_ui(frame)

        if pressed_key == ord("q"):
            break

        cv2.imshow("Camera Feed", frame)
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
