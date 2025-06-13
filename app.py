import json
import tkinter as tk
from tkinter import ttk, messagebox

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("PJ's Plant Planner")

        self.option_add('*tearOff', False)

        menubar = AppMenu(self)
        self['menu'] = menubar

class AppMenu(tk.Menu):
    def __init__(self, parent):
        super().__init__(parent)

        self._parent = parent
        self._map = None

        menu_file = tk.Menu(self)
        menu_plants = tk.Menu(self)
        self.add_cascade(menu=menu_file, label="File")
        self.add_cascade(menu=menu_plants, label="Plants")

        menu_file.add_command(label="New", command=self.new_file)
        menu_file.add_command(label="Open...", command=self.open_file)
        menu_file.add_command(label="Close", command=self.close_file)
        menu_file.add_command(label="Save", command=self.save_file)

        menu_plants.add_command(label="Add Plant", command=self.add_plant)

    def new_file(self):
        if self._map:
            self._map.destroy()
        self._map = MapFrame(self._parent)

    def open_file(self):
        self.new_file()
        with open("./plantmap.json", "r") as f:
            plant_data = json.loads(f.read())
            print(plant_data)
            for plant in plant_data.values():
                self._map._canvas.add_plant(
                    plant.get("name"),
                    plant.get("planted"),
                    plant.get("x"),
                    plant.get("y")
                )

    def save_file(self):
        print(self._map.get_canvas_state())
        if self._map:
            with open("./plantmap.json", "w") as f:
                f.write(json.dumps(self._map.get_canvas_state()))

    def close_file(self):
        # TODO: Wipe the canvas
        pass

    def add_plant(self):
        if self._map:
            self._map.add_plant()

class MapFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(side="right", fill=tk.BOTH, expand=True)
        self._canvas = MapCanvas(self, bg="white")
        self._canvas.pack(fill=tk.BOTH, expand=True)

    def add_plant(self):
        self._canvas.add_plant()

    def get_canvas_state(self):
        return self._canvas.get_canvas_state()

class Plant:
    def __init__(self, canvas, name=None, planted=None, x=10, y=10):
        self.name = tk.StringVar()
        if name:
            self.name.set(name)
        self.planted = tk.StringVar()
        if planted:
            self.planted.set(planted)
        self._tree_icon = tk.PhotoImage(file='icons/tree_planted.gif')
        self._tree_icon = self._tree_icon.subsample(4)
        self.widget = canvas.create_image(x, y, image=self._tree_icon, anchor="nw")
        self._canvas = canvas
        self._x_offset = 0
        self._y_offset = 0

        if not self.name.get():
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
        self._canvas.update_plant_state(self)

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
        self._canvas.update_plant_state(self)

class MapCanvas(tk.Canvas):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self._last_x = 0
        self._last_y = 0
        # Track the state of widgets on the Canvas
        self._state = {}

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

    def add_plant(self, name=None, planted=None, x=0, y=0):
        plant = Plant(self, name, planted, x, y)
        self.update_plant_state(plant)

    def update_plant_state(self, plant):
        x, y = self.coords(plant.widget)

        self._state[plant.widget] = {
            "name": plant.name.get(),
            "planted": plant.planted.get(),
            "x": x,
            "y": y
        }

    def get_canvas_state(self):
        return self._state

