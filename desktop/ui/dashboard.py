from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtCore import Signal
from PySide6.QtCore import QThread

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QFileDialog,
    QProgressBar,
    QMessageBox,
)

from desktop.workers.analysis_worker import AnalysisWorker


class DashboardPage(QWidget):

    analysis_completed = Signal(object)

    def __init__(self):

        super().__init__()

        self.selected_file = None

        self.thread = None

        self.worker = None

        layout = QVBoxLayout(self)

        layout.setSpacing(20)

        title = QLabel("NeuroScreenAI")

        title.setAlignment(Qt.AlignCenter)

        title.setStyleSheet("""

            font-size:34px;

            font-weight:bold;

        """)

        layout.addWidget(title)

        subtitle = QLabel(

            "EEG-Based Depression Screening System\n\n"

            "Developed by\n"

            "Dr. Faezeh Rohani\n"

            "Sayediman Mostafavi"

        )

        subtitle.setAlignment(Qt.AlignCenter)

        subtitle.setStyleSheet("""

            font-size:18px;

        """)

        layout.addWidget(subtitle)

        self.file_label = QLabel(

            "No EDF file selected"

        )

        self.file_label.setAlignment(Qt.AlignCenter)

        layout.addWidget(self.file_label)

        self.select_button = QPushButton(

            "Select EDF File"

        )

        self.select_button.setMinimumHeight(45)

        layout.addWidget(self.select_button)

        self.start_button = QPushButton(

            "Start Analysis"

        )

        self.start_button.setMinimumHeight(45)

        self.start_button.setEnabled(False)

        layout.addWidget(self.start_button)

        self.progress = QProgressBar()

        self.progress.setValue(0)

        layout.addWidget(self.progress)

        layout.addStretch()

        self.select_button.clicked.connect(

            self.select_file

        )

        self.start_button.clicked.connect(

            self.start_analysis

        )

    def select_file(self):

        filename, _ = QFileDialog.getOpenFileName(

            self,

            "Open EDF",

            "",

            "EDF Files (*.edf)"

        )

        if not filename:

            return

        self.selected_file = filename

        self.file_label.setText(

            Path(filename).name

        )

        self.start_button.setEnabled(True)

    def start_analysis(self):

        if self.selected_file is None:

            return

        self.select_button.setEnabled(False)

        self.start_button.setEnabled(False)

        self.progress.setValue(0)

        self.thread = QThread()

        self.worker = AnalysisWorker(

            self.selected_file

        )

        self.worker.moveToThread(

            self.thread

        )

        self.thread.started.connect(

            self.worker.run

        )

        self.worker.progress.connect(

            self.progress.setValue

        )

        self.worker.finished.connect(

            self.analysis_finished

        )

        self.worker.error.connect(

            self.analysis_error

        )

        self.worker.finished.connect(

            self.thread.quit

        )

        self.worker.finished.connect(

            self.worker.deleteLater

        )

        self.thread.finished.connect(

            self.thread.deleteLater

        )

        self.thread.start()

    def analysis_finished(self, result):

        self.progress.setValue(100)

        self.select_button.setEnabled(True)

        self.start_button.setEnabled(True)

        self.analysis_completed.emit(result)

    def analysis_error(self, message):

        self.select_button.setEnabled(True)

        self.start_button.setEnabled(True)

        self.progress.setValue(0)

        QMessageBox.critical(

            self,

            "Error",

            message,

        )
