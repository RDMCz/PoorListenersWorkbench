import PySide6.QtCore as qtc
import PySide6.QtWidgets as qtw

import service.youtube as yt


class TabYTPLDL(qtw.QWidget):
    def __init__(self):
        super().__init__()

        stack_panel = qtw.QVBoxLayout()

        # .: Group 1 :: YouTube playlist URL :.
        group1 = qtw.QGroupBox("Step 1: Provide a YouTube playlist URL")
        group1layout = qtw.QHBoxLayout()
        # URL input
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
        group3layout = qtw.QHBoxLayout()
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
        result = yt.get_song_list_from_youtube_playlist_url(self.g1_input.text())

        self.g2_table.reset()
        self.g2_table.setRowCount(len(result))
        horizontal_header_labels = ["YT code", "Track number", "Title", "Artist", "Album artist", "Year", "Album"]
        self.g2_table.setColumnCount(len(horizontal_header_labels))
        self.g2_table.setHorizontalHeaderLabels(horizontal_header_labels)
        self.g2_table.horizontalHeader().setSectionResizeMode(qtw.QHeaderView.ResizeMode.ResizeToContents)
        self.g2_table.verticalHeader().hide()

        row_number = 0
        for song in result:
            item_id = qtw.QTableWidgetItem(str(song["id"]))
            item_id.setFlags(qtc.Qt.ItemFlag.NoItemFlags)
            self.g2_table.setItem(row_number, 0, item_id)

            self.g2_table.setItem(row_number, 1, qtw.QTableWidgetItem(str(song["number"])))
            self.g2_table.setItem(row_number, 2, qtw.QTableWidgetItem(str(song["title"])))
            self.g2_table.setItem(row_number, 3, qtw.QTableWidgetItem(str(song["artist"])))
            self.g2_table.setItem(row_number, 4, qtw.QTableWidgetItem(str(song["albumartist"])))
            self.g2_table.setItem(row_number, 5, qtw.QTableWidgetItem(str(song["year"])))
            self.g2_table.setItem(row_number, 6, qtw.QTableWidgetItem(str(song["album"])))

            row_number += 1

    def button_g2_clicked(self):
        new_artist = self.g2_global_artist_input.text()
        new_album_artist = self.g2_global_album_artist_input.text()
        new_year = self.g2_global_year_input.text()
        new_album = self.g2_global_album_input.text()
        for row_number in range(self.g2_table.rowCount()):
            self.g2_table.setItem(row_number, 3, qtw.QTableWidgetItem(new_artist))
            self.g2_table.setItem(row_number, 4, qtw.QTableWidgetItem(new_album_artist))
            self.g2_table.setItem(row_number, 5, qtw.QTableWidgetItem(new_year))
            self.g2_table.setItem(row_number, 6, qtw.QTableWidgetItem(new_album))

    def button_g3_clicked(self):
        final_songs = []
        for row_number in range(self.g2_table.rowCount()):
            song = {
                "id": self.g2_table.item(row_number, 0).text(),
                "number": self.g2_table.item(row_number, 1).text(),
                "title": self.g2_table.item(row_number, 2).text(),
                "artist": self.g2_table.item(row_number, 3).text(),
                "albumartist": self.g2_table.item(row_number, 4).text(),
                "year": self.g2_table.item(row_number, 5).text(),
                "album": self.g2_table.item(row_number, 6).text(),
            }
            final_songs.append(song)
        yt.download_song_list(final_songs)
        print("Done")
