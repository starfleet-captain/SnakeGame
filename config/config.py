class Config:
    def __init__(self):
        self.BOARD_X_SIZE = 700 # 500
        self.BOARD_Y_SIZE = 800 # 600
        self.GAME_SPEED = 250
        self.UNIT_SIZE = 20
        self.NUMBER_OF_ITERMS = 3
        self.DEBUG_MSG = True

    def get_game_speed(self):
        return self.GAME_SPEED

    def inc_game_speed(self, speed):
        self.GAME_SPEED -= speed

    def get_window_size(self):
        size = {"WIDTH": self.BOARD_X_SIZE, "HEIGHT": self.BOARD_Y_SIZE}
        return size

    def get_unit_size(self):
        return self.UNIT_SIZE

    def get_number_of_items(self):
        return self.NUMBER_OF_ITERMS

    def get_debug(self):
        return self.DEBUG_MSG
