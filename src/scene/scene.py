from typing import Dict, Optional

from cv2.typing import MatLike

from cube.cube import Cube
from utils.colors import COLORS, calculate_dominant_color, process_image_section
from utils.helper import (
    render_rect,
    render_text,
)
from utils.ui import render_cube


class Scene:
    def on_enter(self):
        pass

    def on_exit(self):
        pass

    def handle_input(self, frame: MatLike, pressed_key) -> Optional[str]:
        pass

    def update(self, frame: MatLike):
        pass

    def render_ui(self, frame: MatLike):
        pass


class SceneManager:
    def __init__(self) -> None:
        self.scenes: Dict[str, Scene] = {
            "Scan": ScanScene(),
            "Calibrate": CalibrateScene(),
        }
        self.current_scene: Scene | None = None
        self.change_scene(self.scenes["Scan"])

    def change_scene(self, newScene: Scene):
        if self.current_scene:
            self.current_scene.on_exit()
        self.current_scene = newScene
        self.current_scene.on_enter()

    def handle_input(self, frame: MatLike, event):
        if self.current_scene:
            next_scene = self.current_scene.handle_input(frame, event)
            if next_scene:
                self.change_scene(self.scenes[next_scene])

    def update(self, frame: MatLike):
        if self.current_scene:
            self.current_scene.update(frame)

    def render_ui(self, frame: MatLike):
        if self.current_scene:
            self.current_scene.render_ui(frame)


class ScanScene(Scene):
    def __init__(self) -> None:
        self.RECT_SIZE = 120
        self.RECT_SPACING = 5
        self.NAME = "Scan"

    def on_enter(self):
        self.cube = Cube()
        self.cube_side_matrix = [["" * 3 for _ in range(3)] for _ in range(3)]

    def update(self, frame: MatLike):
        height, width, _ = frame.shape
        start_x = (width - (3 * self.RECT_SIZE + 2 * self.RECT_SPACING)) // 2
        start_y = (height - (3 * self.RECT_SIZE + 2 * self.RECT_SPACING)) // 2
        for row in range(3):
            for col in range(3):
                x = start_x + col * (self.RECT_SIZE + self.RECT_SPACING)
                y = start_y + row * (self.RECT_SIZE + self.RECT_SPACING)

                sub_rect = frame[y : y + self.RECT_SIZE, x : x + self.RECT_SIZE]

                closest_color = process_image_section(sub_rect)
                self.cube_side_matrix[row][col] = closest_color

                render_rect(
                    frame,
                    (x, y),
                    self.RECT_SIZE,
                    self.RECT_SIZE,
                    COLORS[closest_color],
                    2,
                )
                render_text(
                    frame,
                    f"{row * 3 + col + 1}",
                    (x + self.RECT_SIZE - 20, y + self.RECT_SIZE - 10),
                )
                render_text(
                    frame,
                    f"{closest_color}",
                    (x + self.RECT_SIZE // 2 - 5, y + self.RECT_SIZE // 2 + 5),
                    COLORS[closest_color],
                    0.7,
                )

    def render_ui(self, frame: MatLike):
        render_cube(frame, self.cube)

    def handle_input(self, frame, pressed_key):
        if pressed_key == ord("m"):
            return "Calibrate"
        elif pressed_key == ord("\t"):
            self.cube.next_face()
        elif pressed_key == 13:
            self.cube.set_face(self.cube_side_matrix)
            self.cube.next_face()
        elif pressed_key == 32:
            print(f"Solution: {self.cube.get_solution()}")
        elif pressed_key == ord("r"):
            self.cube.reset_face(self.cube.get_selected_face_index())


class CalibrateScene(Scene):
    def __init__(self) -> None:
        self.RECT_SIZE = 200
        self.NAME = "Calibration"

    def on_enter(self):
        self.dominant_color = ""

    def update(self, frame: MatLike):
        height, width, _ = frame.shape
        x = (width - self.RECT_SIZE) // 2
        y = (height - self.RECT_SIZE) // 2
        sub_rect = frame[y : y + self.RECT_SIZE, x : x + self.RECT_SIZE]
        self.dominant_color = calculate_dominant_color(sub_rect)
        render_text(frame, f"{self.dominant_color}", (x, y - 10))
        render_rect(
            frame,
            (x, y),
            self.RECT_SIZE,
            self.RECT_SIZE,
        )

    def render_ui(self, frame: MatLike):
        height, width, _ = frame.shape
        render_rect(
            frame,
            (width - 200, 0),
            200,
            height,
            (0, 0, 1),
            -1,
        )
        render_text(frame, "Controls:", (width - 190, 30))
        render_text(frame, "'Q' = Close Window", (width - 190, 60))
        render_text(frame, "'M' = Change Mode", (width - 190, 150))
        render_text(frame, f"Mode: {self.NAME}", (width - 190, height - 60))
        render_text(frame, "'Enter' = Print color", (width - 190, 90))

    def handle_input(self, frame, pressed_key):
        if pressed_key == ord("m"):
            return "Scan"
        if pressed_key == 13:
            print(f"Color: {self.dominant_color}")
