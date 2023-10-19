import kociemba

# Empty 000000000000000000000000000000000000000000000000000000
# Test1 BDBBUFLBFDDRURBUFLDULDFLURBRFLBDURRFRLBLLLFRFDRUDBFUUD

class Cube:
    state = list("000000000000000000000000000000000000000000000000000000")
    
    def __str__(self) -> str:
        return ''.join(self.state)

    def get_color_string(self):
        color_string = ""
        for char in self.state:
            if char == "F":
                color_string += "W"
            elif char == "L":
                color_string += "B"
            elif char == "R":
                color_string += "G"
            elif char == "B":
                color_string += "Y"
            elif char == "D":
                color_string += "O"
            elif char == "U":
                color_string += "R"
            elif char == "0":
                color_string += "0"
        return color_string
    
    def get_solution(self):
        try:
            return kociemba.solve(''.join(self.state))
        except:
            return "error"
    
    def reset_full(self):
        self.state = list("000000000000000000000000000000000000000000000000000000")

    def reset_side(self, side):
        for i in range(9):
            self.state[i + side * 9] = "0"