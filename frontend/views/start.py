import multiprocessing
import sys
from tkinter import *

from playsound import playsound

from backend.complayer.omi_player import PlayerData
from frontend.ui import ui_config
from frontend.ui.ui_config import FONT, COLOR, COLOR2
from frontend.views import omi_message
from frontend.views.omi_message import MyMessage
from scripts.helper import image, SOUND_PATH, abs_path

player_data = PlayerData()
width = 770
height = 520
geo = str(width) + 'x' + str(height)
started = False

WINDOW = None


def exit_app():
    sys.exit()


def play_background_music():
    while True:
        print("Playing music")
        playsound(sound=SOUND_PATH + '/ForestWalk.mp3')


def clear_window():
    for child in WINDOW.winfo_children(): child.destroy()


class PlayGame:
    def __init__(self, parent, started=False):
        global musicProsses
        if started:
            musicProsses = multiprocessing.Process(target=play_background_music)
            musicProsses.daemon = True
            if int(player_data.get_value('music')) == 1:
                musicProsses.start()
        self.gui(parent)

    def gui(self, parent):
        if parent == 0:
            self.win_dialog = omi_message.MyMessage(0, size=geo, center='screen')
            self.w = self.win_dialog.win
            global WINDOW
            WINDOW = self.w
        else:
            if type(parent) == omi_message.MyMessage:
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
        print(abs_path('frontend/static/images/backgrounds/aces_gradiant_no_background.png'))
        self.img = image('backgrounds/aces_gradiant_no_background.png', 650, 360)
        self.imgLabel = Label(self.w, image=self.img, bg=COLOR)
        self.win_dialog.set_components([[self.label1], [self.imgLabel], [self.bottum]])
        self.bottum.grid(column=0, row=2, sticky='we', pady=10, padx=20)

    def play(self):
        clear_window()
        from frontend.views.play_board import PlayDesk
        a = PlayDesk(WINDOW)
        a.window.mainloop()

    def goto_settings(self):
        Settings(WINDOW)


def music():
    if check_music.get() == 1:
        player_data.update('music', 1)
        global musicProsses
        musicProsses = multiprocessing.Process(target=play_background_music)
        musicProsses.daemon = True
        musicProsses.start()
    else:
        player_data.update('music', 0)
        globals()['musicProsses'].terminate()


def sound():
    print(check_sound.get())
    if check_sound.get() == 1:
        player_data.update('sound', '1')
    else:
        player_data.update('sound', '0')


class Settings:
    def __init__(self, parent):
        self.img = None
        self.ok_btn = None
        self.sound = None
        self.music = None
        self.title = None
        self.win = None
        self.dialog = None
        self.parent = None
        self.fg = None
        self.bg = None
        self.height = None
        self.width = None
        self.gui(parent)

    def gui(self, parent):
        global check_sound, check_music
        check_music = IntVar()
        check_sound = IntVar()
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
        self.music = Checkbutton(self.win, text="Music", bg=self.bg, fg=self.fg, font=FONT, command=music,
                                 activebackground=COLOR, activeforeground='white', selectcolor=COLOR,
                                 variable=check_music, anchor='w')
        self.sound = Checkbutton(self.win, text="Sound", bg=self.bg, fg=self.fg, font=FONT, variable=check_sound,
                                 activebackground=COLOR, activeforeground='white', selectcolor=COLOR,
                                 command=sound, anchor='w')
        self.ok_btn = Button(self.win, font=font, command=self.ok, text='ok', bg=COLOR2, fg='white',
                             activebackground=COLOR,
                             activeforeground='white')
        self.img = image('backgrounds/domino.png', 380, 380)
        x = int(player_data.get_value('music'))
        if x == 1:
            self.music.select()
        elif x == 0:
            self.music.deselect()
        x = int(player_data.get_value('sound'))
        if x == 1:
            self.sound.select()
        elif x == 0:
            self.sound.deselect()
        self.dialog.set_components([[self.title], [self.music], [self.sound], [self.ok_btn]])
        self.title.grid(column=0, row=0, pady=10)
        self.ok_btn.grid(column=0, row=self.win.grid_size()[1] - 1, pady=10)

    def ok(self):
        self.dialog.hide()


if __name__ == '__main__':
    dilog = omi_message.MyMessage(0, size=geo, center='screen', onclose=exit_app, titlebar=ui_config.NAME)
    WINDOW = dilog.win
    PlayGame(dilog, True)
    WINDOW.mainloop()
