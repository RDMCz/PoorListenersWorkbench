import json

import PySide6.QtWidgets as qtw

import service.youtube as yt


class TabYTPLDL(qtw.QWidget):
    def __init__(self):
        super().__init__()

        self.label = qtw.QLabel("vítejte")

        button = qtw.QPushButton("Do sth")
        button.clicked.connect(self.button_clicked)

        grid = qtw.QGridLayout()
        grid.addWidget(self.label, 0, 0)
        grid.addWidget(button, 1, 0)

        self.setLayout(grid)

    def button_clicked(self):
        result = yt.test()
        self.label.setText(json.dumps(result))
