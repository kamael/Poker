#!/usr/bin/env python

import random
import sys


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

    def __init__(self, values, index):
        self.index = index
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

        self.fours = sorted(list(self.fours))
        self.triples = sorted(list(self.triples))
        self.twices = sorted(list(self.twices))
        self.singles = sorted(list(self.singles))


    def choose_dz(self, pValue):
        if random.randint(0, 2) == 0:
            self.add(pValue)
            return True
        return False

    def empty(self):
        return self.values == []

    def get_value_by_type(self, poker_type):
        if poker_type[0] == "singles":
            return poker_type[1]
        if poker_type[0] == "twices":
            return poker_type[1] * 2
        if poker_type[0] == "triples":
            return [poker_type[1][0]] * 3 + \
                [poker_type[1][1][0]] * poker_type[1][1][1]
        if poker_type[0] == "fours":
            return poker_type[1] * 4
        #
        return []


    def action(self, game):
        # return a list of put out pokers' value and type
        print "Agent need has a action"
        sys.exit()

"""
type:
    [53, 54]                        -> ["jokers", []]
    [3]                             -> ["singles", [3]]
    [3, 3]                          -> ["twices", [3]]
    [3, 3, 3, 4, 4]                 -> ["triples", [3, [4, 2]]]
    [3, 3, 3, 3]                    -> ["fours", [3]]
    [3, 4, 5, 6, 7]                 -> ["shunzi_s", [3, 5]]
    [3, 3, 3, 4, 4, 4, 5, 5, 6, 6]  -> ["shunzi_sss",
                                        [[3, 2], [5, 2], [6, 2]]
                                        ]
"""


class AgentBot(Agent):
    def action(self, game):

        two_jokers = False
        fours = []
        shunzi_sss = []
        shunzi_ss = []
        shunzi_s = []
        triples = []
        twices = []
        singles = []

        values = [i for i in self.values]

        jokers = []

        if 54 in self.values:
            self.send([54])
            jokers.append(54)
        if 53 in self.values:
            self.send([53])
            jokers.append(53)
        if len(jokers) == 2:
            print "has two jokers"
            two_jokers = True
        else:
            self.add(jokers)

        if len(self.fours):
            print "has fours: %s" % self.fours
            fours = [i for i in self.fours]
            for item in self.fours:
                self.send([item] * 4)

        if len(self.shunzi_sss):
            print "has shunzi_sss: %s" % self.shunzi_sss
            shunzi_sss = [i for i in self.shunzi_sss]
            for item in self.shunzi_sss:
                self.send([i for i in range(item[0], item[0] + item[1])] * 3)

        if len(self.shunzi_ss):
            print "has shunzi_ss: %s" % self.shunzi_ss
            shunzi_ss = [i for i in self.shunzi_ss]
            for item in self.shunzi_ss:
                self.send([i for i in range(item[0], item[0] + item[1])] * 2)

        if len(self.shunzi_s):
            print "has shunzi_s: %s" % self.shunzi_s
            shunzi_s = [i for i in self.shunzi_s]
            for item in self.shunzi_s:
                self.send([i for i in range(item[0], item[0] + item[1])])

        if len(self.triples):
            print "has triples: %s" % self.triples
            triples = [i for i in self.triples]
            for item in self.triples:
                self.send([item] * 3)

        if len(self.twices):
            print "has twices: %s" % self.twices
            twices = [i for i in self.twices]
            for item in self.twices:
                self.send([item] * 2)

        if len(self.singles):
            print "has singles: %s" % self.singles
            singles = [i for i in self.singles]
            for item in self.singles:
                self.send([item])

        if len(self.values):
            raise

        self.add(values)

        send = [None, None]





        if not game.puts or game.puts[-1][0] == self.index:
            #MUST SEND POKER
            if singles:
                send = ["singles", [singles[0]]]
            elif twices:
                send = ["twices", [twices[0]]]
            elif shunzi_sss:
                pass

        else:
            last = game.puts[-1][1]
            if last[0] == 'singles':
                value = last[1][0]
                i = 0
                while i < len(singles):
                    if singles[i] > value:
                        send = ["singles", [singles[i]]]
                        break
                    i += 1
                if i == 0 or i == len(singles):
                    send = [None, None]






        self.send(self.get_value_by_type(send))
        game.end = self.empty()

        if random.randint(0, 100) == 0:
            game.end = True

        return send




class Game():
    def __init__(self):
        self.end = False
        self.winner = None
        self.poker = Poker()
        self.ag1 = AgentBot(self.poker.aValue, 0)
        self.ag2 = AgentBot(self.poker.bValue, 1)
        self.ag3 = AgentBot(self.poker.cValue, 2)
        self.agents = [self.ag1, self.ag2, self.ag3]

        self.dz_index = None
        self.__choose_dz()

        self.puts = []

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
            send_poker = game.agents[cur].action(game)
            if send_poker[0]:
                game.puts.append([game.agents[cur].index, send_poker])
            if game.end:
                game.winner = cur
                break

    print game.puts

    print "end"
    print "winner: %d" % game.winner



if __name__ == "__main__":
    main()
