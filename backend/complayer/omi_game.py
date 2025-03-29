import random
from functools import reduce
from random import randint

from backend import card_pack
from backend.card_pack import Card, Hand
from backend.complayer import omi_player


class Score:
    def __init__(self):
        self.score_8, self.score_10, self.tot_score_8 = (0, 0, 0)
        self.times_won = 0


class Team:
    def __init__(self, team_name: str):
        self.players = []
        self.team_name = team_name

    def add_player(self, player):
        self.players.append(player)

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


class RoundEight:
    TIE = 'tie'
    WIN = 'win'

    def __init__(self):
        self.hands = list()

    def add_hand(self, hand: Hand):
        self.hands.append(hand)

    def who_wins(self):
        pass


def get_next_player_relative_to(player):
    return 0 if player == 3 else player + 1


class OmiGame:
    def __init__(self):
        self.trump_suit_call_player = 3
        self.first_play = self.trump_suit_call_player
        self.turn = self.first_play
        self.trump_suit = None
        self.left_cards = card_pack.omi_card_pack()
        self.main_rounds, self.rounds_8, self.rounds_4, self.draw_rounds = (0, 0, 0, 0)
        self.__id = 0
        self.team_1, self.team_2 = (Team("Team 01"), Team("Team 02"))
        self.current_hand = card_pack.Hand()
        self.player1 = omi_player.Player('Player Right', self, self.team_1)
        self.player2 = omi_player.Player('Player Opponent', self, self.team_2)
        self.player3 = omi_player.Player('Player Left', self, self.team_1)
        self.player_you = omi_player.Player('Player You', self, self.team_2)
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

    def players(self):
        return [self.player1, self.player2, self.player3, self.player_you]

    def print_players(self):
        for p in self.players():
            print(p)

    def get_trump_cards(self):
        trump_cards = []
        cards = card_pack.CardSet(self.players()[self.trump_suit_call_player].cards).get_card_list()
        print("Cards for trump:\n", reduce(lambda s, card: s + card.__str__()+'\n', cards,''))
        self.players()[self.trump_suit_call_player].trump_times += 1
        for i in range(4):
            j = randint(0, len(cards) - 1)
            trump_cards.append(cards[j])
            del cards[j]
        if self.trump_suit_call_player != 3:
            trump_cards_ = card_pack.empty_suits_pack()
            for c in trump_cards:
                trump_cards_[c.get_suit()].append(c.get_rank())
            self.trump_suit = self.players()[self.trump_suit_call_player].say_trump(trump_cards_)
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
        current = self.first_play + self.rounds_4 if self.first_play + self.rounds_4 < 4 else 4 - (
                self.first_play + self.rounds_4)
        return self.players()[current + 1 if current < 3 else 0]


if __name__ == '__main__':
    pass
