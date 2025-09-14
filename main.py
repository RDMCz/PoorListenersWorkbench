import PyQt6.QtWidgets as qtw

from view.tab_about import TabAbout
from view.tab_bandcamp16 import TabBandcamp16


class MainWindow(qtw.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Poor Listeners' Workbench")
        self.setMinimumSize(1280, 720)

        tab_bandcamp16 = TabBandcamp16()
        tab_about = TabAbout()

        tabs = qtw.QTabWidget()
        tabs.addTab(tab_bandcamp16, "Bandcamp >16")
        tabs.addTab(tab_about, "About...")

        main_layout = qtw.QVBoxLayout()
        main_layout.addWidget(tabs)
        container = qtw.QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)


app = qtw.QApplication([])

window = MainWindow()
window.show()

app.exec()
