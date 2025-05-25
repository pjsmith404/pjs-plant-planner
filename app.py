import tkinter as tk
from tkinter import ttk

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
        self._widget = canvas.create_rectangle(
            10,
            10,
            20,
            20,
            outline="black",
            fill="green",
            width=2
        )

