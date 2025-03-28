import multiprocessing
import threading
import time
from tkinter import *

from scripts import Helper
from backend.CardPack import width as cwidth, height as cheight
from scripts.Helper import image
from backend.NewGame import *
from frontend.views import OmmyMessage
from frontend.views.OmmyMessage import StatLabel, StatPanel, AskTrump
from frontend.ui.UiConfg import COLOR, FONT2
from frontend.ui.UiHelp import move_object

width = 1100
height = 680
geo = str(width) + 'x' + str(height)
imgcoin, imgxp = (0, 0)
tableimgs = [0, 0, 0, 0]
tablecards = [0, 0, 0, 0]
cardsimgs = {}
playerdata = PlayerData()
newGame = NewGame()


class PlayDesk:
    def __init__(self, parent):
        self.team1, self.team2 = (Score(), Score())
        self.gui(parent)

    def gui(self, parent):
        self.w = Tk() if parent == 0 else parent
        for c in self.w.winfo_children():
            c.destroy()
        self.w.geometry(geo)
        self.w.configure(background=COLOR)
        Helper.center(self.w)
        tw = (cwidth * 4) + 40
        th = height - cheight - 20
        global imgcoin, imgxp
        imgcoin = image("images/icons/coin.png", 30, 30)
        imgxp = image("images/icons/xp.png", 30, 30)
        imghints = image("images/icons/hints.png", 30, 30)
        self.w.update()
        self.collapseepanel = Frame(self.w)
        self.top = Frame(self.collapseepanel)
        self.myhand = LabelFrame(self.collapseepanel, bd=0, bg=COLOR)
        self.sidebar = LabelFrame(self.top)
        self.table = Canvas(self.top, bg=COLOR)
        self.statpanel = LabelFrame(self.top)
        self.topbar = LabelFrame(self.sidebar, bg=COLOR)
        self.topbar = LabelFrame(self.sidebar, bg=COLOR)

        self.coins = StatLabel(self.topbar, image=imgcoin, bg=COLOR, fg='white',
                               value=(playerdata.getvalue('coins')), valuefont=FONT2)
        self.xp = StatLabel(self.topbar, image=imgxp, bg=COLOR, fg='white', value=(playerdata.getvalue('xp')),
                            valuefont=FONT2)
        self.hint=Button(self.topbar,command=self.hints,bg=COLOR,text="hint")
        self.topbar.columnconfigure(0,weight=1)
        self.hint.grid(column=0, row=0, sticky='we')
        self.coins.grid(column=0, row=1, sticky='we')
        self.xp.grid(column=0, row=2, sticky='we')
        self.sidebar.columnconfigure(0, weight=1)
        self.topbar.grid(column=0, row=0, sticky='enw')
        row = 1
        self.label3 = Label(self.sidebar, text="Team stats", font=FONT2, anchor='w', fg=COLOR)
        self.label3.grid(column=0, row=row, padx=5, pady=2, sticky='we')
        row += 1
        self.label3 = Label(self.sidebar, text="Team 01", font=FONT2, anchor='w', fg=COLOR)
        self.label3.grid(column=0, row=row, padx=5, pady=2, sticky='we')
        row += 1
        self.wonlabel = StatLabel(self.sidebar, type='Won cards', value='0', float='|', valuefont=('Arial', 26, 'bold'))
        self.wonlabel.grid(column=0, row=row, padx=5, pady=2, sticky='we')
        row += 1
        self.winproblabel = StatLabel(self.sidebar, type='Win probability', value='0%')
        self.winproblabel.grid(column=0, row=row, padx=5, pady=2, sticky='we')
        row += 1
        self.label3 = Label(self.sidebar, text="Team 02", font=FONT2, anchor='w', fg=COLOR)
        self.label3.grid(column=0, row=row, padx=5, pady=2, sticky='we')
        row += 1
        self.wonlabel1 = StatLabel(self.sidebar, type='Won cards', value='0', float='|',
                                   valuefont=('Arial', 26, 'bold'))
        self.wonlabel1.grid(column=0, row=row, padx=5, pady=2, sticky='we')
        row += 1
        self.winproblabel1 = StatLabel(self.sidebar, type='Win probability', value='0%')
        self.winproblabel1.grid(column=0, row=row, padx=5, pady=2, sticky='we')
        row += 1
        self.label3 = Label(self.sidebar, text="Game stats", font=FONT2, anchor='w', fg=COLOR)
        self.label3.grid(column=0, row=row, padx=5, pady=2, sticky='we')
        row += 1
        self.roundslabel = StatLabel(self.sidebar, type='Rounds played', value='0')
        self.roundslabel.grid(column=0, row=row, padx=5, pady=2, sticky='we')
        row += 1
        self.drawlabel = StatLabel(self.sidebar, type='Draw rounds', value='0')
        self.drawlabel.grid(column=0, row=row, padx=5, pady=2, sticky='we')
        row += 1
        self.trumplabel = StatLabel(self.sidebar, type='Trump', value='Not started')
        self.trumplabel.grid(column=0, row=row, padx=5, pady=2, sticky='we')
        row += 1

        self.collapseepanel.columnconfigure(0, weight=1)
        self.collapseepanel.rowconfigure(0, weight=1, minsize=th)
        self.collapseepanel.columnconfigure(0, weight=1, minsize=(cwidth * 8) + 16)
        self.collapseepanel.rowconfigure(1, weight=1, minsize=cheight)
        self.top.columnconfigure(0, weight=1, minsize=200)
        self.top.columnconfigure(1, weight=1, minsize=tw)
        self.top.columnconfigure(2, weight=1)
        self.top.rowconfigure(0, weight=1, minsize=th)
        self.statpanel.columnconfigure(0, weight=1, minsize=200)
        self.top.grid(column=0, row=0, sticky='news')
        self.table.grid(column=1, row=0, sticky='news')
        self.collapseepanel.pack()
        self.statpanel.grid(column=2, row=0, sticky='news')
        self.myhand.grid(column=0, row=1)
        self.sidebar.grid(column=0, row=0, sticky='news')
        self.w.update()
        self.player1stat = StatPanel(self.statpanel)
        self.player1stat.update(1, "Player 01")
        self.player2stat = StatPanel(self.statpanel)
        self.player2stat.update(1, "Player 02")
        self.player3stat = StatPanel(self.statpanel)
        self.player3stat.update(2, "Your partner")
        self.playerYoustat = StatPanel(self.statpanel)
        self.playerYoustat.update(2, "You")
        self.w.update()
        self.player1stat.w.grid(column=0, row=1, padx=5, pady=5, sticky='ew')
        self.player2stat.w.grid(column=0, row=2, padx=5, pady=5, sticky='ew')
        self.player3stat.w.grid(column=0, row=3, padx=5, pady=5, sticky='ew')
        self.playerYoustat.w.grid(column=0, row=4, padx=5, pady=5, sticky='ew')
        self.c1, self.c2, self.c3, self.c4 = [[], [], [], []]
        self.updatecoords()
        self.w.update_idletasks()
        self.w.update()
        time.sleep(.5)
        self.start()

    def hints(self):
        msg= OmmyMessage.Hints(self.w, newGame.leftcards, newGame.playerYou, newGame.currentHand)
        msg.dlg.show()

    def start(self):
        newGame.suffle()
        threading.Thread(target=Helper.sufflecards())
        trumpcards = newGame.setTrump()
        if not trumpcards:
            OmmyMessage.ShowTrump(self.w, newGame.trump,
                                  f'{newGame.players()[newGame.trumpPly].name} chose trump as {newGame.trump}')
            self.addhand(newGame.playerYou.cards)
            tp = newGame.trumpPly
            newGame.firstplay = tp
            newGame.currentHand = CardPack.Hand(newGame.trump)
            card = newGame.players()[tp].getnext(newGame.currentHand)
            newGame.currentHand.setPlayerCard(tp, card)
            self.addcard(card, tp)
        else:
            newGame.firstplay = newGame.playerYou.id
            newGame.turn = newGame.firstplay
            AskTrump(self.w, trumpcards, self.trumpchoose)

    def updatecoords(self):
        self.table.update()
        tw = self.table.winfo_width()
        th = self.table.winfo_height()
        pad = 19
        self.c1 = [int(tw - cwidth - pad), int((th - cheight) / 2)]
        self.c2 = [int((tw - cwidth) / 2), int(pad)]
        self.c3 = [int(pad), int((th - cheight) / 2)]
        self.c4 = [int((tw - cwidth) / 2), int(th - cheight - pad)]

    def updatestats(self):
        self.player1stat.update(1, newGame.player1.name, newGame.player1.score, newGame.player1.trumptimes)
        self.player2stat.update(2, newGame.player2.name, newGame.player2.score, newGame.player2.trumptimes)
        self.player3stat.update(2, newGame.player3.name, newGame.player3.score, newGame.player3.trumptimes)
        self.playerYoustat.update(1, newGame.playerYou.name, newGame.playerYou.score,
                                  newGame.playerYou.trumptimes)
        self.wonlabel.setval(self.team1.score_10)
        self.wonlabel1.setval(self.team2.score_10)
        if self.team1.score_10 > self.team2.score_10:
            self.wonlabel.valueLabel.configure(fg='green', font=('Arial', 30, 'bold'))
            self.wonlabel1.valueLabel.configure(fg='red', font=('Arial', 26, 'bold'))
        elif self.team1.score_10 < self.team2.score_10:
            self.wonlabel1.valueLabel.configure(fg='green', font=('Arial', 30, 'bold'))
            self.wonlabel.valueLabel.configure(fg='red', font=('Arial', 26, 'bold'))
        else:
            self.wonlabel1.valueLabel.configure(fg=COLOR, font=('Arial', 24, 'bold'))
            self.wonlabel.valueLabel.configure(fg=COLOR, font=('Arial', 24, 'bold'))

        self.trumplabel.setval(f'{newGame.trump} by {newGame.players()[newGame.trumpPly].name}')
        self.roundslabel.setval(newGame.mainrounds)
        self.drawlabel.setval(newGame.drawrounds)
        if self.team1.score_10 > 0:
            self.winproblabel.setval(
                '{:.1f}%'.format(self.team1.wontimes / (newGame.tot_rounds_4) * 100))

        if self.team2.score_10 > 0:
            self.winproblabel1.setval(
                '{:.1f}%'.format(self.team2.wontimes / (newGame.mainrounds - newGame.drawrounds) * 100))

    def addhand(self, hand):
        for child in self.myhand.winfo_children():
            child.destroy()
        del globals()['cardsimgs']
        global cardsimgs
        cardsimgs = {}
        for main, v in hand.items():
            for c in v:
                card = CardPack.Card(main, c)
                cardsimgs[card] = card.getImage()
        i = 0
        threading.Thread(target=Helper.givecards()).start()
        for c1, im in cardsimgs.items():
            b1 = Button(self.myhand, image=im, bg='white', activebackground='white', activeforeground='white', bd=0)
            b1['command'] = lambda b=b1, c=c1: self.addcard_if(c, b)
            b1.pack(anchor=CENTER, side=LEFT)
            i += 1

    def addcard_if(self, card, b):
        player = newGame.playerYou.id
        if newGame.turn == player:
            if player != newGame.firstplay and card.m() != newGame.currentHand.main:
                if newGame.playerYou.havemain(newGame.currentHand.main):
                    print('Hand ', newGame.playerYou.cards)
                    from tkinter import messagebox
                    messagebox.askokcancel('Warning', 'Main card is ' + newGame.currentHand.main)
                    return
            print(f'Add if {card}')
            b.destroy()
            self.addcard(card, player)
        else:
            print('Dont you dare touch that this is player ', newGame.turn, ' s turn')
            return

    def trumpchoose(self, c):
        newGame.trump = c
        self.w.wm_attributes('-disable', False)
        time.sleep(.5)
        self.addhand(newGame.playerYou.cards)

    def addcard(self, card, player):
        self.updatestats()
        if player == newGame.firstplay:
            newGame.currentHand = CardPack.Hand(newGame.trump, card.m())
            print('\n\nHand is on me :', player)
        else:
            print('\nPlayer :', player)
        newGame.removecard(card)
        newGame.players()[player].removecard_(card)
        newGame.currentHand.setPlayerCard(player, card)
        self.updatecoords()
        self.table.update()
        coords = [self.c1, self.c2, self.c3, self.c4][player]
        tableimgs[player] = card.getImage()
        tablecards[player] = self.table.create_image(int(coords[0]), int(coords[1]), image=tableimgs[player], anchor=NW)
        self.table.update()
        multiprocessing.Process(target=Helper.putcard()).start()
        if newGame.rounds_4 == 3:
            time.sleep(1)
        self.passround_4(player)

    def passround_4(self, player):
        newGame.rounds_4 += 1
        newGame.tot_rounds_4 += 1
        newGame.turn = newGame.getNextRelPlayer(player)
        if newGame.rounds_4 == 4:
            newGame.rounds_4 = 0
            winner = newGame.currentHand.whogot()
            newGame.firstplay = int(winner)
            newGame.turn = newGame.firstplay
            if winner == 0 or winner == 2:
                self.team1.score_8 += 1
            else:
                self.team2.score_8 += 1
            newGame.players()[winner].score += 1
            threading.Thread(target=Helper.givecards).start()
            self.givehandtowinner(winner)
            self.table.after(400, self.passround_8)
            return
        elif not player == 2:
            p = newGame.getNextRelPlayer(player)
            card = newGame.players()[p].getnext(newGame.currentHand)
            self.addcard(card, p)

    def passround_8(self):
        newGame.rounds_8 += 1
        if newGame.rounds_8 == 8:
            if self.team1.score_8 >= 5:
                self.team1.score_10 += 3 if self.team1.score_8 == 8 else 2 if newGame.trumpPly not in [0, 2] else 1
                self.team1.wontimes += 1
            elif self.team1.score_8 == self.team2.score_8:
                newGame.drawrounds += 1
            else:
                self.team2.score_10 += 3 if self.team2.score_8 == 8 else 2 if newGame.trumpPly not in [1, 3] else 1
                self.team2.wontimes += 1
            if self.team1.score_10 >= 10:
                win = OmmyMessage.YouLose(self.w, newGame.playerYou.score,
                                          (self.team2.score_10 / newGame.mainrounds) * 100)
                win.dlg.show()
            elif self.team2.score_10 >= 10:
                win = OmmyMessage.YouWin(self.w, newGame.playerYou.score,
                                         (self.team2.score_10 / newGame.mainrounds) * 100)
                win.dlg.show()
            newGame.trumpPly = newGame.getNextRelPlayer(newGame.trumpPly)
            self.team1.score_8 = 0
            self.team2.score_8 = 0
            newGame.mainrounds += 1
            newGame.rounds_8 = 0
            newGame.rounds_4 = 0
            self.table.delete('all')
            print('\n' + ('*' * 100) + '\n' + 'NEW ROUND\n' + ('*' * 100) + '\n')
            self.updatestats()
            self.w.after(2000, self.start())
            return
        print('\n' + ('*' * 50) + '\n' + 'NEW HAND\n' + ('*' * 50) + '\n')
        self.table.update()
        self.w.update()
        newGame.currentHand = CardPack.Hand(newGame.trump)
        if not newGame.firstplay == 3:
            print(newGame.firstplay)
            self.addcard(newGame.players()[newGame.firstplay].getnext(newGame.currentHand),
                         newGame.firstplay)

    def givehandtowinner(self, winner):
        for card in tablecards:
            move_object(self.table, card, self.getcoords2()[winner], (3, 1), True)

    def getcoords2(self, player=None):
        self.updatecoords()
        hide = 200
        if player:
            return [(self.c1[0] + hide, self.c1[1]), (self.c2[0], self.c2[1] - hide), (self.c3[0] - hide, self.c3[1]),
                    (self.c4[0], self.c4[1] + 100)][player]
        else:
            return [(self.c1[0] + hide, self.c1[1]), (self.c2[0], self.c2[1] - hide), (self.c3[0] - hide, self.c3[1]),
                    (self.c4[0], self.c4[1] + hide)]

    def getcoords(self, player=None):
        self.updatecoords()
        if player:
            return [self.c1, self.c2, self.c3, self.c4][player]
        else:
            return [self.c1, self.c2, self.c3, self.c4]


if __name__ == '__main__':
    a = PlayDesk(0)
    a.w.wm_title("Ommy game")
    # a.w.resizable(False, False)
    a.w.mainloop()
