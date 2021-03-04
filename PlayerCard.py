from Sound import *
from HandsCards import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from Genetic import *


class PlayerCard:

    def __init__(self):
        self.identify = -1  # initialized the identity, 1 is landlord, 0 is leftside at landlord, 2 is rightside
        self.labels = []    # initialized empty label
        self.bomb = 0       # check for bomb or rocket happen
        self.hand = HandsCards([])
        self.gene = Genetic()
        self.saveInstance = []

    def setGenetic(self):
        self.gene.setDNA(self.identify)

    def getGeneAndIdentify(self):
        return self.identify, self.gene.gene

    def getGenetic(self):
        return self.gene

    def getHand(self):
        return self.hand

    # add label for the card
    def addLabel(self, label):
        label.hide()
        self.labels.append({'QLabel': label, 'Card': None})

    # check the card is empty or not
    def isEmpty(self):
        for label in self.labels:
            if not label['QLabel'].isHidden():
                return False
        return True

    # hide all labels in the list
    def hideAll(self):
        for label in self.labels:
            label['QLabel'].hide()

    # display the card
    def displayCard(self, showList, bottom=0):
        self.hideAll()
        self.hand.updateHand(showList)
        self.gene.updatehand(showList)
        showList.sort(key=lambda x: x.getRank(), reverse=True)
        k = int((20 - len(showList)) / 2)
        # sort the card
        for card in showList:
            if bottom == 1:
                self.labels[k]['QLabel'].setPixmap(QPixmap("image/cardBack.jpg"))
            else:
                self.labels[k]['QLabel'].setPixmap(QPixmap(card.getFace()))
            self.labels[k]['QLabel'].show()
            self.labels[k]['Card'] = card
            k += 1
        self.saveInstance = self.save(showList, self.gene.gene)

    # up the landlords
    def upLandlordCards(self, landlordCards):
        for label in self.labels:
            for landlordCard in landlordCards:
                if label['Card'] == landlordCard:
                    label['QLabel'].move(label['QLabel'].x(), -20)

    # play card
    def playCard(self, previous_cards):
        showed_list = []
        hand_list = []
        for label in self.labels:
            if label['QLabel'].y() == -20:
                showed_list.append(label['Card'])
        if self.isLegalShow(showed_list, previous_cards):
            for label in self.labels:
                if label['QLabel'].y() == -20:
                    label['QLabel'].hide()
                    label['QLabel'].move(label['QLabel'].x(), 0)

                elif not label['QLabel'].isHidden():
                    hand_list.append(label['Card'])
            self.displayCard(hand_list)
            if self.bomb == 1:
                Sound.bomb()
                self.bomb = 0
            else:
                Sound.cardShove()

            return showed_list, hand_list
        return [], hand_list

    # check the user play the cards are legal
    def isLegalShow(self, showed_cards, previous_cards):
        temp = self.getCombination(showed_cards)
        prc = self.getCombination(previous_cards)
        if len(prc) == 0 and not len(temp) == 0:
            if temp['combination'] == "ROCKET" or temp['combination'] == "BOMB":
                self.bomb = 1
            return True
        if temp == {}:
            return False
        if (temp['combination'] == "BOMB" or temp['combination'] == "ROCKET") and not prc['combination'] == "BOMB":
            self.bomb = 1
            return True
        if (len(temp) > 0 and temp['combination'] == prc['combination'] and
                temp['rank'] > prc['rank'] and temp['numberOfCards'] == prc['numberOfCards']):
            if temp['combination'] == "BOMB":  # check if it is a bigger bomb
                self.bomb = 1
            return True
        return False

    # show card in hand
    def autoshowCard(self, remove_cards, bottom=0):
        # hand = self.getCards()
        hand = self.hand.getCards()
        temp = []
        status = 0
        for card in hand:
            for delete_card in remove_cards:
                if card.getFace() == delete_card.getFace():
                    status = 1
                    break
            if status == 1:
                status = 0
            else:
                temp.append(card)
        if self.bomb == 1:
            Sound.bomb()
            self.bomb = 0
        else:
            Sound.cardShove()
        self.displayCard(temp,bottom)
        return temp

    # set identify
    def setIdentify(self, n):
        assert type(n) == int
        self.identify = n
        self.setGenetic()

    # add card to hand
    def getIdentify(self):
        return self.identify

    # re-select the card in hand
    def reSelect(self):
        for label in self.labels:
            if label['QLabel'].y() == -20:
                label['QLabel'].move(label['QLabel'].x(), 0)

    # to get the card
    def getCards(self):
        lst = []
        for label in self.labels:
            if not label['QLabel'].isHidden():
                lst.append(label['Card'])
        return lst

    # to heple autoplay function player card
    def help_autoplay(self, current_id, pr_id, cards, pre_cards, length, n):
        if length == 0 or cards == []:
            return []
        if current_id == 1 or current_id == 2:
            if current_id == 2 and pr_id == 0:
                return []
            else:
                return cards[0]
        elif current_id == 0:
            if pre_cards[0].getRank() > 12 and pr_id == 2 and n == 1:
                return []
            elif pre_cards[0].getRank() > 11 and pr_id == 2 and n == 2:
                return []
            elif pre_cards[0].getRank() > 10 and pr_id == 2 and n == 3:
                return []
            elif pre_cards[0].getRank() > 9 and pr_id == 2 and n == 4 or n == 5:
                return []
            elif pr_id == 2 and n == 7 or n == 8:
                return []

            else:
                for card in cards:
                    if card == []:
                        return []
                    if card[0].getRank() > 9:
                        return card
                    if n == 1 and card[0].getRank() == 14:
                        if pre_cards[0].getSuit() == 'Red':
                            return []
                        else:
                            return card
                return cards[0]

    # autoplay for noob computer
    def autoplay_noob(self, previous_cards):
        cards = []
        hand = self.getCards()
        card_dic = {'1': [], '2': [], '3': [], '4': [], '5': [], '6': [], '7': [], '8': [], '9': [], '10': [], '11': [],
                    '12': [], '13': [], '14': []}
        for card in hand:
            card_dic[str(card.getRank())].append(card)
        dic = self.getCombination(previous_cards)
        if len(dic) == 0:
            return [hand[-1]]
        if dic['combination'] == 'SINGLE':
            cards = self.getSingle(card_dic, dic['rank'])
        if dic['combination'] == 'PAIR':
            cards = self.getOnePair(card_dic, dic['rank'])
        if dic['combination'] == 'THREE':
            cards = self.getThree(card_dic, dic['rank'])
        if dic['combination'] == 'THREE_ONE':
            cards = self.getThreeWithOne(card_dic, dic['rank'])
        if dic['combination'] == 'CHAIN':
            cards = self.getChain(card_dic, dic['rank'], dic['numberOfCards'])
        if dic['combination'] == 'AIRPLANE':
            cards = self.getAirplane(card_dic, dic['rank'], dic['numberOfCards'])
        if dic['combination'] == 'PAIR_CHAIN':
            cards = self.getPairChain(card_dic, dic['rank'], dic['numberOfCards'])
        if dic['combination'] == 'AIRPLANE_WINGS':
            cards = self.getAirplaneWings(card_dic, dic['rank'], dic['numberOfCards'])
        if dic['combination'] == 'BOMB':
            cards = self.getBomb(card_dic, dic['rank'])
        return cards

    # autoplay for computer
    def autoplay(self, previous_cards, current_id, pr_id=-1):
        dic = self.getCombination(previous_cards)

        # when start a new turn
        if len(dic) == 0:
            dic = self.hand.getALLCombination()
            dic_card = self.hand.getDicCards()
            single = []
            for key in dic_card:
                if len(dic_card[key]) == 1 and int(key) < 12:
                    single.append(dic_card[key])
            # key   ROCKET AIRPLANE_WINGS AIRPLANE CHAIN_PAIR CHAIN BOMB THREE_ONE THREE PAIR SINGLE
            # index 0      1              2        3          4     5    6         7     8    9
            for index, key in enumerate(reversed(dic)):
                if len(dic[key]) > 0:
                    # only left two joker
                    if len(self.hand.getCards()) == 2 and (index == 0 or index == 8):
                        if type(dic[key][0]) == list:
                            return dic[key][0]
                        return dic[key]
                    # only left three
                    elif len(self.hand.getCards()) == 3:
                        if index == 0:
                            return dic[key][0]
                        if index == 7:
                            return dic[key][0]
                        if index == 8:
                            if self.hand.getCards()[1].getRank() > self.hand.getCards()[2].getRank() or self.hand.getCards()[1].getRank() > self.hand.getCards()[0].getRank():
                                return dic[key][0]
                            return self.hand.getCards()[1] if self.hand.getCards()[0].getRank() > self.hand.getCards()[1].getRank() else self.hand.getCards()[0]
                    # only left three with one or bomb
                    elif len(self.hand.getCards()) == 4 and (index == 5 or index == 6):
                        return dic[key][0]
                    elif index == 1 and len(dic[key]) > 0:
                        return dic[key][0]
                    elif len(single) > 4:
                        return single[0]
                    if len(dic[key]) > 0 and not index == 0 and not index == 5:
                        return dic[key][0]
            return [self.hand.getCards()[-1]]

        # In each turn, check previous card to play
        elif dic['combination'] == 'SINGLE':
            cards = self.hand.getLegalSingle(list(previous_cards))
            cards = self.help_autoplay(current_id, pr_id, cards, previous_cards, len(cards), 1)
        elif dic['combination'] == 'PAIR':
            cards = self.hand.getLegalPair(previous_cards)
            cards = self.help_autoplay(current_id, pr_id, cards, previous_cards, len(cards), 2)
        elif dic['combination'] == 'THREE':
            cards = self.hand.getLegalThree(previous_cards)
            cards = self.help_autoplay(current_id, pr_id, cards, previous_cards, len(cards), 3)
        elif dic['combination'] == 'THREE_ONE':
            cards = self.hand.getLegalThreeWithOne(previous_cards)
            cards = self.help_autoplay(current_id, pr_id, cards, previous_cards, len(cards), 4)
        elif dic['combination'] == 'CHAIN':
            cards = self.hand.getLegalChain(previous_cards)
            cards = self.help_autoplay(current_id, pr_id, cards, previous_cards, len(cards), 5)
        elif dic['combination'] == 'AIRPLANE':
            cards = self.hand.getLegalAirplane(previous_cards)
            cards = self.help_autoplay(current_id, pr_id, cards, previous_cards, len(cards), 6)
        elif dic['combination'] == 'CHAIN_PAIR':
            cards = self.hand.getLegalPairChain(previous_cards)
            cards = self.help_autoplay(current_id, pr_id, cards, previous_cards, len(cards), 6)
        elif dic['combination'] == 'AIRPLANE_WINGS':
            cards = self.hand.getLegalAirplaneWithWings(previous_cards)
            cards = self.help_autoplay(current_id, pr_id, cards, previous_cards, len(cards), 7)
        elif dic['combination'] == 'BOMB':
            cards = self.hand.getLegalBomb(previous_cards)
            cards = self.help_autoplay(current_id, pr_id, cards, previous_cards, len(cards), 8)
        else:
            cards = self.hand.getBomborRocker(previous_cards)
            if len(cards) > 0:
                cards = cards[0]
            else:
                cards = []
        return cards

    # autoplay for computer with ai
    def autoplayAI(self, previous_cards, card_left, card_right, current_id, pr_id):
        dic = self.getCombination(previous_cards)
        special_output = self.hand.calculateSpecialoutput(self.gene.gene)
        cards = []
        score = 0
        # In each turn, check previous card to play
        # print(current_id, " ", pr_id)
        if len(dic) == 0:
            score, score_lst = self.hand.calculateHands(self.gene.gene)
            output = self.gene.chooseHighestPoint(score, score_lst, card_left, card_right,1)
            return output
        # let your teammate play
        if current_id == 2 and pr_id == 0:
            return []
        if dic['combination'] == 'ROCKET':
            return []
        elif dic['combination'] == 'SINGLE':
            cards = self.hand.getLegalSingle(list(previous_cards))
            if len(cards) > 0:
                score, score_lst = self.hand.helperCountPoints(cards, self.gene.gene[3])
        elif dic['combination'] == 'PAIR':
            cards = self.hand.getLegalPair(previous_cards)
            if len(cards) > 0:
                score, score_lst = self.hand.helperCountPoints(cards, self.gene.gene[4])
        elif dic['combination'] == 'THREE':
            cards = self.hand.getLegalThree(previous_cards)
            if len(cards) > 0:
                score, score_lst = self.hand.helperCountPoints(cards, self.gene.gene[5])
        elif dic['combination'] == 'THREE_ONE':
            cards = self.hand.getLegalThreeWithOne(previous_cards)
            if len(cards) > 0:
                score, score_lst = self.hand.helperCountPoints(cards, self.gene.gene[6])
        elif dic['combination'] == 'BOMB':
            cards = self.hand.getLegalBomb(previous_cards)
            if len(cards) > 0:
                score, score_lst = self.hand.helperCountPoints(cards, self.gene.gene[7])
                output = self.hand.calculateSpecialoutput(self.gene.gene, 1)
                if len(output) > 0:  # if have two jocker
                    output = np.vstack([np.array([[], -99999]), output])       # to aviod output only have one element
                    score_lst = np.vstack([np.array([[], -999999]), score_lst]) # to aviod score_lst only have one element
                    score_lst = np.vstack([score_lst, output])
                output = self.gene.chooseHighestPoint(score, score_lst, card_left, card_right)
                return output
            return []
        elif dic['combination'] == 'CHAIN':
            cards = self.hand.getLegalChain(previous_cards)
            if len(cards) > 0:
                score, score_lst = self.hand.helperCountPoints(cards, self.gene.gene[8])
        elif dic['combination'] == 'CHAIN_PAIR':
            cards = self.hand.getLegalPairChain(previous_cards)
            if len(cards) > 0:
                score, score_lst = self.hand.helperCountPoints(cards, self.gene.gene[9])
        elif dic['combination'] == 'AIRPLANE':
            cards = self.hand.getLegalAirplane(previous_cards)
            if len(cards) > 0:
                score, score_lst = self.hand.helperCountPoints(cards, self.gene.gene[10])
        elif dic['combination'] == 'AIRPLANE_WINGS':
            cards = self.hand.getLegalAirplaneWithWings(previous_cards)
            if len(cards) > 0:
                score, score_lst = self.hand.helperCountPoints(cards, self.gene.gene[11])
        if cards == []:
            if not special_output == []:
                return self.gene.chooseHighestPoint(score, special_output, card_left, card_right)
            return []
        if len(special_output) > 0:
            output = np.vstack([np.array([[], -999999]), special_output])        # to aviod output only have one element
            if not score_lst == []:
                score_lst = np.vstack([np.array([[], -999999]), score_lst])         # to aviod score_lst only have one element
                score_lst = np.vstack([score_lst, output])
            else:
                score_lst = output
            output = self.gene.chooseHighestPoint(score, score_lst, card_left, card_right)
        else:
            # print("score_list: " ,score_lst[:3])
            output = self.gene.chooseHighestPoint(score, score_lst, card_left, card_right)
            # print(output)
        return output

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
        length = len(lstOfCard)/3
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
            if lstOfCard[i].getRank() == lstOfCard[i + 1].getRank() and lstOfCard[i].getRank() == lstOfCard[i + 2].getRank():
                record.append(lstOfCard[i])
                i += 3
                continue
            i += 1
        if len(record) <= 1:
            return False
        if len(record) == wings_length and self.isChain(record):
            return record[0].getRank()
        if self.isChain(record[:wings_length]) or self.isChain(record[1:wings_length + 1]):
            return record[1].getRank()

        return False

    # check the card is what kind of combination
    def getCombination(self, lstOfCard):
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

    # save the date into file
    def save(self, hand, gene):
        data = hand.copy()
        data.append(gene)
        data.append(len(hand))
        data.append(self.identify)
        data = np.asarray(data)   # data [ cardlst , gene , length of card, identify]
        return data

    # logic for Single
    def getSingle(self, card_dic, rank):
        for key in card_dic:
            if len(card_dic[key]) == 1:
                if int(key) > rank:
                    return card_dic[key]
                elif int(key) == 14 and rank == 14:
                    if card_dic[key][0].getSuit() == 'red':
                        return card_dic[key]
        for key in card_dic:
            if len(card_dic[key]) == 2 and int(key) > rank:
                return [card_dic[key][0]]
        for key in card_dic:
            if len(card_dic[key]) == 3 and int(key) > rank:
                return [card_dic[key][0]]
        return self.getBomb(card_dic)

    # logic for OnePair
    def getOnePair(self, card_dic, rank):
        for key in card_dic:
            if len(card_dic[key]) == 2 and int(key) > rank:
                return card_dic[key]
        for key in card_dic:
            if len(card_dic[key]) == 3 and int(key) > rank:
                return card_dic[key][:2]
        return self.getBomb(card_dic)

    # logic for Three
    def getThree(self, card_dic, rank):
        for key in card_dic:
            if len(card_dic[key]) == 3 and int(key) > rank:
                return card_dic[key]
        return self.getBomb(card_dic)

    # logic for ThreeWithOne
    def getThreeWithOne(self, card_dic, rank):
        lst = []
        temp = card_dic.copy()
        for key in card_dic:
            if len(card_dic[key]) == 3 and int(key) > rank:
                lst += card_dic[key]
                temp[key] = []
                break
        card = self.getSingle(temp, 0)
        if len(lst) == 0:
            return self.getBomb(card_dic)
        return lst + card

    # logic for Bomb
    def getBomb(self, card_dic, rank=0):
        for key in card_dic:
            if len(card_dic[key]) == 4 and int(key) > rank:
                self.bomb = 1
                return card_dic[key]
        if len(card_dic['14']) == 2:
            self.bomb = 1
            return card_dic['14']
        return []

    # logic for Chain
    def getChain(self, card_dic, rank, num):
        lst = []
        for i in range(rank + 1, len(card_dic) - 2):
            if len(card_dic[str(i)]) > 0:
                lst.append(card_dic[str(i)][0])
            else:
                lst = []
            if len(lst) == num:
                return lst
        return self.getBomb(card_dic)

    # logic for Airplane
    def getAirplane(self, card_dic, rank, num):
        lst = []
        for i in range(rank + 1, len(card_dic) - 2):
            if len(card_dic[str(i)]) > 2:
                lst += card_dic[str(i)][:3]
            else:
                lst = []
            if len(lst) == num:
                return lst
        return self.getBomb(card_dic)

    # logic for PairChain
    def getPairChain(self, card_dic, rank, num):
        lst = []
        for i in range(rank + 1, len(card_dic) - 2):
            if len(card_dic[str(i)]) > 1:
                lst += card_dic[str(i)][:2]
            else:
                lst = []
            if len(lst) == num:
                return lst
        return self.getBomb(card_dic)

    # logic for AirplaneWings
    def getAirplaneWings(self, card_dic, rank, num):
        lst = []
        temp = card_dic.copy()
        count = int(num / 4 * 3)
        for i in range(rank + 1, len(card_dic) - 2):
            if len(card_dic[str(i)]) == 3:
                lst += card_dic[str(i)]
            else:
                lst = []
            if len(lst) == count:
                for card in lst:
                    temp[str(card.getRank())] = []
                break
        for i in range(int(count / 3)):
            cardInlst = self.getSingle(temp, 0)
            lst.append(cardInlst[0])
            temp[str(cardInlst[0].getRank())].pop()
        if lst == [] or not lst == num:
            return self.getBomb(card_dic)
        return lst
