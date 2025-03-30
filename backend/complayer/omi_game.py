import random
from enum import Enum, auto
from functools import reduce
from random import randint

from backend import card_pack
from backend.card_pack import Card
from backend.complayer import omi_player


class OmiPlayer(Enum):
    PLAYER_YOU = 0
    PLAYER_RIGHT = 1
    PLAYER_OPPONENT = 2
    PLAYER_LEFT = 3


class Score:
    def __init__(self):
        self.score_8, self.score_10, self.tot_score_8 = (0, 0, 0)
        self.times_won = 0


class Team:
    def __init__(self, team_name: str, member_count: int = 1):
        self.players = [None] * member_count
        self.team_name = team_name

    def add_player(self, player):
        self.players.append(player)

    def set_player(self, player, index: int = 0):
        self.players[index] = player

    def get_player(self, index: int):
        return self.players[index]

    def is_team_member(self, player):
        return self.get_index(player) != -1

    def get_index(self, player):
        for i in range(len(self.players)):
            if player in self.players:
                return i
        return -1

    def get_players(self):
        return self.players


class BinaryTeam(Team):
    def __init__(self, team_name: str):
        super().__init__(team_name, 2)

    def set_player_one(self, player):
        self.set_player(player, 0)

    def set_player_two(self, player):
        self.set_player(player, 1)

    def get_opponent(self, player):
        return self.get_player(1) if self.get_index(player) == 0 else self.get_player(0)

    def set_opponent(self, player, opponent):
        if self.is_team_member(player):
            self.set_player(opponent, 0 if self.get_index(player) == 1 else 1)
        else:
            raise LookupError(player + f" is not in {self.team_name}.")


class RoundEight:
    TIE = 'tie'
    WIN = 'win'

    def __init__(self):
        self.hands = list()

    def add_hand(self, hand):
        self.hands.append(hand)

    def who_wins(self):
        pass


def get_next_pid_relative_to(player):
    return 0 if player == 3 else player + 1


class OmiGame:
    def __init__(self):
        self.trump_suit_call_pid = OmiPlayer.PLAYER_YOU.value
        self.round_start_pid = self.trump_suit_call_pid
        self.next_turn_pid = self.round_start_pid
        self.trump_suit = None
        self.left_cards = card_pack.omi_card_pack()
        self.main_rounds, self.rounds_8, self.rounds_4, self.draw_rounds = [0] * 4
        self.__id = 0
        self.current_hand = card_pack.Hand()
        self.team_1, self.team_2 = [BinaryTeam("Team 01"), BinaryTeam("Team 02")]
        self.player_you = omi_player.Player(OmiPlayer.PLAYER_YOU.value, 'Player You', self, self.team_2)
        self.player_right = omi_player.Player(OmiPlayer.PLAYER_RIGHT.value, 'Player Right', self, self.team_1)
        self.player_opponent = omi_player.Player(OmiPlayer.PLAYER_OPPONENT.value, 'Player Opponent', self, self.team_2)
        self.player_left = omi_player.Player(OmiPlayer.PLAYER_LEFT.value, 'Player Left', self, self.team_1)
        self.team_1.set_player_one(self.player_right)
        self.team_1.set_player_two(self.player_left)
        self.team_2.set_player_one(self.player_opponent)
        self.team_2.set_player_two(self.player_you)
        self.tot_rounds_4 = 0

    def shuffle(self):
        self.left_cards = card_pack.omi_card_pack()
        pack = []
        temp = card_pack.omi_card_pack()
        for j in range(4):
            for i in range(8):
                suit = list(temp.keys())[random.randint(0, len(temp) - 1)]
                while len(temp[suit]) == 0:
                    del temp[suit]
                    suit = list(temp.keys())[random.randint(0, len(temp) - 1)]
                card = Card(suit, temp[suit][random.randint(0, len(temp[suit]) - 1)])
                pack.append(card)
                temp[suit].remove(card.get_rank())

        for player in self.players():
            player.cards = card_pack.empty_suits_pack()
            for i in range(8):
                idx = random.randint(0, len(pack) - 1)
                rand_card = pack[idx]
                player.cards[rand_card.get_suit()].append(rand_card.get_rank())
                del pack[idx]
            for i in card_pack.SUITS:
                if len(player.cards[i]) == 0:
                    del player.cards[i]

    def get_round_start_player(self):
        return self.players()[self.round_start_pid]

    def get_trump_suit_call_player(self):
        return self.players()[self.trump_suit_call_pid]

    def players(self):
        players = [self.player_you] * 4
        players[OmiPlayer.PLAYER_YOU.value] = self.player_you
        players[OmiPlayer.PLAYER_RIGHT.value] = self.player_right
        players[OmiPlayer.PLAYER_OPPONENT.value] = self.player_opponent
        players[OmiPlayer.PLAYER_LEFT.value] = self.player_left
        return players

    def print_players(self):
        for p in self.players():
            print(p)

    def get_trump_cards(self):
        trump_cards = []
        cards = card_pack.CardSet(self.players()[self.trump_suit_call_pid].cards).get_card_list()
        print("Cards for trump:\n", reduce(lambda s, card: s + card.__str__() + '\n', cards, ''))
        self.players()[self.trump_suit_call_pid].trump_times += 1
        for i in range(4):
            j = randint(0, len(cards) - 1)
            trump_cards.append(cards[j])
            del cards[j]
        if self.trump_suit_call_pid != OmiPlayer.PLAYER_YOU.value:
            trump_cards_ = card_pack.empty_suits_pack()
            for c in trump_cards:
                trump_cards_[c.get_suit()].append(c.get_rank())
            self.trump_suit = self.players()[self.trump_suit_call_pid].say_trump(trump_cards_)
            self.current_hand = card_pack.Hand(self.trump_suit)
        else:
            return trump_cards

    def remove_card(self, card):
        if card.get_suit() in self.left_cards.keys():
            if card.get_rank() in self.left_cards[card.get_suit()]:
                self.left_cards[card.get_suit()].remove(card.get_rank())
        if card.get_suit() in self.left_cards:
            if len(self.left_cards[card.get_suit()]) == 0:
                del self.left_cards[card.get_suit()]

    def have_left_cards(self, suit):
        if suit in self.left_cards.keys():
            if len(self.left_cards[suit]) > 0:
                return True
        return False

    def get_next_player(self):
        current = self.round_start_pid + self.rounds_4 if self.round_start_pid + self.rounds_4 < 4 else 4 - (
                self.round_start_pid + self.rounds_4)
        return self.players()[current + 1 if current < 3 else 0]


if __name__ == '__main__':
    pass
