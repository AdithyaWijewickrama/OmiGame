from typing import List

from backend import card_pack
from backend.card_pack import get_biggest_rank, get_bigger_than, Card, get_lowest_rank, sum_of_ranks, \
    empty_suits_pack
from backend.complayer.omi_game import get_next_pid_relative_to
from database.sql import Database
from scripts.helper import remove_sublist_from_list


class Player:
    from backend.complayer.omi_game import OmiGame, BinaryTeam

    def __init__(self, id: int, name: str, game: OmiGame, team: BinaryTeam):
        self.cards = empty_suits_pack()
        self.game = game
        self.id = id
        self.name = name
        team.add_player(self)
        self.put = None
        self.trump_times = 0
        self.score = 0
        self.seen_empty_suit = {}
        self.team = team
        for m in card_pack.SUITS:
            self.seen_empty_suit[m] = False

    def set_opponent(self, player: "Player"):
        self.team.set_opponent(self, player)

    def get_opponent(self) -> "Player":
        return self.team.get_opponent(self)

    def say_trump(self, cards: dict[str, List[str]] = None):
        return card_pack.CardSet(cards if cards else self.cards).get_worthy_suit()

    def get_next(self, hand):
        self.think(self.name, " is Thinking...")
        sum_of_left = sum_of_ranks(self.game.left_cards)
        sum_of_cards = sum_of_ranks(self.cards)
        card = None
        selected_suit = None
        selected_rank = None
        my_turn = hand.get_total_cards() + 1
        lead_suit = hand.get_lead_suit()
        if len(list(self.cards.values())) == 1:
            selected_suit = list(self.cards.keys())[0]
            selected_rank = list(self.cards.values())[0][0]
            self.think("One card left...")
        elif lead_suit is None:
            self.think("I'm starting hand...")
            a = {}
            for suit in card_pack.SUITS:
                for rev_rank in card_pack.RANKS[::-1]:
                    if self.have_suit(suit):
                        if rev_rank in self.cards[suit]:
                            bst = get_biggest_rank([rev_rank] + self.game.left_cards[suit])
                            if bst in self.cards[suit]:
                                if suit in list(a.keys()):
                                    del a[suit]
                                a[suit] = [bst, sum_of_left[suit] - sum_of_cards[suit]]
            i = 0
            for suit, v in a.items():
                if v[1] > i:
                    selected_suit = suit
                    selected_rank = v[0]
            if selected_suit is None:
                card = self.get_worthless_card()
        elif self.have_suit(lead_suit):
            self.think("Have lead cards...")
            cut = (
                    (
                            lead_suit != self.game.trump_suit
                    )
                    and (
                            self.game.trump_suit in list(hand.get_pack_from_cards().keys())
                    )
            )
            current_owner = hand.who_got()
            selected_suit = lead_suit
            worthiest_my = get_biggest_rank(self.cards[lead_suit])
            worthiest_hand = get_biggest_rank(hand.get_pack_from_cards()[lead_suit])
            worthiest_left = get_biggest_rank(self.game.left_cards[lead_suit])
            lowest_my = get_lowest_rank(self.cards[lead_suit])
            if not cut:
                self.think("Hand was not cut..")
                if my_turn == 2:
                    self.think("My turn is 2...")
                    if get_biggest_rank([worthiest_left, worthiest_hand]) == worthiest_my:
                        self.think("I have the worthiest:\t", worthiest_my)
                        selected_rank = worthiest_my
                    else:
                        self.think("I haven't the worthiest:\t", lowest_my)
                        selected_rank = lowest_my
                elif my_turn == 3:
                    self.think("My turn is 3...")
                    if current_owner == self.get_opponent():
                        self.think("Current owner is opponent...")
                        if (not self.game.players()[get_next_pid_relative_to(self.id)].seen_empty_suit[lead_suit]
                                or get_biggest_rank([worthiest_left, worthiest_hand]) == worthiest_hand
                                or (get_biggest_rank([worthiest_left, worthiest_my]) == worthiest_my
                                    and get_biggest_rank(
                                            remove_sublist_from_list(
                                                self.game.left_cards[lead_suit], self.cards[lead_suit])
                                            + [worthiest_hand]
                                        ) == worthiest_hand
                                )):
                            self.think("Putting lowest:\t", lowest_my)
                            selected_rank = lowest_my
                        else:
                            self.think("Putting worthiest:\t", worthiest_my)
                            selected_rank = worthiest_my
                    else:
                        self.think("Current owner is not opponent...")
                        if (get_bigger_than(
                                self.cards[lead_suit], get_biggest_rank(hand.get_pack_from_cards()[lead_suit]))
                                in self.cards[lead_suit]):
                            selected_rank = get_bigger_than(self.cards[lead_suit],
                                                            get_biggest_rank(hand.get_pack_from_cards()[lead_suit]))
                        elif get_biggest_rank([worthiest_hand, worthiest_my]) == worthiest_my:
                            selected_rank = worthiest_my
                        else:
                            selected_rank = lowest_my
                else:
                    if current_owner == self.get_opponent():
                        selected_rank = lowest_my
                    elif get_bigger_than(self.cards[lead_suit],
                                         get_biggest_rank(hand.get_pack_from_cards()[lead_suit])) in \
                            self.cards[
                                lead_suit]:
                        selected_rank = get_bigger_than(self.cards[lead_suit],
                                                        get_biggest_rank(hand.get_pack_from_cards()[lead_suit]))
                    elif get_biggest_rank([worthiest_hand, worthiest_my]) == worthiest_my:
                        selected_rank = worthiest_my
                    else:
                        selected_rank = lowest_my
            else:
                selected_rank = lowest_my
        elif not self.have_suit(lead_suit):
            self.think("Have not lead cards..")
            if lead_suit == self.game.trump_suit:
                card = self.get_worthless_card()
            else:
                cut = ((hand.get_lead_suit() != self.game.trump_suit) and (
                        self.game.trump_suit in list(hand.get_pack_from_cards().keys())))
                if cut:
                    self.think("Hand is cut...")
                current_owner = hand.who_got()
                self.think("Got by ", current_owner)
                self.seen_empty_suit[lead_suit] = True
                worthiest_hand = get_biggest_rank(hand.get_pack_from_cards()[lead_suit])
                if self.game.have_left_cards(lead_suit):
                    worthiest_left = get_biggest_rank(self.game.left_cards[lead_suit])
                else:
                    worthiest_left = None
                if cut:
                    if self.have_suit(self.game.trump_suit):
                        if my_turn == 3 or my_turn == 4:
                            if current_owner == self.get_opponent():
                                card = self.get_worthless_card()
                            else:
                                if (get_bigger_than(self.cards[self.game.trump_suit],
                                                    get_biggest_rank(hand.get_pack_from_cards()[self.game.trump_suit]))
                                        in self.cards[self.game.trump_suit]):
                                    selected_suit = self.game.trump_suit
                                    selected_rank = get_bigger_than(
                                        self.cards[self.game.trump_suit], get_biggest_rank(
                                            hand.get_pack_from_cards()[self.game.trump_suit]))
                                else:
                                    card = self.get_worthless_card()
                        else:
                            selected_suit = self.game.trump_suit
                            if self.game.players()[
                                get_next_pid_relative_to(self.id)
                            ].seen_empty_suit[
                                self.game.trump_suit
                            ] or not self.game.players()[
                                get_next_pid_relative_to(self.id)
                            ].seen_empty_suit[
                                lead_suit
                            ]:
                                selected_rank = get_lowest_rank(self.cards[self.game.trump_suit])
                            else:
                                selected_rank = get_biggest_rank(self.cards[self.game.trump_suit])
                    else:
                        card = self.get_worthless_card()
                else:
                    if self.have_suit(self.game.trump_suit):
                        if my_turn == 3 or my_turn == 4:
                            if current_owner == self.get_opponent():
                                if my_turn == 3:
                                    if get_biggest_rank([worthiest_left, worthiest_hand]) == worthiest_left:
                                        selected_suit = self.game.trump_suit
                                        selected_rank = get_lowest_rank(self.cards[self.game.trump_suit])
                                    else:
                                        card = self.get_worthless_card()
                                if my_turn == 4:
                                    card = self.get_worthless_card()
                            else:
                                selected_suit = self.game.trump_suit
                                if self.game.players()[
                                    get_next_pid_relative_to(self.id)
                                ].seen_empty_suit[
                                    self.game.trump_suit
                                ]:
                                    selected_rank = get_lowest_rank(self.cards[self.game.trump_suit])
                                else:
                                    selected_rank = get_biggest_rank(self.cards[self.game.trump_suit])
                        else:
                            selected_suit = self.game.trump_suit
                            if (self.game.players()[
                                get_next_pid_relative_to(self.id)
                            ].seen_empty_suit[
                                self.game.trump_suit
                            ]
                                    or not self.game.players()[
                                        get_next_pid_relative_to(self.id)
                                    ].seen_empty_suit[
                                        lead_suit
                                    ]):
                                selected_rank = get_lowest_rank(self.cards[self.game.trump_suit])
                            else:
                                selected_rank = get_biggest_rank(self.cards[self.game.trump_suit])
                    else:
                        card = self.get_worthless_card()
        if card is None:
            card = Card(selected_suit, selected_rank)
        return card

    def think(self, *thoughts):
        string = ''
        for thought in thoughts:
            string += thought.__str__()
        print(string)
        # time.sleep(.2)

    def remove_card(self, card):
        self.cards[card.get_suit()].remove(card.get_rank())
        if len(self.cards[card.get_suit()]) == 0:
            del self.cards[card.get_suit()]

    def have_suit(self, suit: str):
        if suit in list(self.cards.keys()):
            if len(self.cards[suit]) > 0:
                return True
        return False

    def get_worthless_card(self):
        if len(self.cards.keys()) == 1:
            selected_main = list(self.cards.keys())[0]
        else:
            sum_of_left = sum_of_ranks(self.game.left_cards)
            sum_of_cards = sum_of_ranks(self.cards)
            a = {}
            for m, c in self.cards.items():
                a[m] = sum_of_left[m] - sum_of_cards[m]
            i = list(a.values())[0]
            selected_main = list(a.keys())[0]
            for m, v in a.items():
                if v < i and m != self.game.trump_suit:
                    selected_main = m
        return Card(selected_main, get_lowest_rank(self.cards[selected_main]))

    def __str__(self):
        return f"""\n[NAME]\t{self.name}\n[OPPONENT]\t{self.get_opponent().name}\n[PACK]\t{self.cards}"""


class PlayerData:
    def __init__(self):
        pass

    def get_value(self, key):
        return Database().get_single_object(f"SELECT value FROM player_data WHERE id=?", (key,))

    def update(self, key, val):
        if key is None:
            return
        return Database().execute(f"UPDATE player_data SET value=? WHERE id=?", (val, key))

    def add_new(self, key, val):
        if key is None:
            return
        Database().execute(f"INSERT INTO player_data (?,?)", (val, key))
