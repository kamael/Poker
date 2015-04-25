#!/usr/bin/env python

import random

class Poker:
    def __init__(self):
        self.cards = self.createCards()
        self.sendCards()

    def createCards(self):
        x = range(1, 55)
        random.shuffle(x)
        return x

    def cardNumToShow(self, x):
        colorName = ["Spade", "Heart", "Club", "Diamond"]
        JQK = ["J", "Q", "K"]
        if x == 53:
            return ("Joker", "Black")
        elif x == 54:
            return ("Joker", "Red")
        else:
            color = x / 13
            num = x % 13
            if num == 0:
                num = 13
                color -= 1
            if num == 1:
                num = "A"
            elif 10 < num < 14:
                num = JQK[num - 11]
            if type(num) != str:
                num = str(num)
            return (num, colorName[color])

    def __numToInnerValue(self, x):
        if x > 52:
            return x
        x = x % 13
        """
        if x == 0:
            x = 13
        if x < 3:
            return x + 20
        return x
        """
        if x == 2:
            x = 20
        elif x < 3:
            x = x + 13
        return x

    def sendCards(self):
        a = self.cards[0:51:3]
        b = self.cards[1:51:3]
        c = self.cards[2:51:3]
        p = self.cards[51:]
        l = a + b + c + p
        l = map(self.__numToInnerValue, l)
        self.aValue = l[:17]
        self.bValue = l[17:34]
        self.cValue = l[34:51]
        self.pValue = l[51:]
        self.aList = map(self.cardNumToShow, a)
        self.bList = map(self.cardNumToShow, b)
        self.cList = map(self.cardNumToShow, c)
        self.pList = map(self.cardNumToShow, p)

    def cardPrint(self):
        print self.aList
        print self.bList
        print self.cList
        print self.pList

    def cardnumPrint(self):
        a = map(lambda x: x[0], self.aList)
        b = map(lambda x: x[0], self.bList)
        c = map(lambda x: x[0], self.cList)
        p = map(lambda x: x[0], self.pList)

        print a
        print b
        print c
        print p

    def cardvaluePrint(self):
        print sorted(self.aValue)
        print sorted(self.bValue)
        print sorted(self.cValue)
        print sorted(self.pValue)


class Agent():

    def __init__(self, values):
        self.values = values
        self.update()

    def send(self, value):
        values_bak = self.values
        for i in value:
            try:
                self.values.remove(i)
            except ValueError:
                print "value %s not in Agent's list"
                self.values = values_bak
                return False
        self.update()
        return True

    def add(self, value):
        self.values += value
        self.update()

    def update(self):
        self.__process()


    def __process(self):
        self.values.sort()

        self.singles = set()
        self.twices = set()
        self.triples = set()
        self.fours = set()

        self.shunzi_s = []
        self.shunzi_ss = []
        self.shunzi_sss = []


        numbers = set(self.values)

        for i in numbers:
            i_count = self.values.count(i)

            if i_count == 4:
                self.fours.add(i)
            if i_count >= 3:
                self.triples.add(i)
            if i_count >= 2:
                self.twices.add(i)
            self.singles.add(i)


        base_shunzi = [sorted(list(self.singles)),
                       sorted(list(self.twices)),
                       sorted(list(self.triples))]
        store_shunzi = [self.shunzi_s, self.shunzi_ss, self.shunzi_sss]
        len_shunzi = [5, 3, 2]

        for i in range(3):
            if not base_shunzi[i]:
                continue
            start = base_shunzi[i][0]
            n = 1

            for j in base_shunzi[i]:
                if j == start:
                    pass
                elif j == start + 1:
                    n += 1
                else:
                    if n >= len_shunzi[i]:
                        store_shunzi[i].append([start - n + 1, n])
                    n = 1

                start = j

            if n >= len_shunzi[i]:
                store_shunzi[i].append([start - n + 1, n])

    def choose_dz(self, pValue):
        if random.randint(0, 2) == 0:
            self.add(pValue)
            return True
        return False

    def action(self, game):
        i = 1
        b = 2


        if random.randint(0, 30) == 0:
            game.end = True




class Game():
    def __init__(self):
        self.end = False
        self.winner = None
        self.poker = Poker()
        self.ag1 = Agent(self.poker.aValue)
        self.ag2 = Agent(self.poker.bValue)
        self.ag3 = Agent(self.poker.cValue)
        self.agents = [self.ag1, self.ag2, self.ag3]

        self.dz_index = None
        self.__choose_dz()

    def __choose_dz(self):
        did = False
        for i in range(3):
            did = self.agents[i].choose_dz(self.poker.pValue)
            if did:
                self.dz_index = i
                break
        if not did:
            self.winner = -1
            self.dz_index = -1
            self.end = True



def main():
    game = Game()
    print "dz: %d" % game.dz_index
    for i in range(3):
        cur = (i + game.dz_index) % 3
        print "%d has: %s" % (cur, str(game.agents[cur].values))

    while not game.end:
        for i in range(3):
            cur = (i + game.dz_index) % 3
            print "agent %d is action" % cur
            game.agents[cur].action(game)
            if game.end:
                game.winner = cur
                break

    print "end"
    print "winner: %d" % game.winner


def main1():
    #ag = Agent([3, 5, 5, 6, 7, 8, 8, 9, 9, 10, 10, 10, 11, 11, 14, 20, 20])
    #print ag.shunzi_ss
    #ag = Agent([3, 3, 4, 4, 4, 5, 5, 6, 7, 7, 7, 10, 11, 11, 12, 13, 13])
    #print ag.shunzi_ss
    #ag = Agent([3, 3, 4, 4, 4, 5, 5, 6, 7, 7, 7, 10, 11, 11, 12, 12, 13, 13])
    #print ag.shunzi_ss
    #ag = Agent([3, 3, 4, 4, 4, 5, 5, 6, 7, 7, 7, 10, 11, 11, 12, 12, 12, 13, 13, 13])
    #print ag.shunzi_ss
    #print ag.shunzi_sss
    #ag = Agent([3, 3, 4, 5, 5, 6, 6, 7, 8, 9, 9, 10, 11, 11, 12, 12, 13, 13, 20, 20])
    #print ag.shunzi_ss

    poker = Poker()
    Ag1 = Agent(poker.aValue)
    Ag2 = Agent(poker.bValue)
    Ag3 = Agent(poker.cValue)
    Ag1.add(poker.pValue)

    for item in [Ag1, Ag2, Ag3]:
        print sorted(item.values)
        print item.singles
        print item.twices
        print item.triples
        print item.fours
        print item.shunzi_s
        print item.shunzi_ss
        print item.shunzi_sss




if __name__ == "__main__":
    main()
