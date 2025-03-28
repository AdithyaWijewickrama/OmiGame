import random

from backend import CardPack, Player
from backend.CardPack import Card

status = ''
trumpPly = 3
pl1 = Player.Player('Player 1')
pl2 = Player.Player('Player 2')
pl3 = Player.Player('Player 3')
realPlayer = Player.Player('Real Player')
pl1.setopponent(pl2)
pl2.setopponent(pl1)
pl3.setopponent(realPlayer)
realPlayer.setopponent(pl3)
team1 = [pl1, pl2]
team2 = [pl3, realPlayer]
teams = {'team1': {'team': team1, 'score': 0}, 'team2': {'team': team2, 'score': 0}}
team1score = 0
team2score = 0

option = ''


def wins():
    print('Team 2 wins! You win :)')


def lost():
    print('Team 1 wins! You lost :(')


def suffle():
    print('card pack')
    c = CPack.cardpack()
    print(c)
    for v in CPack.mainCards:
        pl1.cards[v].clear()
        pl2.cards[v].clear()
        pl3.cards[v].clear()
        realPlayer.cards[v].clear()

    for v in range(4):
        for i in range(8):
            emk = set()
            for v1 in c.keys():
                if len(c[v1]) == 0:
                    emk.add(v1)
            for v2 in emk:
                c.pop(v2)
            main = list(c.keys())[random.randint(0, len(c.keys()) - 1)]
            card = list(c[main])[random.randint(0, len(c[main]) - 1)]
            if v == 0:
                if i == 4 and trumpPly == 0:
                    print(pl1.cards)
                    Player.trump = pl1.sayTrump()
                pl1.cards[main].append(card)
            elif v == 1:
                if i == 4 and trumpPly == 1:
                    print(pl3.cards)
                    Player.trump = pl3.sayTrump()
                pl2.cards[main].append(card)
            elif v == 2:
                if i == 4 and trumpPly == 2:
                    print(pl2.cards)
                    Player.trump = pl2.sayTrump()
                pl3.cards[main].append(card)
            elif v == 3:
                if i == 4 and trumpPly == 3:
                    print("You are to say trump\n" + str(realPlayer.cards))
                    tc = ''
                    while tc == '':
                        tc = getCard(input())
                    Player.trump = tc
                realPlayer.cards[main].append(card)
            c[main].remove(card)
    addpack(realPlayer.cards)


def addpack(hand):
    print('')
    # col = 0
    # for main, v in hand.items():
    #     for card in v:
    #         file = 'cards/' + getcard(card) + '_of_' + main+'.png'
    #         p = PhotoImage(file=file)
    #         p = p.subsample(4, 4)
    #         Button(master=w, image=p).pack(side=LEFT)
    #         # label.grid(row=0, column=col)
    #         col += 1
    # frame.pack(side=BOTTOM)


def getcard(s):
    i = s
    if i == 'A':
        i = 'ace'
    elif i == 'J':
        i = 'jack'
    elif i == 'K':
        i = 'king'
    elif i == 'Q':
        i = 'queen'
    return i


def showcardsofplayers():
    print('Real Player =' + str(realPlayer.cards))
    print('Player 1 =' + str(pl1.cards))
    print('Player 2 =' + str(pl2.cards))
    print('Player 3 =' + str(pl3.cards))
    print('trump ' + Player.trump)


def showstat():
    print('status ==========')
    print('Team 01', '\n\tplayers\t', team1[0].name + '\t' + team1[1].name, '\n\tscore\t', teams['team1']['score'])
    print('Team 02', '\n\tplayers\t', team2[0].name + '\t' + team2[1].name, '\n\tscore\t', teams['team2']['score'])


def getCard(i):
    if i == 'h':
        i = 'hearts'
    elif i == 's':
        i = 'spades'
    elif i == 'd':
        i = 'diamonds'
    elif i == 'c':
        i = 'clubs'
    else:
        i = ''
    return i


def showhand():
    print(f'current hand :\n\tPlayer ====== Card')
    for k, v in hand.items():
        print('\t', k, '\t', str(v))

while option != '2':
    print('===================OMI CARD GAME======================\nhearts-h\ndiamonds-d\nspades-s\nclubs-c')
    print('1.New game\n2.Exit')
    option = input()
    if option == '1':
        print("starting game..")
        while teams['team1']['score'] < 10 or teams['team2']['score'] < 10:
            suffle()
            first = trumpPly
            showstat()
            for gi in range(8):
                side = ''
                li = [0, 1, 2, 3][first:4]
                li.extend([0, 1, 2, 3][0:first])
                print('order ', li)
                hand = {'main': ''}
                for i in li:
                    if i == 0:
                        hand[pl1.name] = pl1.getnext(hand)
                        showhand()
                    elif i == 1:
                        hand[pl3.name] = pl3.getnext(hand)
                        showhand()
                    elif i == 2:
                        hand[pl2.name] = pl2.getnext(hand)
                        showhand()
                    elif i == 3:
                        while True:
                            showcardsofplayers()
                            print('Your card ')
                            c = list(input().split(' '))
                            print(c)
                            if len(c) != 2:
                                print('Invalid card\nValid cars are:\n\thearts-h\n\tdiamonds-d\n\tspades-s\n\tclubs-c')
                                for v in CardPack.cards:
                                    print('\t' + v)
                                print('You want to continue [y/n]')
                                if input() == 'n':
                                    exit(1)
                            elif getCard(c[0]) == '':
                                c = []
                            else:
                                c = Card(getCard(c[0]), c[1])
                                break
                            print(c)
                        hand[realPlayer.name] = c
                        hand['main'] = c.card['m']
                        realPlayer.cards[hand['main']].remove(c.card['c'])
                        Player.prepl = realPlayer.name
                    Player.puthand(hand)
                    side = Player.getside(hand)
                    if side == team1[0].name or side == team1[1].name:
                        team1score += 1
                    elif side == team2[0].name or side == team2[1].name:
                        team2score += 1
                first = 0 if side == pl1.name else 1 if side == pl2.name else 2 if side == pl3.name else 3
            if team1score == 8:
                teams['team1']['score'] += 3
                status = 'team1'
            elif team2score == 8:
                teams['team2']['score'] += 3
                status = 'team2'
            elif team2score == 4 and team1score == 4:
                status = 'equal'
            else:
                teams['team1']['score'] += 1 if trumpPly == 0 or trumpPly == 2 and status != 'equal' else 2
            # team1score=team1score+(1 if ) if Player.getside(hand)==team1[0] or Player.getside(hand)==team1[1] else team2score+1 if Player.getside(hand)==team2[0] or Player.getside(hand)==team2[0] else
            trumpPly = 0 if trumpPly == 3 else trumpPly + 1

