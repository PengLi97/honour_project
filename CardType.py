
# each card corresponding rank:
# 3,4,...., 10, J, Q, K, A, 2,JokerB, JokerR
# 1,2,....,  8, 9,10,11,12,13,    14,     14

class CardType:
    def __init__(self, rank, suit, face):
        suitType = ['club', 'spade', 'dimond', 'heart']
        jokerType = ['red', 'black']
        assert -1 < rank < 15
        assert type(face) == str
        assert type(suit) == str
        if rank == 14:
            assert suit in jokerType
        else:
            assert suit in suitType

        self.rank = rank
        self.suit = suit
        self.face = face
        self.label = None
        if type(suit) is jokerType:
            if suit == 'red':
                self.weight = rank + 4
        self.weight = rank + 3

    def getRank(self):
        return self.rank

    def getFace(self):
        return self.face

    def getLabel(self):
        return self.label

    def getSuit(self):
        return self.suit

    def setRank(self,rank):
        self.rank = rank

    def setFace(self,face):
        self.face = face

    def setSuit(self,suit):
        self.suit = suit

    def setLabel(self,label):
        self.label = label

    def getWeight(self):
        return self.weight
