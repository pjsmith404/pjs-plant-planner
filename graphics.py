from tkinter import Tk, BOTH, Canvas

class Window:
    def __init__(self, width, height):
        self.__root = Tk()
        self.__root.title("PJ's Plant Planner")
        self.__canvas = Canvas(self.__root, bg="white", width=width, height=height)
        self.__canvas.pack(fill=BOTH, expand=1)
        self.__running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.__running = True
        while self.__running:
            self.redraw()

    def close(self):
        self.__running = False

    def draw_rectangle(self, rectangle, outline_colour="black", fill_colour="white"):
        rectangle.draw(self.__canvas, outline_colour, fill_colour)

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Rectangle:
    def __init__(self, top_left, bottom_right):
        self.top_left = top_left
        self.bottom_right = bottom_right

    def draw(self, canvas, outline_colour="black", fill_colour="white"):
        canvas.create_rectangle(
            self.top_left.x,
            self.top_left.y,
            self.bottom_right.x,
            self.bottom_right.y,
            outline=outline_colour,
            fill=fill_colour,
            width=2
        )

class Icon:
    def __init__(self, win):
        self._win = win
        self._rectangle = None

    def draw(self, rectangle):
        self._rectangle = rectangle
        self._win.draw_rectangle(self._rectangle)

