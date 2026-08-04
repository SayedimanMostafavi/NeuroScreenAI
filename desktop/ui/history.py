from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QListWidget,
    QPushButton,
)
from PySide6.QtGui import QDesktopServices
from PySide6.QtCore import QUrl


class HistoryPage(QWidget):

    def __init__(self):

        super().__init__()

        self.history_dir = Path("history")

        self.history_dir.mkdir(exist_ok=True)

        layout = QVBoxLayout(self)

        title = QLabel("Analysis History")

        title.setAlignment(Qt.AlignCenter)

        title.setStyleSheet("""

            font-size:28px;
            font-weight:bold;

        """)

        layout.addWidget(title)

        self.list = QListWidget()

        layout.addWidget(self.list)

        self.refresh_button = QPushButton("Refresh")

        self.open_button = QPushButton("Open Selected Report")

        layout.addWidget(self.refresh_button)

        layout.addWidget(self.open_button)

        self.refresh_button.clicked.connect(

            self.refresh

        )

        self.open_button.clicked.connect(

            self.open_selected

        )

        self.refresh()

    def refresh(self):

        self.list.clear()

        files = sorted(

            self.history_dir.glob("*.pdf"),

            reverse=True,

        )

        for f in files:

            self.list.addItem(f.name)

    def open_selected(self):

        item = self.list.currentItem()

        if item is None:

            return

        pdf = self.history_dir / item.text()

        QDesktopServices.openUrl(

            QUrl.fromLocalFile(

                str(pdf.resolve())

            )

        )
