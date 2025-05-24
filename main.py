from graphics import Window, Point, Rectangle

def main():
    print("Running")

    width = 800
    height = 600

    win = Window(width, height)

    top_left = Point(100, 100)
    bottom_right = Point(200, 200)

    rectangle = Rectangle(top_left, bottom_right)
    win.draw_rectangle(rectangle)

    win.wait_for_close()

if __name__ == "__main__":
    main()
