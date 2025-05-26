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

    def add_plant(self):
        dlg = tk.Toplevel()
        
        ttk.Label(dlg, text="Plant Name:").grid()
        name = ttk.Entry(dlg, textvariable="name")
        name.grid()

        ttk.Label(dlg, text="Planted:").grid()
        planted = ttk.Entry(dlg, textvariable="planted")
        planted.grid()
        
        ttk.Button(dlg, text="Done", command=lambda: self.dismiss_dlg(dlg)).grid()
        dlg.wait_visibility()
        dlg.grab_set()
        dlg.wait_window()
        
        Plant(name.get(), planted.get(), self._canvas)

    def dismiss_dlg(self, dlg):
        dlg.grab_release()
        dlg.destroy()

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
        x = event.x - self._x_offset
        y = event.y - self._y_offset
        self._x_offset = event.x
        self._y_offset = event.y
        self._canvas.move("current", x, y)

    def get_info(self, event):
        messagebox.showinfo(message=f"Plant: {self.name}\nPlanted: {self.planted}")
