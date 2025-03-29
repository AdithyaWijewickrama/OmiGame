import time
from functools import reduce
from tkinter import *
from tkinter import Label, Frame, CENTER, Button, messagebox as mbox, messagebox

from frontend.ui.ui_config import FONT, COLOR
from scripts import helper
from scripts.helper import image

card_width = 120
card_height = 180
trump_image_width = 100
trump_image_height = 100
hearts = 'icons/hearts.png'
clubs = 'icons/clubs.png'
spades = 'icons/spades.png'
diamonds = 'icons/diamonds.png'


def get_suit_image(card, width=trump_image_width, height=trump_image_height):
    from backend import card_pack
    return image([hearts, clubs, spades, diamonds][card_pack.SUITS.index(card)], width, height)


class MyMenu:
    def __init__(self, parent):
        self.parent = parent
        self.bar = Frame(parent, bg=COLOR)
        pading = 5
        self.close_btn = Button(self.bar, text='X', bg=COLOR, fg='white', command=self.close, bd=0,
                                font=('Arial', 10, 'bold'))
        self.close_btn.bind('<Enter>', self.close_btn_entered)
        self.close_btn.bind('<Leave>', self.close_btn_leave)
        self.close_btn.pack(side=RIGHT, anchor=CENTER, ipadx=pading, ipady=pading)
        self.minimize_btn = Button(self.bar, text='▢', bg=COLOR, fg='white', command=self.minimize, bd=0,
                                   font=('Arial', 20, 'bold'))
        self.minimize_btn.bind('<Enter>', self.minimize_btn_entered)
        self.minimize_btn.bind('<Leave>', self.minimize_btn_leave)
        self.minimize_btn.pack(side=RIGHT, anchor=CENTER)
        self.iconify_btn = Button(self.bar, text='_', bg=COLOR, fg='white', command=self.iconify, bd=0,
                                  font=('Arial', 10, 'bold'))
        self.iconify_btn.bind('<Enter>', self.iconify_btn_entered)
        self.iconify_btn.bind('<Leave>', self.iconify_btn_leave)
        self.iconify_btn.pack(side=RIGHT, anchor=CENTER, ipadx=pading, ipady=pading)
        self.bar.update()

    def iconify_btn_entered(self, e):
        c = self.iconify_btn
        c.configure(bg='white', fg=COLOR)
        c.update()

    def iconify_btn_leave(self, e):
        c = self.iconify_btn
        c.configure(bg=COLOR, fg='white')
        c.update()

    def close_btn_entered(self, e):
        c = self.close_btn
        c.configure(bg='white', fg=COLOR)
        c.update()

    def close_btn_leave(self, e):
        c = self.close_btn
        c.configure(bg=COLOR, fg='white')
        c.update()

    def minimize_btn_entered(self, e):
        c = self.minimize_btn
        c.configure(bg='white', fg=COLOR)
        c.update()

    def minimize_btn_leave(self, e):
        c = self.minimize_btn
        c.configure(bg=COLOR, fg='white')
        c.update()

    def close(self):
        self.parent.update()
        self.parent.destroy()

    def minimize(self):
        self.parent.wm_minsize(100, 100)

    def iconify(self):
        self.parent.wm_iconify()
        self.parent.update()


class MyMessage:
    def __init__(self, parent, **options):
        """
        Options:
        bg-background
        fg-foreground
        size(width,height)-geometry of the window
        dialogtype(modal,timeout,focuslost)-[timeout-disappear dialog after the given time],[modal-cannot get focus on p
        arent],[focuslost-hide when focuslost]
        resizable (bool)-can resize
        onclose(function)-execute when window closing
        :param parent:parent window
        :param options: dict:{}
        """
        self.ops = options
        global img
        self.bg = self.get_opt('bg') if self.get_opt('bg') else 'white'
        self.fg = self.get_opt('fg') if self.get_opt('fg') else 'black'
        self.parent = parent
        self.win = Toplevel(parent, bg=self.bg) if parent != 0 else Tk()
        if self.get_opt('size'):
            self.width = self.get_opt('size').split('x')[0]
            self.height = self.get_opt('size').split('x')[1]
            self.win.geometry(f'{int(self.width)}x{int(self.height)}')
        if parent != 0:
            if self.get_opt('dialogtype') == 'modal':
                self.parent.wm_attributes('-disable', True)
            elif self.get_opt('dialogtype') == 'focuslost':
                self.win.focus_set()
                self.win.bind('<FocusOut>', self.focus)
            if self.get_opt('center') == 'relative':
                helper.center_relative(self.win, self.parent)
        if self.get_opt('resizable') == False:
            self.win.resizable(False, False)
        if self.get_opt('titlebar') == False:
            self.win.overrideredirect(True)
        elif type(self.get_opt('titlebar')) == str:
            self.win.title(self.get_opt('titlebar'))
        if self.get_opt('center') == 'screen':
            helper.center(self.win)
        self.win.protocol('WM_DELETE_WINDOW', self.hide if not self.get_opt('onclose') else self.get_opt('onclose'))

    def focus(self, evt):
        self.hide()

    def set_components(self, comps):
        """
        add the components to the window
        :param comps: two dimensional list of widgets
        [row1:[],row2:[]...]
        :return:
        """
        self.win.update()
        self.win.focus_set()
        self.comps = comps
        for i in range(len(self.comps)):
            self.win.rowconfigure(i, weight=1)
        self.max_cols = 1
        for row in self.comps:
            if type(row) == list:
                self.max_cols = len(reduce(lambda x, y: x if len(x) > len(y) else y, self.comps))
                break
        lcm = 1
        for row in self.comps:
            lcm *= len(row)
        for col in range(lcm):
            self.win.columnconfigure(col, weight=1)
        rw = 0
        cl = 0
        for row in self.comps:
            if type(row) == list:
                col_span = int(lcm / len(row))
                for c in row:
                    try:
                        c.grid(column=cl, row=rw, columnspan=col_span)
                    except Exception as e:
                        print(e, ' \ncomponent:', c)
                        raise e
                    cl += col_span
            else:
                row.grid(column=cl, row=rw)
            rw += 1
            cl = 0
        self.win.focus_set()
        self.win.update()

    def remove_components(self):
        for child in self.win.winfo_children():
            child.destroy()

    def get_component(self, tag):
        if tag in list(self.comps.keys()):
            return self.ops[tag]

    def get_opt(self, tag):
        if tag in list(self.ops.keys()):
            return self.ops[tag]

    def show(self):
        if self.get_opt('timeout'):
            self.win.after(self.get_opt('timeout'), self.hide)
        self.win.focus_set()
        self.win.mainloop()

    def hide(self):
        self.win.withdraw()
        if self.parent != 0:
            self.parent.deiconify()
        if self.get_opt('dialogtype') == 'modal' and self.parent != 0:
            self.parent.wm_attributes('-disable', False)


class ShowSelectedTrump:
    def __init__(self, parent, trump_suit, title: str = ''):
        global img
        self.bg = 'white'
        self.fg = COLOR
        self.width = 200
        self.height = 170
        self.parent = parent
        self.win = MyMessage(parent, size=f'{self.width}x{self.height}', titlebar=False, dialogtype='modal',
                             center='relative', bg=self.bg, timeout=3000)
        img = get_suit_image(trump_suit)
        self.img_label = Label(self.win.win, image=img, bg=self.bg, fg=self.fg)
        self.trump_label = Label(self.win.win, bg=self.bg, fg=self.fg,
                                 text=f'Trump is {trump_suit}' if title == '' else title,
                                 font=FONT)
        self.win.set_components([[self.trump_label], [self.img_label],
                                 [Button(self.win.win, text='ok', bg=self.bg, fg=self.fg, command=self.win.hide,
                                         font=FONT)]])

    def show(self):
        self.win.show()


class StatLabel(Frame):
    def __init__(self, parent, dimention=(300, 25), float='-', value='', type='', image='', bg='white', fg='black',
                 valuefont=FONT, typefont=('Arial', 10, 'bold')):
        super().__init__(parent, height=dimention[1], bg=bg, bd=0)
        self.float = float
        self.imageLabel = Label(self, image=image, anchor='w', bg=bg)
        self.typeLabel = Label(self, text=type, anchor='w', font=typefont, bg=bg, fg=fg)
        self.valueLabel = Label(self, text=value, anchor='w', font=valuefont, bg=bg, fg=fg)
        if float == '-':
            r = 0
            if image != '':
                self.columnconfigure(r, weight=1)
                self.imageLabel.grid(column=0, row=0, sticky='ew')
                r += 1
            self.columnconfigure(r, weight=1)
            self.typeLabel.grid(column=r, row=0, sticky='ew')
            r += 1
            self.columnconfigure(r, weight=1)
            self.valueLabel.grid(column=r, row=0, sticky='ew')
            self.rowconfigure(0, weight=1)
        if float == '|':
            r = 0
            if image != '':
                self.imageLabel.grid(column=0, row=0, sticky='ew')
                self.rowconfigure(0, weight=1)
                r += 1
            self.typeLabel.grid(column=0, row=r, sticky='ew')
            self.rowconfigure(r, weight=1)
            r += 1
            self.valueLabel.grid(column=0, row=r, sticky='ew')
            self.rowconfigure(r, weight=1)
            self.columnconfigure(0, weight=1)

    def settype(self, type):
        self.typeLabel['text'] = str(type)

    def setval(self, val):
        self.valueLabel['text'] = str(val)

    def setimage(self, img):
        self.imageLabel['image'] = img


class StatPanel:
    def __init__(self, parent):
        self.gui(parent)

    def gui(self, parent, teamname=0, playername="Player", wontimes=0, trumptimes=0):
        if parent == 0:
            return
        else:
            self.labelwidth = 100
            self.w = Frame(parent, highlightbackground=COLOR, highlightthickness=2, bg='white')
        self.teamname = StatLabel(self.w, value=str(teamname), type='Team No:')
        self.teamname.pack(anchor=CENTER, padx=5)
        self.playername = StatLabel(self.w, value=str(playername), type='Player name')
        self.playername.pack(anchor=CENTER, padx=5)
        self.wontimes = StatLabel(self.w, value=str(wontimes), type='Won hands')
        self.wontimes.pack(anchor=CENTER, padx=5)
        self.trumptimes = StatLabel(self.w, value=str(trumptimes), type='No. of trumps')
        self.trumptimes.pack(anchor=CENTER, padx=5)

    def update(self, teamname=0, playername="Player", wontimes=0, trumptimes=0):
        self.teamname.setval(teamname)
        self.playername.setval(playername)
        self.wontimes.setval(wontimes)
        self.trumptimes.setval(trumptimes)

    def grid(self, cnf):
        self.w.grid(cnf)


class AskTrump:
    def __init__(self, parent, trump_cards, func):
        self.func = func
        self.parent = parent
        self.dlg = MyMessage(parent, size=f'{int(card_width * 4)}x{int((card_height * 2) + (card_width / 2))}',
                             onclose=self.closing, dialogtype='modal', titlebar='You are to say trump',
                             center='relative', resizable=False)
        self.mainCard = ''
        self.suit_buttons = []
        self.card_labels = []
        self.card_images = []
        self.suit_set = set()
        for card in trump_cards:
            self.img = card.get_image_for_card()
            self.card_images.append(self.img)
            self.suit_set.add(card.get_suit())

        for card_img in self.card_images:
            self.card_labels.append(Label(self.dlg.win, image=card_img))

        self.suit_cards = []
        for mc in self.suit_set:
            self.suit_cards.append(get_suit_image(mc, int(card_width / 2), int(card_width / 2)))
        for m0, m1 in zip(self.suit_set, self.suit_cards):
            image_button = Button(self.dlg.win, image=m1, command=(lambda mc0=m0: self.choose(mc0)))
            self.suit_buttons.append(image_button)

        self.dlg.set_components(
            [[self.card_labels[0], self.card_labels[1], self.card_labels[2], self.card_labels[3]], self.suit_buttons])

    def closing(self):
        a = mbox.askyesnocancel('Warning', 'Are you want to quit the game\nPress No to quit to main menu')
        if a is not None:
            if a:
                exit()
            else:
                self.dlg.hide()
                self.parent.destroy()
                from frontend.views import start
                start.PlayGame(0)
        else:
            self.dlg.win.attributes('-topmost', True)
            self.dlg.win.attributes('-topmost', False)

    def choose(self, c):
        self.dlg.win.withdraw()
        self.parent.deiconify()
        self.parent.wm_attributes('-disable', False)
        if self.func is None:
            print('Trump is ' + c)
        else:
            self.func(c)


class Hints:

    def __init__(self, parent, left_cards, player, hand):
        self.cards1 = None
        self.cards2 = None
        self.card = None
        self.ok = None
        self.left_cards = left_cards
        self.player = player
        self.hand = hand
        self.parent = parent
        self.dlg = MyMessage(parent, size=f'{int(card_width * 4)}x{int((card_height * 2) + (card_width / 2))}',
                             dialogtype='modal', titlebar='You are to say trump',
                             center='relative', resizable=False)

        self.b1 = Button(self.dlg.win, text='Next card', command=self.next_card)
        self.b2 = Button(self.dlg.win, text='Left cards', command=self.left_cards)
        self.cancel = Button(self.dlg.win, text='Cancel', command=self.dlg.hide)

        self.dlg.set_components([[self.b1], [self.b2], [self.cancel]])

    def left_cards(self):
        from backend.complayer.omi_player import PlayerData
        coins = int(PlayerData().get_value('coins'))
        if coins >= 150:
            global cards
            self.cards1 = []
            self.cards2 = []
            for m, c in self.left_cards.items():
                self.cards1 = []
                if len(self.left_cards[m]) > 0:
                    for c1 in c:
                        self.cards1.append(Label(self.dlg.win, image=Card(m, c1).get_image_for_card()))
                    self.cards2.append(self.cards1)
            self.ok = Button(self.dlg.win, text='Ok', command=self.dlg.hide)
            self.dlg.remove_components()
            self.cards2.append(self.ok)
            self.dlg.set_components(self.cards2)
            PlayerData().update('coins', coins - 150)
        else:
            messagebox.showerror('Error', 'You have no enough coins')

    def next_card(self):
        from backend.complayer.omi_player import PlayerData
        coins = int(PlayerData().get_value('coins'))
        if coins >= 150:
            self.card = self.player.get_next(self.hand)
            self.ok = Button(self.dlg.win, text='Ok', command=self.dlg.hide)
            self.dlg.remove_components()
            self.dlg.win.update()
            self.dlg.set_components([[Label(self.dlg.win, image=self.card.get_image_for_card())], [self.ok]])
            PlayerData().update('coins', coins - 150)
        else:
            messagebox.showerror('Error', 'You have no enough coins')


class YouWin:

    def __init__(self, parent, xp, coins):
        from backend.complayer.omi_player import PlayerData
        self.parent = parent
        self.player_data = PlayerData()
        self._xp = xp
        self._coins = coins
        self.dlg = MyMessage(parent, size=f'{int(card_width * 4)}x{int((card_height * 2) + (card_width / 2))}',
                             dialogtype='modal', titlebar=False,
                             center='relative', resizable=False)
        self.bar = MyMenu(self.dlg.win)
        self.dlg.win.configure(bg=COLOR)
        f1 = 50
        f2 = 14
        img_r = 30
        self.img = image('icons/coin.png', img_r, img_r)
        self.img1 = image('icons/xp.png', img_r, img_r)
        self.win_label = Label(self.dlg.win, text="YOU WIN", font=('Arial', f1, 'bold'), bg=COLOR, fg='white')
        self.coins = StatLabel(self.dlg.win, float='-', value=self.player_data.get_value('coins'), type='Coins gained',
                               image=self.img, typefont=('Arial', f2, 'bold'),
                               valuefont=('Arial', f2, 'bold'), bg=COLOR, fg='white')
        self.xp = StatLabel(self.dlg.win, float='-', value=self.player_data.get_value('xp'), type='XP gained',
                            image=self.img1, typefont=('Arial', f2, 'bold'),
                            valuefont=('Arial', f2, 'bold'), bg=COLOR, fg='white')
        self.menu = Button(self.dlg.win, text='Main menu', bg='white', fg=COLOR, font=('Arial', f2, 'bold'),
                           command=self.main_menu)
        self.play_again = Button(self.dlg.win, text='Play again', bg='white', fg=COLOR, font=('Arial', f2, 'bold'),
                                 command=self.playa_gain)
        self.bar.minimize_btn.destroy()
        self.dlg.set_components([[self.win_label], [self.coins], [self.xp], [self.menu, self.play_again]])
        self.dlg.win.rowconfigure(0, weight=1)
        self.dlg.win.rowconfigure(1, weight=1)
        self.dlg.win.rowconfigure(2, weight=1)
        self.dlg.win.rowconfigure(3, weight=1)
        self.bar.bar.grid(column=0, row=0, columnspan=self.dlg.win.grid_size()[0], sticky='wen')
        self.player_data.update('coins', int(self.player_data.get_value('coins')) + coins)
        self.player_data.update('xp', int(self.player_data.get_value('xp')) + xp)
        self.dlg.win.after(1000, self.add_xp)
        self.dlg.win.after(1000, self.add_coins)

    def main_menu(self):
        self.dlg.hide()
        from frontend.views.start import PlayGame
        PlayGame(parent=self.parent)

    def playa_gain(self):
        self.dlg.hide()
        from frontend.views.play_board import PlayDesk
        PlayDesk(self.parent)

    def add_xp(self, amount: int):
        for i in range(self._xp):
            self.xp.valueLabel['text'] = str(int(self.xp.valueLabel['text']) + amount)
            self.xp.valueLabel.update()
            time.sleep(.0001)

    def add_coins(self, amount: int):
        for i in range(self._coins):
            self.coins.valueLabel['text'] = str(int(self.coins.valueLabel['text']) + amount)
            self.coins.valueLabel.update()
            time.sleep(.0001)


class YouLose:
    def __init__(self, parent, xp, coins):
        from backend.complayer.omi_player import PlayerData
        self.parent = parent
        self.player_data = PlayerData()
        self._xp = xp
        self._coins = coins
        self.dlg = MyMessage(parent, size=f'{int(card_width * 4)}x{int((card_height * 2) + (card_width / 2))}',
                             dialogtype='modal', titlebar=False,
                             center='relative', resizable=False)
        self.bar = MyMenu(self.dlg.win)
        self.dlg.win.configure(bg=COLOR)
        f1 = 50
        f2 = 14
        img_r = 30
        self.img = image('icons/coin.png', img_r, img_r)
        self.img1 = image('icons/xp.png', img_r, img_r)
        self.win_label = Label(self.dlg.win, text="YOU LOSE", font=('Arial', f1, 'bold'), bg=COLOR, fg='white')
        self.coins = StatLabel(self.dlg.win, float='-', value=self.player_data.get_value('coins'), type='Coins lost',
                               image=self.img, typefont=('Arial', f2, 'bold'),
                               valuefont=('Arial', f2, 'bold'), bg=COLOR, fg='white')
        self.xp = StatLabel(self.dlg.win, float='-', value=self.player_data.get_value('xp'), type='XP lost',
                            image=self.img1, typefont=('Arial', f2, 'bold'),
                            valuefont=('Arial', f2, 'bold'), bg=COLOR, fg='white')
        self.menu = Button(self.dlg.win, text='Main menu', bg='white', fg=COLOR, font=('Arial', f2, 'bold'),
                           command=self.main_menu)
        self.playa_gain = Button(self.dlg.win, text='Retry', bg='white', fg=COLOR, font=('Arial', f2, 'bold'),
                                 command=self.play_again)
        self.bar.minimize_btn.destroy()
        self.dlg.set_components([[self.win_label], [self.coins], [self.xp], [self.menu, self.playa_gain]])
        self.dlg.win.rowconfigure(0, weight=1)
        self.dlg.win.rowconfigure(1, weight=1)
        self.dlg.win.rowconfigure(2, weight=1)
        self.dlg.win.rowconfigure(3, weight=1)
        self.bar.bar.grid(column=0, row=0, columnspan=self.dlg.win.grid_size()[0], sticky='wen')
        self.player_data.update('coins', int(self.player_data.get_value('coins')) + coins)
        self.player_data.update('xp', int(self.player_data.get_value('xp')) + xp)
        self.dlg.win.after(1000, self.dec_xp)
        self.dlg.win.after(1000, self.dec_coins)

    def main_menu(self):
        self.dlg.hide()
        from frontend.views.start import PlayGame
        PlayGame(parent=self.parent)

    def play_again(self):
        self.dlg.hide()
        from frontend.views.play_board import PlayDesk
        PlayDesk(self.parent)

    def dec_xp(self):
        for i in range(self._xp):
            self.xp.valueLabel['text'] = str(int(self.xp.valueLabel['text']) - 1)
            self.xp.valueLabel.update()
            time.sleep(.0001)

    def dec_coins(self):
        for i in range(self._coins):
            self.coins.valueLabel['text'] = str(int(self.coins.valueLabel['text']) - 1)
            self.coins.valueLabel.update()
            time.sleep(.0001)


if __name__ == '__main__':
    from backend.card_pack import Card, width as card_width, height as card_height


    def test_show_trump():
        t = ShowSelectedTrump(w, 'clubs')
        t.show()


    def test_ask_trump():
        cards = [Card('hearts', '7'), Card('clubs', '7'), Card('diamonds', '7'), Card('spades', '7')]
        AskTrump(w, cards, None)


    def test_you_win():
        y = YouWin(w, 100, 100)
        y.dlg.show()


    def test_menu():
        m = MyMenu(w)
        w.columnconfigure(0, weight=1)
        m.bar.grid(column=0, row=0, columnspan=5, sticky='ew')


    wd = 400
    he = 400
    w = Tk()
    w.geometry(f'{wd}x{he}+{int((w.winfo_screenwidth() - wd) / 2)}+{int((w.winfo_screenheight() - he) / 2)}')
    Button(w, command=test_show_trump, text='testShowtrump').grid()
    Button(w, command=test_ask_trump, text='testasktrump').grid()
    Button(w, command=test_you_win, text='testyouwin').grid()
    Button(w, command=test_menu, text='menu').grid()
    w.mainloop()
