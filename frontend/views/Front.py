import random
from tkinter import *

import backend.complayer.Player
from backend import CardPack
from backend.complayer import Player
from backend.CardPack import *
from scripts.Helper import image

# from playsound import playsound as mp3

hand = {}
status = ''
trumpPly = 3
pl1 = backend.complayer.Player.Player('Player 1')
pl2 = backend.complayer.Player.Player('Player 2')
pl3 = backend.complayer.Player.Player('Player 3')
realPlayer = backend.complayer.Player.Player('Real Player')
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
tw = 580
th = 420
cards = {}


def wins():
    print('Team 2 wins! You win :)')


def lost():
    print('Team 1 wins! You lost :(')


def suffle():
    print('card pack')
    c = CardPack.cardpack()
    print(c)
    for v in CardPack.mainCards:
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
                    Player.trump = pl1.saytrump()
                pl1.cards[main].append(card)
            elif v == 1:
                if i == 4 and trumpPly == 1:
                    print(pl3.cards)
                    Player.trump = pl3.saytrump()
                pl2.cards[main].append(card)
            elif v == 2:
                if i == 4 and trumpPly == 2:
                    print(pl2.cards)
                    Player.trump = pl2.saytrump()
                pl3.cards[main].append(card)
            elif v == 3:
                if i == 4 and trumpPly == 3:
                    print("You are to say trump\n" + str(realPlayer.cards))
                    tc = 0
                    # img = image('cards/' + CardPack.getcard(realPlayer.cards) + '_of_' + card.getmain() + '.png',
                    #             width, height)
                    choose=(c1,c2,c3,c4)
                    for k,v in realPlayer.cards.items():
                        for card in v:
                            img = image(
                                'cards/' + card + '_of_' + CardPack.getCardNameByLetter(k) + '.png',
                                width, height)
                            choose[tc].config(image=img,command=lambda c=card:{sel_trump(c)})
                            tc+=1
                    while True:
                        if not Player.trump == '':
                            break
                    # c1.config(image=img)
                    # c2.config(image=img)
                    # c3.config(image=img)
                    # c4.config(image=img)
                    Player.trump = tc
                realPlayer.cards[main].append(card)
            c[main].remove(card)
    addpack(realPlayer.cards)

def sel_trump(card):
    Player.trump=card

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





def showhand():
    print(f'current hand :\n\tPlayer ====== Card')
    for k, v in hand.items():
        print('\t', k, '\t', str(v))


def addpack(hand):
    for main, v in hand.items():
        for card in v:
            c= CardPack.Card(main, card)
            cards[c] = c.getImage()
    for c, im in cards.items():
        b1=Button(playerCards, image=im, bg='white')
        b1.config(command=lambda c1=c,b=b1:[{addcard(c1, c3)},playerCards.winfo_children().remove(b)])
        b1.pack(side=LEFT)
    playerCards.pack(side=BOTTOM)


def addcard(card, c):
    # threading.Thread(target=lambda: mp3(sound='MP3/putcard.mp3'), args=()).start()
    img = card.getImage()
    c.configure(image=img)
    c.image = img


def init():
    frame.destroy()
    label.destroy()
    c1.place(x=tw / 2 - CardPack.width / 2, y=20)
    c2.place(x=tw - CardPack.width - 20, y=th / 2 - CardPack.height / 2)
    c3.place(x=tw / 2 - CardPack.width / 2, y=th - CardPack.height - 20)
    c4.place(x=20, y=th / 2 - CardPack.height / 2)
    table.pack()
    playerCards.pack(side=BOTTOM)
    suffle()


w = Tk()

w.geometry("1000x600")
w.config(bg='gray')
cimage = image('backgrounds/aces.jpg', 600, 600)
label = Label(w, image=cimage)
label.pack(side=LEFT)
frame = Frame(w, bg='black')
frame.pack()
Label(frame, text='Ommi', font=('Arial', 60, 'bold')).grid(row=0, column=1)
Button(frame, text='Play', font=('Arial', 30, 'bold'), command=init).grid(row=4, column=1)
table = Frame(w, background='green', width=tw, height=th)
c1 = Button(table, bg='green', text='card 1',state=ACTIVE,activeforeground='green',activebackground='green',bd=0)
c2 = Button(table, bg='green', text='card 2',state=ACTIVE,activeforeground='green',activebackground='green',bd=0)
c3 = Button(table, bg='green', text='card 3',state=ACTIVE,activeforeground='green',activebackground='green',bd=0)
c4 = Button(table, bg='green', text='card 4',state=ACTIVE,activeforeground='green',activebackground='green',bd=0)
playerCards = Frame(w, bg='black', width=CardPack.width * 8, height=CardPack.height)
card = CardPack.Card('hearts', 'A')
cardlabels = card.getImage()
c1.config(image=cardlabels)
c2.config(image=cardlabels)
c3.config(image=cardlabels)
c4.config(image=cardlabels)

w.mainloop()

addpack({'hearts': ['7', 'J'], 'diamonds': ['A', '10'], 'spades': ['A'], 'clubs': ['Q', '7', 'K']})
