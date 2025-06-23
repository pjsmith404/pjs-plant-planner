import unittest

from app import App

class Tests(unittest.TestCase):
    def test_base_app_config(self):
        app = App()
        self.assertEqual(app.title(), "PJ's Plant Planner")
        self.assertEqual(app.option_get("tearOff", "Tk"), "0")

if __name__ == "__main__":
    unittest.main()
