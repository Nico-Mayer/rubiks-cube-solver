from colors import COLORS
from utils import render_rect, render_text


class UI:
    def render(self, frame, cube, selected_side, mode):
        render_info(frame, selected_side, mode)

        if mode.is_scan():
            for i in range(6):
                render_side(frame, cube, selected_side, i)


def render_side(frame, cube, selected_side, index):
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
            render_rect(frame, (x, y), cell_size, cell_size, color, -1)
    if index == selected_side.get_index():
        render_rect(frame, (start_x - 2, start_y - 2), 65, 65, (0, 0, 255), 2)


def render_info(frame, selected_side, mode):
    height, width, _ = frame.shape
    render_rect(frame, (width - 200, 0), 200, height, (0, 0, 0), -1)
    render_text(frame, "Controls:", (width - 190, 30))
    render_text(frame, "'Q' = Close Window", (width - 190, 60))
    render_text(frame, "'M' = Change Mode", (width - 190, 150))
    render_text(frame, f"Mode: {mode.get_mode()}", (width - 190, height - 60))
    if mode.is_scan():
        render_text(frame, "'Enter' = Scan Side", (width - 190, 90))
        render_text(frame, "'Tab' = Change Side", (width - 190, 120))
        render_text(frame, "'Space' = Print Solution", (width - 190, 180))
        render_text(frame, "'R' = Reset side", (width - 190, 210))
        render_text(
            frame, f"Selected: {selected_side.get_side()}", (width - 190, height - 30)
        )
    elif mode.is_calibration():
        render_text(frame, "'Enter' = Print color", (width - 190, 90))
