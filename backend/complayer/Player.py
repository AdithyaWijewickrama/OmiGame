from backend import CardPack
from backend.CardPack import CardSet, getBiggest, getBiggerThan, Card
from database.sql import Database
from scripts.Helper import removelistfromlist

__id=0

class Player:

    def __init__(self, name, game):
        self.cards = CardPack.emptypack()
        self.game = game
        self.put = None
        self.op = None
        self.id = globals()['__id']
        globals()['__id'] += 1
        self.name = name
        self.trumptimes = 0
        self.score = 0
        self.seencards = {}
        for m in CardPack.mainCards:
            self.seencards[m] = False

    def setopponent(self, op):
        self.op = op

    def saytrump(self, cards=None):
        return CardPack.CardSet(cards if cards else self.cards).getworthmain()

    def getnext(self, hand):
        print(f'Hand:\n{self.cards}')
        card = ''
        sumofleft = CardSet().sumofcards(self.game.leftcards)
        summycards = CardSet().sumofcards(self.cards)
        selected_main = ''
        selected_card = ''
        my_turn = hand.len + 1
        main = hand.main
        if len(list(self.cards.values())) == 1:
            print('len==1:')
            selected_main = list(self.cards.keys())[0]
            selected_card = list(self.cards.values())[0][0]
        elif main == '':
            print('main==\'\':')
            a = {}
            for m in CardPack.mainCards:
                for c in CardPack.cards[::-1]:
                    if self.havemain(m):
                        if c in self.cards[m]:
                            bst = CardSet().getbiggest([c] + self.game.leftcards[m])
                            if bst in self.cards[m]:
                                if m in list(a.keys()):
                                    del a[m]
                                a[m] = [bst, sumofleft[m] - summycards[m]]
            print('a=', a)
            i = 0
            for m, v in a.items():
                if v[1] > i:
                    selected_main = m
                    selected_card = v[0]
            if selected_main == '':
                card = self.getworthless()
        elif self.havemain(main):
            print('have main:')
            cut = ((hand.main != self.game.trump) and (self.game.trump in list(hand.getPackFromCards().keys())))
            got = hand.whogot()
            selected_main = main
            biggest_my = CardSet().getbiggest(self.cards[main])
            biggest_hand = CardSet().getbiggest(hand.getPackFromCards()[main])
            biggest_left = CardSet().getbiggest(self.game.leftcards[main])
            lowest_my = CardSet().getlowest(self.cards[main])
            # lowest_hand = CardSet().getlowest(hand.getcardsaspack()[main])
            # lowest_left = CardSet().getlowest(self.game.leftcards[main])
            if not cut:
                if my_turn == 2:
                    if getBiggest(biggest_left, biggest_hand) == biggest_my:
                        selected_card = biggest_my
                    else:
                        selected_card = lowest_my
                elif my_turn == 3:
                    if got == self.op:
                        if self.game.players()[self.game.getNextPlayerRelativeTo(self.id)].seencards[main] or getBiggest(
                                biggest_left,
                                biggest_hand) == biggest_hand or (
                                getBiggest(biggest_left, biggest_my) == biggest_my and CardSet().getbiggest(
                            removelistfromlist(self.game.leftcards[main], self.cards[main]) + [
                                biggest_hand]) == biggest_hand):
                            selected_card = lowest_my
                        else:
                            selected_card = biggest_my
                            # if getbiggest(biggest_left, biggest_hand) == biggest_my:
                    else:
                        if getBiggerThan(self.cards[main], CardSet().getbiggest(hand.getPackFromCards()[main])) in self.cards[
                            main]:
                            selected_card = getBiggerThan(self.cards[main],
                                                          CardSet().getbiggest(hand.getPackFromCards()[main]))
                        elif getBiggest(biggest_hand, biggest_my) == biggest_my:
                            selected_card = biggest_my
                        else:
                            selected_card = lowest_my
                else:
                    if got == self.op:
                        selected_card = lowest_my
                    elif getBiggerThan(self.cards[main], CardSet().getbiggest(hand.getPackFromCards()[main])) in self.cards[
                        main]:
                        selected_card = getBiggerThan(self.cards[main], CardSet().getbiggest(hand.getPackFromCards()[main]))
                    elif getBiggest(biggest_hand, biggest_my) == biggest_my:
                        selected_card = biggest_my
                    else:
                        selected_card = lowest_my
            else:
                selected_card = lowest_my
        elif not self.havemain(main):
            print('ha not main:')
            cut = ((hand.main != self.game.trump) and (self.game.trump in list(hand.getPackFromCards().keys())))
            got = hand.whogot()
            self.seencards[main] = True
            biggest_hand = CardSet().getbiggest(hand.getPackFromCards()[main])
            if self.game.haveleftcards(main):
                biggest_left = CardSet().getbiggest(self.game.leftcards[main])
            else:
                biggest_left = ''
            # lowest_hand = CardSet().getlowest(hand.getcardsaspack()[main])
            # lowest_left = CardSet().getlowest(self.game.leftcards[main])
            if main == self.game.trump:
                card = self.getworthless()
            elif cut:
                if self.havemain(self.game.trump):
                    if my_turn == 3 or my_turn == 4:
                        if got == self.op:
                            card = self.getworthless()
                        else:
                            if getBiggerThan(self.cards[self.game.trump],
                                             CardSet().getbiggest(hand.getPackFromCards()[self.game.trump])) in \
                                    self.cards[self.game.trump]:
                                selected_main = self.game.trump
                                selected_card = getBiggerThan(self.cards[self.game.trump],
                                                              CardSet().getbiggest(hand.getPackFromCards()[self.game.trump]))
                            else:
                                card = self.getworthless()
                    else:
                        selected_main = self.game.trump
                        if self.game.players()[self.game.getNextPlayerRelativeTo(self.id)].seencards[self.game.trump] or not \
                                self.game.players()[self.game.getNextPlayerRelativeTo(self.id)].seencards[main]:
                            selected_card = CardSet().getlowest(self.cards[self.game.trump])
                        else:
                            selected_card = CardSet().getbiggest(self.cards[self.game.trump])
                else:
                    card = self.getworthless()
            else:
                if self.havemain(self.game.trump):
                    if my_turn == 3 or my_turn == 4:
                        if got == self.op:
                            if my_turn == 3:
                                if getBiggest(biggest_left, biggest_hand) == biggest_left:
                                    selected_main = self.game.trump
                                    selected_card = CardSet().getlowest(self.cards[self.game.trump])
                                else:
                                    card = self.getworthless()
                            if my_turn == 4:
                                card = self.getworthless()
                        else:
                            selected_main = self.game.trump
                            if self.game.players()[self.game.getNextPlayerRelativeTo(self.id)].seencards[self.game.trump]:
                                selected_card = CardSet().getlowest(self.cards[self.game.trump])
                            else:
                                selected_card = CardSet().getbiggest(self.cards[self.game.trump])
                    else:
                        selected_main = self.game.trump
                        if self.game.players()[self.game.getNextPlayerRelativeTo(self.id)].seencards[self.game.trump] or not \
                                self.game.players()[self.game.getNextPlayerRelativeTo(self.id)].seencards[main]:
                            selected_card = CardSet().getlowest(self.cards[self.game.trump])
                        else:
                            selected_card = CardSet().getbiggest(self.cards[self.game.trump])
                else:
                    card = self.getworthless()
        if card == '':
            card = Card(selected_main, selected_card)
        print('Got next card ', card)
        return card

    def removecard_(self, card):
        self.cards[card.m()].remove(card.c())
        if len(self.cards[card.m()]) == 0:
            del self.cards[card.m()]

    def havemain(self, main):
        if main in list(self.cards.keys()):
            if len(self.cards[main]) > 0:
                return True

    def getworthless(self):
        print('Getting worthless:')
        print('My cards', self.cards)
        print('left cards:', self.game.leftcards)
        if len(self.cards.keys()) == 1:
            selected_main = list(self.cards.keys())[0]
        else:
            sumofleft = CardSet().sumofcards(self.game.leftcards)
            summycards = CardSet().sumofcards(self.cards)
            a = {}
            for m, c in self.cards.items():
                a[m] = sumofleft[m] - summycards[m]
            print('a=', a)
            i = list(a.values())[0]
            selected_main = list(a.keys())[0]
            for m, v in a.items():
                if v < i and m != self.game.trump:
                    selected_main = m
        print('Got worthless:', Card(selected_main, CardSet().getlowest(self.cards[selected_main])))
        return Card(selected_main, CardSet().getlowest(self.cards[selected_main]))

    def __str__(self):
        return f"""[NAME]{self.name} details:\t\n[OPPONENT]{self.op.name}\t\n[PACK]{self.cards}"""


class PlayerData:
    def __init__(self):
        pass

    def getvalue(self, key):
        return Database.getInstance().getSingleObject(f"select value from player_data where id=?", (key,))

    def update(self, key, val):
        if key is None:
            return
        return Database.getInstance().execute(f"update player_data set value=? where id=?", (val, key))

    def addnew(self, key, val):
        if key is None:
            return
        Database.getInstance().execute(f"insert into player_data (?,?)", (val, key))
