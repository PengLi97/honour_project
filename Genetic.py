import numpy as np
import matplotlib.pyplot as plt
from HandsCards import *
import types
import random


class Category:
    SELF = 0
    SELF_LEFT = 1
    SELF_RIGHT = 2
    SINGLE = 3
    PAIR = 4
    THREE = 5
    THREE_ONE = 6
    BOMB = 7
    CHAIN = 8
    CHAIN_PAIR = 9
    AIRPLANE = 10
    AIRPLANE_WINGS = 11
    ROCKET = 12
    SCORE = 13
    K = 14


class Genetic:
    def __init__(self):

        # DNA length {hand_card,pre_player,next_player,
        # Single,Pair,Three,ThreeWithOne,Bomb,
        # Chain,ChainPair,Airplane,AirplaneWithWings,Rocket,score,k}
        #  DNA_SIZE total is 15
        #  POP_SIZE is 10 (population size)
        self.POP_SIZE = 20
        self.CROSS_RATE = 0.8  # mating probability (DNA crossover)
        self.MUTATION_RATE = 0.003  # mutation probability
        N_GENERATIONS = 200
        X_BOUND = [0, 5]  # x upper and lower bounds
        self.lanlord_dnas = np.load('database/DNAlandlord.npy')
        self.left_dnas = np.load('database/DNAup.npy')
        self.right_dnas = np.load('database/DNAdown.npy')
        self.gene = []
        self.gene_left = []
        self.gene_right = []
        self.identify = -1
        self.left_identify = -1
        self.right_identify = -1
        self.n = 0
        self.hand = HandsCards([])
        self.hand_left = HandsCards([])
        self.hand_right = HandsCards([])

    def updateLeftRightInformation(self, left, right, G_left, G_right):
        self.left_identify = left
        self.right_identify = right
        self.gene_left = G_left
        self.gene_right = G_right

    def updatehand(self, hand):
        self.hand.updateHand(hand)

    def updatehand_left(self, hand):
        self.hand_left.updateHand(hand)

    def updatehand_right(self, hand):
        self.hand_right.updateHand(hand)

    # S1-S2 to get the DNA after landlord been select
    def setDNA(self, Id):
        self.n = np.random.randint(0, 19)
        if Id == 0:
            temp_dna = self.left_dnas  # [self.left_dnas[:, 13].argsort()]
            self.identify = 0
            self.gene = temp_dna[self.n, :]
        elif Id == 1:
            temp_dna = self.lanlord_dnas  # [self.lanlord_dnas[:, 13].argsort()]
            self.identify = 1
            self.gene = temp_dna[self.n, :]
        else:
            temp_dna = self.right_dnas  # [self.right_dnas[:, 13].argsort()]
            self.identify = 2
            self.gene = temp_dna[self.n, :]
        self.gene[Category.K] += 1

        # count ouput score

    # S3-S4 count all the show cards way, calculate the weight and return the highest point
    def helperChooseHP(self, card_type, pre, hand, G):
        # special output such as bomb
        special_output = hand.getBomborRocker()
        output = []
        special_point = 0
        plus = 0
        self_point, _ = hand.calculateHands(G)
        # no card greater than rocker
        if card_type == 'ROCKET':
            return self_point
        # special output such as bomb
        if len(special_output) > 0:
            special_output.insert(0, [])
            if not special_output[0] == []:
                for cards in special_output:
                    if len(cards) == 2:
                        special_point += cards[0].getWeight() * G[Category.ROCKET]
                    if not card_type == 'BOMB':
                        special_point += cards[0].getWeight() * G[Category.BOMB]
                special_point = special_point / len(special_output) if not card_type == 'BOMB' else special_point
        if special_point == -999999:
            special_point = 0
        # if no special output denominator should not plus 1
        if not len(special_output) == 0:
            plus = 1
        if card_type == 'SINGLE':
            card = np.asarray(pre)
            output = hand.getLegalSingle(card)
            if len(output) == 0:
                return self_point - special_point
            score, _ = hand.helperCountPoints(output, G[Category.SINGLE], "Single")
        elif card_type == 'PAIR':
            output = hand.getLegalPair(pre)
            if len(output) == 0:
                return self_point - special_point
            score, _ = hand.helperCountPoints(output, G[Category.PAIR], "Pair")
        elif card_type == 'THREE':
            output = hand.getLegalThree(pre)
            if len(output) == 0:
                return self_point - special_point
            score, _ = hand.helperCountPoints(output, G[Category.THREE])
        elif card_type == 'THREE_ONE':
            output = hand.getLegalThreeWithOne(pre)
            if len(output) == 0:
                return self_point - special_point
            score, _ = hand.helperCountPoints(output, G[Category.THREE_ONE], "ThreeOne")
        elif card_type == 'BOMB':
            output = hand.getLegalBomb(pre)
            if len(output) == 0:
                return self_point - special_point
            score, _ = hand.helperCountPoints(output, G[Category.BOMB])
        elif card_type == 'CHAIN':
            output = hand.getLegalChain(pre)
            if len(output) == 0:
                return self_point - special_point
            score, _ = hand.helperCountPoints(output, G[Category.CHAIN])
        elif card_type == 'CHAIN_PAIR':
            output = hand.getLegalPairChain(pre)
            if len(output) == 0:
                return self_point - special_point
            score, _ = hand.helperCountPoints(output, G[Category.CHAIN_PAIR])
        elif card_type == 'AIRPLANE':
            output = hand.getLegalAirplane(pre)
            if len(output) == 0:
                return self_point - special_point
            score, _ = hand.helperCountPoints(output, G[Category.AIRPLANE])
        elif card_type == 'AIRPLANE_WINGS':
            output = hand.getLegalAirplaneWithWings(pre)
            if len(output) == 0:
                return self_point - special_point
            score, _ = hand.helperCountPoints(output, G[Category.AIRPLANE_WINGS])
        score = self_point - (score + special_point) / (len(output) + plus)
        # if score < -20:
        #     score = -10
        return score

    # calculate the point in current situation
    # every player play card their score should be update
    # calculate the point on that situation
    def chooseHighestPoint(self, self_score, AllPossiblePlay, hand_left, hand_right, state=0):
        self.hand_left.updateHand(hand_left)
        self.hand_right.updateHand(hand_right)
        score_list = []
        length = len(self.hand.cards)
        # print("here is the length:",length)
        t = 0
        # too avoid AllPossiblePlay only have one element, but this should never happen
        if AllPossiblePlay == []:
            return []
        AllPossiblePlay = np.vstack([np.array([[], -999999]), AllPossiblePlay])

        individual = []
        keep_bomb = []
        card_dic = {'1': [], '2': [], '3': [], '4': [], '5': [], '6': [], '7': [], '8': [], '9': [], '10': [], '11': [],
                    '12': [], '13': [], '14': []}
        for card in self.hand.cards:
            card_dic[str(card.getRank())].append(card)
        # record individual card
        for c in card_dic:
            if len(card_dic[c]) == 1 and (not c == 13 or not c == 14):
                individual.append(card_dic[c][0].getRank())
        # record bomb card
        for c in card_dic:
            if len(card_dic[c]) == 4 and not c == 14:
                keep_bomb.append(card_dic[c][0].getRank())

        for cards_score in AllPossiblePlay:
            # always ignore first element
            if not cards_score[0] == []:
                a = CardType(2, 'dimond', '-')
                if type(cards_score[0]) == type(a):
                    cards_score[0] = [cards_score[0]]
                card_type = self.getCombination(cards_score[0])
                if card_type == {}:
                    continue
                player_L_score = self.helperChooseHP(card_type['combination'], cards_score[0], self.hand_left,
                                                     self.gene_left)
                player_R_score = self.helperChooseHP(card_type['combination'], cards_score[0], self.hand_right,
                                                     self.gene_right)
                L_not_change = self.helperChooseHP("ROCKET", cards_score[0], self.hand_left,
                                                   self.gene_left)
                R_not_change = self.helperChooseHP("ROCKET", cards_score[0], self.hand_right,
                                                   self.gene_right)
                # single card has priority
                bonus = 0
                minus = 0
                if card_type['combination'] == "SINGLE":
                    for rank in individual:
                        if rank == cards_score[0][0].getRank():
                            bonus = 1
                            break
                if card_type['combination'] == "BOMB":
                    for rank in keep_bomb:
                        if rank == cards_score[0][0].getRank():
                            minus = -5
                            break
                # deal with the special case
                extra = 0
                if (length == 2 and (card_type['combination'] == "PAIR" or card_type['combination'] == "ROCKET")) or (
                        length == 3 and (card_type['combination'] == "THREE" or card_type['combination'] == "PAIR")) or (
                        (length == 4 or length == 5 or length == 6) and (
                        card_type['combination'] == "THREE_ONE" or card_type['combination'] == "PAIR" or
                        card_type['combination'] == "CHAIN" or card_type['combination'] == "CHAIN_PAIR" or
                        card_type['combination'] == 'AIRPLANE')):
                    if card_type['combination'] == "PAIR":
                        extra = 3
                    else:
                        extra = 5
                if self.identify == 1:
                    if state == 1:
                        if len(self.hand_left.cards) > 3 or len(self.hand_right.cards) > 3:
                            score = (self_score - cards_score[1] + bonus) * self.gene[0] - L_not_change * self.gene[
                                1] - R_not_change * self.gene[2] + extra
                            # for c in cards_score[0]:
                            #     print(c.getRank(), end=" ")
                        else:
                            score = (self_score - cards_score[1] + bonus) * self.gene[0] - player_L_score * self.gene[
                                1] - player_R_score * self.gene[2] + extra
                    else:
                        score = (self_score - cards_score[1] + bonus) * self.gene[0] - player_L_score * self.gene[
                            1] - player_R_score * self.gene[2]
                else:
                    if self.left_identify == 1:
                        if state == 1:
                            if len(self.hand_right.cards) == 1 and card_type['combination'] == "PAIR":
                                    extra+=2
                            if len(self.hand_left.cards) > 3 or len(self.hand_right.cards) > 3:
                                score = (self_score - cards_score[1] + bonus) * self.gene[0] - L_not_change * self.gene[
                                    1] + R_not_change * self.gene[2] + extra

                            else:
                                score = (self_score - cards_score[1] + bonus) * self.gene[0] - player_L_score * \
                                        self.gene[
                                            1] + player_R_score * self.gene[2] + extra
                        else:
                            score = (self_score - cards_score[1]) * self.gene[0] - player_L_score * self.gene[
                                1] + player_R_score * self.gene[2]
                    else:
                        if state == 1:
                            if len(self.hand_right.cards) == 1 and card_type['combination'] == "SINGLE":
                                extra -= 1
                            if len(self.hand_right.cards) == 2 and card_type['combination'] == "PAIR":
                                extra -= 1
                            if len(self.hand_left.cards) > 3 or len(self.hand_right.cards) > 3:
                                score = (self_score - cards_score[1]) * self.gene[0] + L_not_change * self.gene[
                                    1] - R_not_change * self.gene[2] + extra
                            else:
                                score = (self_score - cards_score[1] + bonus) * self.gene[0] + player_L_score * \
                                        self.gene[
                                            1] - player_R_score * self.gene[2] + extra
                        else:
                            score = (self_score - cards_score[1] + bonus) * self.gene[0] + player_L_score * self.gene[
                                1] - player_R_score * self.gene[2]

                if minus == -5 and (length == 4 or length == 5):
                    minus = 3
                elif len(self.hand_left.cards) < 4 or len(self.hand_right.cards) < 4:
                    minus = 0

                score = score + minus
                # print("final score:", score, "  miuns = ", minus, "  bonus = ", bonus)
                # for c in cards_score[0]:
                #     print(c.getRank(),end=" ")
                # print("")
                score_list.append(score)
            else:
                t = 1
                score_list.append(-999999)  # make sure their dimension are same

        score_list = np.asarray(score_list)
        score_list = np.reshape(score_list, (len(score_list), 1))
        twoD_array = AllPossiblePlay.copy()
        new_2d_array = np.hstack((twoD_array, score_list))  # merge two array
        new_2d_array = new_2d_array[new_2d_array[:, 2].argsort()]  # sort 3 element array by score, pick the last one
        # print(new_2d_array)
        # print(new_2d_array[-1], "   ",new_2d_array[-2])
        if len(self.hand_left.cards) > 4 or len(self.hand_right.cards) > 4:
            card_type = self.getCombination(new_2d_array[-1][0])
            if card_type['combination'] == 'ROCKET' or card_type['combination'] == 'BOMB':
                if state == 1:
                    return new_2d_array[-2][0]
                if new_2d_array[-2][1] > 0:
                    return new_2d_array[-2][0]
                return []
        return new_2d_array[-1][0]

    # after game end, calculate the point for DNA
    # Y would be 20 if win, otherwise is 0
    def calculateDNApoint(self, prePoint, Y):
        # DNA point = pre + this time
        point = Y - (prePoint + self.hand.initial_point)
        self.gene[Category.SCORE] = point
        if self.identify == 0:
            self.left_dnas[self.n] = self.gene
            np.save('database/DNAup', self.left_dnas)
        elif self.identify == 1:
            self.lanlord_dnas[self.n] = self.gene
            # print("in calculateDNA function \n", self.lanlord_dnas)
            np.save('database/DNAlandlord', self.lanlord_dnas)
            temp = np.load('database/DNAlandlord.npy')
            # print("DNAlandlord.npy update\n", temp)
        else:
            self.right_dnas[self.n] = self.gene
            np.save('database/DNAdown', self.right_dnas)

    def crossover(self, position_dna, k):
        check = False
        dna = position_dna.copy()
        for p in position_dna:
            if p[Category.K] > k:
                check = True
                break
        if check:
            dna = np.delete(dna, [0, 1, 2, 3], 0)
            # print("delete first 4 of it length:", len(dna))
            dna[:, 13:15] = 0
            dna_copy = dna.copy()
            for i in range(0, len(dna)):
                if np.random.rand() < self.CROSS_RATE:  # dna should corss or not
                    cross_points = np.random.randint(1, 11)
                    # random select one of the dna
                    index = np.random.randint(0, (self.POP_SIZE - 4))
                    while i == index:  # make sure first and second are not same
                        index = np.random.randint(0, (self.POP_SIZE - 4))
                    # print("i: ", i, "   index: ", index, " cross_points: ", cross_points)
                    dna_copy[i] = np.concatenate((dna_copy[i][:cross_points], dna[index][cross_points:]))
            for _ in range(0, 4):  # create 4 child, to make our dna groups still have the same size
                first = np.random.randint(11, 16, size=1)  # choose one of the best five
                second = np.random.randint(0, self.POP_SIZE - 4, size=1)  # choose one of dna in delete dna group
                while second == first:  # make sure first and second are not same
                    second = np.random.randint(0, self.POP_SIZE - 4, size=1)
                cross_points = np.random.randint(1, 11)
                # new_dna = first[:cross_points] + second[cross_points:]
                new_dna = np.concatenate((dna[first][:cross_points], dna[second][cross_points:]))
                # print("child : ", new_dna)
                # do mutate for child that been create:
                for point in range(len(new_dna) - 2):
                    if np.random.rand() < self.MUTATION_RATE:
                        new_dna[point] = random.random()
                dna_copy = np.vstack((dna_copy, new_dna))
            dna_copy[:, 13:15] = 0
            return dna_copy
        return []

    # check each DNA used time, the one over k times. Delete the lowest one in genome
    # crossover and mutate rest of them match size of DNA_SIZE
    def mutate(self):
        k = 4
        lanlord_dnas = np.load('database/DNAlandlord.npy')
        left_dnas = np.load('database/DNAup.npy')
        right_dnas = np.load('database/DNAdown.npy')
        lanlord_dnas = lanlord_dnas[lanlord_dnas[:, 13].argsort()]
        left_dnas = left_dnas[left_dnas[:, 13].argsort()]
        right_dnas = right_dnas[right_dnas[:, 13].argsort()]
        new_landlord = self.crossover(lanlord_dnas, k)
        # print("in mutate function \n", new_landlord)
        if not new_landlord == []:
            np.save('database/DNAlandlord', new_landlord)
        new_left = self.crossover(left_dnas, k)
        if not new_left == []:
            np.save('database/DNAup', new_left)
        new_right = self.crossover(right_dnas, k)
        if not new_right == []:
            np.save('database/DNAdown', new_right)

    # check whether the cards is chain or not
    def isChain(self, lstOfCard):
        length = len(lstOfCard) - 1
        for i in range(length):
            if lstOfCard[i].getRank() - 1 != lstOfCard[i + 1].getRank() or lstOfCard[i].getRank() >= 13:
                return False
        return True

    # check whether the cards is pairs chain or not (ie. 33 44 55)
    def isPairsChain(self, lstOfCard):
        i = 0
        length = int(len(lstOfCard) / 2)
        for _ in range(length - 1):
            if (lstOfCard[i].getRank() != lstOfCard[i + 1].getRank() or
                lstOfCard[i].getRank() - 1 != lstOfCard[i + 2].getRank()) or lstOfCard[i].getRank() >= 13:
                return False
            i += 2
        if lstOfCard[-1].getRank() != lstOfCard[-2].getRank():
            return False
        return True

    # check whether the cards is three same cards Chain or not (ie. 333 444)
    def isAirplane(self, lstOfCard):
        i = 0
        length = len(lstOfCard) / 3
        while i <= length:
            if (lstOfCard[i].getRank() - 1 != lstOfCard[i + 3].getRank() or
                lstOfCard[i].getRank() != lstOfCard[i + 1].getRank() or
                lstOfCard[i].getRank() != lstOfCard[i + 2].getRank()) or lstOfCard[i].getRank() >= 13:
                return False
            i += 3
        if lstOfCard[-1].getRank() != lstOfCard[-2].getRank() or lstOfCard[-1].getRank() != lstOfCard[-3].getRank():
            return False
        return True

    # check whether the cards is three same cards with one singe card chain with  or not (ie. 3335 4446 or 54443333)
    def isAirplaneWithWings(self, lstOfCard):
        i = 0
        length = len(lstOfCard) - 3
        record = []
        wings_length = len(lstOfCard) / 4
        while i <= length:
            if lstOfCard[i].getRank() == lstOfCard[i + 1].getRank() and lstOfCard[i].getRank() == lstOfCard[
                i + 2].getRank():
                record.append(lstOfCard[i])
                i += 3
                continue
            i += 1
        if len(record) <= 1:
            return False
        if len(record) == wings_length and self.isChain(record):
            return record[0].getRank()
        if len(record) == 4 and len(lstOfCard) == 12:
            return record[3].getRank()
        # if self.isChain(record[:wings_length]) or self.isChain(record[1:wings_length + 1]):
        #     return record[1].getRank()

        return False

    # check the card is what kind of combination
    def getCombination(self, lstOfCard):
        a = CardType(2, 'dimond', '-')
        if type(lstOfCard) == type(a):
            return {'combination': 'SINGLE', 'rank': lstOfCard.getRank(), 'numberOfCards': 1}
        lstOfCard.sort(key=lambda x: x.getRank(), reverse=True)
        if len(lstOfCard) == 0 or len(lstOfCard) == 13 or len(lstOfCard) == 17 or len(lstOfCard) == 19:
            return {}
        elif len(lstOfCard) == 1:
            if lstOfCard[0].getSuit() == 'red':
                return {'combination': 'SINGLE', 'rank': 15, 'numberOfCards': 1}
            return {'combination': 'SINGLE', 'rank': lstOfCard[0].getRank(), 'numberOfCards': 1}

        elif len(lstOfCard) == 2:
            if lstOfCard[0].getRank() == lstOfCard[1].getRank() and not lstOfCard[1].getRank() == 14:
                return {'combination': 'PAIR', 'rank': lstOfCard[0].getRank(), 'numberOfCards': 2}
            if lstOfCard[0].getRank() == 14 and lstOfCard[1].getRank() == 14:
                return {'combination': 'ROCKET', 'rank': lstOfCard[0].getRank(), 'numberOfCards': 2}
            return {}

        elif len(lstOfCard) == 3:
            if lstOfCard[0].getRank() == lstOfCard[1].getRank() and lstOfCard[2].getRank() == lstOfCard[1].getRank():
                return {'combination': 'THREE', 'rank': lstOfCard[0].getRank(), 'numberOfCards': 3}
            return {}

        elif len(lstOfCard) == 4:
            if (lstOfCard[0].getRank() == lstOfCard[1].getRank() and lstOfCard[1].getRank() == lstOfCard[2].getRank()
                    and lstOfCard[2].getRank() == lstOfCard[3].getRank()):
                return {'combination': 'BOMB', 'rank': lstOfCard[0].getRank(), 'numberOfCards': 4}
            if lstOfCard[2].getRank() == lstOfCard[1].getRank():
                if lstOfCard[0].getRank() == lstOfCard[1].getRank() or lstOfCard[2].getRank() == lstOfCard[3].getRank():
                    return {'combination': 'THREE_ONE', 'rank': lstOfCard[2].getRank(), 'numberOfCards': 4}
            return {}

        elif len(lstOfCard) == 5:
            if self.isChain(lstOfCard):
                return {'combination': 'CHAIN', 'rank': lstOfCard[4].getRank(), 'numberOfCards': 5}
            return {}

        elif len(lstOfCard) == 6:
            if self.isChain(lstOfCard):
                return {'combination': 'CHAIN', 'rank': lstOfCard[5].getRank(), 'numberOfCards': 6}
            if self.isPairsChain(lstOfCard):
                return {'combination': 'CHAIN_PAIR', 'rank': lstOfCard[5].getRank(), 'numberOfCards': 6}
            if self.isAirplane(lstOfCard):
                return {'combination': 'AIRPLANE', 'rank': lstOfCard[5].getRank(), 'numberOfCards': 6}
            return {}

        elif len(lstOfCard) == 7:
            if self.isChain(lstOfCard):
                return {'combination': 'CHAIN', 'rank': lstOfCard[6].getRank(), 'numberOfCards': 7}
            return {}

        elif len(lstOfCard) == 8:
            airplane_rank = self.isAirplaneWithWings(lstOfCard)
            if self.isPairsChain(lstOfCard):
                return {'combination': 'CHAIN_PAIR', 'rank': lstOfCard[7].getRank(), 'numberOfCards': 8}
            if self.isChain(lstOfCard):
                return {'combination': 'CHAIN', 'rank': lstOfCard[7].getRank(), 'numberOfCards': 8}
            if airplane_rank:
                return {'combination': 'AIRPLANE_WINGS', 'rank': airplane_rank, 'numberOfCards': 8}
            return {}

        elif len(lstOfCard) == 9:
            if self.isChain(lstOfCard):
                return {'combination': 'CHAIN', 'rank': lstOfCard[8].getRank(), 'numberOfCards': 9}
            if self.isAirplane(lstOfCard):
                return {'combination': 'AIRPLANE', 'rank': lstOfCard[8].getRank(), 'numberOfCards': 9}
            return {}

        elif len(lstOfCard) == 10:
            if self.isChain(lstOfCard):
                return {'combination': 'CHAIN', 'rank': lstOfCard[9].getRank(), 'numberOfCards': 10}
            if self.isPairsChain(lstOfCard):
                return {'combination': 'CHAIN_PAIR', 'rank': lstOfCard[9].getRank(), 'numberOfCards': 10}
            return {}

        elif len(lstOfCard) == 11:
            if self.isChain(lstOfCard):
                return {'combination': 'CHAIN', 'rank': lstOfCard[10].getRank(), 'numberOfCards': 11}
            return {}

        elif len(lstOfCard) == 12:
            airplane_rank = self.isAirplaneWithWings(lstOfCard)
            if self.isChain(lstOfCard):
                return {'combination': 'CHAIN', 'rank': lstOfCard[11].getRank(), 'numberOfCards': 12}
            if self.isPairsChain(lstOfCard):
                return {'combination': 'CHAIN_PAIR', 'rank': lstOfCard[11].getRank(), 'numberOfCards': 12}
            if self.isAirplane(lstOfCard):
                return {'combination': 'AIRPLANE', 'rank': lstOfCard[11].getRank(), 'numberOfCards': 12}
            if airplane_rank:
                return {'combination': 'AIRPLANE_WINGS', 'rank': airplane_rank, 'numberOfCards': 12}
            # for card in lstOfCard:
            #     # print(card.getRank(), end=" ")
            return {}

        elif len(lstOfCard) == 14:
            if self.isPairsChain(lstOfCard):
                return {'combination': 'CHAIN_PAIR', 'rank': lstOfCard[13].getRank(), 'numberOfCards': 14}
            return {}

        elif len(lstOfCard) == 15:
            if self.isAirplane(lstOfCard):
                return {'combination': 'AIRPLANE', 'rank': lstOfCard[14].getRank(), 'numberOfCards': 15}
            return {}

        elif len(lstOfCard) == 16:
            airplane_rank = self.isAirplaneWithWings(lstOfCard)
            if self.isPairsChain(lstOfCard):
                return {'combination': 'CHAIN_PAIR', 'rank': lstOfCard[15].getRank(), 'numberOfCards': 16}
            if airplane_rank:
                return {'combination': 'AIRPLANE_WINGS', 'rank': airplane_rank, 'numberOfCards': 16}
            # for card in lstOfCard:
            #     print(card.getRank(), end=" ")
            return {}

        elif len(lstOfCard) == 18:
            if self.isPairsChain(lstOfCard):
                return {'combination': 'CHAIN_PAIR', 'rank': lstOfCard[17].getRank(), 'numberOfCards': 18}
            if self.isAirplane(lstOfCard):
                return {'combination': 'AIRPLANE', 'rank': lstOfCard[17].getRank(), 'numberOfCards': 18}
            return {}

        elif len(lstOfCard) == 20:
            airplane_rank = self.isAirplaneWithWings(lstOfCard)
            if self.isPairsChain(lstOfCard):
                return {'combination': 'CHAIN_PAIR', 'rank': lstOfCard[19].getRank(), 'numberOfCards': 20}
            if airplane_rank:
                return {'combination': 'AIRPLANE_WINGS', 'rank': airplane_rank, 'numberOfCards': 20}
            return {}
