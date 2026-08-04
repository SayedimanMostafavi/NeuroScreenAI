from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QFrame,
)


class AboutPage(QWidget):

    def __init__(self):

        super().__init__()

        layout = QVBoxLayout(self)

        title = QLabel("NeuroScreenAI")

        title.setAlignment(Qt.AlignCenter)

        title.setStyleSheet("""

            font-size:34px;
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

        card = QFrame()

        card.setStyleSheet("""

            QFrame{

                background:#2b2b2b;

                border-radius:12px;

                padding:20px;

            }

        """)

        card_layout = QVBoxLayout(card)

        info = QLabel("""

Version

1.0


Artificial Intelligence Model

Subject-Level SVM

Estimated Accuracy

90%


Features

• Power Spectral Density

• Relative PSD

• Band Ratios

• Hjorth Parameters

• Spectral Entropy

• Frontal Alpha Asymmetry


Developed By

Dr. Faezeh Rohani

Sayediman Mostafavi


Disclaimer

This software is intended for research and screening purposes only.

It must not be used as a substitute for professional clinical diagnosis.

""")

        info.setWordWrap(True)

        info.setStyleSheet("""

            font-size:16px;

        """)

        card_layout.addWidget(info)

        layout.addWidget(card)

        layout.addStretch()
