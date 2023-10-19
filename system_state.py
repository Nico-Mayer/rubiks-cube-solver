class Mode:
    CALIBRATION = 1
    SCAN = 2

    def __init__(self):
        self.mode = Mode.SCAN

    def change(self):
        if self.mode == Mode.CALIBRATION:
            self.mode = Mode.SCAN
        elif self.mode == Mode.SCAN:
            self.mode = Mode.CALIBRATION

    def set_mode(self, mode):
        self.mode = mode

    def get_mode(self) -> str:
        if self.mode == Mode.CALIBRATION:
            return "CALIBRATION"
        else:
            return "SCAN"

    def is_calibration(self) -> bool:
        return self.mode == Mode.CALIBRATION

    def is_scan(self) -> bool:
        return self.mode == Mode.SCAN


class Selected_Side:
    index: int = 0

    def next(self):
        self.index += 1
        if self.index >= 6:
            self.index = 0

    def get_index(self) -> int:
        return self.index

    def get_side(self) -> str:
        return ["UP", "Right", "Front", "Down", "Left", "Back"][self.index]
