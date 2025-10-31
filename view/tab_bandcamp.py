import PySide6.QtCore as qtc
import PySide6.QtWidgets as qtw

import service.bandcamp as bc


class TabBandcamp(qtw.QWidget):
    def __init__(self):
        super().__init__()

        # .: Group 1 :: Bandcamp artist's music grid URL :.
        group1 = qtw.QGroupBox("Step 1: Provide a Bandcamp artist's music grid URL")
        group1layout = qtw.QHBoxLayout()
        # Bandcamp artist's music grid URL input
        self.input_link = qtw.QLineEdit()
        self.input_link.setPlaceholderText("Bandcamp music grid URL")
        group1layout.addWidget(self.input_link)
        # Process URL button – fetch album links
        g1_button = qtw.QPushButton("Fetch albums from music grid")
        g1_button.clicked.connect(self.button_g1_clicked)
        group1layout.addWidget(g1_button)
        group1.setLayout(group1layout)
        # .::.

        # .: Group 2 :: Album chooser :.
        group2 = qtw.QGroupBox("Step 2: Tick the chexkboxes of albums you want to get downloaded")
        group2layout = qtw.QVBoxLayout()

        self.album_table = qtw.QTableWidget()
        group2layout.addWidget(self.album_table)

        group2.setLayout(group2layout)
        # .::.

        # .: Group 3 :: Download button :.
        group3 = qtw.QGroupBox("Step 3: Start downloading")
        group3layout = qtw.QVBoxLayout()

        g3_button = qtw.QPushButton("Download")
        g3_button.clicked.connect(self.button_g3_clicked)
        group3layout.addWidget(g3_button)

        group3.setLayout(group3layout)
        # .::.

        stack_panel = qtw.QVBoxLayout()
        stack_panel.addWidget(group1)
        stack_panel.addWidget(group2)
        stack_panel.addWidget(group3)

        self.setLayout(stack_panel)

    def button_g1_clicked(self):
        result = bc.get_all_links_from_music_grid(self.input_link.text())

        self.album_table.reset()
        self.album_table.setRowCount(len(result))
        horizontal_header_labels = ["Download?", "Bandcamp link"]
        self.album_table.setColumnCount(len(horizontal_header_labels))
        self.album_table.setHorizontalHeaderLabels(horizontal_header_labels)
        self.album_table.horizontalHeader().setSectionResizeMode(qtw.QHeaderView.ResizeMode.ResizeToContents)
        self.album_table.verticalHeader().hide()

        for row_number, album_link in enumerate(result):
            # Check box in first column
            # (to center it we would have to make QWidget with some centered layout with the checkbox)
            self.album_table.setCellWidget(row_number, 0, qtw.QCheckBox())

            # Album link in second column
            album_link_item = qtw.QTableWidgetItem(album_link)
            album_link_item.setFlags(qtc.Qt.ItemFlag.NoItemFlags)
            self.album_table.setItem(row_number, 1, album_link_item)

    def button_g3_clicked(self):
        album_links_to_download = []  # Append album link here if checkbox on the same row is checked
        for row_number in range(self.album_table.rowCount()):
            checkbox: qtw.QCheckBox = self.album_table.cellWidget(row_number, 0)
            album_link = self.album_table.item(row_number, 1).text()
            if checkbox.isChecked():
                album_links_to_download.append(album_link)

        bc.download_song_list(album_links_to_download)
