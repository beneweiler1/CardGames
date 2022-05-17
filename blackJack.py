from multiprocessing import Array
from pickletools import read_bytes1
import random
from stat import S_IFCHR
from nbformat import ValidationError
import numpy as np
import csv


with open('BJCS.csv', newline='') as f:
    reader = csv.reader(f)
    data = list(reader)

class Card:
    def __init__(self, suit, val):
        self.suit = suit
        self.val = val
    def show(self):
        print("{} of {}".format(self.val, self.suit))

    def getSuite(self):
        return self.suit

    def getVal(self):
        return self.val

    def getCard(self):
        return self.val, self.suit


class Deck:
    def __init__(self):
        self.cards = []
        self.build()

    def build(self):
        for s in ["Spades", "Clubs", "Diamonds", "Hearts"]: #where is ace
            for v in range (1,14):
                if v < 10:
                    self.cards.append(Card(s,v))
                else:
                    self.cards.append(Card(s,10))
            #self.cards.append(Card('W','W')) #wizard
            #self.cards.append(Card('J','J')) #joker
    def show(self):
        for c in self.cards:
            c.show()

    def shuffle(self):
        random.shuffle(self.cards)
    
    def drawCard(self):
        return self.cards.pop()
    
    def removeCard(self, val):
        for c in self.cards:
            if c.getVal() == val:
                self.cards.remove(c)

class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.sum = 0
        self.win = -1

    def getWin(self):
        return self.win

    def changeWin(self, val):
        self.win = val

    def draw(self, deck):
        self.hand.append(deck.drawCard())
        return self

    def getName(self):
        return self.name

    def showHand(self):
        for card in self.hand:
            card.show() 

    def setHand(self,deck,c1,c2):
        self.sum = c1 + c1
        card1 = Card("Spades",c1)
        card2 = Card("Hearts", c2) 
        self.hand.append(card1)
        self.hand.append(card2)
        deck.removeCard(c1)
        deck.removeCard(c2)


    def getSum(self):
        self.sum = 0
        self.aces = 0
        for card in self.hand:
            if card.getVal() == 1:
                self.aces += 1
            else:
                self.sum = self.sum + card.getVal()

        if self.sum + self.aces <= 21: #account for when we are given another ace?
            if self.aces > 0:
                if (self.sum + (11*self.aces) <= 21): #two aces
                    return (self.sum + (11*self.aces))
                elif((self.sum + 10 + self.aces) <= 21):
                    return self.sum + self.aces
                elif (self.sum + self.aces) <= 21:
                    return self.sum + self.aces
            else: 
                return self.sum
        else:
            return -1
        
    def printHand(self):
        for card in self.hand:
            print(card.getCard())

    def getHand(self):
        currentHand = []
        for card in self.hand:
            currentHand.append(card.val)
        return currentHand

    def resetHand(self):
        self.hand = []
        self.win = -1

    def countAces(self):
        return self.hand.count(1)

class Game():
    def __init__(self):
        self.players = []
        self.deck = Deck()
        self.turn = 2
        self.dealer = Player("Dealer")
        self.players.append(self.dealer)

    def addPlayer(self, name):
        player = Player(name)
        self.players.append(player)

    def getPlayer(self,name):
        for p in self.players:
            if name == p.getName():
                return p
        print('player does not exist')

    def newRound(self):
        self.deck = Deck()
        self.deck.shuffle()
        for p in self.players:
            p.resetHand()
        for p in self.players:
            p.resetHand()
            for r in range (0, self.turn):
                p.draw(self.deck)
            #print(p.getName())
            #p.showHand()

    def customHand(self,name, c1,c2):
        player = self.getPlayer(name)
        player.setHand(self.deck, c1,c2)
        self.deck.shuffle()
        self.dealer.draw(self.deck)
        self.dealer.draw(self.deck)
        #give player exact cards and remove them from deck

    def playerSum(self,name):
        p = self.getPlayer(name)
        return p.getSum()

    def checkAllSum(self):
        for p in self.players:
            print(p.getSum())
        #give player a null val if over 21

    def dealerCompare(self, name):
        dSum = self.dealer.getSum()
        p = self.getPlayer(name)
        pSum = p.getSum()
        #print(pSum)
        if pSum == 21: #add case for face cards only
            #print('BlackJack!')
            p.changeWin(1)
            #return 1
        while True:
            dSum = self.dealer.getSum()
            #print('Dealer Sum:', dSum)
            if pSum == -1 or pSum <= dSum:
                p.changeWin(0)
                #print('You Lose')
                break
            elif dSum == -1:
                p.changeWin(1)
                #print('You Win')
                break
            elif pSum > dSum and dSum >= 17:
                p.changeWin(1)
                #print('You Win')
                break
            else:
                p.changeWin(1)
                #self.hit("Dealer")
                self.dealer.draw(self.deck) #check
                #print("Dealer: Hit")
        return p.getWin()

    def getCards(self,name):
        p = self.getPlayer(name)
        #print(name, p.getHand())
        return p.getHand()
    
    def getAces(self,name):
        p = self.getPlayer(name)
        return p.countAces()

    def hit(self, name):
        p = self.getPlayer(name)
        p.draw(self.deck)

def sigmoid(x):
    y = 1/x
    return 0.5/ (y*(1+ np.exp(-x)))

def machineBot(game,name): #30% win rate
        while True:
            pSum = game.playerSum(name) 
            #print('pSum:', pSum)
            if pSum == -1:
                #print('Bust!')
                break
            if sigmoid(pSum) <= 8:
                #print("Hit!")
                game.hit(name)
            else: 
                #print("Stay")
                break

def randoBot(game, name): #17%ish
    hit = np.random.randint(0,2)
    if hit == 1:
        #print("Hit!")
        game.hit(name)
    else: 
        print("Stay")

def statBot(game,name): #0.2878 percent lookin for 42.22
    cards = game.getCards(name)
    d1 = game.getCards("Dealer")[1] #dealer card 1
    while True:
        c1 = cards[0]
        c2 = cards[1]
        aces = game.getAces(name)
        pSum = game.playerSum(name)
        #print(game.playerSum(name))
        #print(c1,c2)
        if pSum == -1:
            #print('Bust')
            break
        elif pSum == 21:
            #print('BlackJack!')
            break
        else:
            if aces > 0:
                move = data[pSum - 19][d1] #check if correct
            else:
                move = data[pSum][d1]
            if move in 'HD':
                #print('Hit')
                game.hit(name)
            else:
                #print('Stand')
                break
    #look at sum and d1 to compare to index of table?


#maximizeBot 
    #gives dealer x card
    #gives player a sum of 20 down to 2 
    #if 20 do not hit
    #compares to dealer
    #hits 100 times 
    #stands 100 times
    #compare wins and ocupy array value with H or S depending on outcome
    #change dealers card

def createArray():
    rows, cols = (20, 11)
    arr = [[0 for i in range(cols)] for j in range(rows)]   
    r1 = ['T','A',2,3,4,5,6,7,8,9,10]
    arr.insert(0,r1)
    np.savetxt("foo.csv", arr, delimiter=",", fmt="%s")
    return arr

def populateArray(arr):
    if len(arr) != 0:
        arr = createArray()
        H = ['H']*11
        arr.append(H)
        np.savetxt("foo.csv", arr, delimiter=",", fmt="%s")
        return arr

def modArray(arr, c1, c2, wr):
    if wr >= 0.5:
        arr[c1][c2] = 'S'
    else:
        arr[c1][c2] = 'H'
    np.savetxt("foo.csv", arr, delimiter=",", fmt="%s")

def simBot(arr, c1,c2):
    winRate = 0
    trials = 500
    for x in range(0,trials):
        G1 = Game()
        G1.addPlayer('Ben')
        G1.customHand('Ben', c1, c2)
        stat = G1.dealerCompare('Ben')
        winRate += stat
    winRate = winRate/trials
    print(winRate)
    modArray(arr,c1,c2,winRate)


# arr = createArray()
# arr = populateArray(arr)
# for x in range (1,11):
#     simBot(arr,1,x) #add set dealer show card
# def sumSimBot(game,name, state):
#     game.playerSum(name)
    
#     if state == 'hit':
#         game.hit(name)

#     row = [0]*11
#     row[0] = row[0]+1
#     np.savetxt("foo.csv", row, delimiter=",", fmt="%s")


wins = 0
for x in range (0,50000): #0.267
    g = Game()
    g.addPlayer("statBot")
    g.newRound()
    statBot(g,"statBot")
    #print(g.dealerCompare('statBot'))
    if (g.dealerCompare("statBot")):
        wins += 1
    g.newRound()

print(wins/50000)

# g = Game()
# while True:
#     g.addPlayer("statBot")
#     g.newRound()
#     if g.playerSum("randoBot") == -1:
#         break
#     if randoBot(g, "randoBot") == 1:
#         g.hit("randoBot")
#     else:
#         break
# print(g.playerSum("randoBot"))

# def learnBot(game, name):
    #Given hand 
    #determine P = c1x1 + c2x2 + dx3 + Bias
    #activation button for hit or stay
    #if hit return to activation for hit and stay