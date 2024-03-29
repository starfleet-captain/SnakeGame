import sys
import random
from PIL import Image, ImageTk
from tkinter import Canvas, Frame, NW, Tk, ALL
from config.config import Config

# TODO: snake tail
# TODO: speed up when level up
# TODO: score

class WonszCode(Canvas):
    """
    Main class.
    """
    def __init__(self, config):
        self.dimensions = config.get_window_size()

        if config.get_debug():
            print("Window dimensions: {0}x{1}".format(self.dimensions["WIDTH"], self.dimensions["HEIGHT"]))

        super().__init__(width=self.dimensions["WIDTH"], height=self.dimensions["HEIGHT"], background='black')

        self.config = config

        self.in_game = True
        self.snake_size = 2
        self.score = 0
        self.level = 0

        self.move_x = config.get_unit_size()
        self.move_y = 0

        self.items_list = [("item_" + str(x + 1) + ".png") for x in range(self.config.get_number_of_items())]
        self.items_images = []
        self.item_x = 150
        self.item_y = 150

        self.load_graphics()
        self.create_graphics()
        self.locate_item()
        self.bind_all("<Key>", self.on_key_pressed)
        self.after(config.get_game_speed(), self.on_timer)
        self.pack()

    def load_graphics(self):
        """
        Loads all of the graphics. Creates objects for current and future use.
        :return:
        """
        try:
            self.raw_image = Image.open("./static/head.png")
            self.head_up = ImageTk.PhotoImage(self.raw_image)
            self.head_left = ImageTk.PhotoImage(self.raw_image.rotate(90))
            self.head_down = ImageTk.PhotoImage(self.raw_image.rotate(180))
            self.head_right = ImageTk.PhotoImage(self.raw_image.rotate(270))

            self.raw_image = Image.open("./static/body.png")
            self.body = ImageTk.PhotoImage(self.raw_image)

            for item in self.items_list:
                self.raw_image = Image.open("./static/" + item)
                self.items_images.append(ImageTk.PhotoImage(self.raw_image))

        except IOError as e:
            print("Error: " + e)
            sys.exit(-1)

    def create_graphics(self):
        """
        Locates objects at the beginning of the game.
        :return:
        """
        self.create_image(100, 100, image=self.head_right, anchor=NW, tag="head")
        self.create_image(100, 120, image=self.body, anchor=NW, tag="body")
        self.create_image(130, 100, image=self.items_images[0], anchor=NW, tag="item")
        self.create_text(5, self.dimensions['HEIGHT']-15, text="SCORE: {}, LEVEL: {}".format(0, 0), font="Arial, 10",
                         fill="white", tag="score", anchor=NW)


    def locate_item(self):
        """
        Locate item in new location.
        :return:
        """
        item = self.find_withtag("item")
        self.delete(item[0])

        new_item = random.randint(0, self.config.get_number_of_items()-1)

        item_collision = True

        while item_collision:
            position = random.randint(1, self.dimensions["WIDTH"]/self.config.get_unit_size() - 2)
            self.item_x = position * self.config.get_unit_size()
            position = random.randint(1, self.dimensions["HEIGHT"]/self.config.get_unit_size() - 2)
            self.item_y = position * self.config.get_unit_size()

            elements_overlap = self.find_overlapping(self.item_x, self.item_y,
                                                     self.item_x + self.config.get_unit_size(),
                                                     self.item_y + self.config.get_unit_size())

            if len(elements_overlap) == 0:
                self.create_image(self.item_x, self.item_x, anchor=NW, image=self.items_images[new_item], tag="item")
                item_collision = False
            else:
                if self.config.get_debug():
                    print("Wylosowano na wężu!")

                item_collision = True

    def on_key_pressed(self, catched_key):
        """
        Check what kay was pressed. Acttion for each key.
        :param catched_key:
        :return:
        """
        pressed_key = catched_key.keysym

        LEFT_KEY = "Left"
        RIGHT_KEY = "Right"
        UP_KEY = "Up"
        DOWN_KEY = "Down"

        head_element = self.find_withtag("head")
        head_coords = self.coords(head_element)

        if pressed_key == LEFT_KEY and self.move_x <= 0:
            self.delete(head_element)
            self.create_image(head_coords[0], head_coords[1], anchor=NW, image=self.head_left, tag="head")
            self.move_x = -self.config.get_unit_size()
            self.move_y = 0

            if self.config.get_debug():
                print("LEFT")

        if pressed_key == RIGHT_KEY and self.move_x >= 0:
            self.delete(head_element)
            self.create_image(head_coords[0], head_coords[1], anchor=NW, image=self.head_right, tag="head")
            self.move_x = self.config.get_unit_size()
            self.move_y = 0

            if self.config.get_debug():
                print("RIGHT")

        if pressed_key == UP_KEY and self.move_y <= 0:
            self.delete(head_element)
            self.create_image(head_coords[0], head_coords[1], anchor=NW, image=self.head_up, tag="head")
            self.move_x = 0
            self.move_y = -self.config.get_unit_size()

            if self.config.get_debug():
                print("UP")

        if pressed_key == DOWN_KEY and self.move_y >= 0:
            self.delete(head_element)
            self.create_image(head_coords[0], head_coords[1], anchor=NW, image=self.head_down, tag="head")
            self.move_x = 0
            self.move_y = self.config.get_unit_size()

            if self.config.get_debug():
                print("DOWN")

    def move_megawonsz(self):
        """
        Move all snake.
        :return:
        """
        head = self.find_withtag("head")
        body = self.find_withtag("body")

        whole_megawonsz = body + head

        for element in range(0, len(whole_megawonsz)-1, 1):
            e1 = self.coords(whole_megawonsz[element])
            e2 = self.coords(whole_megawonsz[element+1])

            self.move(whole_megawonsz[element], e2[0]-e1[0], e2[1]-e1[1])

        self.move(head, self.move_x, self.move_y)

        if self.config.get_debug():
            print("X: {}, Y: {}".format(self.move_x, self.move_y))

    def check_item_border_collision(self):
        """
        Check is snake is on item or if it hit something.
        :return:
        """
        item_element = self.find_withtag("item")
        head_element = self.find_withtag("head")
        body_element = self.find_withtag("body")

        head_x0, head_y0, head_x1, head_y1 = self.bbox(head_element)
        item_coords = self.coords(item_element)

        elements_overlap = self.find_overlapping(head_x0, head_y0, head_x1, head_y1)

        for overlap in elements_overlap:
            if item_element[0] == overlap:
                self.create_image(item_coords[0], item_coords[1], image=self.body, anchor=NW, tag="body")
                self.locate_item()
                self.score += 1

                if self.score % 10 == 0:
                    self.level += 1
                    self.config.inc_game_speed(20)

                self.update_score()

                if self.config.get_debug():
                    print("TRAFIONY! Punkty: {}".format(self.score))

            for body_part in body_element:
                if body_part == overlap:
                    print("Trafiony w ciało węża!")
                    self.in_game = False

        if head_x0 <= 0 or head_x1 >= self.dimensions["WIDTH"] or head_y0 <= 0 or head_y1 >= self.dimensions["HEIGHT"]:
            return False

        return True

    def on_timer(self):
        """
        Timer tick. Action list for each tick.
        :return:
        """
        if self.in_game:
            if self.check_item_border_collision():
                self.move_megawonsz()
                self.after(self.config.get_game_speed(), self.on_timer)
            else:
                if self.config.get_debug():
                    print("GAME OVER!")

                self.in_game = False
                self.after(self.config.get_game_speed(), self.on_timer)
        else:
            self.game_over()

    def update_score(self):
        score_label = self.find_withtag("score")
        self.delete(score_label)
        self.create_text(5, self.dimensions['HEIGHT'] - 15, text="SCORE: {}, LEVEL: {}".format(self.score, self.level),
                         font="Arial, 10", fill="white", tag="score", anchor=NW)

    def game_over(self):
        """
        Finish the game.
        :return:
        """
        print("IN GAME OVER")
        # self.delete(ALL)
        self.create_text(250, 250, text="GAME OVER", font="Arial, 35", fill="red")


class MegaWonsz(Frame):
    def __init__(self, config):
        super().__init__()
        self.master.title("MegaWonsz9")
        self.board = WonszCode(config)
        self.pack()


def main():
    config = Config()
    root = Tk()
    game = MegaWonsz(config)
    root.mainloop()


if __name__ == '__main__':
    main()
