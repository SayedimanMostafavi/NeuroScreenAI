from pathlib import Path

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QFileDialog,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class UploadCard(QWidget):

    fileSelected = Signal(str)

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        self.label = QLabel(
            "Drag & Drop EDF File\n\nor"
        )

        self.label.setStyleSheet("""
            font-size:16px;
        """)

        self.label.setAlignment(
            Qt.AlignCenter
        )

        self.button = QPushButton(
            "Select EDF File"
        )

        self.button.clicked.connect(
            self.open_file
        )

        layout.addStretch()

        layout.addWidget(self.label)

        layout.addWidget(self.button)

        layout.addStretch()

    def open_file(self):

        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Open EDF",
            "",
            "EDF Files (*.edf)"
        )

        if file_path:

            self.fileSelected.emit(file_path)
