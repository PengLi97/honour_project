import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from GameUI import *
from Sound import *


class StartUI(QWidget):

    def __init__(self):
        super().__init__()
        self.open = 1
        self.label_guide = QLabel(self)
        self.initUI()  # initialize

    def initUI(self):
        self.resize(800, 600)  # windows size
        self.setFixedSize(800, 600)
        self.center()  # window
        self.setWindowTitle('Fighting the Landlord')  # window title
        self.setWindowIcon(QIcon('icon.jpg'))  # window icon
        oImage = QImage("background.jpg")
        sImage = oImage.scaled(QSize(800, 600))  # resize Image to widgets size
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(sImage))
        self.setPalette(palette)
        self.initStartGame()

    # initialize the start page
    def initStartGame(self):

        # button
        style0 = ("QPushButton{color:#169BD5}"
                  "QPushButton:hover{color:blue}"
                  "QPushButton{background-color:orange}"
                  "QPushButton:hover{background-color:yellow}"
                  "QPushButton{border-radius:10px}"
                  "QPushButton{width:60}"
                  "QPushButton{height:30}"
                  "QPushButton{font-size:18px}")

        start_button = QPushButton("start", self)
        start_button.setStyleSheet(style0)
        start_button.move(370, 550)
        start_button.clicked.connect(self.toStart)
        close_button = QPushButton(" close ", self)
        close_button.setStyleSheet(style0)
        close_button.move(570, 550)
        close_button.clicked.connect(self.toClose)

        self.label_guide.setFixedSize(700, 393)
        pixmap = QPixmap('image/guide1.png')
        self.label_guide.setPixmap(pixmap)
        self.label_guide.setStyleSheet("QLabel{border-radius:10px}")
        self.label_guide.move(20, 60)
        self.label_guide.hide()

        guide_button = QPushButton(" guide ", self)
        guide_button.setStyleSheet(style0)
        guide_button.move(170, 550)
        guide_button.clicked.connect(self.guide)

        Sound.background(1)

    # close game
    def toStart(self):
        self.close()
        gameUI.show()
        Sound.background(0)

    # close game
    def toClose(self):
        self.close()

    # guide
    def guide(self):
        if self.open == 1:
            self.label_guide.show()
            self.open = 0
        else:
            self.label_guide.hide()
            self.open = 1

    # move window to center
    def center(self):
        fg = self.frameGeometry()
        ct = QDesktopWidget().availableGeometry().center()
        fg.moveCenter(ct)
        self.move(fg.topLeft())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    startUI = StartUI()
    startUI.show()
    gameUI = GameUI()
    sys.exit(app.exec_())
