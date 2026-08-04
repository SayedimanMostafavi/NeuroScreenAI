from PySide6.QtWidgets import (
    QLabel,
    QDialog,
    QVBoxLayout,
    QProgressBar,
)


class ProgressDialog(QDialog):

    def __init__(self):

        super().__init__()

        self.setWindowTitle("NeuroScreenAI")

        self.setModal(True)

        self.setFixedSize(420,180)

        layout = QVBoxLayout(self)

        title = QLabel("Analyzing EEG...")

        title.setStyleSheet("""
            font-size:18px;
            font-weight:bold;
        """)

        self.status = QLabel("Preparing...")

        self.bar = QProgressBar()

        self.bar.setRange(0,0)

        layout.addWidget(title)

        layout.addSpacing(20)

        layout.addWidget(self.status)

        layout.addWidget(self.bar)

    def update_status(self, text):

        self.status.setText(text)
