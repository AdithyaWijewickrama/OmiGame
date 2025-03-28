import tkinter as tk
import tkinter.font as font


class Dashboard:
    def __init__(self, parent):
        self.gui(parent)

    def gui(self, parent):
        if parent == 0:
            self.mainWidget = tk.Tk()  # Create the main window (only once)
            self.mainWidget.geometry('810x560')
        else:
            self.mainWidget = tk.Frame(parent)  # Create a frame inside the parent
            self.mainWidget.place(x=0, y=0, width=810, height=560)

        self.image1 = tk.Canvas(self.mainWidget, bg='white')
        self.image1.place(x=50, y=60, width=384, height=384)

        # Load the image and set it in the canvas
        self.img = tk.PhotoImage(file="../frontend/static/images/backgrounds/domino.png")
        self.image1.create_image(0, 0, image=self.img, anchor=tk.NW)


if __name__ == '__main__':
    # Creating the second widget window
    a = Dashboard(0)  # Passing 0 to create a root Tk instance
    a.mainWidget.mainloop()