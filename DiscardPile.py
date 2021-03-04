from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PlayerCard import *


class DiscardPile(PlayerCard):

    def __init__(self):
        super().__init__()

    def addLabel(self, label):
        label.hide()
        self.labels.append(label)

    # hide all labels in the list
    def hideAll(self):
        for label in self.labels:
            label.hide()

    # return max size
    def size(self):
        return 20

    # display the card
    def displayCard(self, showList):
        self.hideAll()
        k = int((20 - len(showList)) / 2)
        # sort the card
        for card in showList:
            self.labels[k].setPixmap(QPixmap(card.getFace()))
            self.labels[k].show()
            k += 1
