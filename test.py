import numpy as np
import random
from HandsCards import *
from CardType import *
from Genetic import *

desk = []
suitType = ['club', 'spade', 'dimond', 'heart']
jokerType = ['red', 'black']
for i in range(52):
    rank = i % 13 + 1
    suit = suitType[i % 4]
    face = 'image/' + suit[0] + str(rank) + '.jpg'
    card = CardType(rank, suit, face)
    desk.append(card)
random.shuffle(desk)
hand = HandsCards(desk[:17])
print(hand.print())
special = [CardType(5, 'club', 'image/' + 'club' + '3' + '.jpg'),CardType(5, 'spade', 'image/' + 'spade' + '3' + '.jpg'),
        CardType(5, 'heart', 'image/' + 'heart' + '3' + '.jpg'),CardType(6, 'heart', 'image/' + 'heart' + '4' + '.jpg'),
        CardType(6, 'heart', 'image/' + 'heart' + '4' + '.jpg'),CardType(6, 'heart', 'image/' + 'heart' + '4' + '.jpg'),
        CardType(7, 'heart', 'image/' + 'heart' + '4' + '.jpg'),CardType(7, 'heart', 'image/' + 'heart' + '4' + '.jpg'),
        CardType(8, 'club', 'image/' + 'club' + '3' + '.jpg'),CardType(9, 'spade', 'image/' + 'spade' + '3' + '.jpg'),
        CardType(9, 'heart', 'image/' + 'heart' + '3' + '.jpg'),CardType(9, 'heart', 'image/' + 'heart' + '4' + '.jpg'),
        CardType(10, 'heart', 'image/' + 'heart' + '4' + '.jpg'),CardType(10, 'heart', 'image/' + 'heart' + '4' + '.jpg'),
        CardType(10, 'heart', 'image/' + 'heart' + '4' + '.jpg'),CardType(11, 'heart', 'image/' + 'heart' + '4' + '.jpg'),
        CardType(13, 'heart', 'image/' + 'heart' + '4' + '.jpg')]
special1 = [CardType(5, 'club', 'image/' + 'club' + '3' + '.jpg'),CardType(5, 'spade', 'image/' + 'spade' + '3' + '.jpg'),
        CardType(5, 'heart', 'image/' + 'heart' + '3' + '.jpg'),CardType(5, 'heart', 'image/' + 'heart' + '4' + '.jpg'),
        CardType(6, 'heart', 'image/' + 'heart' + '4' + '.jpg'),CardType(6, 'heart', 'image/' + 'heart' + '4' + '.jpg'),
        CardType(7, 'heart', 'image/' + 'heart' + '4' + '.jpg'),CardType(7, 'heart', 'image/' + 'heart' + '4' + '.jpg'),
        CardType(8, 'club', 'image/' + 'club' + '3' + '.jpg'),CardType(8, 'spade', 'image/' + 'spade' + '3' + '.jpg'),
        CardType(9, 'heart', 'image/' + 'heart' + '3' + '.jpg'),CardType(13, 'heart', 'image/' + 'heart' + '4' + '.jpg'),
        CardType(10, 'heart', 'image/' + 'heart' + '4' + '.jpg'),CardType(10, 'heart', 'image/' + 'heart' + '4' + '.jpg'),
        CardType(10, 'heart', 'image/' + 'heart' + '4' + '.jpg'),CardType(14, 'red', 'image/' + 'heart' + '4' + '.jpg'),
        CardType(14, 'black', 'image/' + 'heart' + '4' + '.jpg')]

special3 = [CardType(7, 'club', 'image/' + 'club' + '3' + '.jpg'),CardType(7, 'spade', 'image/' + 'spade' + '3' + '.jpg'),
        CardType(7, 'heart', 'image/' + 'heart' + '3' + '.jpg'),CardType(7, 'heart', 'image/' + 'heart' + '4' + '.jpg'),
        CardType(6, 'heart', 'image/' + 'heart' + '4' + '.jpg'),CardType(6, 'heart', 'image/' + 'heart' + '4' + '.jpg'),
        CardType(3, 'heart', 'image/' + 'heart' + '4' + '.jpg'),CardType(3, 'heart', 'image/' + 'heart' + '4' + '.jpg'),
        CardType(8, 'club', 'image/' + 'club' + '3' + '.jpg'),CardType(8, 'spade', 'image/' + 'spade' + '3' + '.jpg'),
        CardType(9, 'heart', 'image/' + 'heart' + '3' + '.jpg'),CardType(13, 'heart', 'image/' + 'heart' + '4' + '.jpg'),
        CardType(10, 'heart', 'image/' + 'heart' + '4' + '.jpg'),CardType(10, 'heart', 'image/' + 'heart' + '4' + '.jpg'),
        CardType(10, 'heart', 'image/' + 'heart' + '4' + '.jpg'),CardType(14, 'red', 'image/' + 'heart' + '4' + '.jpg'),
        CardType(14, 'black', 'image/' + 'heart' + '4' + '.jpg')]

special4 = [CardType(4, 'club', 'image/' + 'club' + '3' + '.jpg'),CardType(4, 'spade', 'image/' + 'spade' + '3' + '.jpg'),
        CardType(4, 'heart', 'image/' + 'heart' + '3' + '.jpg'),CardType(4, 'heart', 'image/' + 'heart' + '4' + '.jpg'),
        CardType(6, 'heart', 'image/' + 'heart' + '4' + '.jpg'),CardType(6, 'heart', 'image/' + 'heart' + '4' + '.jpg'),
        CardType(7, 'heart', 'image/' + 'heart' + '4' + '.jpg'),CardType(7, 'heart', 'image/' + 'heart' + '4' + '.jpg'),
        CardType(8, 'club', 'image/' + 'club' + '3' + '.jpg'),CardType(8, 'spade', 'image/' + 'spade' + '3' + '.jpg'),
        CardType(9, 'heart', 'image/' + 'heart' + '3' + '.jpg'),CardType(13, 'heart', 'image/' + 'heart' + '4' + '.jpg'),
        CardType(10, 'heart', 'image/' + 'heart' + '4' + '.jpg'),CardType(10, 'heart', 'image/' + 'heart' + '4' + '.jpg'),
        CardType(10, 'heart', 'image/' + 'heart' + '4' + '.jpg'),CardType(14, 'red', 'image/' + 'heart' + '4' + '.jpg'),
        CardType(14, 'black', 'image/' + 'heart' + '4' + '.jpg')]
# test airplane or airplane with wing
special_fly = [CardType(3, 'club', 'image/' + 'c' + '3' + '.jpg'),
                    CardType(3, 'spade', 'image/' + 'c' + '3' + '.jpg'),
                    CardType(3, 'heart', 'image/' + 'c' + '3' + '.jpg'),
                    CardType(4, 'heart', 'image/' + 'c' + '4' + '.jpg'),
                    CardType(4, 'heart', 'image/' + 'c' + '4' + '.jpg'),
                    CardType(4, 'heart', 'image/' + 'c' + '4' + '.jpg'),
                    CardType(5, 'heart', 'image/' + 'c' + '5' + '.jpg'),
                    CardType(5, 'heart', 'image/' + 'c' + '5' + '.jpg'),
                    CardType(5, 'club', 'image/' + 'c' + '5' + '.jpg'),
                    CardType(8, 'spade', 'image/' + 's' + '8' + '.jpg'),
                    CardType(9, 'heart', 'image/' + 's' + '9' + '.jpg'),
                    CardType(13, 'heart', 'image/' + 'h' + '13' + '.jpg'),
                    CardType(10, 'heart', 'image/' + 'h' + '10' + '.jpg'),
                    CardType(10, 'heart', 'image/' + 'h' + '10' + '.jpg'),
                    CardType(10, 'heart', 'image/' + 'h' + '10' + '.jpg'),
                    CardType(12, 'heart', 'image/' + 'h' + '12' + '.jpg'),
                    CardType(12, 'heart', 'image/' + 'h' + '12' + '.jpg')]
special_fly2 = [CardType(1, 'club', 'image/' + 'c' + '1' + '.jpg'),
                    CardType(1, 'spade', 'image/' + 'c' + '1' + '.jpg'),
                    CardType(1, 'heart', 'image/' + 'c' + '1' + '.jpg'),
                    CardType(2, 'heart', 'image/' + 'c' + '2' + '.jpg'),
                    CardType(2, 'heart', 'image/' + 'c' + '2' + '.jpg'),
                    CardType(2, 'heart', 'image/' + 'c' + '2' + '.jpg'),
                    CardType(5, 'heart', 'image/' + 'c' + '5' + '.jpg'),
                    CardType(5, 'heart', 'image/' + 'c' + '5' + '.jpg'),
                    CardType(5, 'club', 'image/' + 'c' + '5' + '.jpg'),
                    CardType(8, 'spade', 'image/' + 's' + '8' + '.jpg'),
                    CardType(9, 'heart', 'image/' + 's' + '9' + '.jpg'),
                    CardType(13, 'heart', 'image/' + 'h' + '13' + '.jpg'),
                    CardType(10, 'heart', 'image/' + 'h' + '10' + '.jpg'),
                    CardType(10, 'heart', 'image/' + 'h' + '10' + '.jpg'),
                    CardType(10, 'heart', 'image/' + 'h' + '10' + '.jpg'),
                    CardType(12, 'heart', 'image/' + 'h' + '12' + '.jpg'),
                    CardType(12, 'heart', 'image/' + 'h' + '12' + '.jpg')]
        # self.cards_right = special1
        # self.cards_bottom = special2
# test pair chain
special_pc = [CardType(3, 'club', 'image/' + 'c' + '3' + '.jpg'),
                    CardType(3, 'spade', 'image/' + 'c' + '3' + '.jpg'),
                    CardType(4, 'heart', 'image/' + 'c' + '4' + '.jpg'),
                    CardType(4, 'heart', 'image/' + 'c' + '4' + '.jpg'),
                    CardType(5, 'heart', 'image/' + 'c' + '5' + '.jpg'),
                    CardType(5, 'heart', 'image/' + 'c' + '5' + '.jpg'),
                    CardType(6, 'heart', 'image/' + 'c' + '6' + '.jpg'),
                    CardType(6, 'heart', 'image/' + 'c' + '6' + '.jpg'),
                    CardType(7, 'club', 'image/' + 'c' + '7' + '.jpg'),
                    CardType(8, 'spade', 'image/' + 's' + '8' + '.jpg'),
                    CardType(9, 'heart', 'image/' + 's' + '9' + '.jpg'),
                    CardType(13, 'heart', 'image/' + 'h' + '13' + '.jpg'),
                    CardType(10, 'heart', 'image/' + 'h' + '10' + '.jpg'),
                    CardType(10, 'heart', 'image/' + 'h' + '10' + '.jpg'),
                    CardType(10, 'heart', 'image/' + 'h' + '10' + '.jpg'),
                    CardType(12, 'heart', 'image/' + 'h' + '12' + '.jpg'),
                    CardType(12, 'heart', 'image/' + 'h' + '12' + '.jpg')]
special_pc2 = [CardType(5, 'club', 'image/' + 'c' + '5' + '.jpg'),
                    CardType(5, 'spade', 'image/' + 'c' + '5' + '.jpg'),
                    CardType(6, 'heart', 'image/' + 'c' + '6' + '.jpg'),
                    CardType(6, 'heart', 'image/' + 'c' + '6' + '.jpg'),
                    CardType(7, 'heart', 'image/' + 'c' + '7' + '.jpg'),
                    CardType(7, 'heart', 'image/' + 'c' + '7' + '.jpg'),
                    CardType(8, 'heart', 'image/' + 'c' + '8' + '.jpg'),
                    CardType(8, 'heart', 'image/' + 'c' + '8' + '.jpg'),
                    CardType(10, 'club', 'image/' + 'c' + '10' + '.jpg'),
                    CardType(11, 'spade', 'image/' + 's' + '11' + '.jpg'),
                    CardType(9, 'heart', 'image/' + 's' + '9' + '.jpg'),
                    CardType(13, 'heart', 'image/' + 'h' + '13' + '.jpg'),
                    CardType(10, 'heart', 'image/' + 'h' + '10' + '.jpg'),
                    CardType(10, 'heart', 'image/' + 'h' + '10' + '.jpg'),
                    CardType(10, 'heart', 'image/' + 'h' + '10' + '.jpg'),
                    CardType(12, 'heart', 'image/' + 'h' + '12' + '.jpg'),
                    CardType(12, 'heart', 'image/' + 'h' + '12' + '.jpg')]



new = HandsCards(special)
new1 = HandsCards(special1)
# print(new.print())
pre_single = [CardType(3, 'club', 'image/' + 'club' + '3' + '.jpg')]
pre_two = [CardType(3, 'club', 'image/' + 'club' + '3' + '.jpg'),CardType(3, 'spade', 'image/' + 'spade' + '3' + '.jpg')]
pre_three = [CardType(3, 'club', 'image/' + 'club' + '3' + '.jpg'),CardType(3, 'spade', 'image/' + 'spade' + '3' + '.jpg'),CardType(3, 'heart', 'image/' + 'heart' + '3' + '.jpg')]
pre_31 = [CardType(3, 'club', 'image/' + 'club' + '3' + '.jpg'),CardType(3, 'spade', 'image/' + 'spade' + '3' + '.jpg'),
        CardType(3, 'heart', 'image/' + 'heart' + '3' + '.jpg'),CardType(4, 'heart', 'image/' + 'heart' + '4' + '.jpg')]
pre_4 = [CardType(3, 'club', 'image/' + 'club' + '3' + '.jpg'),CardType(3, 'spade', 'image/' + 'spade' + '3' + '.jpg'),
        CardType(3, 'heart', 'image/' + 'heart' + '3' + '.jpg'),CardType(3, 'dimond', 'image/' + 'dimond' + '4' + '.jpg')]
pre_5 = [CardType(3, 'club', 'image/' + 'club' + '3' + '.jpg'),CardType(4, 'spade', 'image/' + 'spade' + '4' + '.jpg'),
        CardType(5, 'heart', 'image/' + 'heart' + '5' + '.jpg'),CardType(6, 'dimond', 'image/' + 'dimond' + '6' + '.jpg'),
        CardType(7, 'heart', 'image/' + 'heart' + '7' + '.jpg')]
pre_6 = [CardType(3, 'club', 'image/' + 'club' + '3' + '.jpg'),CardType(3, 'spade', 'image/' + 'spade' + '3' + '.jpg'),
        CardType(4, 'heart', 'image/' + 'heart' + '5' + '.jpg'),CardType(4, 'dimond', 'image/' + 'dimond' + '6' + '.jpg'),
        CardType(5, 'heart', 'image/' + 'heart' + '5' + '.jpg'),CardType(5, 'heart', 'image/' + 'heart' + '5' + '.jpg')]
pre_8 = [CardType(3, 'club', 'image/' + 'club' + '3' + '.jpg'),CardType(3, 'spade', 'image/' + 'spade' + '3' + '.jpg'),
        CardType(3, 'heart', 'image/' + 'heart' + '3' + '.jpg'),CardType(4, 'heart', 'image/' + 'heart' + '4' + '.jpg'),
        CardType(4, 'heart', 'image/' + 'heart' + '4' + '.jpg'),CardType(4, 'heart', 'image/' + 'heart' + '4' + '.jpg'),
        CardType(5, 'heart', 'image/' + 'heart' + '4' + '.jpg'),CardType(5, 'heart', 'image/' + 'heart' + '4' + '.jpg')]
single = hand.getLegalSingle(pre_single)
two = hand.getLegalPair(pre_two)
three = hand.getLegalThree(pre_three)
t31 = hand.getLegalThreeWithOne(pre_31)
t4 = hand.getLegalBomb(pre_4)
t5 = hand.getLegalChain(pre_5)
t6 =hand.getLegalPairChain(pre_6)
t8 = new.getLegalAirplaneWithWings(pre_8)

landlord = Genetic()
# dna = landlord.getDNA(1)
# print(landlord.checkOutput(new1, pre_8))
lanlord_dnas = np.load('database/DNAlandlord.npy')
print(lanlord_dnas)
# dna = lanlord_dnas[1]
# data = pre_8.copy()
# data.append(dna)
# data.append((len(pre_8)))
# print(data)
# np.save("t", data)
#
# d_left = np.load("t.npy",allow_pickle=True)
# print(d_left)
# print(d_left[1].getRank())
# print("single")
# for card in single:
#     if len(card) == 2 or len(card) == 4:
#         print("bomb",end=" ")
#     else:
#         print(card[0].getRank(),end=" ")
# print("\n"+"two")
# for card in two:
#     print(card[0].getRank(),end=" ")
# for card in three:
#     print(card[0].getRank(),end=" ")
# for card in t31:
#     print(str(card[0].getRank()) + "-" + str(card[3].getRank()),end=" ")
# for card in t4:
#     print(str(card[0].getRank()),end=" ")
# for card in t5:
#     for c in card:
#         print(str(c.getRank()),end="")
#     print(end=" ")
# for card in t6:
#     for c in card:
#         print(str(c.getRank()),end="")
#     print(end=" ")
for card in t8:
     for c in card:
         print(str(c.getRank()),end="")
     print(end=" ")
