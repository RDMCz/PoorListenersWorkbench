import PySide6.QtCore as qtc
import PySide6.QtWidgets as qtw

import service.bandcamp as bc

OPTION_URL_MUSIC_GRID = "Bandcamp music grid URL:"
OPTION_URL_ALBUM = "Bandcamp album URL:"


class TabBandcamp(qtw.QWidget):
    def __init__(self):
        super().__init__()

        # .: Group 1 :: Bandcamp artist's music grid URL :.
        group1 = qtw.QGroupBox("Step 1: Provide a Bandcamp artist's music grid URL or just an album URL")
        group1layout = qtw.QHBoxLayout()
        # Select URL type
        self.select_url_type = qtw.QComboBox()
        self.select_url_type.addItems([OPTION_URL_MUSIC_GRID, OPTION_URL_ALBUM])
        group1layout.addWidget(self.select_url_type)
        # URL input
        self.input_link = qtw.QLineEdit()
        group1layout.addWidget(self.input_link)
        # Process URL button
        g1_button = qtw.QPushButton("Fetch album(s)")
        g1_button.clicked.connect(self.button_g1_clicked)
        group1layout.addWidget(g1_button)
        #
        group1.setLayout(group1layout)
        # .::.

        # .: Group 2 :: Album chooser :.
        group2 = qtw.QGroupBox("Step 2: Tick the checkboxes of albums you want to get downloaded")
        group2layout = qtw.QVBoxLayout()

        self.album_table = qtw.QTableWidget()
        group2layout.addWidget(self.album_table)

        g2_button = qtw.QPushButton("(Un)check all")
        g2_button.clicked.connect(self.button_g2_clicked)
        g2_button.setMaximumWidth(80)
        group2layout.addWidget(g2_button)

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

    #
    def button_g1_clicked(self):
        url_type = self.select_url_type.currentText()

        if url_type == OPTION_URL_MUSIC_GRID:
            result = bc.get_all_links_from_music_grid(self.input_link.text())
        elif url_type == OPTION_URL_ALBUM:
            result = [self.input_link.text()]
        else:
            result = []

        self.album_table.reset()
        self.album_table.setRowCount(len(result))
        horizontal_header_labels = ["Download?", "Bandcamp link"]
        self.album_table.setColumnCount(len(horizontal_header_labels))
        self.album_table.setHorizontalHeaderLabels(horizontal_header_labels)
        self.album_table.horizontalHeader().setSectionResizeMode(qtw.QHeaderView.ResizeMode.ResizeToContents)
        self.album_table.verticalHeader().hide()

        for row_number, album_link in enumerate(result):
            # Checkbox in first column
            # (All this is for making the checkbox centered, otherwise could be one-liner)
            checkbox = qtw.QCheckBox()
            checkbox_widget = qtw.QWidget()
            checkbox_layout = qtw.QHBoxLayout(checkbox_widget)
            checkbox_layout.addWidget(checkbox)
            checkbox_layout.setAlignment(qtc.Qt.AlignmentFlag.AlignCenter)
            checkbox_layout.setContentsMargins(0, 0, 0, 0)
            checkbox_widget.checkbox_reference = checkbox  # Will be used to check the value later
            self.album_table.setCellWidget(row_number, 0, checkbox_widget)

            # Album link in second column
            album_link_item = qtw.QTableWidgetItem(album_link)
            album_link_item.setFlags(qtc.Qt.ItemFlag.NoItemFlags)
            self.album_table.setItem(row_number, 1, album_link_item)

    #
    def button_g2_clicked(self):
        is_all_checked = True
        for row_number in range(self.album_table.rowCount()):
            checkbox: qtw.QCheckBox = self.__get_checkbox_from_table(row_number)
            if not checkbox.isChecked():
                is_all_checked = False
                break

        for row_number in range(self.album_table.rowCount()):
            checkbox: qtw.QCheckBox = self.__get_checkbox_from_table(row_number)
            checkbox.setChecked(not is_all_checked)

    #
    def button_g3_clicked(self):
        album_links_to_download = []  # Append album link here if checkbox on the same row is checked
        for row_number in range(self.album_table.rowCount()):
            checkbox: qtw.QCheckBox = self.__get_checkbox_from_table(row_number)
            album_link = self.album_table.item(row_number, 1).text()
            if checkbox.isChecked():
                album_links_to_download.append(album_link)

        bc.download_song_list(album_links_to_download)
        print("Done")

    #
    def __get_checkbox_from_table(self, row_number: int) -> qtw.QCheckBox:
        return self.album_table.cellWidget(row_number, 0).checkbox_reference
