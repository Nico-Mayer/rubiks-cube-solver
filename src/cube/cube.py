import kociemba

from utils.colors import map_colors_to_faces, map_faces_to_colors


# Empty 000000000000000000000000000000000000000000000000000000
# Test1 BDBBUFLBFDDRURBUFLDULDFLURBRFLBDURRFRLBLLLFRFDRUDBFUUD
class Cube:
    def __init__(self) -> None:
        self.state = list("000000000000000000000000000000000000000000000000000000")
        self.selected_face = 0

    def get_state(self) -> str:
        return "".join(self.state)

    def get_color_string(self) -> str:
        color_string = map_faces_to_colors(self.get_state())
        return color_string

    def get_solution(self) -> str:
        try:
            return kociemba.solve("".join(self.state))
        except Exception as e:
            print(e)
            return "error"

    def set_face(self, face_matrix: list[list[str]]):
        color_str = "".join([char for row in face_matrix for char in row])
        siede_str = map_colors_to_faces(color_str)
        i = self.selected_face * 9
        self.state[i : i + len(siede_str)] = list(siede_str)

    def reset_full(self):
        self.state = list("000000000000000000000000000000000000000000000000000000")

    def reset_face(self, face_index: int):
        for i in range(9):
            self.state[i + face_index * 9] = "0"

    def next_face(self):
        self.selected_face += 1
        if self.selected_face >= 6:
            self.selected_face = 0

    def get_selected_face_index(self) -> int:
        return self.selected_face

    def get_selected_face(self) -> str:
        return ["UP", "Right", "Front", "Down", "Left", "Back"][self.selected_face]
