import sys
from frontend.ui import UiConfg
from frontend.views import OmmyMessage, Start
from frontend.views.Start import PlayGame

width = 770
height = 520
geo = str(width) + 'x' + str(height)


def exitApp():
    sys.exit()


if __name__ == '__main__':
    dilog = OmmyMessage.MyMessage(0, size=geo, center='screen', onclose=exitApp, titlebar=UiConfg.NAME)
    Start.WINDOW = dilog.win
    PlayGame(dilog, True)
    Start.WINDOW.mainloop()
