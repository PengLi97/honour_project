from CardType import *
import numpy as np
class HandsCards:
    def __init__(self, cardlist):
        self.cards = cardlist
        self.card_dic = {'1': [], '2': [], '3': [], '4': [], '5': [], '6': [], '7': [], '8': [], '9': [], '10': [],
                         '11': [], '12': [], '13': [], '14': []}
        self.combination_dic = {'SINGLE': [], 'PAIR': [], 'THREE': [], 'THREE_ONE': [], 'BOMB': [], 'CHAIN': [],
                                'CHAIN_PAIR': [], 'AIRPLANE': [], 'AIRPLANE_WINGS': [], 'ROCKET': []}
        self.samllestCard = []
        self.output_point = [] # [cards, points]
        self.initial_point = 0

    def setInitialPoint(self, gene):
        self.initial_point,_ = self.calculateHands(gene)

    # Rocket = 8point, bomb = 6point, Airplane_wings = 5point, 2 = 2point, red jocker = 4point, black jocker = 3points
    def bidLandlord(self):
        score = len(self.card_dic['12']) * 2
        if len(self.card_dic['14']) == 1:
            if self.card_dic['14'][0].getSuit() == 'red':
                score += 4
            else:
                score += 3
        if not len(self.combination_dic['ROCKET']) == 0:
            score += 8
        if not len(self.combination_dic['AIRPLANE_WINGS']) == 0:
            score += 5
        if not len(self.combination_dic['BOMB']) == 0:
            score += 6
        status = True if score >= 9 else False
        return status

    # convert type string to number
    def converter(self, cards_type):
        if cards_type == 'SINGLE':
            return 3
        elif cards_type == 'PAIR':
            return 4
        elif cards_type == 'THREE':
            return 5
        elif cards_type == 'THREE_ONE':
            return 6
        elif cards_type == 'BOMB':
            return 7
        elif cards_type == 'CHAIN':
            return 8
        elif cards_type == 'CHAIN_PAIR':
            return 9
        elif cards_type == 'AIRPLANE':
            return 10
        elif cards_type == 'AIRPLANE_WINGS':
            return 11
        elif cards_type == 'ROCKET':
            return 12

    # help function to count total score for each type(single, pair...)
    def helperCountPoints(self, type_cards, w, check_type=""):
        # eg. (（4 * 3 + 5）/ 4) * G5
        score = 0  # recode output points
        score_lst = []
        s = 0
        w = w + 1e-7
        if len(type_cards) == 0:  # if output is empty
            return score, []
        for card_list in type_cards:
            temp_score = 0
            if type(card_list) == list and len(card_list) > 0:
                if check_type == "ThreeOne":
                    if card_list[0].getWeight() == card_list[1].getWeight():
                        temp_score += card_list[0].getWeight() * 3 + card_list[-1].getWeight() * card_list[-1].getWeight()
                        # print(temp_score/4 * w," ",card_list[0].getRank(),card_list[1].getRank(),card_list[2].getRank(),card_list[3].getRank())
                    else:
                        temp_score += card_list[-1].getWeight() * 3 + card_list[0].getWeight() * card_list[-1].getWeight()
                        # print((temp_score/4) * w, " ", card_list[0].getRank(), card_list[1].getRank(), card_list[2].getRank(), card_list[3].getRank())
                    s = temp_score / 4 * w
                else:
                    for c in card_list:
                        temp_score += c.getWeight()
                    s = temp_score / len(card_list) * w
                temp_output = np.array([card_list, s])
                score_lst = temp_output if len(score_lst) == 0 else np.vstack([score_lst, temp_output])
                score += s
            else:
                if not type(card_list) == list:
                    temp_score += card_list.getWeight()
                    s = temp_score/2 * w
                    temp_output = np.array([card_list, s])
                    score_lst = temp_output if len(score_lst) == 0 else np.vstack([score_lst, temp_output])
                    score += s
        score = score/len(type_cards)
        return score, score_lst

    # total combination score = ( sum of all combination / number of type )  * weight
    # return score of hand, and all the output with socre
    def calculateHands(self, gene):
        count = 0
        total_score = 0
        all_score_list = []
        self.output_point = []
        score = 0
        # count all number of combination
        for key in self.combination_dic:
            if len(self.combination_dic[key]) == 0:
                continue
            count += len(self.combination_dic[key])
            index = self.converter(key)
            score, score_lst = self.helperCountPoints(self.combination_dic[key], gene[index])
            if score == 0:
                continue
            total_score += score
            all_score_list = score_lst if len(all_score_list) == 0 else np.vstack([all_score_list, score_lst])

            res = (total_score / count) * gene[0]
        return res, all_score_list

    # every time after play card should call this method
    def updateHand(self, cardlist):
        self.cards = cardlist
        self.card_dic = {'1': [], '2': [], '3': [], '4': [], '5': [], '6': [], '7': [], '8': [], '9': [], '10': [],
                         '11': [], '12': [], '13': [], '14': []}
        for card in self.cards:
            self.card_dic[str(card.getRank())].append(card)
        self.getALLCombination()

    # get the dictionary of card_dic
    def getDicCards(self):
        return self.card_dic

    # output all combination that the cards list can make
    def getALLCombination(self):
        self.combination_dic = {'SINGLE': [], 'PAIR': [], 'THREE': [], 'THREE_ONE': [], 'BOMB': [], 'CHAIN': [],
                                'CHAIN_PAIR': [], 'AIRPLANE': [], 'AIRPLANE_WINGS': [], 'ROCKET': []}
        self.samllestCard = []
        for i in range(1, len(self.cards)+1):
            self.samllestCard.append(CardType(0, 'spade', 'None'))
            if i == 1:
                self.combination_dic['SINGLE'] = self.getLegalSingle(self.samllestCard)
            elif i == 2:
                self.combination_dic['PAIR'] = self.getLegalPair(self.samllestCard)
            elif i == 3:
                self.combination_dic['THREE'] = self.getLegalThree(self.samllestCard)
            elif i == 4:
                self.combination_dic['THREE_ONE'] = self.getLegalThreeWithOne(self.samllestCard)
                self.combination_dic['BOMB'] = self.getLegalBomb(self.samllestCard)
            elif i == 5 or i == 7 or i == 11:
                if len(self.combination_dic['CHAIN']) == 0:
                    self.combination_dic['CHAIN'] = self.getLegalChain(self.samllestCard)
                else:
                    self.combination_dic['CHAIN'] += self.getLegalChain(self.samllestCard)
            elif i == 6:
                self.combination_dic['CHAIN'] += self.getLegalChain(self.samllestCard)
                self.combination_dic['CHAIN_PAIR'] += self.getLegalPairChain(self.samllestCard)
                self.combination_dic['AIRPLANE'] += self.getLegalAirplane(self.samllestCard)
            elif i == 8 or 12:
                self.combination_dic['CHAIN'] += self.getLegalChain(self.samllestCard)
                self.combination_dic['CHAIN_PAIR'] += self.getLegalPairChain(self.samllestCard)
                self.combination_dic['AIRPLANE_WINGS'] += self.getLegalAirplaneWithWings(self.samllestCard)
                if i == 12:
                    self.combination_dic['AIRPLANE'] += self.getLegalAirplane(self.samllestCard)
            elif i == 9:
                self.combination_dic['CHAIN'] += self.getLegalChain(self.samllestCard)
                self.combination_dic['AIRPLANE'] += self.getLegalAirplane(self.samllestCard)
            elif i == 10:
                self.combination_dic['CHAIN'] += self.getLegalChain(self.samllestCard)
                self.combination_dic['CHAIN_PAIR'] += self.getLegalPairChain(self.samllestCard)
            elif i == 14:
                self.combination_dic['CHAIN_PAIR'] += self.getLegalPairChain(self.samllestCard)
            elif i == 15:
                self.combination_dic['AIRPLANE'] += self.getLegalAirplane(self.samllestCard)
            elif i == 16 or i == 20:
                self.combination_dic['CHAIN_PAIR'] += self.getLegalPairChain(self.samllestCard)
                self.combination_dic['AIRPLANE_WINGS'] += self.getLegalAirplaneWithWings(self.samllestCard)
            elif i == 18:
                self.combination_dic['CHAIN_PAIR'] += self.getLegalPairChain(self.samllestCard)
                self.combination_dic['AIRPLANE'] += self.getLegalAirplane(self.samllestCard)
        if len(self.card_dic['14']) == 2:
            self.combination_dic['ROCKET'] = [self.card_dic['14']]

        return self.combination_dic

    # get the cards in hand
    def getCards(self):
        return self.cards

    # All possible output for Single        [[3], [4]]
    def getLegalSingle(self, pre_cards):
        a = CardType(2, 'dimond', '-')
        if type(pre_cards) == type(a):
            card_type = pre_cards.getSuit()
        else:
            card_type = pre_cards[0].getSuit()
        i = pre_cards[0].getRank()
        output = []
        if card_type == 'red' and len(self.card_dic['14']) == 0:  # if pre_cards is single largest, go check for bomb
            return output
        if card_type == 'black':
            output.append(list(self.card_dic['14']))
            return output
        n = i + 1
        for j in range(n, 15):
            if len(self.card_dic[str(j)]) >= 1:
                card = self.card_dic[str(j)][0]
                l = [card]
                output.append(l)
        return output

    # All possible output for Pair [[22], [33]]
    def getLegalPair(self, pre_cards):
        pre_card_rank = pre_cards[0].getRank()
        output = []
        if pre_card_rank == 13:
            return output
        n = pre_card_rank + 1
        for j in range(n, 14):
            if len(self.card_dic[str(j)]) >= 2:
                cards = self.card_dic[str(j)][:2]
                output.append(cards)
        return output

    # All possible output for Three
    def getLegalThree(self, pre_cards):
        pre_card_rank = pre_cards[0].getRank()
        output = []
        if pre_card_rank == 13:
            return output
        n = pre_card_rank + 1
        for j in range(n, 14):
            if len(self.card_dic[str(j)]) >= 3:
                output.append(self.card_dic[str(j)][:3])
        return output

    # All possible output for Three
    def getLegalThreeWithOne(self, pre_cards):
        pre_card_rank = pre_cards[1].getRank()
        output = []
        if pre_card_rank == 13:
            return output
        n = pre_card_rank + 1
        for j in range(n, 14):
            if len(self.card_dic[str(j)]) >= 3:
                for key in self.card_dic:
                    temp = self.card_dic[str(j)][:3]
                    if len(self.card_dic[key]) > 0 and not key == str(j):
                        temp.append(self.card_dic[key][0])
                        output.append(temp)
        return output

    # All possible output for bomb
    def getLegalBomb(self, pre_cards):
        pre_card_rank = pre_cards[0].getRank()
        output = []
        if pre_card_rank < 13:
            n = pre_card_rank + 1
            for j in range(n, 14):
                if len(self.card_dic[str(j)]) == 4:
                    temp = self.card_dic[str(j)]
                    output.append(temp)
        return output

    # All possible output for chain [[34567], [45678]]
    def getLegalChain(self, pre_cards):
        index = 0 if pre_cards[-1].getRank() > pre_cards[0].getRank() else -1
        pre_card_rank = pre_cards[index].getRank()
        output = []
        temp = []
        for i in range(pre_card_rank + 1, 13):
            if len(self.card_dic[str(i)]) > 0:
                temp.append(self.card_dic[str(i)][0])
            else:
                temp = []
            if len(temp) == len(pre_cards):
                temp2 = temp.copy()
                output.append(temp2)
                temp.pop(0)
        return output

    # All possible output for pair chain
    def getLegalPairChain(self, pre_cards):
        index = 0 if pre_cards[-1].getRank() > pre_cards[0].getRank() else -1
        pre_card_rank = pre_cards[index].getRank()
        output = []
        temp = []
        for i in range(pre_card_rank + 1, len(self.card_dic) - 2):
            if len(self.card_dic[str(i)]) > 1:
                temp += self.card_dic[str(i)][:2]
            else:
                temp = []
            if len(temp) == len(pre_cards):
                temp2 = temp.copy()
                output.append(temp2)
                temp = temp[2:]
        return output

    # All possible output for airplane
    def getLegalAirplane(self, pre_cards):
        index = 0 if pre_cards[-1].getRank() > pre_cards[0].getRank() else -1
        pre_card_rank = pre_cards[index].getRank()
        output = []
        temp = []
        for i in range(pre_card_rank + 1, len(self.card_dic) - 2):
            if len(self.card_dic[str(i)]) > 2:
                temp += self.card_dic[str(i)][:3]
            else:
                temp = []
            if len(temp) == len(pre_cards):
                temp2 = temp.copy()
                output.append(temp2)
                temp = temp[3:]
        return output

    # total of m cards choose n card, output all possible value
    def MChooseN(self, m, n, b, output, lst, number):
        for i in range(m, n - 1, -1):
            b[n - 1] = i
            if n - 1 > 0:
                self.MChooseN(i - 1, n - 1, b, output, lst, number)
            else:
                t = []
                for j in range(0, number):
                    index = b[j] - 1
                    t.append(lst[index])
                output.append(t)

        return

    # temporary remove card in list
    def afterRemoved(self, hand, remove_lst):
        result = hand.copy()
        for remove_card in remove_lst:
            for card in hand:
                if card == remove_card:
                    result.remove(card)
        return result

    # All possible output for airplane with wings
    def getLegalAirplaneWithWings(self, pre_cards):
        num = len(pre_cards)
        temp_lst = []
        lst = []
        count = int(num / 4 * 3)
        index = int(num / 4) * (-1)
        pre_card_rank = pre_cards[index - 1].getRank()

        for i in range(pre_card_rank + 1, len(self.card_dic) - 2):  # eg. temp_lst = [333444]
            if len(self.card_dic[str(i)]) >= 3:
                temp_lst += self.card_dic[str(i)][:3]
            else:
                temp_lst = []
            if len(temp_lst) == count:
                lst.append(temp_lst)
                temp_lst = temp_lst[3:]
        if len(lst) == 0:    # lst is empty return
            return []
        if len(self.cards) == len(pre_cards):    # cards is same type and same amount
            return self.cards
        copy_hand = self.cards.copy()
        m = len(self.cards) - count
        n = index * (-1)
        assert m > n
        for i in range(len(lst)):  # eg. lst = [[333444],[666777]]
            rank_lst = []
            removed_list = self.afterRemoved(copy_hand, lst[i])
            temp = removed_list.copy()
            output = []
            number = n
            self.MChooseN(m, n, temp, output, removed_list, number)
            for comb in output:
                rank_lst.append(lst[i]+comb)
        return rank_lst

    # helper function to get single card
    def getSingleCard(self, hands):
        for key in hands:
            if len(hands[key]) == 1 and not key == '14' and not key == '13':
                return hands[key][0]
        for key in hands:
            if len(hands[key]) == 2 and not key == '14' and not key == '13':
                return hands[key][0]
        if not len(hands['13']) > 0:
            return hands['13'][0]
        if not len(hands['14']) > 0:
            return hands['14'][0]
        for key in hands:
            if len(hands[key]) == 3 and not key == '14' and not key == '13':
                return hands[key][0]
        return []

    # check if the cards have bomb or rocket
    def getBomborRocker(self, state=1):
        output = []
        if len(self.card_dic['14']) == 2:
            output.append(self.card_dic['14'])
        if state == 0:
            return output
        for key in self.card_dic:
            if len(self.card_dic[key]) == 4:
                temp = self.card_dic[str(key)]
                output.append(temp)
        return output

    # if hand have bomb or rocket, return them with score
    def calculateSpecialoutput(self, gene, state=0):
        count = 0
        all_score_list = []
        self.output_point = []
        if len(self.card_dic['14']) == 2:
            index = self.converter("ROCKET")
            score = 14 * gene[index]
            all_score_list = np.array([self.combination_dic["ROCKET"][0], score])
        if state == 1:
            return all_score_list
        if not len(self.combination_dic["BOMB"]) == 0:
            index = self.converter("BOMB")
            _, score_lst = self.helperCountPoints(self.combination_dic["BOMB"], gene[index])
            all_score_list = score_lst if len(all_score_list) == 0 else np.vstack([all_score_list, score_lst])

        return all_score_list

    # print all card in hand as dictionary
    def print(self):
        for card in self.card_dic:
            print(card + ":" + str(len(self.card_dic[card])) + " ", end="")

