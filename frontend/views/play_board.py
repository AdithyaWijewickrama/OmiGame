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
from frontend.views.start import Settings
from scripts import helper
from scripts.helper import image

width = 1100
height = 740
geo = str(width) + 'x' + str(height)
img_coin, img_xp, img_hints = (None, None, None)
table_images = [None, None, None, None]
table_cards = [None, None, None, None]
card_images = {}
player_data = PlayerData()
new_game = OmiGame()


class PlayDesk:
    def __init__(self, parent):
        self.label5 = None
        self.last_round_draw = None
        self.won_hands_label_t2 = None
        self.won_hands_label_t1 = None
        self.won_hand_panel = None
        self.trump_suit_label = None
        self.rounds_count_label = None
        self.draw_count_label = None
        self.label3 = None
        self.win_probability_t2 = None
        self.won_tricks_label_t2 = None
        self.win_probability_t1 = None
        self.top_bar = None
        self.stat_panel = None
        self.desk = None
        self.my_hand = None
        self.top = None
        self.collapse_panel = None
        self.sidebar = None
        self.xp = None
        self.hint = None
        self.coins = None
        self.won_tricks_label_t1 = None
        self.right_coord, self.top_coord, self.left_coord, self.bottom_coord = [[]] * 4
        self.window = None
        self.player_right_stat, self.player_left_stat, self.player_opponent_stat, self.player_you_stat = [None] * 4
        self.team1, self.team2 = [Score(), Score()]
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
        self.desk = Canvas(self.top, bg=COLOR)
        self.stat_panel = Frame(self.top)
        self.top_bar = LabelFrame(self.sidebar, bg=COLOR)

        self.coins = StatLabel(self.top_bar, image=img_coin, bg=COLOR, fg='white',
                               value=(player_data.get_value('coins')), value_font=FONT2)
        self.xp = StatLabel(self.top_bar, image=img_xp, bg=COLOR, fg='white', value=(player_data.get_value('xp')),
                            value_font=FONT2)
        self.hint = Button(self.top_bar, command=self.hints, bg=COLOR, fg='white', text="Hint", image=img_hints)
        self.settings = Button(self.top_bar, command=self.show_settings, bg=COLOR, fg='white', text="Settings")
        self.top_bar.columnconfigure(0, weight=1)
        self.hint.grid(column=0, row=0, sticky='we')
        self.settings.grid(column=0, row=1, sticky='we')
        self.coins.grid(column=0, row=2, sticky='we')
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
        self.won_tricks_label_t1 = StatLabel(self.sidebar, label_type='Won tricks', value='0', floating='|',
                                             value_font=('Arial', 26, 'bold'))
        self.won_tricks_label_t1.grid(column=0, row=row, padx=5, pady=2, sticky='we')
        row += 1
        self.win_probability_t1 = StatLabel(self.sidebar, label_type='Win probability', value='0%')
        self.win_probability_t1.grid(column=0, row=row, padx=5, pady=2, sticky='we')
        row += 1
        self.label3 = Label(self.sidebar, text="Your team", font=FONT2, anchor='w', fg=COLOR)
        self.label3.grid(column=0, row=row, padx=5, pady=2, sticky='we')
        row += 1
        self.won_tricks_label_t2 = StatLabel(self.sidebar, label_type='Won tricks', value='0', floating='|',
                                             value_font=('Arial', 26, 'bold'))
        self.won_tricks_label_t2.grid(column=0, row=row, padx=5, pady=2, sticky='we')
        row += 1
        self.win_probability_t2 = StatLabel(self.sidebar, label_type='Win probability', value='0%')
        self.win_probability_t2.grid(column=0, row=row, padx=5, pady=2, sticky='we')
        row += 1
        self.label3 = Label(self.sidebar, text="Game stats", font=FONT2, anchor='w', fg=COLOR)
        self.label3.grid(column=0, row=row, padx=5, pady=2, sticky='we')
        row += 1
        self.rounds_count_label = StatLabel(self.sidebar, label_type='Rounds played', value='0')
        self.rounds_count_label.grid(column=0, row=row, padx=5, pady=2, sticky='we')
        row += 1
        self.draw_count_label = StatLabel(self.sidebar, label_type='Draw rounds', value='0')
        self.draw_count_label.grid(column=0, row=row, padx=5, pady=2, sticky='we')
        row += 1
        self.trump_suit_label = StatLabel(self.sidebar, label_type='Trump', value='Not started')
        self.trump_suit_label.grid(column=0, row=row, padx=5, pady=2, sticky='we')
        row += 1

        self.collapse_panel.columnconfigure(0, weight=1)
        self.collapse_panel.rowconfigure(0, weight=1, minsize=th)
        self.collapse_panel.columnconfigure(0, weight=1, minsize=(card_width * 8))
        self.collapse_panel.rowconfigure(1, weight=1, minsize=card_height)
        self.top.columnconfigure(0, weight=1, minsize=200)
        self.top.columnconfigure(1, weight=1, minsize=tw)
        self.top.columnconfigure(2, weight=1)
        self.top.rowconfigure(0, weight=1, minsize=th)
        self.stat_panel.columnconfigure(0, weight=1, minsize=200)
        self.top.grid(column=0, row=0, sticky='news')
        self.desk.grid(column=1, row=0, sticky='news')
        self.collapse_panel.pack()
        self.stat_panel.grid(column=2, row=0, sticky='news')
        self.my_hand.grid(column=0, row=1)
        self.sidebar.grid(column=0, row=0, sticky='news')
        self.player_right_stat = StatPanel(self.stat_panel)
        self.player_right_stat.update("Player right")
        self.player_left_stat = StatPanel(self.stat_panel)
        self.player_left_stat.update("Player left")
        self.player_opponent_stat = StatPanel(self.stat_panel)
        self.player_opponent_stat.update("Your partner")
        self.player_you_stat = StatPanel(self.stat_panel)
        self.player_you_stat.update("You")
        self.won_hands_label_t1 = StatLabel(self.stat_panel, label_type='Won hands', value='0', floating='|',
                                            value_font=('Arial', 26, 'bold'))
        # self.won_hands_label_t1.pack(anchor=CENTER, padx=5)
        self.won_hands_label_t2 = StatLabel(self.stat_panel, label_type='Won hands', value='0', floating='|',
                                            value_font=('Arial', 26, 'bold'))
        # self.won_hands_label_t2.pack(anchor=CENTER, padx=5)
        self.window.update()
        row = 0
        self.label4 = StatLabel(self.stat_panel, label_type=new_game.team_1.team_name, value='',
                                type_font=('Arial', 18, 'bold'))
        self.label4.grid(column=0, row=row, padx=5, pady=2, sticky='we')
        row += 1
        self.player_right_stat.w.grid(column=0, row=row, padx=5, pady=5, sticky='ew')
        row += 1
        self.player_left_stat.w.grid(column=0, row=row, padx=5, pady=5, sticky='ew')
        row += 1
        self.won_hands_label_t1.grid(column=0, row=row, padx=5, pady=5, sticky='ew')
        row += 1
        self.label5 = StatLabel(self.stat_panel, label_type=new_game.team_2.team_name, value='',
                                type_font=('Arial', 18, 'bold'))
        self.label5.grid(column=0, row=row, padx=5, pady=2, sticky='we')
        row += 1
        self.player_opponent_stat.w.grid(column=0, row=row, padx=5, pady=5, sticky='ew')
        row += 1
        self.player_you_stat.w.grid(column=0, row=row, padx=5, pady=5, sticky='ew')
        row += 1
        self.won_hands_label_t2.grid(column=0, row=row, padx=5, pady=5, sticky='ew')
        row += 1
        self.update_coordinates()
        self.window.update_idletasks()
        self.window.update()
        time.sleep(.5)
        self.start()

    def show_settings(self):
        Settings(self.window)

    def hints(self):
        msg = Hints(self.window, new_game.left_cards, new_game.player_you, new_game.current_hand)
        threading.Thread(target=msg.dlg.show)

    def start(self):
        new_game.shuffle()
        threading.Thread(target=helper.shuffle_cards).start()
        trump_cards = new_game.get_trump_cards()
        if not trump_cards:
            ShowSelectedTrump(self.window, new_game.trump_suit,
                              f'{new_game.players()[new_game.trump_suit_call_pid].name} chose trump as '
                              f'{new_game.trump_suit}')
            self.add_hand(new_game.player_you.cards)
            tp = new_game.players()[new_game.trump_suit_call_pid]
            new_game.round_start_pid = tp.id
            new_game.current_hand = card_pack.Hand(new_game.trump_suit)
            card = new_game.players()[tp.id].get_next(new_game.current_hand)
            new_game.current_hand.set_player_card(tp, card)
            self.add_card(card, tp)
        else:
            new_game.round_start_pid = new_game.player_you.id
            new_game.next_turn_pid = new_game.round_start_pid
            AskTrump(self.window, trump_cards, self.trump_chosen)

    def update_coordinates(self):
        self.desk.update()
        tw = self.desk.winfo_width()
        th = self.desk.winfo_height()
        pad = 20
        self.right_coord = [int(tw - card_width - pad), int((th - card_height) / 2)]
        self.top_coord = [int((tw - card_width) / 2), int(pad)]
        self.left_coord = [int(pad), int((th - card_height) / 2)]
        self.bottom_coord = [int((tw - card_width) / 2), int(th - card_height - pad)]

    def update_stats(self):
        self.player_right_stat.update(new_game.player_right.name, new_game.player_right.score,
                                      new_game.player_right.trump_times)
        self.player_left_stat.update(new_game.player_left.name, new_game.player_left.score,
                                     new_game.player_left.trump_times)
        self.player_opponent_stat.update(new_game.player_opponent.name, new_game.player_opponent.score,
                                         new_game.player_opponent.trump_times)
        self.player_you_stat.update(new_game.player_you.name, new_game.player_you.score,
                                    new_game.player_you.trump_times)
        self.won_tricks_label_t1.setval(self.team1.score_10)
        self.won_tricks_label_t2.setval(self.team2.score_10)
        self.won_hands_label_t1.setval(self.team1.score_8)
        self.won_hands_label_t2.setval(self.team2.score_8)
        self.xp.value = player_data.get_value('xp')
        self.coins.value = player_data.get_value('coins')
        if self.team1.score_10 > self.team2.score_10:
            self.won_tricks_label_t1.valueLabel.configure(fg='green', font=('Arial', 30, 'bold'))
            self.won_tricks_label_t2.valueLabel.configure(fg='red', font=('Arial', 26, 'bold'))
        elif self.team1.score_10 < self.team2.score_10:
            self.won_tricks_label_t2.valueLabel.configure(fg='green', font=('Arial', 30, 'bold'))
            self.won_tricks_label_t1.valueLabel.configure(fg='red', font=('Arial', 26, 'bold'))
        else:
            self.won_tricks_label_t2.valueLabel.configure(fg=COLOR, font=('Arial', 24, 'bold'))
            self.won_tricks_label_t1.valueLabel.configure(fg=COLOR, font=('Arial', 24, 'bold'))
        if self.team1.score_8 > self.team2.score_8:
            self.won_hands_label_t1.valueLabel.configure(fg='green', font=('Arial', 30, 'bold'))
            self.won_hands_label_t2.valueLabel.configure(fg='red', font=('Arial', 26, 'bold'))
        elif self.team1.score_8 < self.team2.score_8:
            self.won_hands_label_t2.valueLabel.configure(fg='green', font=('Arial', 30, 'bold'))
            self.won_hands_label_t1.valueLabel.configure(fg='red', font=('Arial', 26, 'bold'))
        else:
            self.won_hands_label_t2.valueLabel.configure(fg=COLOR, font=('Arial', 24, 'bold'))
            self.won_hands_label_t1.valueLabel.configure(fg=COLOR, font=('Arial', 24, 'bold'))

        self.trump_suit_label.setval(
            f'{new_game.trump_suit} by {new_game.players()[new_game.trump_suit_call_pid].name}')
        self.rounds_count_label.setval(new_game.main_rounds)
        self.draw_count_label.setval(new_game.draw_rounds)
        if self.team1.score_10 > 0:
            self.win_probability_t1.setval(
                '{:.1f}%'.format(self.team1.times_won / (new_game.main_rounds - new_game.draw_rounds) * 100))

        if self.team2.score_10 > 0:
            self.win_probability_t2.setval(
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
        threading.Thread(target=helper.give_cards).start()
        for card, img in card_images.items():
            button = Button(self.my_hand, image=img, bg='white', activebackground='white', activeforeground='white',
                            bd=0)
            button['command'] = lambda _button=button, _card=card: self.add_card_if_my_turn(_card, _button)
            button.pack(anchor=CENTER, side=RIGHT)
            i += 1

    def add_card_if_my_turn(self, card: Card, button: Button):
        player = new_game.player_you
        if new_game.next_turn_pid == player.id:
            if player.id != new_game.round_start_pid and card.get_suit() != new_game.current_hand.lead_suit:
                if new_game.player_you.have_suit(new_game.current_hand.lead_suit):
                    print('Hand ', new_game.player_you.cards)
                    from tkinter import messagebox
                    messagebox.showwarning('Warning', 'Main card is ' + new_game.current_hand.lead_suit)
                    return
            print(f'Add if {card}')
            button.destroy()
            self.add_card(card, player)
        else:
            print('Don\'t you dare touch that this is player ', new_game.next_turn_pid, ' s turn')
            return

    def trump_chosen(self, suit: str):
        new_game.trump_suit = suit
        self.window.wm_attributes('-disable', False)
        multiprocessing.Process(target=helper.give_cards).start()
        self.update_stats()
        time.sleep(.5)
        self.add_hand(new_game.player_you.cards)

    def add_card(self, card, player):
        self.update_stats()
        if player.id == new_game.round_start_pid:
            new_game.current_hand = card_pack.Hand(new_game.trump_suit, card.get_suit())
            print('\nHand is on me :\n', player)
        else:
            print('\nPlayer :\n', player)
        new_game.remove_card(card)
        new_game.players()[player.id].remove_card(card)
        new_game.current_hand.set_player_card(player, card)
        self.update_coordinates()
        self.desk.update()
        coord = self.get_coordinates(player.id)
        table_images[player.id] = card.get_image_for_card()
        table_cards[player.id] = self.desk.create_image(int(coord[0]),
                                                        int(coord[1]),
                                                        image=table_images[player.id],
                                                        anchor=NW)
        self.desk.update()
        helper.put_card()
        # multiprocessing.Process(target=helper.put_card).start()
        if new_game.rounds_4 == 3:
            time.sleep(1)
        self.pass_round_4(player.id)

    def pass_round_4(self, player_id):
        new_game.rounds_4 += 1
        new_game.tot_rounds_4 += 1
        new_game.next_turn_pid = get_next_pid_relative_to(player_id)
        if new_game.rounds_4 == 4:
            new_game.rounds_4 = 0
            winner = new_game.current_hand.who_got()
            new_game.round_start_pid = int(winner.id)
            new_game.next_turn_pid = new_game.round_start_pid
            if winner.id == OmiPlayer.PLAYER_LEFT.value or winner.id == OmiPlayer.PLAYER_RIGHT.value:
                self.team1.score_8 += 1
            else:
                self.team2.score_8 += 1
            new_game.players()[winner.id].score += 1
            threading.Thread(target=helper.give_cards).start()
            self.give_hand_to_winner(winner)
            self.desk.after(400, self.pass_round_8)
            self.update_stats()
            return
        if not player_id == OmiPlayer.PLAYER_LEFT.value:
            p = get_next_pid_relative_to(player_id)
            card = new_game.players()[p].get_next(new_game.current_hand)
            self.add_card(card, new_game.players()[p])
        self.update_stats()

    def pass_round_8(self):
        new_game.rounds_8 += 1
        if new_game.rounds_8 == 8:
            if self.team1.score_8 >= 5:
                self.team1.score_10 += 3 if (self.team1.score_8 == 8) else 2 if (
                        new_game.team_2.is_team_member(new_game.get_trump_suit_call_player())
                        or (
                                new_game.team_1.is_team_member(new_game.get_trump_suit_call_player())
                                and self.last_round_draw
                        )) else 1
                self.team1.times_won += 1
            elif self.team2.score_8 >= 5:
                self.team2.score_10 += 3 if (self.team2.score_8 == 8) else 2 if (
                        new_game.team_1.is_team_member(new_game.get_trump_suit_call_player())
                        or (
                                new_game.team_1.is_team_member(new_game.get_trump_suit_call_player())
                                and self.last_round_draw
                        )) else 1
                self.team2.times_won += 1
            elif self.team1.score_8 == self.team2.score_8:
                if self.last_round_draw is None:
                    self.last_round_draw = True
                else:
                    self.last_round_draw = not self.last_round_draw

                new_game.draw_rounds += 1

            if self.team1.score_10 >= 10:
                win = YouLose(self.window, 500,
                              200)
                win.dlg.show()
            elif self.team2.score_10 >= 10:
                win = YouWin(self.window, 1000,
                             1000)
                win.dlg.show()
            new_game.trump_suit_call_pid = get_next_pid_relative_to(new_game.trump_suit_call_pid)
            self.team1.score_8 = 0
            self.team2.score_8 = 0
            new_game.main_rounds += 1
            new_game.rounds_8 = 0
            new_game.rounds_4 = 0
            for plyr in new_game.players():
                plyr.score = 0
            self.desk.delete('all')
            print('\n' + ('*' * 100) + '\n' + 'NEW ROUND\n' + ('*' * 100) + '\n')
            self.update_stats()
            self.window.after(2000, self.start)
            return
        print('\n' + ('*' * 50) + '\n' + 'NEW HAND\n' + ('*' * 50) + '\n')
        self.desk.update()
        self.window.update()
        new_game.current_hand = card_pack.Hand(new_game.trump_suit)
        if not new_game.round_start_pid == OmiPlayer.PLAYER_YOU.value:
            self.add_card(new_game.players()[new_game.round_start_pid].get_next(new_game.current_hand),
                          new_game.get_round_start_player())

    def give_hand_to_winner(self, winner):
        for card in table_cards:
            move_object(self.desk, card, self.get_coordinates_hide()[winner.id], (3, 1), True)

    def get_coordinates_hide(self, player=None):
        self.update_coordinates()
        hide = 200
        coordinates = [(0, 0)] * 4
        coordinates[OmiPlayer.PLAYER_RIGHT.value] = (self.right_coord[0] + hide, self.right_coord[1])
        coordinates[OmiPlayer.PLAYER_OPPONENT.value] = (self.top_coord[0], self.top_coord[1] - hide)
        coordinates[OmiPlayer.PLAYER_LEFT.value] = (self.left_coord[0] - hide, self.left_coord[1])
        coordinates[OmiPlayer.PLAYER_YOU.value] = (self.bottom_coord[0], self.bottom_coord[1] + hide)
        if player:
            return coordinates[player]
        else:
            return coordinates

    def get_coordinates(self, player_id=None):
        self.update_coordinates()
        coordinates = [(0, 0)] * 4
        coordinates[OmiPlayer.PLAYER_YOU.value] = self.bottom_coord
        coordinates[OmiPlayer.PLAYER_RIGHT.value] = self.right_coord
        coordinates[OmiPlayer.PLAYER_OPPONENT.value] = self.top_coord
        coordinates[OmiPlayer.PLAYER_LEFT.value] = self.left_coord
        if player_id is not None:
            return coordinates[player_id]
        else:
            return coordinates
