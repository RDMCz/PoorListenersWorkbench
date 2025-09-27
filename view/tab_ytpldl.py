from typing import Dict, List

import PySide6.QtCore as qtc
import PySide6.QtGui as qtg
import PySide6.QtWidgets as qtw

import service.youtube as yt
from constant.audiotag_strenum import AudioTag

AUDIOTAG_TO_COLNUM = {
    # Column 0 reserved for index ("#")
    AudioTag.ID: 1,
    AudioTag.NUMBER: 2,
    AudioTag.TITLE: 3,
    AudioTag.ARTIST: 4,
    AudioTag.ALBUMARTIST: 5,
    AudioTag.YEAR: 6,
    AudioTag.ALBUM: 7,
}


class TabYTPLDL(qtw.QWidget):
    def __init__(self):
        super().__init__()

        stack_panel = qtw.QVBoxLayout()

        # .: Group 1 :: YouTube playlist URL :.
        group1 = qtw.QGroupBox("Step 1: Provide a YouTube playlist URL")
        group1layout = qtw.QHBoxLayout()
        # YouTube playlist URL input
        self.g1_input = qtw.QLineEdit()
        self.g1_input.setPlaceholderText("YouTube playlist URL")
        group1layout.addWidget(self.g1_input)
        # Process URL button – fetch songs
        g1_button = qtw.QPushButton("Fetch songs from playlist")
        g1_button.clicked.connect(self.button_g1_clicked)
        group1layout.addWidget(g1_button)
        group1.setLayout(group1layout)
        # .::.

        # .: Group 2 :: Metadata edit :.
        group2 = qtw.QGroupBox("Step 2: Edit metadata (table cells are editable)")
        group2layout = qtw.QGridLayout()
        # Table of all fetched songs
        self.g2_table = qtw.QTableWidget()
        group2layout.addWidget(self.g2_table, 0, 0, 1, 5)
        # Global metadata set
        # - artist
        self.g2_global_artist_input = qtw.QLineEdit()
        self.g2_global_artist_input.setPlaceholderText("Artist")
        group2layout.addWidget(self.g2_global_artist_input, 1, 0)
        # - album artist
        self.g2_global_album_artist_input = qtw.QLineEdit()
        self.g2_global_album_artist_input.setPlaceholderText("Album artist")
        group2layout.addWidget(self.g2_global_album_artist_input, 1, 1)
        # - year
        self.g2_global_year_input = qtw.QLineEdit()
        self.g2_global_year_input.setPlaceholderText("Year")
        group2layout.addWidget(self.g2_global_year_input, 1, 2)
        # - album
        self.g2_global_album_input = qtw.QLineEdit()
        self.g2_global_album_input.setPlaceholderText("Album")
        group2layout.addWidget(self.g2_global_album_input, 1, 3)
        # - button to apply
        g2_button = qtw.QPushButton("Set to all")
        g2_button.clicked.connect(self.button_g2_clicked)
        group2layout.addWidget(g2_button, 1, 4)
        group2.setLayout(group2layout)
        # .::.

        # .: Group 3 :: Download and convert :.
        group3 = qtw.QGroupBox("Step 3: Download and convert")
        group3layout = qtw.QVBoxLayout()
        # - hbox where you can set start index
        g3_start_innerlayout = qtw.QHBoxLayout()
        g3_start_label = qtw.QLabel("Start from index: ")
        g3_start_innerlayout.addWidget(g3_start_label)
        self.g3_start_input = qtw.QLineEdit()
        validator = qtg.QIntValidator(0, 999)
        self.g3_start_input.setValidator(validator)
        self.g3_start_input.setFixedWidth(30)
        g3_start_innerlayout.addWidget(self.g3_start_input)
        g3_start_innerlayout.addStretch()  # Adds a "stretch space" to the end so label and input are right next to each other (no big gap between them)
        group3layout.addLayout(g3_start_innerlayout)
        # - button to download
        g3_button = qtw.QPushButton("Download and convert")
        g3_button.clicked.connect(self.button_g3_clicked)
        group3layout.addWidget(g3_button)
        group3.setLayout(group3layout)
        # .::.

        stack_panel.addWidget(group1)
        stack_panel.addWidget(group2)
        stack_panel.addWidget(group3)

        self.setLayout(stack_panel)

    def button_g1_clicked(self):
        """Fetch songs from YouTube playlist URL and put data into the table."""
        result: List[Dict[AudioTag, str]] = yt.get_song_list_from_youtube_playlist_url(self.g1_input.text())

        self.g2_table.reset()
        self.g2_table.setRowCount(len(result))
        horizontal_header_labels = ["#", "YT code", "Track number", "Title", "Artist", "Album artist", "Year", "Album"]
        self.g2_table.setColumnCount(len(horizontal_header_labels))
        self.g2_table.setHorizontalHeaderLabels(horizontal_header_labels)
        self.g2_table.horizontalHeader().setSectionResizeMode(qtw.QHeaderView.ResizeMode.ResizeToContents)
        self.g2_table.verticalHeader().hide()
        self.g3_start_input.setText("0")

        for row_number, song in enumerate(result):
            # ("#")
            item_id = qtw.QTableWidgetItem(str(row_number))
            item_id.setFlags(qtc.Qt.ItemFlag.NoItemFlags)
            self.g2_table.setItem(row_number, 0, item_id)

            # ("YT code")
            item_id = qtw.QTableWidgetItem(str(song[AudioTag.ID]))
            item_id.setFlags(qtc.Qt.ItemFlag.NoItemFlags)
            self.g2_table.setItem(row_number, AUDIOTAG_TO_COLNUM[AudioTag.ID], item_id)

            # ("Track number", "Title", "Artist", "Album artist", "Year", "Album")
            for audio_tag in AudioTag:
                if audio_tag != AudioTag.ID:
                    self.g2_table.setItem(row_number, AUDIOTAG_TO_COLNUM[audio_tag],
                                          qtw.QTableWidgetItem(str(song[audio_tag])))
                    # e.g.:
                    # self.g2_table.setItem(row_number, AUDIOTAG_TO_COLNUM[AudioTag.NUMBER],
                    #                      qtw.QTableWidgetItem(str(song[AudioTag.NUMBER])))
                    # foreach tag

    def button_g2_clicked(self):
        """Apply certain tag edits to all songs (rows)."""
        new_artist = self.g2_global_artist_input.text()
        new_album_artist = self.g2_global_album_artist_input.text()
        new_year = self.g2_global_year_input.text()
        new_album = self.g2_global_album_input.text()
        for row_number in range(self.g2_table.rowCount()):
            self.g2_table.setItem(row_number, AUDIOTAG_TO_COLNUM[AudioTag.ARTIST], qtw.QTableWidgetItem(new_artist))

            self.g2_table.setItem(row_number, AUDIOTAG_TO_COLNUM[AudioTag.ALBUMARTIST],
                                  qtw.QTableWidgetItem(new_album_artist))

            self.g2_table.setItem(row_number, AUDIOTAG_TO_COLNUM[AudioTag.YEAR], qtw.QTableWidgetItem(new_year))

            self.g2_table.setItem(row_number, AUDIOTAG_TO_COLNUM[AudioTag.ALBUM], qtw.QTableWidgetItem(new_album))

    def button_g3_clicked(self):
        """Download songs and them according to the table values."""
        final_songs: List[Dict[AudioTag, str]] = []
        for row_number in range(self.g2_table.rowCount()):
            song = {}
            for audio_tag in AudioTag:
                song[audio_tag] = self.g2_table.item(row_number, AUDIOTAG_TO_COLNUM[audio_tag]).text()
                # e.g.:
                # AudioTag.ID: self.g2_table.item(row_number, AUDIOTAG_TO_COLNUM[AudioTag.ID]).text()
                # foreach tag

            final_songs.append(song)

        start_index = 0
        if self.g3_start_input.text().isnumeric():
            start_index = int(self.g3_start_input.text())

        yt.download_song_list(final_songs, start_index)
        print("Done")
