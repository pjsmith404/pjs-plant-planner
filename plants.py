class Plant:
    def __init__(self, name, planted, icon, win):
        self.name = name
        self.planted = planted
        self._icon = icon
        self._win = win

    def _draw_plant(self, rectangle):
        self._icon.draw(rectangle)
