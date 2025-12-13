import PySide6.QtWidgets as qtw

from view.tab_about import TabAbout
from view.tab_bandcamp import TabBandcamp
from view.tab_ytpldl import TabYTPLDL

_VERSION = "0.2.1"


class MainWindow(qtw.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle(f"Poor Listeners' Workbench [v{_VERSION}]")
        self.setMinimumSize(1280, 720)

        tab_bandcamp16 = TabBandcamp()
        tab_ytpldl = TabYTPLDL()
        tab_about = TabAbout()

        tabs = qtw.QTabWidget()
        tabs.addTab(tab_bandcamp16, "Bandcamp DL")
        tabs.addTab(tab_ytpldl, "YouTube playlist DL")
        tabs.addTab(tab_about, "About...")

        # TabWidget could be directly set as central widget, but putting it in a
        # VBoxLayout first creates adequate looking border around the TabWidget
        main_layout = qtw.QVBoxLayout()
        main_layout.addWidget(tabs)
        container = qtw.QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)


app = qtw.QApplication([])

window = MainWindow()
window.show()

app.exec()
