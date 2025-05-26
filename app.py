import tkinter as tk
from tkinter import ttk, messagebox

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("PJ's Plant Planner")

        self.control = ControlFrame(self)

class ControlFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(side="left")
        self._map = MapFrame(self)

        self.okay_button = ttk.Button(self, text="Add Plant", command=self._map.add_plant)
        self.okay_button.pack()

class MapFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(side="right")
        self._canvas = tk.Canvas(self, bg="white", width=300, height=300)
        self._canvas.pack()
        self._plants = []

    def add_plant(self):
        self._plants.append(Plant("Test", "2025-01-01", self._canvas))

class Plant:
    def __init__(self, name, planted, canvas):
        self.name = name
        self.planted = planted
        self.widget = canvas.create_rectangle(
            10,
            10,
            20,
            20,
            outline="black",
            fill="green",
            width=2
        )
        self._canvas = canvas
        self._x_offset = 0
        self._y_offset = 0

        canvas.tag_bind(self.widget, "<Button-1>", self.drag_start)
        canvas.tag_bind(self.widget, "<B1-Motion>", self.drag_motion)
        canvas.tag_bind(self.widget, "<Button-3>", self.get_info)
    
    def drag_start(self, event):
        self._x_offset = event.x
        self._y_offset = event.y

    def drag_motion(self, event):
        print(event)
        print(self._x_offset, self._y_offset)
        x = event.x - self._x_offset
        y = event.y - self._y_offset
        self._canvas.move("current", x, y)
        self._x_offset = event.x
        self._y_offset = event.y

    def get_info(self, event):
        messagebox.showinfo(message=f"Plant: {self.name}\nPlanted: {self.planted}")
