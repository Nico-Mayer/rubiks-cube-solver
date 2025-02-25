from enum import Enum

import kociemba

from utils.colors import map_colors_to_faces, map_faces_to_colors

#               +------------+
#               | U1  U2  U3 |
#               | U4  U5  U6 |
#               | U7  U8  U9 |
#   +-----------+-------------+------------+------------+
#   | L1  L2  L3 | F1  F2  F3 | R1  R2  R3 | B1  B2  B3 |
#   | L4  L5  L6 | F4  F5  F6 | R4  R5  R6 | B4  B5  B6 |
#   | L7  L8  L9 | F7  F8  F9 | R7  R8  R9 | B7  B8  B9 |
#   +-----------+-------------+------------+------------+
#               | D1  D2  D3 |
#               | D4  D5  D6 |
#               | D7  D8  D9 |
#               +------------+
#
# EMPTY: 000000000000000000000000000000000000000000000000000000
# SOVED: UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB
# Scramble: BDBBUFLBFDDRURBUFLDULDFLURBRFLBDURRFRLBLLLFRFDRUDBFUUD


class Face(Enum):
    UP = 0
    RIGHT = 1
    FRONT = 2
    DOWN = 3
    LEFT = 4
    BACK = 5

    @classmethod
    def get_name(cls, index: int) -> str:
        """Convert face index to string representation."""
        return cls(index).name


class Cube:
    EMPTY_STATE = "0" * 54
    FACE_SIZE = 9
    NUM_FACES = 6

    def __init__(self) -> None:
        self.state = list(self.EMPTY_STATE)
        self.selected_face: Face = Face.UP

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
        start = self.selected_face.value * self.FACE_SIZE
        color_str = "".join([char for row in face_matrix for char in row])
        self.state[start : start + self.FACE_SIZE] = map_colors_to_faces(color_str)

    def reset(self):
        self.state = list(self.EMPTY_STATE)

    def reset_face(self, face_index: int):
        start = face_index * self.FACE_SIZE
        self.state[start : start + self.FACE_SIZE] = ["0"] * self.FACE_SIZE

    def next_face(self):
        next_face_index = (self.selected_face.value + 1) % self.NUM_FACES
        self.selected_face = Face(next_face_index)

    def get_selected_face_index(self) -> int:
        return self.selected_face.value

    def get_selected_face(self) -> str:
        return self.selected_face.name
