import os.path
from functools import reduce

from scripts.Helper import image

width = 120
height = 180
cards = ['7', '8', '9', '10', 'jack', 'queen', 'king', 'ace']
mainCards = ['hearts', 'clubs', 'spades', 'diamonds']


def emptypack():
    return {'hearts': list(), 'clubs': list(), 'spades': list(), 'diamonds': list()}


def cardpack():
    pack = {'hearts': list(), 'clubs': list(), 'spades': list(), 'diamonds': list()}
    for v in pack.keys():
        for c in cards:
            pack[v].append(c)
    return pack


def decs(s):
    """
    decsending order of cards
    :param s:
    :return:
    """
    d = cards[::-1]
    r = []
    i = 0
    for v in d:
        if v in s:
            r.append(v)
            i += 1
    return r


def getIdx(s):
    i = 1
    for v in cards:
        if v == s:
            return i
        i += 1
    return -1


def getBiggest(f, s):
    return f if getIdx(f) > getIdx(s) else s


def getLowest(f, s):
    return f if getIdx(f) < getIdx(s) else s


def getAfter10(s):
    r = []
    i = 0
    for v in s:
        if getIdx(v) > 3:
            r.append(v)
            i += 1
    return r


def getBefore10(s):
    r = []
    i = 0
    for v in s:
        if getIdx(v) < 4:
            r.append(v)
            i += 1
    return r


# print(sumofcards({'hearts': [], 'clubs': ['Q', 'A'], 'spades': ['J'], 'diamonds': ['A']}))


def getCardNameByLetter(s=""):
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


def getMainCardNameByLetter(i):
    if i == 'h':
        i = 'hearts'
    elif i == 's':
        i = 'spades'
    elif i == 'd':
        i = 'diamonds'
    elif i == 'c':
        i = 'clubs'
    else:
        print(f'[NOT A MAIN CARD]:{i}')
    return i


def order(cp):
    """
    Order cards by ascending order
    :param cp:
    :return:
    """
    r = []
    for c in cards:
        if c in cp:
            r.append(c)
    return r


def getBiggerThan(cardList, card):
    """
    Returns first card bigger than the given card in the list
    :param cardList:
    :param card:
    :return:
    """
    orderedList = order(cardList + [card])
    return card if orderedList.index(card) == len(orderedList) - 1 else orderedList[orderedList.index(card) + 1]


class Card():
    def __init__(self, main, card, short=False):
        self.card = {'m': getMainCardNameByLetter(main) if short else main,
                     'c': getCardNameByLetter(card) if short else card}
        if (self.m() not in mainCards) or (self.c() not in cards):
            print(f'Card not valid {self.__str__()}')

    def getImage(self):
        try:
            filename = str((self.card['c']) + '_of_' + (self.card['m']) + '.png')
            return image(os.path.join('cards', filename), width, height)
        except Exception as e:
            print(f"new image -> {self.__str__()}")

    def setmain(self, main):
        self.card['m'] = main

    def setcard(self, card):
        self.card['c'] = card

    def m(self):
        """
        get the main
        :return:
        """
        return self.card['m']

    def c(self):
        """
        get the card
        :return:
        """
        return self.card['c']

    def __str__(self):
        return 'main : ' + str(self.card['m']) + ' card : ' + str(self.card['c'])


class Hand:
    def __init__(self, trump, main=''):
        self.trump = trump
        self.main = main
        self.len = 0 if main == '' else 1
        self.__player1 = {'m': '', 'c': ''}
        self.__player2 = {'m': '', 'c': ''}
        self.__opponent = {'m': '', 'c': ''}
        self.__playerYou = {'m': '', 'c': ''}

    def setPlayerCard(self, player, card):
        if player == 0:
            self.__player1['m'] = card.m()
            self.__player1['c'] = card.c()
        elif player == 2:
            self.__player2['m'] = card.m()
            self.__player2['c'] = card.c()
        elif player == 1:
            self.__opponent['m'] = card.m()
            self.__opponent['c'] = card.c()
        elif player == 3:
            self.__playerYou['m'] = card.m()
            self.__playerYou['c'] = card.c()
        else:
            self.len -= 1
        self.len += 1

    def getHand(self):
        return [self.__player1, self.__opponent, self.__player2, self.__playerYou]

    def getCards(self):
        """
        dict to card object
        :return:
        """
        cards = []
        for c in self.getHand():
            cards.append(Card(c['m'], c['c']))
        return cards

    def getPackFromCards(self):
        pack = {}
        for p in self.getHand():
            if p['m'] != '':
                pack[p['m']] = []
                pack[p['m']].append(p['c'])
        return pack

    def setHand(self, cards):
        """
        card object to dict
        :param cards:
        :return:
        """
        p = self.getHand()
        for i, c in zip(list(range(0, 4)), list(cards)):
            p[i]['m'] = c.m()
            p[i]['c'] = c.c()

    def __str__(self):
        s = 'Trump:' + str(self.trump) + '\nMain:' + str(self.main) + '\n'
        for c, i in zip(self.getHand(), range(0, 4)):
            s += (f'Player {i}:' + str(i) + 'main:' + c['m'] + ' card:' + c['c'] + '\n')
        return s

    def whogot(self):
        pack = emptypack()
        for c in self.getHand():
            if not c['m'] == '':
                pack[c['m']].append(c['c'])
        for m, c in pack.items():
            pack[m] = CardSet().getbiggest(c)
        if not pack[self.trump] == '':
            p = Card(self.trump, pack[self.trump])
        else:
            p = Card(self.main, pack[self.main])
        for c, i in zip(self.getHand(), list(range(0, 4))):
            if p.m() == c['m'] and p.c() == c['c']:
                p = i
                break
        return p


class CardSet():
    def __init__(self, pack=None):
        self.pack = pack

    def getbiggest(self, cards=None):
        r = ''
        if cards is not None:
            for v in cards:
                if r == '':
                    r = v
                    continue
                r = getBiggest(r, v)
        else:
            main = ''
            for m in mainCards:
                r1 = self.getbiggest(m)
                main = m if getBiggest(r, r1) == r1 else main
                r = getBiggest(r, r1)
            r = Card(main, r)
        return r

    def getlowest(self, cards=None):
        r = ''
        if cards:
            for v in cards:
                if r == '':
                    r = v
                    continue
                r = getLowest(r, v)
        else:
            main = ''
            for m in mainCards:
                r1 = self.getlowest(m)
                main = m if getLowest(r, r1) == r1 else m
                r = getLowest(r, r1)
            r = Card(main, r)
        return r

    def sumofcards(self, hn=None):
        r = {}
        if hn is None:
            hn = self.pack
        for k, v in hn.items():
            r[k] = -1 if len(hn[k]) == 0 else reduce(lambda t, x: t + x, map(lambda x: getIdx(x) + 1, hn[k]))
        return r

    def lengthofcards(self, hn=None):
        r = {}
        if hn is None:
            hn = self.pack
        for k, v in hn.items():
            r[k] = len(v)
        return r

    def getworthmain(self):
        sum = self.sumofcards()
        main = 'hearts'
        for m, v in sum.items():
            main = m if sum[main] < sum[m] else main if sum[main] > sum[m] else m if len(self.pack[main]) < len(
                self.pack[m]) else main
        return main

    def getCardList(self):
        cards = []
        for m, c in self.pack.items():
            for c1 in c:
                cards.append(Card(m, c1))
        return cards


if __name__ == '__main__':
    # h = Hand('clubs', 'hearts')
    # h.sethand([Card('h', 'A', True), Card('h', 'J', True), Card('h', '7', True), Card('s', 'K', True)])
    # print(h.whogot())
    print(getBiggerThan(['7', '9', 'jack', 'queen'], 'ace'))
