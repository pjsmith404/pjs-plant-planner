from graphics import Window, Point, Rectangle, Icon
from plants import Plant

def main():
    print("Running")

    width = 800
    height = 600

    win = Window(width, height)

    top_left = Point(10, 10)
    bottom_right = Point(20, 20)

    rectangle = Rectangle(top_left, bottom_right)
    icon = Icon(win)
    plant = Plant("Test", "2025-01-01", icon, win)
    plant._draw_plant(rectangle)
    
    top_left2 = Point(40, 40)
    bottom_right2 = Point(50, 50)

    rectangle2 = Rectangle(top_left2, bottom_right2)
    icon2 = Icon(win)
    plant2 = Plant("Test", "2025-01-01", icon2, win)
    plant2._draw_plant(rectangle2)

    win.run()

if __name__ == "__main__":
    main()
