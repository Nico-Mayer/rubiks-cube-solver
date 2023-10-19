import kociemba

# Test1 BDBBUFLBFDDRURBUFLDULDFLURBRFLBDURRFRLBLLLFRFDRUDBFUUD

class Cube:
    state = list("BDBBUFLBFDDRURBUFLDULDFLURBRFLBDURRFRLBLLLFRFDRUDBFUUD")
    
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
            else:
                color_string += "error"
        return color_string
    
    def get_solution(self):
        try:
            return kociemba.solve(''.join(self.state))
        except:
            return "error"