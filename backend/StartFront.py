import tkinter as tk
import tkinter.font as font

class Widget1:
    def __init__(self, parent):
        self.gui(parent)

    def gui(self, parent):
        if parent == 0:
            self.w1 = tk.Tk()  # Create the main window (only once)
            self.w1.geometry('810x560')
        else:
            self.w1 = tk.Frame(parent)  # Create a frame inside the parent
            self.w1.place(x=0, y=0, width=810, height=560)

        self.image1 = tk.Canvas(self.w1, bg='white')
        self.image1.place(x=50, y=60, width=384, height=384)

        # Load the image and set it in the canvas
        self.img = tk.PhotoImage(file="../frontend/static/images/backgrounds/domino.png")
        self.image1.create_image(0, 0, image=self.img, anchor=tk.NW)

    def rt(self):
        print('rt')

    def fgf(self):
        print('fgf')


class Widget2:
    def __init__(self, parent):
        self.gui(parent)

    def gui(self, parent):
        if parent == 0:
            self.w1 = tk.Tk()  # Only create the root window once
            self.w1.geometry('500x450')
        else:
            self.w1 = tk.Frame(parent)  # Create frame inside parent
            self.w1.place(x=0, y=0, width=500, height=450)

        # Create a Spinbox widget with specific font
        self.spin1 = tk.Spinbox(self.w1, from_=0, to=100, increment=1,
                                value=0, font=font.Font(family="MS Shell Dlg 2", size=8),
                                cursor="arrow", state="normal")
        self.spin1.place(x=220, y=120, width=40, height=22)


if __name__ == '__main__':
    # Creating the second widget window
    a = Widget1(0)  # Passing 0 to create a root Tk instance
    a.w1.mainloop()