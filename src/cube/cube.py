import kociemba

from utils.colors import map_colors_to_faces, map_faces_to_colors


# Empty 000000000000000000000000000000000000000000000000000000
# Test1 BDBBUFLBFDDRURBUFLDULDFLURBRFLBDURRFRLBLLLFRFDRUDBFUUD
class Cube:
    EMPTY_STATE = "0" * 54

    def __init__(self) -> None:
        self.state = list(self.EMPTY_STATE)
        self.selected_face = 0

    def get_state(self) -> str:
        return "".join(self.state)

    def get_color_string(self) -> str:
        return map_faces_to_colors(self.get_state())

    def get_solution(self) -> str:
        try:
            return kociemba.solve("".join(self.state))
        except Exception as e:
            print(e)
            return "error"

    def set_face(self, face_matrix: list[list[str]]):
        start = self.selected_face * 9
        color_str = "".join([char for row in face_matrix for char in row])
        self.state[start : start + 9] = map_colors_to_faces(color_str)

    def reset(self):
        self.state = list(self.EMPTY_STATE)

    def reset_face(self, face_index: int):
        start = face_index * 9
        self.state[start : start + 9] = ["0"] * 9

    def next_face(self):
        self.selected_face = (self.selected_face + 1) % 6

    def get_selected_face_index(self) -> int:
        return self.selected_face

    def get_selected_face(self) -> str:
        return ["UP", "Right", "Front", "Down", "Left", "Back"][self.selected_face]
