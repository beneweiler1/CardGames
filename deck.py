import random

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
        for s in ["Spades", "Clubs", "Diamonds", "Hearts"]:
            for v in range (1,14):
                self.cards.append(Card(s,v))
            #self.cards.append(Card('W','W')) #wizard
            #self.cards.append(Card('J','J')) #joker
    def show(self):
        for c in self.cards:
            c.show()

    def shuffle(self):
        random.shuffle(self.cards)
    
    def drawCard(self):
        return self.cards.pop()

class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.sum = 0

    def draw(self, deck):
        self.hand.append(deck.drawCard())
        return self

    def getName(self):
        return self.name

    def showHand(self):
        for card in self.hand:
            card.show() 

    def getSum(self):
        self.sum = 0
        for card in self.hand:
            self.sum = self.sum + card.getVal()
        return self.sum
        
    def getHand(self):
        for card in self.hand:
            print(card.getCard())

    def resetHand(self):
        self.hand = []

class Game():
    def __init__(self):
        self.players = []
        self.deck = Deck()
        self.turn = 2

    def addPlayer(self, name):
        player = Player(name)
        self.players.append(player)

    def getPlayer(self,name):
        for p in self.players:
            if name == p.getName():
                return p
        print('player does not exist')

    def newRound(self):
        #self.turn += 1 ## increase cards handed each turn
        self.deck = Deck()
        self.deck.shuffle()
        for p in self.players:
            p.resetHand()
        for p in self.players:
            p.resetHand()
            for r in range (0, self.turn):
                p.draw(self.deck)
            print(p.getName())
            p.showHand()
        

    def checkSum(self):
        for p in self.players:
            print(p.getSum())
        #give player a null val if over 21

    def hit(self, name):
        p = self.getPlayer(name)
        p.draw(self.deck)
        p.showHand()

G1 = Game()
G1.addPlayer("Ben")
G1.addPlayer("G")
G1.newRound()
G1.checkSum()
G1.hit("Ben")