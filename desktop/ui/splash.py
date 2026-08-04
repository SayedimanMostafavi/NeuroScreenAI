from PySide6.QtCore import Qt
from PySide6.QtCore import QTimer

from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QProgressBar,
)


class SplashScreen(QWidget):

    def __init__(self):

        super().__init__()

        self.setWindowTitle("NeuroScreenAI")

        self.setFixedSize(700, 420)

        layout = QVBoxLayout(self)

        layout.setSpacing(25)

        layout.addStretch()

        title = QLabel("NeuroScreenAI")

        title.setAlignment(Qt.AlignCenter)

        title.setStyleSheet("""

            font-size:40px;

            font-weight:bold;

        """)

        layout.addWidget(title)

        subtitle = QLabel(

            "EEG-Based Depression Screening System"

        )

        subtitle.setAlignment(Qt.AlignCenter)

        subtitle.setStyleSheet("""

            font-size:18px;

        """)

        layout.addWidget(subtitle)

        authors = QLabel(

            "Dr. Faezeh Rohani\n"

            "Sayediman Mostafavi"

        )

        authors.setAlignment(Qt.AlignCenter)

        authors.setStyleSheet("""

            font-size:16px;

        """)

        layout.addWidget(authors)

        self.progress = QProgressBar()

        self.progress.setRange(0,100)

        layout.addWidget(self.progress)

        self.status = QLabel("Loading AI Model...")

        self.status.setAlignment(Qt.AlignCenter)

        layout.addWidget(self.status)

        layout.addStretch()

        self.value = 0

        self.timer = QTimer()

        self.timer.timeout.connect(

            self.animate

        )

        self.timer.start(25)

    def animate(self):

        self.value += 1

        self.progress.setValue(self.value)

        if self.value >= 100:

            self.timer.stop()

            self.close()
