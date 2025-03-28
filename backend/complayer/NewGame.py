import random

from backend import CardPack
from backend.CardPack import Card
from backend.complayer.Player import Player

class Score:
    def __init__(self):
        self.score_8, self.score_10, self.tot_score_8 = (0, 0, 0)
        self.timesWon = 0


class Team:
    def __init__(self, ply01, ply02):
        self.player1 = ply01
        self.player2 = ply02
        self.score = Score()


class NewGame:
    def __init__(self):
        self.trumpPly = 3
        self.firstplay = self.trumpPly
        self.turn = self.firstplay
        self.trump = ''
        self.leftcards = CardPack.cardpack()
        self.mainrounds, self.rounds_8, self.rounds_4, self.drawrounds = (0, 0, 0, 0)
        self.__id = 0
        self.currentHand = CardPack.Hand('')
        self.player1 = Player('Player 01', self)
        self.player2 = Player('Player 02', self)
        self.player3 = Player('Player 03', self)
        self.playerYou = Player('You', self)
        self.setTeam(self.player1, self.player3)
        self.setTeam(self.player2, self.playerYou)
        self.tot_rounds_4 = 0

    def suffle(self):
        self.leftcards = CardPack.cardpack()
        pack = []
        temp = CardPack.cardpack()
        for j in range(4):
            for i in range(8):
                main = list(temp.keys())[random.randint(0, len(temp) - 1)]
                while len(temp[main]) == 0:
                    del temp[main]
                    main = list(temp.keys())[random.randint(0, len(temp) - 1)]
                card = Card(main, temp[main][random.randint(0, len(temp[main]) - 1)])
                pack.append(card)
                temp[main].remove(card.c())

        for p in self.players():
            p.cards = CardPack.emptypack()
            for i in range(8):
                idx = random.randint(0, len(pack) - 1)
                c = pack[idx]
                p.cards[c.m()].append(c.c())
                del pack[idx]
            for i in CardPack.mainCards:
                if len(p.cards[i]) == 0:
                    del p.cards[i]
            print(p.name, '\n', p.cards)

    def players(self):
        return [self.player1, self.player2, self.player3, self.playerYou]

    def setTeam(self, pl1, pl2):
        pl1.setopponent(pl2)
        pl2.setopponent(pl1)

    def printPlayers(self):
        for p in self.players():
            print(p)

    def setTrump(self):
        trumpCards = []
        cards = CardPack.CardSet(self.players()[self.trumpPly].cards).getCardList()
        self.players()[self.trumpPly].trumptimes += 1
        for i in range(4):
            j = random.randint(0, len(cards) - 1)
            trumpCards.append(cards[j])
            del cards[j]
        if self.trumpPly != 3:
            trumpCards_ = CardPack.emptypack()
            for c in trumpCards:
                trumpCards_[c.m()].append(c.c())
            self.trump = self.players()[self.trumpPly].saytrump(trumpCards_)
            self.currentHand = CardPack.Hand(self.trump)
        else:
            return trumpCards

    def removecard(self, card):
        if card.m() in self.leftcards.keys():
            if card.c() in self.leftcards[card.m()]:
                self.leftcards[card.m()].remove(card.c())
        if card.m() in self.leftcards:
            if len(self.leftcards[card.m()]) == 0:
                del self.leftcards[card.m()]

    def haveleftcards(self, main):
        if main in self.leftcards:
            if len(self.leftcards[main]) > 0:
                return True
        return False

    def getNextPlayerRelativeTo(self, player):
        return 0 if player == 3 else player + 1

    def getNextPlayer(self):
        current = self.firstplay + self.rounds_4 if self.firstplay + self.rounds_4 < 4 else 4 - (
                self.firstplay + self.rounds_4)
        return self.players()[current + 1 if current < 3 else 0]


if __name__ == '__main__':
    pass
