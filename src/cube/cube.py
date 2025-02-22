import kociemba

from utils.colors import map_colors_to_sides, map_sides_to_colors


# Empty 000000000000000000000000000000000000000000000000000000
# Test1 BDBBUFLBFDDRURBUFLDULDFLURBRFLBDURRFRLBLLLFRFDRUDBFUUD
class Cube:
    state = list("000000000000000000000000000000000000000000000000000000")
    selected_side = 0

    def get_state(self) -> str:
        return "".join(self.state)

    def get_color_string(self) -> str:
        color_string = map_sides_to_colors(self.get_state())
        return color_string

    def get_solution(self) -> str:
        try:
            return kociemba.solve("".join(self.state))
        except Exception as e:
            print(e)
            return "error"

    def set_side(self, side_matrix: list[list[str]]):
        color_str = "".join([char for row in side_matrix for char in row])
        siede_str = map_colors_to_sides(color_str)
        i = self.selected_side * 9
        self.state[i : i + len(siede_str)] = list(siede_str)

    def reset_full(self):
        self.state = list("000000000000000000000000000000000000000000000000000000")

    def reset_side(self, side: int):
        for i in range(9):
            self.state[i + side * 9] = "0"

    def next_side(self):
        self.selected_side += 1
        if self.selected_side >= 6:
            self.selected_side = 0

    def get_selected_side_index(self) -> int:
        return self.selected_side

    def get_selected_side(self) -> str:
        return ["UP", "Right", "Front", "Down", "Left", "Back"][self.selected_side]
