import multiprocessing
from tkinter import *

from backend import NewGame
from scripts.Helper import image
from frontend.views import OmmyMessage
from frontend.views.OmmyMessage import MyMessage
from frontend.ui import UiConfg
from frontend.ui.UiConfg import FONT, COLOR, COLOR2

playerdata = NewGame.PlayerData()
width = 770
height = 520
geo = str(width) + 'x' + str(height)
started = False

import sys


def ext():
    sys.exit()


def playbackmusic():
    # while True:
    print("Playing music")
        # playsound(sound=SOUNDPATH + 'ForestWalk.mp3')


def clearwindow():
    for child in WINDOW.winfo_children(): child.destroy()


class PlayGame:
    def __init__(self, parent, started=False):
        global prosses
        if started:
            prosses = multiprocessing.Process(target=playbackmusic)
            prosses.daemon = True
            if int(playerdata.getvalue('music')) == 1:
                prosses.start()
        self.gui(parent)

    def gui(self, parent):
        if parent == 0:
            self.win_dialog = OmmyMessage.MyMessage(0, size=geo, center='scree')
            self.w = self.win_dialog.win
            global WINDOW
            WINDOW = self.w
        else:
            if type(parent) == OmmyMessage.MyMessage:
                self.win_dialog = parent
                self.w = parent.win
            else:
                self.w = Frame(parent)
                globals()['WINDOW'] = parent
        self.w.configure(bg=COLOR)

        self.label1 = Label(self.w, text="Ommy", font=('Arial', 40, 'bold'), bg=COLOR, fg='white')
        self.bottum = Frame(self.w, bg=COLOR)
        self.button1 = Button(self.bottum, text="Play", command=self.play, font=('Arial', 20, 'bold'), bg='white',
                              fg=COLOR)
        self.button2 = Button(self.bottum, text="Settings", command=self.goto_settings, font=('Arial', 20, 'bold'),
                              bg='white', fg=COLOR)
        self.button1.pack(side=RIGHT)
        self.button2.pack(side=LEFT)
        self.img = image("images/backgrounds/aces-2-gradiant.png", 650, 360)
        self.imgLabel = Label(self.w, image=self.img, bg=COLOR)
        self.win_dialog.setcomponents([[self.label1], [self.imgLabel], [self.bottum]])
        self.bottum.grid(column=0, row=2, sticky='we', pady=10, padx=20)

    def play(self):
        clearwindow()
        from frontend.views.PlayBoard import PlayDesk
        a = PlayDesk(WINDOW)
        a.w.mainloop()

    def goto_settings(self):
        Settings(WINDOW)


class Settings:
    def __init__(self, parent):
        self.gui(parent)

    def gui(self, parent):
        global checksound, checkmusic
        checkmusic = IntVar()
        checksound = IntVar()
        self.width = 300
        self.height = 280
        self.bg = COLOR
        self.fg = 'white'
        self.parent = parent if parent != 0 else Tk()
        self.dialog = MyMessage(self.parent, size=f'{self.width}x{self.height}', titlebar='', dialogtype='modal',
                                center='relative', bg=self.bg, resizable=False)
        self.win = self.dialog.win
        font = ('Arial', 15, 'normal')
        self.title = Label(self.win, text='Settings', bg=self.bg, fg=self.fg, font=font)
        self.music = Checkbutton(self.win, text="Music", bg=self.bg, fg=self.fg, font=FONT, command=self.music,
                                 activebackground=COLOR, activeforeground='white',selectcolor=COLOR,
                                 variable=checkmusic, anchor='w')
        self.sound = Checkbutton(self.win, text="Sound", bg=self.bg, fg=self.fg, font=FONT, variable=checksound,
                                 activebackground=COLOR, activeforeground='white',selectcolor=COLOR,
                                 command=self.sound, anchor='w')
        self.ok_btn = Button(self.win, font=font, command=self.ok, text='ok', bg=COLOR2, fg='white', activebackground=COLOR,
                             activeforeground='white')
        self.img = image("../static/images/backgrounds/domino.png", 380, 380)
        x = int(playerdata.getvalue('music'))
        if x == 1:
            self.music.select()
        elif x == 0:
            self.music.deselect()
        x = int(playerdata.getvalue('sound'))
        if x == 1:
            self.sound.select()
        elif x == 0:
            self.sound.deselect()
        self.dialog.setcomponents([[self.title], [self.music], [self.sound], [self.ok_btn]])
        self.title.grid(column=0, row=0, pady=10)
        self.ok_btn.grid(column=0, row=self.win.grid_size()[1] - 1, pady=10)

    def music(self):
        if checkmusic.get() == 1:
            playerdata.update('music', '1')
            global prosses
            prosses = multiprocessing.Process(target=playbackmusic)
            prosses.daemon = True
            prosses.start()
        else:
            playerdata.update('music', '0')
            globals()['t'].terminate()

    def sound(self):
        print(checksound.get())
        if checksound.get() == 1:
            playerdata.update('sound', '1')
        else:
            playerdata.update('sound', '0')

    def ok(self):
        self.dialog.hide()

    def save(self):
        clearwindow()
        PlayGame(WINDOW)


if __name__ == '__main__':
    dilog = OmmyMessage.MyMessage(0, size=geo, center='screen', onclose=ext, titlebar=UiConfg.NAME)
    WINDOW = dilog.win
    PlayGame(dilog, True)
    WINDOW.mainloop()
