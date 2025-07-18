import os
import unittest
import tkinter as tk

from app import App, AppMenu, MapCanvas


class TestApp(unittest.TestCase):
    def test_app_config(self):
        app = App()
        self.assertEqual(app.title(), "PJ's Plant Planner")
        self.assertEqual(app.option_get("tearOff", "Tk"), "0")


class TestAppMenu(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.menubar = AppMenu(self.root)

    def tearDown(self):
        self.root.destroy()

    def test_app_menu_config(self):
        self.assertEqual(self.menubar._map, None)
        self.assertEqual(self.menubar._save_file, None)

        self.assertEqual(self.menubar.menu_file.entrycget("Save", "state"), "disabled")
        self.assertEqual(
            self.menubar.menu_file.entrycget("Save As...", "state"), "disabled"
        )
        self.assertEqual(self.menubar.menu_file.entrycget("Close", "state"), "disabled")
        self.assertEqual(
            self.menubar.menu_plants.entrycget("Add Plant", "state"), "disabled"
        )

    def test_new_file(self):
        self.menubar.new_file()

        self.assertEqual(self.menubar._save_file, None)
        self.assertIsInstance(self.menubar._map, tk.Canvas)

        self.assertEqual(self.menubar.menu_file.entrycget("Save", "state"), "normal")
        self.assertEqual(
            self.menubar.menu_file.entrycget("Save As...", "state"), "normal"
        )
        self.assertEqual(self.menubar.menu_file.entrycget("Close", "state"), "normal")
        self.assertEqual(
            self.menubar.menu_plants.entrycget("Add Plant", "state"), "normal"
        )

    def test_save_file(self):
        save_file = "./test_file"

        self.menubar.new_file()
        self.menubar._save_file = save_file
        self.menubar.save_file()

        with open(save_file, "r") as f:
            self.assertEqual(f.read(), "{}")

        os.remove(save_file)

    def test_save_file_no_map(self):
        save_file = "./test_file"

        self.menubar._save_file = save_file
        self.menubar.save_file()

        with self.assertRaises(FileNotFoundError):
            open(save_file, "r")

    def test_save_file_prompt(self):
        save_file = "./test_file"

        self.menubar.new_file()
        self.menubar.save_file_prompt(save_file)

        with open(save_file, "r") as f:
            self.assertEqual(f.read(), "{}")

        os.remove(save_file)

    def test_close_file(self):
        self.menubar.new_file()
        self.menubar.close_file()

        self.assertEqual(self.menubar._map, None)
        self.assertEqual(self.menubar._save_file, None)

        self.assertEqual(self.menubar.menu_file.entrycget("Save", "state"), "disabled")
        self.assertEqual(
            self.menubar.menu_file.entrycget("Save As...", "state"), "disabled"
        )
        self.assertEqual(self.menubar.menu_file.entrycget("Close", "state"), "disabled")
        self.assertEqual(
            self.menubar.menu_plants.entrycget("Add Plant", "state"), "disabled"
        )


class TestMapCanvas(unittest.TestCase):
    def test_config(self):
        root = tk.Tk()
        canvas = MapCanvas(root)

        self.assertEqual(canvas._background, None)
        self.assertEqual(canvas._state, {})

    def test_add_plant(self):
        root = tk.Tk()
        canvas = MapCanvas(root)

        test_state = {
            1: {
                "name": "1",
                "planted": "1",
                "x1": 10.0,
                "x2": 20.0,
                "y1": 10.0,
                "y2": 20.0,
            }
        }

        canvas.add_plant(name="1", planted="1")

        self.assertEqual(canvas.get_canvas_state(), test_state)


if __name__ == "__main__":
    unittest.main()
