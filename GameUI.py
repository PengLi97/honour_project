import sys
import random

from CardType import *
from PlayerCard import *
from Genetic import *
from DiscardPile import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import numpy as np

class cardLabel(QLabel):
    clicked = pyqtSignal()

    def mouseReleaseEvent(self, QMouseEvent):
        if QMouseEvent.button() == Qt.LeftButton:
            self.clicked.emit()

class GameUI(QWidget):

    def __init__(self):
        super().__init__()
        self.landlord_label_bottom = QLabel(self)
        self.landlord_label_right = QLabel(self)
        self.landlord_label_left = QLabel(self)
        self.pass_label_bottom = QLabel(self)
        self.pass_label_right = QLabel(self)
        self.pass_label_left = QLabel(self)
        self.record_right = QLabel("17", self)
        self.record_left = QLabel("17", self)
        self.initUI()       # initialize
        self.winner = -1    # initialize winner 0 = left player, 1 = user, 2 = right player
        self.count = 0      # count each round
        self.nobid_count = 0 # count if no one bid, game should restart
        self.ai = 0

        self.count_l_b_r = [0, 0, 0]
        self.loop = 0
        self.count_win = 0
        self.ai_state = 3 # 1: landlord use genetic  0: is farmer use genetic  -1: both use  3: both not use
        self.noob = True #  noob computer palyer active when it is true

    def initUI(self):
        self.resize(1400, 800)  # windows size
        self.setFixedSize(1400, 800)
        self.setWindowTitle('Fighting the Landlord')  # window title
        self.setWindowIcon(QIcon('icon.jpg'))  # window icon
        oImage = QImage("image/gamebackground.jpg")
        sImage = oImage.scaled(QSize(1400, 800))  # resize Image to widgets size
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(sImage))
        self.setPalette(palette)
        # using counter to show computer action slowly
        self.timer = QBasicTimer()
        self.timer.start(200, self)
        self.counter = 9999

        self.initgamePage()

    # initialize the start page
    def initgamePage(self):
        style0 = ("QPushButton{color:#169BD5}"
                  "QPushButton:hover{color:blue}"
                  "QPushButton{background-color:orange}"
                  "QPushButton:hover{background-color:yellow}"
                  "QPushButton{border-radius:10px}"
                  "QPushButton{width:80}"
                  "QPushButton{height:30}"
                  "QPushButton{font-size:18px}")
        style1 = ("QLabel{font-size:20px}"
                  "QLabel{color:#169BD5})")

        style2 = ("QLabel{width:80}"
                  "QLabel{height:80}")

        cardback = QPixmap('image/cardBack.jpg')  # set back of card's picture

        # label for card
        self.record_left.setFixedSize(60, 60)
        self.record_left.setStyleSheet(style1)
        self.record_left.move(130, 600)
        self.record_right.setFixedSize(60, 60)
        self.record_right.setStyleSheet(style1)
        self.record_right.move(1250, 600)
        # display pass if player pss the turn
        pixmap = QPixmap('image/pass.png')
        self.pass_label_left.setStyleSheet(style2)
        self.pass_label_left.setPixmap(pixmap)
        self.pass_label_left.move(300, 300)
        self.pass_label_left.hide()
        self.pass_label_right.setStyleSheet(style2)
        self.pass_label_right.setPixmap(pixmap)
        self.pass_label_right.move(1000, 300)
        self.pass_label_right.hide()
        self.pass_label_bottom.setStyleSheet(style2)
        self.pass_label_bottom.setPixmap(pixmap)
        self.pass_label_bottom.move(600, 500)
        self.pass_label_bottom.hide()
        # label shows who's the landlord
        pixmap = QPixmap('image/landlord_pic.png')
        self.landlord_label_left.setStyleSheet(style2)
        self.landlord_label_left.setPixmap(pixmap)
        self.landlord_label_left.move(0, 600)
        self.landlord_label_right.setStyleSheet(style2)
        self.landlord_label_right.setPixmap(pixmap)
        self.landlord_label_right.move(1330, 600)
        self.landlord_label_bottom.setStyleSheet(style2)
        self.landlord_label_bottom.setPixmap(pixmap)
        self.landlord_label_bottom.move(1200, 720)

        # frame record 3 card on top
        frame_top = QFrame(self)
        frame_top.resize(400, 150)
        frame_top.move(500, 10)

        self.label_top1 = QLabel(frame_top)
        self.label_top1.setFixedSize(105, 150)
        pixmap = QPixmap('image/cardBack.jpg')
        self.label_top1.setPixmap(pixmap)
        self.label_top1.move(0, 0)

        self.label_top2 = QLabel(frame_top)
        self.label_top2.setFixedSize(105, 150)
        pixmap = QPixmap('image/cardBack.jpg')
        self.label_top2.setPixmap(pixmap)
        self.label_top2.move(110, 0)

        self.label_top3 = QLabel(frame_top)
        self.label_top3.setFixedSize(105, 150)
        pixmap = QPixmap('image/cardBack.jpg')
        self.label_top3.setPixmap(pixmap)
        self.label_top3.move(220, 0)

        # frame at bottom side to show card
        self.frame_bottom = QFrame(self)
        self.frame_bottom.resize(1000, 160)
        self.frame_bottom.move(200, 630)

        # frame at left side to show card
        self.frame_left = QFrame(self)
        self.frame_left.resize(120, 540)
        self.frame_left.move(80, 70)

        # frame at right side to show card
        self.frame_right = QFrame(self)
        self.frame_right.resize(120, 540)
        self.frame_right.move(1200, 70)

        self.player_card_bottom = PlayerCard()
        self.player_card_left = PlayerCard()
        self.player_card_right = PlayerCard()
        j, k = 40, 0
        for i in range(20):
            temp_b = cardLabel(self.frame_bottom)
            temp_l = cardLabel(self.frame_left)
            temp_r = cardLabel(self.frame_right)
            temp_b.resize(120, 180)
            temp_l.resize(120, 180)
            temp_r.resize(120, 180)
            temp_b.move(j, 0)
            temp_l.move(0, k)
            temp_r.move(0, k)
            temp_b.clicked.connect(self.click_card)
            self.player_card_bottom.addLabel(temp_b)
            self.player_card_left.addLabel(temp_l)
            self.player_card_right.addLabel(temp_r)
            j += 40
            k += 20

        # left palyed card
        frame_left_played = QFrame(self)
        frame_left_played.resize(500, 160)
        frame_left_played.move(210, 200)
        self.discard_pile_left = DiscardPile()

        # right palyed card
        frame_right_played = QFrame(self)
        frame_right_played.resize(500, 160)
        frame_right_played.move(700, 200)
        self.discard_pile_right = DiscardPile()

        # bottom palyed card
        frame_bottom_played = QFrame(self)
        frame_bottom_played.resize(600, 180)
        frame_bottom_played.move(400, 400)
        self.discard_pile_bottom = DiscardPile()

        j = 0
        for i in range(20):
            temp_b = QLabel(frame_bottom_played)
            temp_l = QLabel(frame_left_played)
            temp_r = QLabel(frame_right_played)
            temp_b.resize(120, 180)
            temp_l.resize(120, 180)
            temp_r.resize(120, 180)
            temp_b.move(j, 0)
            temp_l.move(j, 0)
            temp_r.move(j, 0)
            j += 25
            self.discard_pile_bottom.addLabel(temp_b)
            self.discard_pile_left.addLabel(temp_l)
            self.discard_pile_right.addLabel(temp_r)

        # button
        self.loading = QPushButton(" Load ", self)
        self.loading.setStyleSheet(style0)
        self.loading.resize(100, 30)
        self.loading.move(1090, 10)
        self.loading.clicked.connect(self.load)
        self.newgame = QPushButton(" New Game ", self)
        self.newgame.setStyleSheet(style0)
        self.newgame.resize(100, 30)
        self.newgame.move(1200, 10)
        self.newgame.clicked.connect(self.new_game)
        self.exit = QPushButton("EXIT", self)
        self.exit.setStyleSheet(style0)
        self.exit.move(1310, 10)
        self.exit.clicked.connect(self.to_close)
        self.play = QPushButton("  play ", self)
        self.play.setStyleSheet(style0)
        self.play.move(800, 550)
        self.play.clicked.connect(self.show_cards)
        self.reselect = QPushButton("re-select", self)
        self.reselect.setStyleSheet(style0)
        self.reselect.move(600, 550)
        self.reselect.clicked.connect(self.reSelect)
        self.pass_turn = QPushButton("pass", self)
        self.pass_turn.setStyleSheet(style0)
        self.pass_turn.move(400, 550)

        self.pass_landlord = QPushButton("pass", self)
        self.pass_landlord.setStyleSheet(style0)
        self.pass_landlord.move(500, 550)
        self.bid = QPushButton("bid", self)
        self.bid.setStyleSheet(style0)
        self.bid.move(700, 550)

        self.pass_landlord.clicked.connect(self.passLandlord)
        self.pass_turn.clicked.connect(self.passTurn)
        self.bid.clicked.connect(self.bidLandlord)

        self.ai_button = QPushButton("AI", self)
        self.ai_button.setStyleSheet(style0)
        self.ai_button.move(50, 750)
        self.ai_button.clicked.connect(self.switchAI)

        self.level_button = QPushButton("level-1(noob)", self)
        self.level_button.setStyleSheet(style0)
        self.level_button.resize(120, 30)
        self.level_button.move(50, 50)
        self.level_button.clicked.connect(self.switchLevel)


        # winner label
        pixmap = QPixmap('image/win.png')
        self.winner_label = QLabel(self)
        self.winner_label.setPixmap(pixmap)
        self.winner_label.move(420, 150)
        self.winner_label.hide()
        pixmap = QPixmap('image/landlordwin.png')
        self.winner_landlord_label = QLabel(self)
        self.winner_landlord_label.setPixmap(pixmap)
        self.winner_landlord_label.move(520, 220)
        self.winner_landlord_label.hide()
        pixmap = QPixmap('image/framerwin.png')
        self.winner_framer_label = QLabel(self)
        self.winner_framer_label.setPixmap(pixmap)
        self.winner_framer_label.move(520, 220)
        self.winner_framer_label.hide()

        # refresh the desk, and random give to three players and sort it
        self.hideAll()

    # inital game board function
    def initgameBoard(self):
        self.discard_pile_bottom.hideAll()
        self.discard_pile_left.hideAll()
        self.discard_pile_right.hideAll()
        self.previous_cards = [[], []]
        self.previous_cards_id = -1
        self.nobid_count = 0
        self.counter = 9999
        desk = []
        suitType = ['club', 'spade', 'dimond', 'heart']
        jokerType = ['red', 'black']
        for i in range(52):
            rank = i % 13 + 1
            suit = suitType[i % 4]
            face = 'image/' + suit[0] + str(rank) + '.jpg'
            card = CardType(rank, suit, face)
            desk.append(card)
        desk.append(CardType(14, jokerType[1], "image/jokerB.jpg"))
        desk.append(CardType(14, jokerType[0], "image/jokerR.jpg"))
        random.shuffle(desk)
        self.cards_left = desk[:17]
        self.cards_right = desk[17:34]
        self.cards_bottom = desk[34:51]
        self.landlordCard = desk[51:]

        self.player_card_left.displayCard(desk[:17], 1)
        self.player_card_right.displayCard(desk[17:34], 1)
        self.player_card_bottom.displayCard(desk[34:51])

        self.reSelect()
        self.label_top1.setPixmap(QPixmap('image/cardBack.jpg'))
        self.label_top2.setPixmap(QPixmap('image/cardBack.jpg'))
        self.label_top3.setPixmap(QPixmap('image/cardBack.jpg'))
        self.num_left = 17
        self.num_right = 17
        self.record_left.setText(str(self.num_left))
        self.record_right.setText(str(self.num_right))

    # swith to ai
    def switchAI(self):
        if self.ai == 1:
            self.ai = 0
            self.ai_button.setText("AI")
        else:
            self.ai = 1
            self.ai_button.setText("User")

    # swith the level of the game
    def switchLevel(self):
        if self.level_button.text().__str__() == "level-1(noob)":
            self.noob = False
            self.ai_state = 3
            self.level_button.setText("level-2")
        elif self.level_button.text().__str__() == "level-2":
            self.ai_state = -1
            self.level_button.setText("level-3(AI)")
        else:
            self.noob = True
            self.ai_state = 3
            self.level_button.setText("level-1(noob)")

    # new game button clicked
    def new_game(self):
        self.count_l_b_r = [0, 0, 0]
        Sound.sortcard()
        self.initgameBoard()
        self.winner_framer_label.hide()
        self.winner_label.hide()
        self.winner_landlord_label.hide()
        self.startGame()

    # load the previous crash game, or unfinished game
    def load(self):
        # data [ cardlst , gene , length of card, identify]
        d_left = np.load("database/left_data.npy", allow_pickle=True)
        d_right = np.load("database/right_data.npy", allow_pickle=True)
        d_bottom = np.load("database/bottom_data.npy", allow_pickle=True)
        # if d_left[0] == "None" or d_right[0] == "None" or d_bottom == "None":
        #     return
        self.player_card_left.displayCard(d_left[:-3].tolist(), 1)
        self.player_card_left.setIdentify(d_left[-1])
        if d_left[-1] == 1:
            self.landlord_label_left.show()
        self.player_card_left.gene.gene = d_left[-3]
        self.player_card_left.gene.updatehand_left(d_right[:-3].tolist())
        self.player_card_left.gene.updatehand_right(d_bottom[:-3].tolist())
        self.player_card_left.gene.updateLeftRightInformation(self.player_card_right.identify,
                                                              self.player_card_bottom.identify,
                                                              d_right[-3],
                                                              d_bottom[-3])
        self.num_left = d_left[-2]
        self.record_left.setText((str(self.num_left)))

        self.player_card_right.displayCard(d_right[:-3].tolist(), 1)
        self.player_card_right.setIdentify(d_right[-1])
        if d_right[-1] == 1:
            self.landlord_label_right.show()
        self.player_card_right.gene.gene = d_right[-3]
        self.player_card_right.gene.updatehand_left(d_bottom[:-3].tolist())
        self.player_card_right.gene.updatehand_right(d_left[:-3].tolist())
        self.player_card_right.gene.updateLeftRightInformation(self.player_card_bottom.identify,
                                                              self.player_card_left.identify,
                                                              d_bottom[-3],
                                                              d_left[-3])
        self.num_right = d_right[-2]
        self.record_right.setText((str(self.num_right)))

        self.player_card_bottom.displayCard(d_bottom[:-3].tolist())
        self.player_card_bottom.setIdentify(d_bottom[-1])
        if d_bottom[-1] == 1:
            self.landlord_label_bottom.show()
        self.player_card_bottom.gene.gene = d_bottom[-3]
        self.player_card_bottom.gene.updatehand_left(d_left[:-3].tolist())
        self.player_card_bottom.gene.updatehand_right(d_right[:-3].tolist())
        self.player_card_bottom.gene.updateLeftRightInformation(self.player_card_left.identify,
                                                              self.player_card_right.identify,
                                                              d_left[-3],
                                                              d_right[-3])

        d_pre = np.load("database/preivouscard_data.npy", allow_pickle=True)
        d_pre = d_pre.tolist()
        self.previous_cards = [d_pre[0], d_pre[1]]
        d_topThree = np.load("database/topThree_data.npy", allow_pickle=True)
        self.landlordCard = d_topThree[:-2].tolist()
        self.previous_cards_id = d_topThree[-1]
        if d_topThree[-1] == "left":
            self.counter = 40
        elif d_topThree[-1] == "right":
            self.counter = 90
        else:
            self.userPlay()

    # close game
    def to_close(self):
        self.timer.stop()
        self.close()

    # move card up and down
    def click_card(self):
        label = self.sender()
        Sound.click()
        if label.y() == 0:
            label.move(label.x(), label.y() - 20)
        else:
            label.move(label.x(), label.y() + 20)

    # re-select the card
    def reSelect(self):
        self.player_card_bottom.reSelect()

    # pass to next player
    def passTurn(self):
        if len(self.previous_cards[0]) == 0 and len(self.previous_cards[1]) == 0:
            return
        self.previous_cards_id = self.player_card_left.getIdentify()
        self.previous_cards.pop()
        self.previous_cards.insert(0, [])
        self.discard_pile_bottom.hideAll()
        self.pass_label_bottom.show()
        self.hideUserButton()
        self.counter = 40  # call autoPlayRight()
        self.pass_label_right.hide()  # hide pass label for right
        self.discard_pile_right.hideAll()
        Sound.passToNext()
        self.saveInstance("bottom")

    def saveInstance(self, player):
        data_previouscard = self.previous_cards.copy()
        data_previouscard =np.asarray(data_previouscard)
        # topthree [ three card, who's turn, pre_id]
        data_topThree = self.landlordCard.copy()
        data_topThree.append(player)
        data_topThree.append(self.previous_cards_id)
        data_topThree = np.asarray(data_topThree)
        np.save("database/preivouscard_data", data_previouscard)
        np.save("database/topThree_data", data_topThree)

    # display the button
    def displayUserButtons(self):
        self.play.show()
        self.pass_turn.show()
        self.reselect.show()
        self.pass_landlord.hide()
        self.bid.hide()

    # start biding the landlord
    def bidLandlord(self):
        self.player_card_bottom.setIdentify(1)
        self.player_card_left.setIdentify(0)
        self.player_card_right.setIdentify(2)
        self.cards_bottom += self.landlordCard
        self.updateInfo_bid(self.player_card_right, self.player_card_left, self.player_card_bottom)
        self.player_card_bottom.displayCard(self.cards_bottom)
        self.player_card_bottom.upLandlordCards(self.landlordCard)
        self.displayTopCards()
        self.displayUserButtons()
        self.landlord_label_bottom.show()

    # display landlord card on the top
    def displayTopCards(self):
        self.label_top1.setPixmap(QPixmap(self.landlordCard[0].getFace()))
        self.label_top2.setPixmap(QPixmap(self.landlordCard[1].getFace()))
        self.label_top3.setPixmap(QPixmap(self.landlordCard[2].getFace()))

    # not bid the landlord
    def passLandlord(self):
        self.bid.hide()
        self.pass_landlord.hide()
        self.pass_label_bottom.show()
        self.counter = 40  # pass to righter player
        self.nobid_count += 1
        if not self.nobid_count == 3:
            self.checkLandlord(1)
            Sound.passToNext()
        else:
            self.new_game()

    # def start the game
    def startGame(self):
        self.hideAll()
        num = random.randint(0, 2)
        Sound.sortcard()
        self.checkLandlord(num)

    def updateInfo_bid(self, r, l, b):
        # update information for each genetic class
        r_identify, r_g = r.getGeneAndIdentify()
        l_identify, l_g = l.getGeneAndIdentify()
        b_identify, b_g = b.getGeneAndIdentify()
        r.getGenetic().updateLeftRightInformation(b_identify, l_identify, b_g, l_g)
        l.getGenetic().updateLeftRightInformation(r_identify, b_identify, r_g, b_g)
        b.getGenetic().updateLeftRightInformation(l_identify, r_identify, l_g, r_g)
        # record point for each point
        r.hand.setInitialPoint(r.getGenetic().gene)
        l.hand.setInitialPoint(l.getGenetic().gene)
        b.hand.setInitialPoint(b.getGenetic().gene)

    # decide who be the landlord
    def checkLandlord(self, num):
        if num == 0:
            if self.ai == 0:
                self.bid.show()
                self.pass_landlord.show()
                self.pass_label_bottom.hide()
            else:
                self.pass_label_bottom.hide()
                status = self.player_card_bottom.getHand().bidLandlord()
                if status: # bottom is landlord
                    self.player_card_right.setIdentify(2)
                    self.player_card_left.setIdentify(0)
                    self.player_card_bottom.setIdentify(1)
                    self.cards_bottom += self.landlordCard
                    self.player_card_bottom.displayCard(self.cards_bottom)
                    self.updateInfo_bid(self.player_card_bottom, self.player_card_right, self.player_card_left)
                    self.displayTopCards()
                    self.autoPlayBottom()
                    self.landlord_label_bottom.show()
                    return
                else:
                    self.pass_label_bottom.show()
                    num = 1
                    self.nobid_count += 1
                    if not self.nobid_count == 3:
                        self.checkLandlord(num)
                        Sound.passToNext()
                    else:
                        self.new_game()
                return
        elif num == 1:
            self.pass_label_right.hide()
            status = self.player_card_right.getHand().bidLandlord()
            if status: # right is landlord
                self.player_card_right.setIdentify(1)
                self.player_card_left.setIdentify(2)
                self.player_card_bottom.setIdentify(0)
                self.cards_right += self.landlordCard
                self.player_card_right.displayCard(self.cards_right, 1)
                self.updateInfo_bid(self.player_card_right, self.player_card_left, self.player_card_bottom)
                self.num_right = 20
                self.record_right.setText(str(self.num_right))
                self.displayTopCards()
                self.autoPlayRight()

                self.landlord_label_right.show()
                return
            else:
                self.pass_label_right.show()
                num = 2
                self.nobid_count += 1
                if not self.nobid_count == 3:
                    self.checkLandlord(num)
                    Sound.passToNext()
                else:
                    self.new_game()
        else:
            self.pass_label_left.hide()
            status = self.player_card_left.getHand().bidLandlord()
            if status:           # left is landlord
                self.player_card_left.setIdentify(1)
                self.player_card_bottom.setIdentify(2)
                self.player_card_right.setIdentify(0)
                self.cards_left += self.landlordCard
                self.player_card_left.displayCard(self.cards_left,1)
                self.updateInfo_bid(self.player_card_right, self.player_card_left, self.player_card_bottom)
                self.num_left = 20
                self.record_left.setText(str(self.num_right))
                self.displayTopCards()
                self.autoPlayLeft()
                self.landlord_label_left.show()
                return
            else:
                self.pass_label_left.show()
                num = 0
                self.nobid_count += 1
                if not self.nobid_count == 3:
                    self.checkLandlord(num)
                    Sound.passToNext()
                else:
                    self.new_game()

    # left player play
    def autoPlayRight(self):
        # print("\nright:")
        self.pass_label_right.hide()
        current_cards = []
        left = self.player_card_bottom.getHand().getCards()
        right = self.player_card_left.getHand().getCards()
        if not self.previous_cards:
            self.previous_cards_id = -1
        current_id = self.player_card_right.getIdentify()
        pr_id = self.previous_cards_id
        if len(self.previous_cards[0]) > 0:
        # implement AI
            if (self.ai_state == 1 and current_id == 1) or (self.ai_state == 0 and not current_id == 1) or self.ai_state == -1:
                temp = self.player_card_right.autoplayAI(self.previous_cards[0], left, right, current_id, pr_id)
            else:   # stupid computer
                if self.noob:
                    temp = self.player_card_right.autoplay_noob(self.previous_cards[0])
                else:
                    temp = self.player_card_right.autoplay(self.previous_cards[0], current_id, pr_id)

        elif len(self.previous_cards[1]) > 0:
            # implement AI
            if (self.ai_state == 1 and current_id == 1) or (self.ai_state == 0 and not current_id == 1) or self.ai_state == -1:
                temp = self.player_card_right.autoplayAI(self.previous_cards[1], left, right, current_id, pr_id)
            else:   # stupid computer
                if self.noob:
                    temp = self.player_card_right.autoplay_noob(self.previous_cards[1])
                else:
                    temp = self.player_card_right.autoplay(self.previous_cards[1], current_id, pr_id)
        else:
        # implement AI
            if (self.ai_state == 1 and current_id == 1) or (self.ai_state == 0 and not current_id == 1) or self.ai_state == -1:
                temp = self.player_card_right.autoplayAI(self.previous_cards[0], left, right, current_id, pr_id)
            else:  # stupid computer
                if self.noob:
                    temp = self.player_card_right.autoplay_noob(self.previous_cards[0])
                else:
                    temp = self.player_card_right.autoplay(self.previous_cards[0], current_id)
        a = CardType(2, 'dimond', '-')
        if type(temp) == type(a):
            temp = [temp]
        self.previous_cards.pop()
        self.previous_cards.insert(0, temp)
        if temp == [] or len(temp) == 0:
            self.pass_label_right.show()
            Sound.passToNext()
        else:
            self.count_l_b_r[2] += 1
            self.previous_cards_id = self.player_card_right.getIdentify()
            current_cards = self.player_card_right.autoshowCard(temp,1)
            self.player_card_left.gene.updatehand_left(current_cards)
            self.player_card_bottom.gene.updatehand_right(current_cards)
            self.discard_pile_right.displayCard(temp)
            self.num_right -= len(temp)
            self.record_right.setText(str(self.num_right))

        # save instance
        c = current_cards if not current_cards == [] else self.player_card_right.getHand().getCards()
        data = self.player_card_right.save(c, self.player_card_right.gene.gene)
        np.save("database/right_data", data)
        self.saveInstance("right")

        self.pass_label_left.hide()
        self.discard_pile_left.hideAll()
        if self.player_card_right.isEmpty():
            self.winner = 2
            self.gameover(self.player_card_right, self.player_card_left, self.player_card_bottom)
            self.cleanDateInstance()
        else:
            self.counter = 90  # call autoplayLeft()

    # show the user decide cards
    def show_cards(self):
        self.counter = 9999
        self.userPlay()
        if not self.previous_cards:
            self.previous_cards_id = -1
        pr_id = self.previous_cards_id
        if len(self.previous_cards[0]) > 0:
            showed_list, current_cards = self.player_card_bottom.playCard(self.previous_cards[0])
        elif len(self.previous_cards[1]) > 0:
            showed_list, current_cards = self.player_card_bottom.playCard(self.previous_cards[1])
        else:
            showed_list, current_cards = self.player_card_bottom.playCard([])
        if not len(showed_list) == 0:
            self.previous_cards_id = self.player_card_bottom.getIdentify()
            self.previous_cards.pop()
            self.previous_cards.insert(0, showed_list)
            self.pass_label_bottom.hide()
            self.discard_pile_bottom.displayCard(showed_list)
            self.player_card_left.gene.updatehand_right(current_cards)
            self.player_card_right.gene.updatehand_left(current_cards)
            data = self.player_card_left.save(current_cards, self.player_card_bottom.gene.gene)
            np.save("database/bottom_data", data)
            self.saveInstance("bottom")
            self.counter = 40  # call autoPlayRight()
            self.hideUserButton()
            self.pass_label_right.hide()  # hide pass label for right
            self.discard_pile_right.hideAll()
        if self.player_card_bottom.isEmpty():
            self.gameover(self.player_card_bottom, self.player_card_left, self.player_card_right,0)
            self.cleanDateInstance()

    # bottom player
    def autoPlayBottom(self):
        # print("bottom:")
        current_cards = []
        self.counter = -999
        left = self.player_card_left.getHand().getCards()
        right = self.player_card_right.getHand().getCards()
        if not self.previous_cards:
            self.previous_cards_id = -1
        current_id = self.player_card_bottom.getIdentify()
        pr_id = self.previous_cards_id
        if len(self.previous_cards[0]) > 0:
            if (self.ai_state == 1 and current_id == 1) or (self.ai_state == 0 and not current_id == 1) or self.ai_state == -1:
                temp = self.player_card_bottom.autoplayAI(self.previous_cards[0], left, right, current_id, pr_id)
            else:
                if self.noob:
                    temp = self.player_card_bottom.autoplay_noob(self.previous_cards[0])
                else:
                    temp = self.player_card_bottom.autoplay(self.previous_cards[0], current_id, pr_id)
        elif len(self.previous_cards[1]) > 0:
            if (self.ai_state == 1 and current_id == 1) or (self.ai_state == 0 and not current_id == 1) or self.ai_state == -1:
                temp = self.player_card_bottom.autoplayAI(self.previous_cards[1], left, right, current_id, pr_id)
            else:
                if self.noob:
                    temp = self.player_card_bottom.autoplay_noob(self.previous_cards[1])
                else:
                    temp = self.player_card_bottom.autoplay(self.previous_cards[1], current_id, pr_id)
        else:
            if (self.ai_state == 1 and current_id == 1) or (self.ai_state == 0 and not current_id == 1) or self.ai_state == -1:
                temp = self.player_card_bottom.autoplayAI(self.previous_cards[0], left, right, current_id, pr_id)
            else:
                if self.noob:
                    temp = self.player_card_bottom.autoplay_noob(self.previous_cards[0])
                else:
                    temp = self.player_card_bottom.autoplay(self.previous_cards[0], current_id, pr_id)
        a = CardType(2, 'dimond', '-')
        if type(temp) == type(a):
            temp = [temp]
        self.previous_cards.pop()
        self.previous_cards.insert(0, temp)
        if temp == [] or len(temp) == 0:
            self.pass_label_bottom.show()
            Sound.passToNext()
        else:
            self.count_l_b_r[1] += 1
            self.previous_cards_id = self.player_card_bottom.getIdentify()
            current_cards = self.player_card_bottom.autoshowCard(temp)
            self.player_card_left.gene.updatehand_right(current_cards)
            self.player_card_right.gene.updatehand_left(current_cards)
            self.discard_pile_bottom.displayCard(temp)
        # save instance
        c = current_cards if not current_cards == [] else self.player_card_bottom.getHand().getCards()
        data = self.player_card_bottom.save(c, self.player_card_left.gene.gene)
        np.save("database/bottom_data", data)
        self.saveInstance("bottom")
        if self.player_card_bottom.isEmpty():
            self.winner = 0
            self.gameover(self.player_card_bottom, self.player_card_left, self.player_card_right)
            self.cleanDateInstance()
        else:
            self.counter = 40

    # left player play
    def autoPlayLeft(self):
        # print("Left:")
        current_cards=[]
        left = self.player_card_right.getHand().getCards()
        right = self.player_card_bottom.getHand().getCards()
        if not self.previous_cards:
            self.previous_cards_id = -1
        current_id = self.player_card_left.getIdentify()
        pr_id = self.previous_cards_id
        if len(self.previous_cards[0]) > 0:
            # implement AI
            if (self.ai_state == 1 and current_id == 1) or (self.ai_state == 0 and not current_id == 1) or self.ai_state == -1:
                temp = self.player_card_left.autoplayAI(self.previous_cards[0], left, right, current_id, pr_id)

            else:  # stupid computer
                if self.noob:
                    temp = self.player_card_left.autoplay_noob(self.previous_cards[0])
                else:
                    temp = self.player_card_left.autoplay(self.previous_cards[0], current_id, pr_id)
        elif len(self.previous_cards[1]) > 0:
            # implement AI
            if (self.ai_state == 1 and current_id == 1) or (self.ai_state == 0 and not current_id == 1) or self.ai_state == -1:
                temp = self.player_card_left.autoplayAI(self.previous_cards[1], left, right, current_id, pr_id)
            else: # stupid computer
                if self.noob:
                    temp = self.player_card_left.autoplay_noob(self.previous_cards[1])
                else:
                    temp = self.player_card_left.autoplay(self.previous_cards[1], current_id, pr_id)
        else:
            if (self.ai_state == 1 and current_id == 1) or (self.ai_state == 0 and not current_id == 1) or self.ai_state == -1:
                temp = self.player_card_left.autoplayAI(self.previous_cards[0], left, right, current_id, pr_id)
            else:
                if self.noob:
                    temp = self.player_card_left.autoplay_noob(self.previous_cards[0])
                else:
                    temp = self.player_card_left.autoplay(self.previous_cards[0], current_id)
        a = CardType(2, 'dimond', '-')
        if type(temp) == type(a):
            temp = [temp]
        self.previous_cards.pop()
        self.previous_cards.insert(0, temp)
        if temp == [] or len(temp) == 0:
            self.pass_label_left.show()
            Sound.passToNext()
        else:
            self.count_l_b_r[0] += 1
            self.previous_cards_id = self.player_card_left.getIdentify()
            current_cards = self.player_card_left.autoshowCard(temp,1)
            self.player_card_right.gene.updatehand_right(current_cards)
            self.player_card_bottom.gene.updatehand_left(current_cards)
            self.discard_pile_left.displayCard(temp)
            self.num_left -= len(temp)
            self.record_left.setText(str(self.num_left))
        # save instance
        c = current_cards if not current_cards == [] else self.player_card_left.getHand().getCards()
        data = self.player_card_left.save(c, self.player_card_left.gene.gene)
        np.save("database/left_data", data)
        self.saveInstance("left")
        if self.player_card_left.isEmpty():
            self.winner = 0
            self.gameover(self.player_card_left, self.player_card_right, self.player_card_bottom)
            self.cleanDateInstance()
        else:
            if self.ai == 1:
                self.autoPlayBottom()
            else:
                self.show_cards()

   # game is end, donot have to save data instance
    def cleanDateInstance(self):
        data = np.asarray(["None"])
        np.save("database/left_data", data)
        np.save("database/bottom_data", data)
        np.save("database/right_data", data)

    # user player player
    def userPlay(self):
        self.displayUserButtons()
        self.pass_label_bottom.hide()
        self.discard_pile_bottom.hideAll()
        # self.player_card_bottom.play()

    # after play or pass user should not have any action
    def hideUserButton(self):
        self.reselect.hide()
        self.pass_turn.hide()
        self.play.hide()

    # def hide all buttons and labels
    def hideAll(self):
        self.play.hide()
        self.reselect.hide()
        self.pass_turn.hide()
        self.pass_landlord.hide()
        self.bid.hide()
        self.pass_label_left.hide()
        self.pass_label_right.hide()
        self.pass_label_bottom.hide()
        self.landlord_label_right.hide()
        self.landlord_label_left.hide()
        self.landlord_label_bottom.hide()
        self.winner_framer_label.hide()
        self.winner_landlord_label.hide()
        self.winner_label.hide()

    # game is end
    def gameover(self, player, player2, player3, p=1):
        self.counter = 9999
        self.hideUserButton()
        self.winner_label.show()
        self.upadateDNApoint(player, player2, player3)

        # --------- to check the gene is whether necessary to mutate
        # player.gene.mutate()

        # --------- to recode the round that have played
        # f = open("count.txt", "a")
        # text = "\n" + str(self.count_l_b_r[0]) + "  " + str(self.count_l_b_r[1]) + "  " + str(self.count_l_b_r[2])
        # f.write(text)
        # f.close()
        if player.getIdentify() == 1:
            # self.count_win += 1
            if p == 0:
                Sound.winMusic()
                self.winner_landlord_label.show()
            else:
                Sound.loseMusic()
                self.winner_landlord_label.show()
        else:
            if self.player_card_bottom.getIdentify() == 1:
                Sound.loseMusic()
            else:
                Sound.winMusic()
            self.winner_framer_label.show()
        # self.loop += 1
        # print("i ",self.loop)
        # print(self.loop,"landlord win:  ", self.count_win,"/10")
        # if self.loop < 10:
        #     self.new_game()

    # when gameover update dna points
    def upadateDNApoint(self, player, player2, player3):
        if player.getIdentify() == 1:
            player.gene.calculateDNApoint(player.hand.initial_point, 20)
            player2.gene.calculateDNApoint(player.hand.initial_point, 0)
            player3.gene.calculateDNApoint(player.hand.initial_point, 0)
        else:
            player.gene.calculateDNApoint(player.hand.initial_point, 20)
            if player2.getIdentify() == 1:
                player2.gene.calculateDNApoint(player.hand.initial_point, 0)
                player3.gene.calculateDNApoint(player.hand.initial_point, 20)
            else:
                player2.gene.calculateDNApoint(player.hand.initial_point, 20)
                player3.gene.calculateDNApoint(player.hand.initial_point, 0)

    # overwrite time event
    def timerEvent(self, event):
        """handles timer event"""
        self.counter += self.timer.timerId()
        if event.timerId() == self.timer.timerId():
            if self.counter == 50:
                self.autoPlayRight()
            elif self.counter == 100:
                self.autoPlayLeft()
