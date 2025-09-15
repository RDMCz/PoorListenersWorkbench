import PySide6.QtWidgets as qtw


class TabAbout(qtw.QWidget):
    def __init__(self):
        super().__init__()

        label = qtw.QLabel("<a href=https://github.com/RDMCz/PoorListenersWorkbench>https://github.com/RDMCz/PoorListenersWorkbench</a>")
        label.setOpenExternalLinks(True)

        stack_panel = qtw.QVBoxLayout()
        stack_panel.addWidget(label)

        self.setLayout(stack_panel)
