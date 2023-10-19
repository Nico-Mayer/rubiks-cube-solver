class MODE:
    CALIBRATION = 1
    SCAN = 2

    def __init__(self):
        self.mode = MODE.SCAN

    def change(self):
        if self.mode == MODE.CALIBRATION:
            self.mode = MODE.SCAN
        elif self.mode == MODE.SCAN:
            self.mode = MODE.CALIBRATION

    def set_mode(self, mode):
        self.mode = mode

    def get_mode(self):
        if self.mode == MODE.CALIBRATION:
            return "CALIBRATION"
        elif self.mode == MODE.SCAN:
            return "SCAN"

    def is_calibration(self):
        return self.mode == MODE.CALIBRATION

    def is_scan(self):
        return self.mode == MODE.SCAN


class SELECTED_SIDE:
    index = 0

    def next(self):
        self.index += 1
        if self.index >= 6:
            self.index = 0

    def get_index(self):
        return self.index

    def get_side(self):
        return ["UP", "Right", "Front", "Down", "Left", "Back"][self.index]
