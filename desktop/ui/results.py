from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QPushButton,
    QFrame,
    QFileDialog,
)

from desktop.services.pdf_service import PDFService


class ResultsPage(QWidget):

    def __init__(self):

        super().__init__()

        self._result = None

        self.pdf_service = PDFService()

        layout = QVBoxLayout(self)

        layout.setSpacing(20)

        # --------------------------------------------------
        # Title
        # --------------------------------------------------

        title = QLabel("Analysis Report")

        title.setAlignment(Qt.AlignCenter)

        title.setStyleSheet("""

            font-size:28px;
            font-weight:bold;

        """)

        layout.addWidget(title)

        # --------------------------------------------------
        # Card
        # --------------------------------------------------

        card = QFrame()

        card.setStyleSheet("""

            QFrame{

                background:#2b2b2b;

                border-radius:12px;

                padding:20px;

            }

        """)

        card_layout = QVBoxLayout(card)

        # --------------------------------------------------
        # Diagnosis
        # --------------------------------------------------

        self.diagnosis = QLabel("--")

        self.diagnosis.setAlignment(Qt.AlignCenter)

        self.diagnosis.setStyleSheet("""

            font-size:34px;
            font-weight:bold;

        """)

        card_layout.addWidget(self.diagnosis)

        # --------------------------------------------------
        # Probability
        # --------------------------------------------------

        self.probability = QLabel("--")

        self.probability.setAlignment(Qt.AlignCenter)

        self.probability.setStyleSheet("""

            font-size:22px;

        """)

        card_layout.addWidget(self.probability)

        # --------------------------------------------------
        # Confidence
        # --------------------------------------------------

        self.confidence = QLabel("--")

        self.confidence.setAlignment(Qt.AlignCenter)

        self.confidence.setStyleSheet("""

            font-size:20px;

        """)

        card_layout.addWidget(self.confidence)

        card_layout.addSpacing(15)

        # --------------------------------------------------
        # Details
        # --------------------------------------------------

        self.details = QLabel()

        self.details.setAlignment(Qt.AlignLeft)

        self.details.setWordWrap(True)

        self.details.setStyleSheet("""

            font-size:16px;

        """)

        card_layout.addWidget(self.details)

        card_layout.addSpacing(20)

        # --------------------------------------------------
        # Disclaimer
        # --------------------------------------------------

        self.warning = QLabel(

            "This software is intended for screening only.\n"
            "Final diagnosis must be confirmed by a qualified clinician."

        )

        self.warning.setAlignment(Qt.AlignCenter)

        self.warning.setWordWrap(True)

        self.warning.setStyleSheet("""

            color:#ffcc66;
            font-size:15px;

        """)

        card_layout.addWidget(self.warning)

        layout.addWidget(card)

        # --------------------------------------------------
        # Export Button
        # --------------------------------------------------

        self.export_button = QPushButton("Export PDF Report")

        self.export_button.setMinimumHeight(45)

        self.export_button.clicked.connect(self.export_pdf)

        layout.addWidget(self.export_button)

        layout.addStretch()

    # ======================================================

    def update_result(self, result):

        self._result = result

        if result.prediction:

            color = "#ff5555"

        else:

            color = "#55ff7f"

        self.diagnosis.setStyleSheet(f"""

            color:{color};
            font-size:34px;
            font-weight:bold;

        """)

        self.diagnosis.setText(result.diagnosis)

        probability = result.probability * 100

        self.probability.setText(

            f"Probability : {probability:.2f}%"

        )

        if probability >= 90:

            confidence = "Very High"

        elif probability >= 80:

            confidence = "High"

        elif probability >= 70:

            confidence = "Moderate"

        else:

            confidence = "Low"

        self.confidence.setText(

            f"Confidence : {confidence}"

        )

        self.details.setText(

            f"""

File Name          : {result.file_name}

Channels           : {result.channels}

Windows            : {result.windows}

Sampling Rate      : {result.sampling_rate:.0f} Hz

Duration           : {result.duration} sec

Model              : Subject-Level SVM

Estimated Accuracy : 90%

"""

        )

    # ======================================================

    def export_pdf(self):

        if self._result is None:

            return

        filename, _ = QFileDialog.getSaveFileName(

            self,

            "Save Report",

            "NeuroScreenAI_Report.pdf",

            "PDF Files (*.pdf)",

        )

        if not filename:

            return

        self.pdf_service.output = Path(filename).parent

        pdf = self.pdf_service.export(self._result)

        pdf.rename(filename)
