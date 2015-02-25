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
        if x == 0:
            x = 13
        if x < 3:
            return x + 20
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


if __name__ == "__main__":
    poker = Poker()
    poker.cardnumPrint()
    poker.cardvaluePrint()


