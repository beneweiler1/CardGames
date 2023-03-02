#ride the bus simulation
from deck import Card, Deck, Player
import deck
import random
#create deck
#assign players
#use their hand?


#guess red or black
#pop card from deck (guess, actual) - return bool

#guess hi/low 
#pop card from deck - return bool

#guess in or out
#pop card from deck - return bool

#guess suite
#pop card from deck - return bool


class RTB:
    def __init__(self):
        self.players = []
        self.deck = Deck()
        self.deck.shuffle()

    def addPlayer(self, name):
        self.players.append(Player(name))

    def getPlayer(self,name):
        for p in self.players:
            if name == p.getName():
                return p
        print('player does not exist')

    def hit(self, name):
        p = self.getPlayer(name)
        p.draw(self.deck)

    def newRound(self):
        #self.turn += 1 ## increase cards handed each turn
        #self.deck.build()
        self.deck.shuffle()
        for p in self.players:
            p.resetHand()
            for r in range (0, self.handSize):
                p.draw(self.deck)
            print(p.getName())
            p.showHand()
    #red or black check
    def RoundOneCheck(self, guess, hand):
        card = hand[0]
        blackSuite = ["Spades", "Clubs"]
        if guess == "black" and card.getSuite() in blackSuite:
            return True
        if guess == "red" and card.getSuite() not in blackSuite:
            return True
        else:
            return False

    #hi low check
    def RoundTwoCheck(self, guess, hand):
        c1 = hand[0].getVal()
        c2 = hand[1].getVal()
        if c2 > c1 and guess == "high":
            return True
        if c2 < c1 and guess == "low":
            return True
        return False

    #InOutCheck
    def RoundThreeCheck(self, guess, hand):
        c1 = hand[0].getVal()
        c2 = hand[1].getVal()
        c3 = hand[2].getVal()
        if c3 == c1 or c3 == c2:
            return False
        if c3 in range(c1, c2) and guess == "in":
            return True
        if c3 not in range(c1,c2) and guess == "out":
            return True
        return False
        #SuiteCheck
    def RoundFourCheck(self, guess, hand):
        if (guess == hand[3].getSuite()):
            return True
        return False


class RTBGame:
    def __init__(self):
        self.rtb = RTB()
        self.rtb.addPlayer("P1")
        self.hand = self.rtb.getPlayer("P1").getHand()
        self.colors = ["red", "black"]
        self.hiLows = ["high", "low"]
        self.inOut = ["in", "out"]
        self.suites = ["Spades", "Clubs", "Hearts", "Diamonds"]

    def StartRandomBot(self):
        iterations = 0
        while True:
            self.rtb.getPlayer("P1").resetHand()
            self.hand = self.rtb.getPlayer("P1").getHand()
            iterations += 1
            choice = random.choice(self.colors)
            self.rtb.hit("P1")
            #Round 1
            if self.rtb.RoundOneCheck(choice, self.hand):
                choice = random.choice(self.hiLows)
                self.rtb.hit("P1")
                #Round 2
                if self.rtb.RoundTwoCheck(choice, self.hand):
                    choice = random.choice(self.inOut)
                    self.rtb.hit("P1")
                    #Round 3
                    if self.rtb.RoundThreeCheck(choice, self.hand):
                        choice = random.choice(self.suites)
                        self.rtb.hit("P1")
                        #Round 4
                        if self.rtb.RoundFourCheck(choice, self.hand):
                            return iterations
                            break
            if iterations % self.rtb.deck.getSize():
                self.rtb.deck = Deck()
                self.rtb.deck.shuffle()

    def StartProbabilityBot(self):
        redCardCount = 0
        blackCardCount = 0

        iterations = 0
        while True:
            self.rtb.getPlayer("P1").resetHand()
            self.hand = self.rtb.getPlayer("P1").getHand()
            iterations += 1
            if redCardCount == 0 and blackCardCount == 0: #chose random for new deck
                choice = random.choice(self.hiLows)
            else: # pick most probable choice
                if redCardCount > blackCardCount:
                    choice = "black"
                else:
                    choice = "red"
            self.rtb.hit("P1")
            #increment red and black count
            if self.hand[0].getSuite() == "black":
                blackCardCount += 1
            else:
                redCardCount += 1
            #Round 1
            if self.rtb.RoundOneCheck(choice, self.hand):
                if self.hand[0].getVal > 7:
                    choice = "low"
                else:
                    choice = "high"               

                self.rtb.hit("P1")
                #increment red and black count
                #if self.rtb.RoundOneCheck("black", self.hand):
                if self.hand[1].getSuite() == "black":
                    blackCardCount += 1
                else:
                    redCardCount += 1 
                    
                #Round 2
                if self.rtb.RoundTwoCheck(choice, self.hand):
                    #calculate difference between c1 and c2
                    diff = abs(self.hand[0].getVal(), self.hand[1].getVal())
                    if diff >= 7:
                        choice = "in"
                    else:
                        choice = "out"

                    self.rtb.hit("P1")
                    if self.hand[2].getSuite() == "black":
                        blackCardCount += 1
                    else:
                        redCardCount += 1 
                    #Round 3
                    if self.rtb.RoundThreeCheck(choice, self.hand):
                        if blackCardCount >= redCardCount:
                            choice = "red"
                        else:
                            choice = "black"
        
                        self.rtb.hit("P1")
                        if self.hand[3].getSuite() == "black":
                            blackCardCount += 1
                        else:
                            redCardCount += 1
                        #Round 4
                        if self.rtb.RoundFourCheck(choice, self.hand):
                            return iterations
                            break

            if iterations % self.rtb.deck.getSize():
                self.rtb.deck = Deck()
                self.rtb.deck.shuffle()


                
rg = RTBGame()
avg = 0
for x in range(0,999):
    avg += rg.StartProbabilityBot()
print(avg/999)
