#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import subprocess
from PyQt5.QtWidgets import (QMainWindow, QDesktopWidget, QGridLayout, QWidget,
                             QPushButton, QLabel, QApplication)
from PyQt5.QtGui import QPixmap

import udp_socket


class Interface(QWidget):

    def __init__(self):
        super().__init__()

        self.size_edit = QLabel("None     ")
        self.size_grade_edit = QLabel("None     ")
        self.roundness_edit = QLabel("None     ")
        self.roundness_grade_edit = QLabel("None     ")
        self.color_edit = QLabel("None     ")
        self.color_grade_edit = QLabel("None     ")
        self.healthy_rot_edit = QLabel("None     ")

        self.img = QLabel(self)

        self.init_ui()

        self.udp_soc = udp_socket.udp_init(self.size_edit, self.size_grade_edit, self.roundness_edit,
                                           self.roundness_grade_edit, self.color_edit, self.color_grade_edit,
                                           self.healthy_rot_edit, self.img)

    def init_ui(self):

        self.center()
        self.setWindowTitle("Apple Sorting System")

        pixmap = QPixmap("/home/jon/Pictures/img_init.jpg")
        self.img.setPixmap(pixmap)

        start = QPushButton("Get information", self)
        start.minimumSize()
        start.clicked.connect(self.start_clicked)

        disconnect = QPushButton("Disconnect", self)
        disconnect.clicked.connect(self.dis_clicked)

        size = QLabel('size: ')
        size_grade = QLabel('size_grade: ')

        roundness = QLabel('roundness: ')
        roundness_grade = QLabel('roundness_grade: ')

        color = QLabel('color: ')
        color_grade = QLabel('color_grade: ')

        healthy_rot = QLabel('healthy_rot')

        grid = QGridLayout()
        grid.setSpacing(20)

        grid.addWidget(self.img, 0, 0, 20, 5)
        grid.addWidget(start, 0, 6, 1, 2)
        grid.addWidget(disconnect, 1, 6, 1, 2)

        grid.addWidget(size, 2, 6)
        grid.addWidget(self.size_edit, 2, 7)
        grid.addWidget(size_grade, 3, 6)
        grid.addWidget(self.size_grade_edit, 3, 7)

        grid.addWidget(roundness, 4, 6)
        grid.addWidget(self.roundness_edit, 4, 7)
        grid.addWidget(roundness_grade, 5, 6)
        grid.addWidget(self.roundness_grade_edit, 5, 7)

        grid.addWidget(color, 6, 6)
        grid.addWidget(self.color_edit, 6, 7)
        grid.addWidget(color_grade, 7, 6)
        grid.addWidget(self.color_grade_edit, 7, 7)

        grid.addWidget(healthy_rot, 8, 6)
        grid.addWidget(self.healthy_rot_edit, 8, 7)

        self.setLayout(grid)

        self.show()

    def center(self):

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def start_clicked(self):

        udp_socket.udp_send(self.udp_soc, "get")

    def dis_clicked(self):

        udp_socket.udp_send(self.udp_soc, "disconnect")


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Interface()
    sys.exit(app.exec_())
