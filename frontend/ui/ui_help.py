from tkinter import *


class Tooltip:
    def __init__(self, widget, text='widget info', waittime=500, wraplength=180):
        self.waittime = waittime  # miliseconds
        self.wraplength = wraplength  # pixels
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
        self.widget.bind("<ButtonPress>", self.leave)
        self.id = None
        self.tw = None

    def enter(self, event=None):
        self.schedule()

    def leave(self, event=None):
        self.unschedule()
        self.hidetip()

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(self.waittime, self.showtip)

    def unschedule(self):
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)

    def showtip(self, event=None):
        x = y = 0
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        self.tw = Toplevel(self.widget)
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        label = Label(self.tw, text=self.text, justify='left',
                      background="#ffffff", relief='solid', borderwidth=1,
                      wraplength=self.wraplength)
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tw
        self.tw = None
        if tw:
            tw.destroy()


def move_object(canvas, object_id, destination, v=(2, 10), delete=False):
    dest_x, dest_y = destination
    cords = canvas.coords(object_id)
    current_x = cords[0]
    current_y = cords[1]
    new_x, new_y = current_x, current_y
    delta_x, delta_y = (abs(abs(current_x) - abs(destination[0])), abs(abs(current_y) - abs(destination[1])))
    if delta_x > 2 or delta_y > 2:
        if current_x < dest_x:
            delta_x = v[0]
        elif current_x > dest_x:
            delta_x = -v[0]

        if current_y < dest_y:
            delta_y = v[0]
        elif current_y > dest_y:
            delta_y = -v[0]

        if (delta_x, delta_y) != (0, 0):
            canvas.move(object_id, delta_x, delta_y)

        if (new_x, new_y) != (dest_x, dest_y):
            canvas.after(v[1], move_object, canvas, object_id, destination, v)
    else:
        canvas.delete(object_id)
        canvas.update()
