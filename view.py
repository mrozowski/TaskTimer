from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QRectF, Qt
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QAbstractButton


class PicButton(QAbstractButton):
    """Custom buttons"""
    def __init__(self, text, parent=None):
        super().__init__(parent)
        self.text = text
        self.active = False

        """default button graphic"""
        self.pixmap = QtGui.QPixmap("Graphic/button.png")
        self.pixmap_hover = QtGui.QPixmap("Graphic/button_hover.png")
        self.pixmap_pressed = QtGui.QPixmap("Graphic/button_pressed.png")
        self.pixmap_cancel = QtGui.QPixmap("Graphic/button_cancel.png")
        self.pixmap_cancel_hover = QtGui.QPixmap("Graphic/button_cancel_hover.png")
        self.pixmap_cancel_pressed = QtGui.QPixmap("Graphic/button_cancel_pressed.png")

        self.pressed.connect(self.update)
        self.released.connect(self.update)
        self.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

    def paintEvent(self, event):
        if self.active:
            """show cancel button"""
            pix = self.pixmap_cancel_hover if self.underMouse() else self.pixmap_cancel
            if self.isDown():
                pix = self.pixmap_cancel_pressed
        else:
            """show start button"""
            pix = self.pixmap_hover if self.underMouse() else self.pixmap
            if self.isDown():
                pix = self.pixmap_pressed

        painter = QPainter(self)
        painter.drawPixmap(event.rect(), pix)  # draw button
        painter.drawText(QRectF(0.0,0.0,self.width(), self.height()), Qt.AlignCenter, self.text)  # draw text in the center of button

    def mouseReleaseEvent(self, e: QtGui.QMouseEvent) -> None:
        super().mouseReleaseEvent(e)
        if self.active is False:
            self.active = True
        else:
            self.active = False

class Dial(QtWidgets.QDial):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.pixmap = QtGui.QPixmap("Graphic/dial.png")
        self.setSliderPosition(0)
        self.setObjectName("dial")
        self.setStyleSheet("QDial{background-color: #4FEC42;}")
        self.setNotchesVisible(True)
        self.setRange(0, 480)
        self.setWrapping(True)
        self.transform = QtGui.QTransform()
        self.transform.rotate(0)
        self.oldValue = 0

class View(object):
    def __init__(self):
        self.presenter = None
        self.dial = None
        self.timer_button = None
        self.day_label = None
        self.time_label = None
        self.hours = None
        self.minutes = None
        self.seconds = None
        self.dots = None

    def setup(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(500, 300)

        self.main = QtWidgets.QWidget(MainWindow)
        self.main.setStyleSheet("#main{background: #121212;} QLabel{color: white; font-size: 18px; }")
        self.main.setObjectName("main")

        self.dial = Dial(self.main)
        self.dial.setGeometry(QtCore.QRect(295, 105, 166, 166))

        self.timer_button = PicButton("", self.main)
        self.timer_button.setGeometry(QtCore.QRect(311, 15, 130, 61))
        self.timer_button.setObjectName("pushButton")
        self.timer_button.clicked.connect(lambda: self.presenter.timer_button_clicked(self.timer_button.active))

        self.day_label = QtWidgets.QLabel(self.main)
        self.day_label.setGeometry(QtCore.QRect(20, 30, 221, 21))
        self.day_label.setStyleSheet("QLabel{color: #429AEC; font-size: 20px;}")
        self.day_label.setAlignment(QtCore.Qt.AlignCenter)
        self.day_label.setObjectName("day_label")

        self.time_label = QtWidgets.QLabel(self.main)
        self.time_label.setGeometry(QtCore.QRect(20, 80, 221, 21))
        self.time_label.setStyleSheet("QLabel{color: #429AEC; font-size: 20px;}")
        self.time_label.setAlignment(QtCore.Qt.AlignCenter)
        self.time_label.setObjectName("time_label_3")

        self.hours = QtWidgets.QLabel(self.main)
        self.hours.setGeometry(QtCore.QRect(20, 150, 90, 90))
        self.hours.setAlignment(QtCore.Qt.AlignCenter)
        self.hours.setObjectName("label_3")

        self.minutes = QtWidgets.QLabel(self.main)
        self.minutes.setGeometry(QtCore.QRect(160, 150, 90, 90))
        self.minutes.setAlignment(QtCore.Qt.AlignCenter)
        self.minutes.setObjectName("label_4")

        self.seconds = QtWidgets.QLabel(self.main)
        self.seconds.setGeometry(QtCore.QRect(333, 143, 90, 90))
        self.seconds.setAlignment(QtCore.Qt.AlignCenter)
        self.seconds.setObjectName("label_5")
        self.seconds.setText("59")
        self.seconds.hide()
        self.seconds.setStyleSheet("QLabel{color: #4FEC42; font-size: 50px;}")

        self.dial.valueChanged.connect(self.presenter.dial_moved)

        """Graphic elements"""

        self.dots = QtWidgets.QLabel(self.main)
        self.dots.setGeometry(QtCore.QRect(125, 170, 21, 51))
        self.dots.setText("")
        self.dots.setPixmap(QtGui.QPixmap("Graphic/green_dots.png"))
        self.dots.setObjectName("green_dots")


        self.square_hour = QtWidgets.QLabel(self.main)
        self.square_hour.setGeometry(QtCore.QRect(20, 150, 90, 90))
        self.square_hour.setText("")
        self.square_hour.setPixmap(QtGui.QPixmap("Graphic/square.png"))
        self.square_hour.setObjectName("square_hour")

        self.square_min = QtWidgets.QLabel(self.main)
        self.square_min.setGeometry(QtCore.QRect(160, 150, 90, 90))
        self.square_min.setText("")
        self.square_min.setPixmap(QtGui.QPixmap("Graphic/square.png"))
        self.square_min.setObjectName("square_min")

        self.day_baground = QtWidgets.QLabel(self.main)
        self.day_baground.setGeometry(QtCore.QRect(20, 20, 230, 40))
        self.day_baground.setText("")
        self.day_baground.setPixmap(QtGui.QPixmap("Graphic/time_container.png"))
        self.day_baground.setObjectName("day_baground")

        self.time_bacground = QtWidgets.QLabel(self.main)
        self.time_bacground.setGeometry(QtCore.QRect(20, 70, 230, 40))
        self.time_bacground.setText("")
        self.time_bacground.setPixmap(QtGui.QPixmap("Graphic/time_container.png"))
        self.time_bacground.setObjectName("time_bacground")

        """Labels"""

        self.min_label = QtWidgets.QLabel(self.main)
        self.min_label.setGeometry(QtCore.QRect(160, 250, 81, 20))
        self.min_label.setAlignment(QtCore.Qt.AlignCenter)
        self.min_label.setObjectName("time_label")

        self.h_label = QtWidgets.QLabel(self.main)
        self.h_label.setGeometry(QtCore.QRect(20, 250, 81, 20))
        self.h_label.setAlignment(QtCore.Qt.AlignCenter)
        self.h_label.setObjectName("time_label_2")

        self.day_label.raise_()
        self.time_label.raise_()
        self.hours.raise_()
        self.minutes.raise_()
        self.dial.raise_()
        MainWindow.setCentralWidget(self.main)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.min_label.setText(_translate("MainWindow", "Minutes"))
        self.h_label.setText(_translate("MainWindow", "Hours"))
        self.timer_button.setText(_translate("MainWindow", "PushButton"))
        self.day_label.setText(_translate("MainWindow", "Week day"))
        self.time_label.setText(_translate("MainWindow", "Time"))
        self.hours.setText(_translate("MainWindow", "0"))
        self.minutes.setText(_translate("MainWindow", "0"))

    def set_presenter(self, presenter):
        self.presenter = presenter

