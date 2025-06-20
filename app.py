import json
import base64

import tkinter as tk
from tkinter import ttk, messagebox, filedialog

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

        self._save_file = None

        menu_file = tk.Menu(self)
        self.add_cascade(menu=menu_file, label="File")

        menu_file.add_command(label="New File", command=self.new_file)
        menu_file.add_command(label="Open...", command=self.open_file)
        menu_file.add_separator()
        menu_file.add_command(label="Save", command=self.save_file)
        menu_file.add_command(label="Save As...", command=self.save_file_prompt)
        menu_file.add_separator()
        menu_file.add_command(label="Close", command=self.close_file)
        menu_file.add_command(label="Exit", command=self._parent.destroy)

        menu_plants = tk.Menu(self)
        self.add_cascade(menu=menu_plants, label="Plants")
        menu_plants.add_command(label="Add Plant", command=self.add_plant)

        menu_map = tk.Menu(self)
        self.add_cascade(menu=menu_map, label="Map")
        menu_map.add_command(label="Import Background...", command=self.import_background)

    def new_file(self):
        if self._map:
            self._map.destroy()
        self._map = MapCanvas(self._parent)

    def open_file(self):
        self.new_file()
        filename = filedialog.askopenfilename()
        self._save_file = filename
        with open(filename, "r") as f:
            plant_data = json.loads(f.read())

            background_data = base64.b64decode(plant_data.pop("background", None))
            background_image = tk.PhotoImage(data=background_data)
            if background_data:
                self._map.set_background(background_image)

            for plant in plant_data.values():
                self._map.add_plant(
                    plant.get("name"),
                    plant.get("planted"),
                    plant.get("x"),
                    plant.get("y")
                )

    def save_file(self):
        if not self._save_file:
            # TODO: This somehow causes an infinite loop if you decide not to save a new file
            self.save_file_prompt()
        if self._map:
            with open(self._save_file, "w") as f:
                f.write(json.dumps(self._map.get_canvas_state()))

    def save_file_prompt(self):
        if self._map:
            filename = filedialog.asksaveasfilename()
            self._save_file = filename
            self.save_file()

    def close_file(self):
        if self._map:
            self._map.destroy()
            self._save_file = None

    def add_plant(self):
        if self._map:
            self._map.add_plant()

    def import_background(self):
        filename = filedialog.askopenfilename()
        background_image = tk.PhotoImage(file=filename)

        if self._map:
            self._map.set_background(background_image)
        else:
            self.new_file()
            self._map.set_background(background_image)

class MapCanvas(tk.Canvas):
    def __init__(self, parent):
        super().__init__(parent, bg="white")

        self.pack(fill=tk.BOTH, expand=True)

        self._tree_icon = tk.PhotoImage(file='icons/tree_planted.gif')
        self._tree_icon = self._tree_icon.subsample(4)

        self._background = None

        self._state = {}

    def add_plant(self, name=None, planted=None, x=10, y=10):
        widget = self.create_image(x, y, image=self._tree_icon, anchor="nw", tags=("plant"))
        plant = Plant(self, widget, name, planted)
        self.update_plant_state(plant)

    def update_plant_state(self, plant):
        x, y = self.coords(plant.widget)

        self._state[plant.widget] = {
            "name": plant.name.get(),
            "planted": plant.planted.get(),
            "x": x,
            "y": y
        }

    def update_background_state(self):
        background = self._background.data("png")
        b64_encoded_bg = base64.b64encode(background)
        b64_ascii_bg = b64_encoded_bg.decode("ascii")
        self._state["background"] = b64_ascii_bg

    def get_canvas_state(self):
        return self._state

    def set_background(self, image):
        self._background = image

        self.config(width=self._background.width(), height=self._background.height())
        widget = self.create_image(0, 0, image=self._background, anchor="nw", tags=("background"))
        self.pack(fill=tk.NONE, expand=False)
        self.lower(widget)
        self.update_background_state()

class Plant:
    def __init__(self, canvas, widget, name=None, planted=None):
        self.name = tk.StringVar()
        if name:
            self.name.set(name)
        self.planted = tk.StringVar()
        if planted:
            self.planted.set(planted)
        self.widget = widget
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
        self._x_offset = event.x
        self._y_offset = event.y

    def drag_motion(self, event):
        x = event.x - self._x_offset
        y = event.y - self._y_offset
        self._x_offset = event.x
        self._y_offset = event.y
        self._canvas.move("current", x, y)

    def drag_stop(self, event):
        self._canvas.update_plant_state(self)

