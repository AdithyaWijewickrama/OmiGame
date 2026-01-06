import sys
import time
from functools import reduce
from pathlib import Path
from PIL import ImageTk, Image
from playsound3 import playsound


def image(file, w=0, h=0, a=0):
    img = Image.open(abs_path('frontend/static/images/' + file))
    if not (w == 0 or h == 0):
        img = img.resize((w, h), Image.Resampling.LANCZOS)
    return ImageTk.PhotoImage(img.rotate(a))


def center(win):
    win.update()
    sw = win.winfo_screenwidth()
    sh = win.winfo_screenheight()
    w = win.winfo_width()
    h = win.winfo_height()
    x = int((sw - w) / 2)
    y = int((sh - h) / 2)
    win.geometry(f"{w}x{h}+{x}+{y}")
    print(f"{w}x{h}+{x}+{y}")


def center_relative(win, parent):
    win.update()
    sw = parent.winfo_width()
    sh = parent.winfo_height()
    w = win.winfo_width()
    h = win.winfo_height()
    x = int(((sw - w) / 2) + parent.winfo_x())
    y = int(((sh - h) / 2) + parent.winfo_y())
    win.geometry(f"{w}x{h}+{x}+{y}")


def abs_path(file):
    """ Get absolute path of file """
    try:
        abs_pth = Path(sys._MEIPASS)
    except AttributeError:
        abs_pth = Path.cwd()
    return str((abs_pth / file).resolve())


def put_card(i: int = 1):
    from backend.complayer.omi_player import PlayerData
    if int(PlayerData().get_value('sound')) == 1:
        for k in range(i):
            try:
                print("Playing sound: Putting cards")
                playsound(SOUND_PATH + '/putcard.mp3')
            except Exception as e:
                print('[PLAY SONG EXP]', e)
                raise e
    else:
        time.sleep(1)


def shuffle_cards():
    from backend.complayer.omi_player import PlayerData
    if int(PlayerData().get_value('sound')) == 1:
        playsound(SOUND_PATH + '/shuffling-cards-1.wav')
    else:
        time.sleep(1)


def give_cards():
    from backend.complayer.omi_player import PlayerData
    if int(PlayerData().get_value('sound')) == 1:
        print("Playing sound: Giving cards")
        playsound(SOUND_PATH + '/shuffling-cards-6.wav')
    else:
        time.sleep(1)


def listinlist(l, lm):
    if len(l) == 0 or len(lm) == 0 and len(lm) == len(l):
        return 0 if l == lm else None
    elif len(lm) > len(l):
        for i in range(0, len(lm) - len(l) + 1):
            if lm[i:len(l) + i] == l:
                return i


def remove_sublist_from_list(main_list, sub_list=[]):
    for e in sub_list:
        main_list.remove(e)
    return main_list


def lcm(vals):
    r = reduce(lambda x, y: x * y, vals)
    r1 = reduce(lambda x, y: x + y, map(lambda x: r / x, vals))
    return r if (r1 % r) % 1 == 0 else r - (r1 % r)


IMAGE_PATH = abs_path('frontend/static/images/')
SOUND_PATH = abs_path('frontend/static/sounds/')
