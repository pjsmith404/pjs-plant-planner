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
        self.pack(side="left", fill=tk.BOTH, expand=True)
        self._map = MapFrame(self)

        self.okay_button = ttk.Button(self, text="Add Plant", command=self._map.add_plant)
        self.okay_button.pack()

class MapFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(side="right", fill=tk.BOTH, expand=True)
        self._canvas = MapCanvas(self, bg="white")
        self._canvas.pack(fill=tk.BOTH, expand=True)

    def add_plant(self):
        Plant(self._canvas)

    def dismiss_dlg(self, dlg):
        dlg.grab_release()
        dlg.destroy()

class Plant:
    def __init__(self, canvas):
        self.name = tk.StringVar()
        self.planted = tk.StringVar()
        self._tree_icon = tk.PhotoImage(file='icons/tree_planted.gif')
        self._tree_icon = self._tree_icon.subsample(4)
        self.widget = canvas.create_image(10, 10, image=self._tree_icon, anchor="nw")
        self._canvas = canvas
        self._x_offset = 0
        self._y_offset = 0

        self.plant_dlg()

        self._canvas.tag_bind(self.widget, "<Button-1>", self.drag_start)
        self._canvas.tag_bind(self.widget, "<B1-Motion>", self.drag_motion)
        self._canvas.tag_bind(self.widget, "<ButtonRelease-1>", self.drag_stop)
        self._canvas.tag_bind(self.widget, "<Button-3>", self.plant_dlg)

    def plant_dlg(self, *args):
        dlg = tk.Toplevel()

        ttk.Label(dlg, text="Name:").grid()
        name_entry = ttk.Entry(dlg, textvariable=self.name)
        name_entry.grid()

        ttk.Label(dlg, text="Planted:").grid()
        planted_entry = ttk.Entry(dlg, textvariable=self.planted)
        planted_entry.grid()

        ttk.Button(dlg, text="Done", command=lambda: self.dismiss_dlg(dlg)).grid()

        dlg.wait_visibility()
        dlg.grab_set()
        dlg.wait_window()

    def dismiss_dlg(self, dlg):
        dlg.grab_release()
        dlg.destroy()

    def drag_start(self, event):
        self._canvas.disable_draw()
        self._x_offset = event.x
        self._y_offset = event.y

    def drag_motion(self, event):
        x = event.x - self._x_offset
        y = event.y - self._y_offset
        self._x_offset = event.x
        self._y_offset = event.y
        self._canvas.move("current", x, y)

    def drag_stop(self, event):
        self._canvas.enable_draw()

class MapCanvas(tk.Canvas):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self._last_x = 0
        self._last_y = 0

        self.enable_draw()

    def save_posn(self, event):
        self._last_x, self._last_y = event.x, event.y

    def add_line(self, event):
        line = self.create_line(self._last_x, self._last_y, event.x, event.y, width=2)
        self.lower(line)
        self.save_posn(event)

    def disable_draw(self):
        self.unbind("<Button-1>")
        self.unbind("<B1-Motion>")

    def enable_draw(self):
        self.bind("<Button-1>", self.save_posn)
        self.bind("<B1-Motion>", self.add_line)

