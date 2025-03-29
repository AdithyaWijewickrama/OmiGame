import multiprocessing
import threading
import time
from tkinter import *

from backend.card_pack import width as card_width, height as card_height
from backend.complayer.omi_game import *
from backend.complayer.omi_player import PlayerData
from frontend.ui.ui_config import COLOR, FONT2
from frontend.ui.ui_help import move_object
from frontend.views.omi_message import StatLabel, StatPanel, AskTrump, Hints, ShowSelectedTrump, YouLose, YouWin
from scripts import helper
from scripts.helper import image

width = 1100
height = 680
geo = str(width) + 'x' + str(height)
img_coin, img_xp, img_hints = (None, None, None)
table_images = [None, None, None, None]
table_cards = [None, None, None, None]
card_images = {}
player_data = PlayerData()
new_game = OmiGame()


class PlayDesk:
    def __init__(self, parent):
        self.player_you_stat = None
        self.trump_suit_label = None
        self.rounds_count_label = None
        self.draw_count_label = None
        self.label3 = None
        self.win_probability_1 = None
        self.won_label1 = None
        self.win_probability = None
        self.top_bar = None
        self.stat_panel = None
        self.table = None
        self.my_hand = None
        self.top = None
        self.collapse_panel = None
        self.sidebar = None
        self.xp = None
        self.hint = None
        self.coins = None
        self.won_label = None
        self.c1, self.c2, self.c3, self.c4 = [[], [], [], []]
        self.window = None
        self.player1stat, self.player2stat, self.player3stat, self.player4stat = (None, None, None, None)
        self.team1, self.team2 = (Score(), Score())
        self.gui(parent)

    def gui(self, parent):
        self.window = parent if parent else Tk()
        for c in self.window.winfo_children():
            c.destroy()
        self.window.geometry(geo)
        self.window.configure(background=COLOR)
        helper.center(self.window)
        tw = (card_width * 4) + 40
        th = height - card_height - 20
        global img_coin, img_xp, img_hints
        img_coin = image("icons/coin.png", 30, 30)
        img_xp = image("icons/xp.png", 30, 30)
        img_hints = image("icons/hints.png", 30, 30)
        self.window.update()
        self.collapse_panel = Frame(self.window)
        self.top = Frame(self.collapse_panel)
        self.my_hand = LabelFrame(self.collapse_panel, bd=0, bg=COLOR)
        self.sidebar = LabelFrame(self.top)
        self.table = Canvas(self.top, bg=COLOR)
        self.stat_panel = LabelFrame(self.top)
        self.top_bar = LabelFrame(self.sidebar, bg=COLOR)

        self.coins = StatLabel(self.top_bar, image=img_coin, bg=COLOR, fg='white',
                               value=(player_data.get_value('coins')), valuefont=FONT2)
        self.xp = StatLabel(self.top_bar, image=img_xp, bg=COLOR, fg='white', value=(player_data.get_value('xp')),
                            valuefont=FONT2)
        self.hint = Button(self.top_bar, command=self.hints, bg=COLOR, fg='white', text="Hint", image=img_hints)
        self.top_bar.columnconfigure(0, weight=1)
        self.hint.grid(column=0, row=0, sticky='we')
        self.coins.grid(column=0, row=1, sticky='we')
        self.xp.grid(column=0, row=2, sticky='we')
        self.sidebar.columnconfigure(0, weight=1)
        self.top_bar.grid(column=0, row=0, sticky='enw')
        row = 1
        self.label3 = Label(self.sidebar, text="Team stats", font=FONT2, anchor='w', fg=COLOR)
        self.label3.grid(column=0, row=row, padx=5, pady=2, sticky='we')
        row += 1
        self.label3 = Label(self.sidebar, text="Opponents team", font=FONT2, anchor='w', fg=COLOR)
        self.label3.grid(column=0, row=row, padx=5, pady=2, sticky='we')
        row += 1
        self.won_label = StatLabel(self.sidebar, type='Won cards', value='0', float='|',
                                   valuefont=('Arial', 26, 'bold'))
        self.won_label.grid(column=0, row=row, padx=5, pady=2, sticky='we')
        row += 1
        self.win_probability = StatLabel(self.sidebar, type='Win probability', value='0%')
        self.win_probability.grid(column=0, row=row, padx=5, pady=2, sticky='we')
        row += 1
        self.label3 = Label(self.sidebar, text="Your team", font=FONT2, anchor='w', fg=COLOR)
        self.label3.grid(column=0, row=row, padx=5, pady=2, sticky='we')
        row += 1
        self.won_label1 = StatLabel(self.sidebar, type='Won cards', value='0', float='|',
                                    valuefont=('Arial', 26, 'bold'))
        self.won_label1.grid(column=0, row=row, padx=5, pady=2, sticky='we')
        row += 1
        self.win_probability_1 = StatLabel(self.sidebar, type='Win probability', value='0%')
        self.win_probability_1.grid(column=0, row=row, padx=5, pady=2, sticky='we')
        row += 1
        self.label3 = Label(self.sidebar, text="Game stats", font=FONT2, anchor='w', fg=COLOR)
        self.label3.grid(column=0, row=row, padx=5, pady=2, sticky='we')
        row += 1
        self.rounds_count_label = StatLabel(self.sidebar, type='Rounds played', value='0')
        self.rounds_count_label.grid(column=0, row=row, padx=5, pady=2, sticky='we')
        row += 1
        self.draw_count_label = StatLabel(self.sidebar, type='Draw rounds', value='0')
        self.draw_count_label.grid(column=0, row=row, padx=5, pady=2, sticky='we')
        row += 1
        self.trump_suit_label = StatLabel(self.sidebar, type='Trump', value='Not started')
        self.trump_suit_label.grid(column=0, row=row, padx=5, pady=2, sticky='we')
        row += 1

        self.collapse_panel.columnconfigure(0, weight=1)
        self.collapse_panel.rowconfigure(0, weight=1, minsize=th)
        self.collapse_panel.columnconfigure(0, weight=1, minsize=(card_width * 8) + 16)
        self.collapse_panel.rowconfigure(1, weight=1, minsize=card_height)
        self.top.columnconfigure(0, weight=1, minsize=200)
        self.top.columnconfigure(1, weight=1, minsize=tw)
        self.top.columnconfigure(2, weight=1)
        self.top.rowconfigure(0, weight=1, minsize=th)
        self.stat_panel.columnconfigure(0, weight=1, minsize=200)
        self.top.grid(column=0, row=0, sticky='news')
        self.table.grid(column=1, row=0, sticky='news')
        self.collapse_panel.pack()
        self.stat_panel.grid(column=2, row=0, sticky='news')
        self.my_hand.grid(column=0, row=1)
        self.sidebar.grid(column=0, row=0, sticky='news')
        self.window.update()
        self.player1stat = StatPanel(self.stat_panel)
        self.player1stat.update(1, "Player 01")
        self.player2stat = StatPanel(self.stat_panel)
        self.player2stat.update(1, "Player 02")
        self.player3stat = StatPanel(self.stat_panel)
        self.player3stat.update(2, "Your partner")
        self.player_you_stat = StatPanel(self.stat_panel)
        self.player_you_stat.update(2, "You")
        self.window.update()
        self.player1stat.w.grid(column=0, row=1, padx=5, pady=5, sticky='ew')
        self.player2stat.w.grid(column=0, row=2, padx=5, pady=5, sticky='ew')
        self.player3stat.w.grid(column=0, row=3, padx=5, pady=5, sticky='ew')
        self.player_you_stat.w.grid(column=0, row=4, padx=5, pady=5, sticky='ew')
        self.update_coordinates()
        self.window.update_idletasks()
        self.window.update()
        time.sleep(.5)
        self.start()

    def hints(self):
        msg = Hints(self.window, new_game.left_cards, new_game.player_you, new_game.current_hand)
        msg.dlg.show()

    def start(self):
        new_game.shuffle()
        threading.Thread(target=helper.shuffle_cards())
        trump_cards = new_game.get_trump_cards()
        if not trump_cards:
            ShowSelectedTrump(self.window, new_game.trump_suit,
                      f'{new_game.players()[new_game.trump_suit_call_player].name} chose trump as {new_game.trump_suit}')
            self.add_hand(new_game.player_you.cards)
            tp = new_game.trump_suit_call_player
            new_game.first_play = tp
            new_game.current_hand = card_pack.Hand(new_game.trump_suit)
            card = new_game.players()[tp].get_next(new_game.current_hand)
            new_game.current_hand.set_player_card(tp, card)
            self.add_card(card, tp)
        else:
            new_game.first_play = new_game.player_you.id
            new_game.turn = new_game.first_play
            AskTrump(self.window, trump_cards, self.trump_chosen)

    def update_coordinates(self):
        self.table.update()
        tw = self.table.winfo_width()
        th = self.table.winfo_height()
        pad = 19
        self.c1 = [int(tw - card_width - pad), int((th - card_height) / 2)]
        self.c2 = [int((tw - card_width) / 2), int(pad)]
        self.c3 = [int(pad), int((th - card_height) / 2)]
        self.c4 = [int((tw - card_width) / 2), int(th - card_height - pad)]

    def update_stats(self):
        self.player1stat.update(1, new_game.player1.name, new_game.player1.score, new_game.player1.trump_times)
        self.player2stat.update(2, new_game.player2.name, new_game.player2.score, new_game.player2.trump_times)
        self.player3stat.update(2, new_game.player3.name, new_game.player3.score, new_game.player3.trump_times)
        self.player_you_stat.update(1, new_game.player_you.name, new_game.player_you.score,
                                    new_game.player_you.trump_times)
        self.won_label.setval(self.team1.score_10)
        self.won_label1.setval(self.team2.score_10)
        if self.team1.score_10 > self.team2.score_10:
            self.won_label.valueLabel.configure(fg='green', font=('Arial', 30, 'bold'))
            self.won_label1.valueLabel.configure(fg='red', font=('Arial', 26, 'bold'))
        elif self.team1.score_10 < self.team2.score_10:
            self.won_label1.valueLabel.configure(fg='green', font=('Arial', 30, 'bold'))
            self.won_label.valueLabel.configure(fg='red', font=('Arial', 26, 'bold'))
        else:
            self.won_label1.valueLabel.configure(fg=COLOR, font=('Arial', 24, 'bold'))
            self.won_label.valueLabel.configure(fg=COLOR, font=('Arial', 24, 'bold'))

        self.trump_suit_label.setval(
            f'{new_game.trump_suit} by {new_game.players()[new_game.trump_suit_call_player].name}')
        self.rounds_count_label.setval(new_game.main_rounds)
        self.draw_count_label.setval(new_game.draw_rounds)
        if self.team1.score_10 > 0:
            self.win_probability.setval(
                '{:.1f}%'.format(self.team1.times_won / (new_game.main_rounds - new_game.draw_rounds) * 100))

        if self.team2.score_10 > 0:
            self.win_probability_1.setval(
                '{:.1f}%'.format(self.team2.times_won / (new_game.main_rounds - new_game.draw_rounds) * 100))

    def add_hand(self, hand):
        for child in self.my_hand.winfo_children():
            child.destroy()
        del globals()['card_images']
        global card_images
        card_images = {}
        for main, v in hand.items():
            for c in v:
                card = card_pack.Card(main, c)
                card_images[card] = card.get_image_for_card()
        i = 0
        threading.Thread(target=helper.give_cards()).start()
        for c1, im in card_images.items():
            b1 = Button(self.my_hand, image=im, bg='white', activebackground='white', activeforeground='white', bd=0)
            b1['command'] = lambda b=b1, c=c1: self.add_card_if(c, b)
            b1.pack(anchor=CENTER, side=LEFT)
            i += 1

    def add_card_if(self, card, b):
        player = new_game.player_you.id
        if new_game.turn == player:
            if player != new_game.first_play and card.get_suit() != new_game.current_hand.lead_suit:
                if new_game.player_you.have_suit(new_game.current_hand.lead_suit):
                    print('Hand ', new_game.player_you.cards)
                    from tkinter import messagebox
                    messagebox.askokcancel('Warning', 'Main card is ' + new_game.current_hand.lead_suit)
                    return
            print(f'Add if {card}')
            b.destroy()
            self.add_card(card, player)
        else:
            print('Don\'t you dare touch that this is player ', new_game.turn, ' s turn')
            return

    def trump_chosen(self, suit: str):
        new_game.trump_suit = suit
        self.window.wm_attributes('-disable', False)
        self.update_stats()
        time.sleep(.5)
        self.add_hand(new_game.player_you.cards)

    def add_card(self, card, player):
        self.update_stats()
        if player == new_game.first_play:
            new_game.current_hand = card_pack.Hand(new_game.trump_suit, card.get_suit())
            print('\n\nHand is on me :', player)
        else:
            print('\nPlayer :', player)
        new_game.remove_card(card)
        new_game.players()[player].remove_card(card)
        new_game.current_hand.set_player_card(player, card)
        self.update_coordinates()
        self.table.update()
        coords = [self.c1, self.c2, self.c3, self.c4][player]
        table_images[player] = card.get_image_for_card()
        table_cards[player] = self.table.create_image(int(coords[0]), int(coords[1]), image=table_images[player],
                                                      anchor=NW)
        self.table.update()
        multiprocessing.Process(target=helper.put_card()).start()
        if new_game.rounds_4 == 3:
            time.sleep(1)
        self.passround_4(player)

    def passround_4(self, player):
        new_game.rounds_4 += 1
        new_game.tot_rounds_4 += 1
        new_game.turn = get_next_player_relative_to(player)
        if new_game.rounds_4 == 4:
            new_game.rounds_4 = 0
            winner = new_game.current_hand.who_got()
            new_game.first_play = int(winner)
            new_game.turn = new_game.first_play
            if winner == 0 or winner == 2:
                self.team1.score_8 += 1
            else:
                self.team2.score_8 += 1
            new_game.players()[winner].score += 1
            threading.Thread(target=helper.give_cards).start()
            self.givehandtowinner(winner)
            self.table.after(400, self.passround_8)
            return
        elif not player == 2:
            p = get_next_player_relative_to(player)
            card = new_game.players()[p].get_next(new_game.current_hand)
            self.add_card(card, p)

    def passround_8(self):
        new_game.rounds_8 += 1
        if new_game.rounds_8 == 8:
            if self.team1.score_8 >= 5:
                self.team1.score_10 += 3 if self.team1.score_8 == 8 else 2 if new_game.trump_suit_call_player not in [0,
                                                                                                                      2] else 1
                self.team1.times_won += 1
            elif self.team1.score_8 == self.team2.score_8:
                new_game.draw_rounds += 1
            else:
                self.team2.score_10 += 3 if self.team2.score_8 == 8 else 2 if new_game.trump_suit_call_player not in [1,
                                                                                                                      3] else 1
                self.team2.times_won += 1
            if self.team1.score_10 >= 10:
                win = YouLose(self.window, new_game.player_you.score,
                              (self.team2.score_10 / new_game.main_rounds) * 100)
                win.dlg.show()
            elif self.team2.score_10 >= 10:
                win = YouWin(self.window, new_game.player_you.score,
                             (self.team2.score_10 / new_game.main_rounds) * 100)
                win.dlg.show()
            new_game.trump_suit_call_player = get_next_player_relative_to(new_game.trump_suit_call_player)
            self.team1.score_8 = 0
            self.team2.score_8 = 0
            new_game.main_rounds += 1
            new_game.rounds_8 = 0
            new_game.rounds_4 = 0
            self.table.delete('all')
            print('\n' + ('*' * 100) + '\n' + 'NEW ROUND\n' + ('*' * 100) + '\n')
            self.update_stats()
            self.window.after(2000, self.start())
            return
        print('\n' + ('*' * 50) + '\n' + 'NEW HAND\n' + ('*' * 50) + '\n')
        self.table.update()
        self.window.update()
        new_game.current_hand = card_pack.Hand(new_game.trump_suit)
        if not new_game.first_play == 3:
            print(new_game.first_play)
            self.add_card(new_game.players()[new_game.first_play].get_next(new_game.current_hand),
                          new_game.first_play)

    def givehandtowinner(self, winner):
        for card in table_cards:
            move_object(self.table, card, self.getcoords2()[winner], (3, 1), True)

    def getcoords2(self, player=None):
        self.update_coordinates()
        hide = 200
        if player:
            return [(self.c1[0] + hide, self.c1[1]), (self.c2[0], self.c2[1] - hide), (self.c3[0] - hide, self.c3[1]),
                    (self.c4[0], self.c4[1] + 100)][player]
        else:
            return [(self.c1[0] + hide, self.c1[1]), (self.c2[0], self.c2[1] - hide), (self.c3[0] - hide, self.c3[1]),
                    (self.c4[0], self.c4[1] + hide)]

    def getcoords(self, player=None):
        self.update_coordinates()
        if player:
            return [self.c1, self.c2, self.c3, self.c4][player]
        else:
            return [self.c1, self.c2, self.c3, self.c4]


if __name__ == '__main__':
    a = PlayDesk(0)
    a.window.wm_title("Ommy game")
    # a.w.resizable(False, False)
    a.window.mainloop()
