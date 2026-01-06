import sys
from multiprocessing import freeze_support

from frontend.ui import ui_config
from frontend.views import omi_message, start
from frontend.views.start import PlayGame

width = 770
height = 520
geo = str(width) + 'x' + str(height)


def exit_app():
    sys.exit()

def main():
    dilog = omi_message.MyMessage(0, size=geo, center='screen', onclose=exit_app, titlebar=ui_config.NAME)
    start.WINDOW = dilog.win
    PlayGame(dilog, True)
    start.WINDOW.mainloop()
    pass


if __name__ == '__main__':
    freeze_support()
    main()
