import PyQt6.QtGui as qtg
import PyQt6.QtWidgets as qtw

import service.bandcamp as bc


class TabBandcamp16(qtw.QWidget):
    def __init__(self):
        super().__init__()

        self.input_link = qtw.QLineEdit()
        self.input_link.setPlaceholderText("Bandcamp music grid URL")

        self.input_result1 = qtw.QTextEdit()
        self.input_result1.setReadOnly(True)
        # self.input_result1.setMinimumHeight(self.input_result1.fontMetrics().lineSpacing() * 16)
        self.input_result1.setWordWrapMode(qtg.QTextOption.WrapMode.NoWrap)

        self.input_result2 = qtw.QTextEdit()
        self.input_result2.setReadOnly(True)
        self.input_result2.setWordWrapMode(qtg.QTextOption.WrapMode.NoWrap)

        self.button_run = qtw.QPushButton("Run")
        self.button_run.clicked.connect(self.button_run_clicked)

        stack_panel = qtw.QVBoxLayout()
        stack_panel.addWidget(self.input_link)
        stack_panel.addWidget(self.input_result1)
        stack_panel.addWidget(self.input_result2)
        stack_panel.addWidget(self.button_run)

        self.setLayout(stack_panel)

    def button_run_clicked(self):
        results = bc.get_all_links_from_music_grid(self.input_link.text())
        text1 = "\n".join(results[0])
        text2 = "\n".join(results[1])
        self.input_result1.setText(text1)
        self.input_result2.setText(text2)
