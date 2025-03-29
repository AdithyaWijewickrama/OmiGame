import os.path
from enum import Enum
from functools import reduce
from typing import Dict, Any, List

from scripts.helper import image

width = 120
height = 180
RANKS = ['7', '8', '9', '10', 'jack', 'queen', 'king', 'ace']
SUITS = ['hearts', 'clubs', 'spades', 'diamonds']


def empty_suits_pack() -> Dict[str, List[str]]:
    """
    Create an empty pack of suits with no cards in it.
    :return: A dictionary with suits as keys and empty lists as values.
    """
    return {'hearts': list(), 'clubs': list(), 'spades': list(), 'diamonds': list()}


def omi_card_pack() -> Dict[str, List[str]]:
    """
    Create a pack of cards with all ranks for each suit.
    :return: A dictionary with suits as keys and a list of ranks as values.
    """
    pack = empty_suits_pack()
    for suit in pack.keys():
        for rank in RANKS:
            pack[suit].append(rank)
    return pack


def pack_to_asc(pack: List[str]) -> List[str]:
    """
    Order cards by ascending order.
    :param pack: List of card ranks.
    :return: List of card ranks sorted in ascending order.
    """
    r = []
    for c in RANKS:
        if c in pack:
            r.append(c)
    return r


def pack_to_desc(pack: List[str]) -> List[str]:
    """
    Descending order of cards.
    :param pack: List of card ranks.
    :return: List of card ranks sorted in descending order.
    """
    r = []
    for rank in RANKS[::-1]:
        if rank in pack:
            r.append(rank)
    return r


def get_idx_of_rank(s: str) -> int:
    """
    Get the index of the rank in the RANKS list.
    :param s: The rank to find.
    :return: The index of the rank in RANKS, or -1 if not found.
    """
    i = 1
    for v in RANKS:
        if v == s:
            return i
        i += 1
    return -1


def get_biggest_rank(ranks: List[str]) -> str:
    """
    Get the biggest rank from a set of ranks.
    :param ranks: A set of card ranks.
    :return: The highest rank from the set.
    """
    for rank in RANKS[::-1]:
        if rank in ranks:
            return rank


def get_lowest_rank(ranks: List[str]) -> str:
    """
    Get the lowest rank from a set of ranks.
    :param ranks: A set of card ranks.
    :return: The lowest rank from the set.
    """
    for rank in RANKS:
        if rank in ranks:
            return rank


def get_after_10(s: List[str]) -> List[str]:
    """
    Get cards with ranks greater than 10.
    :param s: List of card ranks.
    :return: List of card ranks greater than 10.
    """
    r = []
    for v in s:
        if get_idx_of_rank(v) > 3:
            r.append(v)
    return r


def get_before_10(s: List[str]) -> List[str]:
    """
    Get cards with ranks less than 10.
    :param s: List of card ranks.
    :return: List of card ranks less than 10.
    """
    r = []
    for v in s:
        if get_idx_of_rank(v) < 4:
            r.append(v)
    return r


def get_rank_by_letter(s: str = "") -> str:
    """
    Convert a letter to its corresponding card rank.
    :param s: The letter representing a rank (e.g., 'a' for 'ace').
    :return: The corresponding card rank.
    """
    i = s.lower()
    if i == 'a':
        i = 'ace'
    elif i == 'j':
        i = 'jack'
    elif i == 'k':
        i = 'king'
    elif i == 'q':
        i = 'queen'
    return i


def get_suit_by_letter(i: str) -> str:
    """
    Convert a letter to its corresponding card suit.
    :param i: The letter representing a suit (e.g., 'h' for 'hearts').
    :return: The corresponding card suit.
    """
    if i == 'h':
        i = 'hearts'
    elif i == 's':
        i = 'spades'
    elif i == 'd':
        i = 'diamonds'
    elif i == 'rank':
        i = 'clubs'
    else:
        print(f'[NOT A MAIN CARD]:{i}')
    return i


def get_bigger_than(card_list: List[str], card: str) -> str:
    """
    Returns the first card bigger than the given card in the list.
    :param card_list: List of card ranks.
    :param card: A card rank.
    :return: The first card bigger than the given card in the list.
    """
    ordered_list = pack_to_asc(card_list + [card])
    return card if ordered_list.index(card) == len(ordered_list) - 1 else ordered_list[ordered_list.index(card) + 1]


def sum_of_ranks(hand: Dict[str, List[str]]) -> Dict[str, int]:
    """
    Get the sum of ranks in the hand.
    :param hand: A dictionary of cards in the hand, default is the pack.
    :return: A dictionary of suits and their respective sum of ranks.
    """
    sum_set = {}
    for suit, ranks in hand.items():
        sum_set[suit] = -1 if len(hand[suit]) == 0 \
            else reduce((lambda t, x: t + x), map(lambda rank: get_idx_of_rank(rank) + 1, hand[suit]))
    return sum_set


def count_of_ranks(hand: Dict[str, List[str]]) -> Dict[str, int]:
    """
        Get the sum of ranks in the hand.
        :param hand: A dictionary of cards in the hand, default is the pack.
        :return: A dictionary of suits and their respective sum of ranks.
        """
    count_set = {}
    for suit, ranks in hand.items():
        count_set[suit] = len(ranks)
    return count_set


class Card:
    def __init__(self, suit: str, rank: str, short: bool = False):
        """
        Initialize a card object with suit and rank.
        :param suit: The suit of the card.
        :param rank: The rank of the card.
        :param short: A boolean indicating if the inputs are abbreviated.
        """
        self.card = {'suit': get_suit_by_letter(suit) if short else suit,
                     'rank': get_rank_by_letter(rank) if short else rank}
        if (self.get_suit() not in SUITS) or (self.get_rank() not in RANKS):
            print(f'Card not valid {self.__str__()}')
            raise SyntaxError(f'Card not valid {self.__str__()}')

    def get_image_for_card(self) -> Any:
        """
        Get the image of the corresponding card.
        If the card is 7 of hearts this method will look for 7_of_hearts.png in images directory.
        :return: PLI Image of the card.
        """
        try:
            filename = str((self.card['rank']) + '_of_' + (self.card['suit']) + '.png')
            return image(os.path.join('cards', filename), width, height)
        except Exception as e:
            print(e)
            raise IOError(f"Corresponding png for card {self.__str__()} does not exist")

    def set_suit(self, suit: str):
        """
        Set the suit of the card.
        :param suit: hearts, clubs, spades, diamonds
        """
        self.card['suit'] = suit

    def set_rank(self, rank: str):
        """
        Set the rank of the card.
        :param rank: 7, 8, 9, 10, jack, queen, king, ace
        """
        self.card['rank'] = rank

    def get_suit(self) -> str:
        """
        Get the suit of the card.
        :return: The suit of the card.
        """
        return self.card['suit']

    def get_rank(self) -> str:
        """
        Get the rank of the card.
        :return: The rank of the card.
        """
        return self.card['rank']

    def __str__(self) -> str:
        """
        Get a string representation of the card.
        :return: A string representing the card's suit and rank.
        """
        return 'Suit : ' + str(self.card['suit']) + '\tRank : ' + str(self.card['rank'])


class OmiPlayer(Enum):
    PLAYER_RIGHT = 0
    PLAYER_OPPONENT = 1
    PLAYER_LEFT = 2
    PLAYER_YOU = 3


class Hand:
    def __init__(self, trump: str = None, main_suit: str = None):
        """
        Initialize the hand with trump suit and lead suit.
        :param trump: The trump suit for the hand.
        :param main_suit: The lead suit for the hand.
        """
        self.trump_suit = trump
        self.lead_suit = main_suit
        self.total_cards = 0
        self.hand = {}

    def set_hand(self, hand: Dict[OmiPlayer, Card]):
        """
        Set the hand to a new set of cards.
        :param hand: A dictionary of players and their respective cards.
        """
        self.hand = hand

    def set_lead_suit(self, main_suit: str):
        """
        Set the lead suit of the hand.
        :param main_suit: The lead suit for the hand.
        """
        self.lead_suit = main_suit

    def set_player_card(self, player: OmiPlayer, card: Card):
        """
        Set the card for a specific player in the hand.
        :param player: The player (OmiPlayers enum).
        :param card: The card to set for the player.
        """
        self.hand[player] = card
        self.total_cards += 1

    def get_hand(self) -> Dict[OmiPlayer, Card]:
        """
        Get the hand of cards.
        :return: A dictionary of players and their respective cards.
        """
        return self.hand

    def get_total_cards(self) -> int:
        return self.total_cards

    def get_trump_suit(self) -> str:
        return self.trump_suit

    def get_lead_suit(self) -> str:
        return self.lead_suit

    def get_pack_from_cards(self) -> Dict[str, List[str]]:
        """
        Get a dictionary of cards sorted by suit and rank.
        :return: A dictionary where keys are suits, and values are lists of ranks.
        """
        pack = {}
        for card in self.get_hand().values():
            if card is not None:
                if card.get_suit() not in pack.keys():
                    pack[card.get_suit()] = []
                pack[card.get_suit()].append(card.get_rank())
        return pack

    def get_biggest_card(self) -> Card:
        """
        Get the biggest card in the hand.
        :return: The biggest card in the hand.
        """
        pack = self.get_pack_from_cards()
        if self.trump_suit in pack.keys():
            big_card = Card(self.trump_suit, get_biggest_rank(pack[self.trump_suit]))
        else:
            big_card = Card(self.lead_suit, get_biggest_rank(pack[self.lead_suit]))
        return big_card

    def who_got(self) -> OmiPlayer:
        """
        Determine who has the biggest card in the hand.
        :return: The player who has the biggest card, or -1 if not determined.
        """
        big_card = self.get_biggest_card()
        for player, card in self.hand.items():
            if big_card.get_suit() == card.get_suit() and big_card.get_rank() == card.get_rank():
                return player

    def __str__(self) -> str:
        """
        Get a string representation of the hand.
        :return:
        :return: A string representing the hand.
        """
        string = 'Trump:' + str(self.trump_suit) + '\tLead:' + str(self.lead_suit) + '\n'
        for card, i in zip(self.get_hand(), range(0, 4)):
            string += (f'Player {i}:' + str(i) + card.__str__() + '\n')
        return string


class CardSet:
    def __init__(self, card_pack: dict[str: List[str]]):
        """
        Initialize a set of cards.
        :param card_pack: A list of Card objects.
        """
        self.card_pack = card_pack

    def add_card(self, card: Card):
        """
        Add a card to the card set.
        :param card: The card to add to the set.
        """
        self.card_pack.append(card)

    def get_worthiest(self, trump_suit: str = None) -> Card:
        """
        Get the worthiest card from a set of cards.
        :param trump_suit: Trump suit for finding the worthiest card
        :return: The biggest card in the set.
        """
        pass

    def get_lowest(self, cards: List[Card] = None) -> Card:
        """
        Get the lowest card from a set of cards.
        :param cards: A list of cards to evaluate.
        :return: The lowest card in the set.
        """
        pass

    def rank_count(self, hand: Dict[str, List[str]] = None) -> Dict[str, int]:
        """
        Get the count of ranks in the hand.
        :param hand: A dictionary of cards in the hand, default is the pack.
        :return: A dictionary of suits and their respective rank counts.
        """
        pass

    def get_worthy_suit(self) -> str:
        """
        Get the suit with the highest value based on rank sum and card count.
        :return: The suit with the highest value.
        """
        sum_of_ranks_set = sum_of_ranks(self.get_pack_from_cards())
        count_of_ranks_set = count_of_ranks(self.get_pack_from_cards())

        sum_count_multiple = {key: sum_of_ranks_set.get(key, 0) * count_of_ranks_set.get(key, 0) for key in
                              set(self.get_pack_from_cards())}
        sorted_sum_count_multiple = sorted(sum_count_multiple, key=lambda item: item[1])
        sorted_sum_count_multiple.reverse()
        return sorted_sum_count_multiple[0]

    def get_card_list(self) -> List[Card]:
        """
        Get the list of cards in the pack.
        :return: A list of Card objects.
        """
        card_list = []
        for suit, ranks in self.card_pack.items():
            for rank in ranks:
                card_list.append(Card(suit, rank))
        return card_list

    def get_pack_from_cards(self) -> Dict[str, List[str]]:
        """
        Get a dictionary of cards sorted by suit and rank.
        :return: A dictionary where keys are suits, and values are lists of ranks.
        """
        return self.card_pack


if __name__ == '__main__':
    # h = Hand('clubs', 'hearts')
    # h.sethand([Card('h', 'A', True), Card('h', 'J', True), Card('h', '7', True), Card('s', 'K', True)])
    # print(h.whogot())
    # print(get_bigger_than(['7', '9', 'jack', 'queen'], 'ace'))
    d = {'a': ['1', '2']}
    d['a'].reverse()
    print(d)
    d['a'] = '2'
    print(get_biggest_rank(['9', 'ace', '7']))
    pass
