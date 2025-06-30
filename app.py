import json
import base64

import tkinter as tk
from tkinter import ttk, messagebox, filedialog


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("PJ's Plant Planner")

        self.option_add("*tearOff", False)

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        menubar = AppMenu(self)
        self["menu"] = menubar


class AppMenu(tk.Menu):
    def __init__(self, parent):
        super().__init__(parent)

        self._parent = parent
        self._map = None

        self._save_file = None

        self.menu_file = tk.Menu(self)
        self.add_cascade(menu=self.menu_file, label="File")

        self.menu_file.add_command(label="New File", command=self.new_file)
        self.menu_file.add_command(label="Open...", command=self.open_file)

        self.menu_file.add_separator()
        self.menu_file.add_command(
            label="Save", command=self.save_file, state=tk.DISABLED
        )
        self.menu_file.add_command(
            label="Save As...", command=self.save_file_prompt, state=tk.DISABLED
        )

        self.menu_file.add_separator()
        self.menu_file.add_command(
            label="Close", command=self.close_file, state=tk.DISABLED
        )
        self.menu_file.add_command(label="Exit", command=self._parent.destroy)

        self.menu_plants = tk.Menu(self)
        self.add_cascade(menu=self.menu_plants, label="Plants")
        self.menu_plants.add_command(
            label="Add Plant", command=self.add_plant, state=tk.DISABLED
        )
        self.menu_plants.add_command(
            label="List Plants", command=self.list_plants, state=tk.DISABLED
        )

        self.menu_map = tk.Menu(self)
        self.add_cascade(menu=self.menu_map, label="Map")
        self.menu_map.add_command(
            label="Import Background...", command=self.import_background
        )

    def map_active(self):
        if self._map:
            self.menu_file.entryconfigure("Save", state=tk.NORMAL)
            self.menu_file.entryconfigure("Save As...", state=tk.NORMAL)
            self.menu_file.entryconfigure("Close", state=tk.NORMAL)
            self.menu_plants.entryconfigure("Add Plant", state=tk.NORMAL)
            self.menu_plants.entryconfigure("List Plants", state=tk.NORMAL)

    def map_inactive(self):
        if not self._map:
            self.menu_file.entryconfigure("Save", state=tk.DISABLED)
            self.menu_file.entryconfigure("Save As...", state=tk.DISABLED)
            self.menu_file.entryconfigure("Close", state=tk.DISABLED)
            self.menu_plants.entryconfigure("Add Plant", state=tk.DISABLED)
            self.menu_plants.entryconfigure("List Plants", state=tk.DISABLED)

    def new_file(self):
        self._save_file = None
        if self._map:
            self._map.destroy()
        self._map = MapCanvas(self._parent)

        self.map_active()

    def open_file(self):
        filename = filedialog.askopenfilename()
        if filename:
            self.new_file()
            self._save_file = filename
            with open(filename, "r") as f:
                plant_data = json.loads(f.read())

                background_data = plant_data.pop("background", None)
                if background_data:
                    background_image = tk.PhotoImage(data=background_data)
                    self._map.set_background(background_image)

                for plant in plant_data.values():
                    self._map.add_plant(
                        plant.get("name"),
                        plant.get("planted"),
                        plant.get("x1"),
                        plant.get("y1"),
                        plant.get("x2"),
                        plant.get("y2"),
                    )
            self.map_active()

    def save_file(self):
        if not self._save_file:
            self.save_file_prompt()
        if self._map and self._save_file:
            with open(self._save_file, "w") as f:
                f.write(json.dumps(self._map.get_canvas_state()))

    def save_file_prompt(self, filename=None):
        # filename exists as a parameter purely for unit testing around the UI
        if self._map:
            if not filename:
                filename = filedialog.asksaveasfilename()
            if filename:
                self._save_file = filename
                self.save_file()

    def close_file(self):
        if self._map:
            self._map.destroy()
            self._map = None
            self._save_file = None

            self.map_inactive()

    def add_plant(self):
        if self._map:
            self._map.add_plant()

    def list_plants(self):
        if not self._map:
            return

        state = self._map.get_plant_state()

        plant_window = PlantWindow(self._parent, state)

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
        self.h = ttk.Scrollbar(parent, orient=tk.HORIZONTAL)
        self.v = ttk.Scrollbar(parent, orient=tk.VERTICAL)
        super().__init__(
            parent,
            bg="white",
            scrollregion=(
                0,
                0,
                parent.winfo_screenwidth(),
                parent.winfo_screenheight(),
            ),
            yscrollcommand=self.v.set,
            xscrollcommand=self.h.set,
        )
        self.h["command"] = self.xview
        self.v["command"] = self.yview

        self.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
        self.columnconfigure(0, weight=1)
        self.h.grid(column=0, row=1, sticky=(tk.W, tk.E))
        self.v.grid(column=1, row=0, sticky=(tk.N, tk.S))

        # self.grid(fill=tk.BOTH, expand=True)

        self._background = None
        self._state = {}

    def add_plant(self, name=None, planted=None, x1=10, y1=10, x2=20, y2=20):
        widget = self.create_rectangle(
            x1, y1, x2, y2, outline="black", fill="green", width=2, tags=("plant")
        )

        plant = Plant(self, widget, name, planted)
        self.update_plant_state(plant)

    def update_plant_state(self, plant):
        x1, y1, x2, y2 = self.coords(plant.widget)

        self._state[plant.widget] = {
            "name": plant.name.get(),
            "planted": plant.planted.get(),
            "x1": x1,
            "y1": y1,
            "x2": x2,
            "y2": y2,
        }

    def update_background_state(self):
        background = self._background.data("png")
        b64_encoded_bg = base64.b64encode(background)
        b64_ascii_bg = b64_encoded_bg.decode("ascii")
        self._state["background"] = b64_ascii_bg

    def get_canvas_state(self):
        return self._state

    def get_plant_state(self):
        state = self.get_canvas_state()
        state.pop("background", None)

        return state

    def set_background(self, image):
        self._background = image

        self.config(
            scrollregion=(0, 0, self._background.width(), self._background.height()),
            yscrollcommand=self.v.set,
            xscrollcommand=self.h.set,
        )
        widget = self.create_image(
            0, 0, image=self._background, anchor="nw", tags=("background")
        )

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


class PlantWindow(tk.Toplevel):
    def __init__(self, parent, plant_state):
        super().__init__(parent)

        self.title("Plant List")
        self.columnconfigure(0, weight=1)

        name_column = 0
        planted_column = 2

        frame = ttk.Frame(self, padding=10, relief="ridge")
        frame.grid(column=0, row=0)

        name_label = ttk.Label(frame, text="Name:")
        name_label.grid(column=name_column, row=0, padx=50)

        planted_label = ttk.Label(frame, text="Planted:")
        planted_label.grid(column=planted_column, row=0, padx=50)

        s = ttk.Separator(frame, orient=tk.HORIZONTAL)
        s.grid(columnspan=3, row=1, column=0, sticky=(tk.W, tk.E))

        sv = ttk.Separator(frame, orient=tk.VERTICAL)
        sv.grid(rowspan=1000, row=0, column=1, sticky=(tk.N, tk.S))

        self.update_idletasks()
        self.minsize(frame.winfo_width(), 300)

        plant_row = 2

        for plant in plant_state.values():
            name_label = ttk.Label(frame, text=plant.get("name"))
            name_label.grid(column=name_column, row=plant_row)

            planted_label = ttk.Label(frame, text=plant.get("planted"))
            planted_label.grid(column=planted_column, row=plant_row)

            plant_row += 1
