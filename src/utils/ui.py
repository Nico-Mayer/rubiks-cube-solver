from cv2.typing import MatLike

from cube.cube import Cube, Face
from utils.colors import COLORS, map_faces_to_colors
from utils.helper import render_rect, render_text


def render_cube(frame: MatLike, cube: Cube):
    for i in range(6):
        render_cube_face(frame, cube, i)


def render_cube_face(frame: MatLike, cube: Cube, index: int):
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
            color = COLORS[val]
            if col == 1 and row == 1:
                face_name = Face(index).name
                color = COLORS[map_faces_to_colors(face_name[0])]
            render_rect(frame, (x, y), cell_size, cell_size, color, -1)
    if index == cube.get_selected_face_index():
        render_rect(frame, (start_x - 2, start_y - 2), 65, 65, (0, 0, 255), 2)


def render_info(frame: MatLike, cube: Cube):
    height, width, _ = frame.shape
    render_rect(frame, (width - 200, 0), 200, height, (0, 0, 0), -1)
    render_text(frame, "Controls:", (width - 190, 30))
    render_text(frame, "'Q' = Close Window", (width - 190, 60))
    render_text(frame, "'M' = Change Mode", (width - 190, 150))
    # render_text(frame, f"Mode: {mode.get_mode()}", (width - 190, height - 60))
    render_text(frame, "'Enter' = Scan Side", (width - 190, 90))
    render_text(frame, "'Tab' = Change Side", (width - 190, 120))
    render_text(frame, "'Space' = Print Solution", (width - 190, 180))
    render_text(frame, "'R' = Reset side", (width - 190, 210))
    render_text(
        frame, f"Selected: {cube.get_selected_face()}", (width - 190, height - 30)
    )
