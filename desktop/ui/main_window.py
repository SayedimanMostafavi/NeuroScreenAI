from PySide6.QtCore import Qt

from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QStackedWidget,
)

from desktop.ui.dashboard import DashboardPage
from desktop.ui.results import ResultsPage
from desktop.ui.history import HistoryPage
from desktop.ui.about import AboutPage


class MainWindow(QMainWindow):

    def __init__(self):

        super().__init__()

        self.setWindowTitle("NeuroScreenAI")

        self.resize(1400, 850)

        root = QWidget()

        self.setCentralWidget(root)

        main_layout = QHBoxLayout(root)

        ##################################################

        sidebar = QVBoxLayout()

        sidebar.setSpacing(12)

        self.dashboard_btn = QPushButton("Dashboard")

        self.results_btn = QPushButton("Results")

        self.history_btn = QPushButton("History")

        self.about_btn = QPushButton("About")

        for btn in [

            self.dashboard_btn,

            self.results_btn,

            self.history_btn,

            self.about_btn,

        ]:

            btn.setMinimumHeight(55)

            sidebar.addWidget(btn)

        sidebar.addStretch()

        ##################################################

        self.pages = QStackedWidget()

        self.dashboard = DashboardPage()

        self.results = ResultsPage()

        self.history = HistoryPage()

        self.about = AboutPage()

        self.pages.addWidget(self.dashboard)

        self.pages.addWidget(self.results)

        self.pages.addWidget(self.history)

        self.pages.addWidget(self.about)

        ##################################################

        main_layout.addLayout(sidebar, 1)

        main_layout.addWidget(self.pages, 5)

        ##################################################

        self.dashboard_btn.clicked.connect(

            lambda: self.pages.setCurrentWidget(

                self.dashboard

            )

        )

        self.results_btn.clicked.connect(

            lambda: self.pages.setCurrentWidget(

                self.results

            )

        )

        self.history_btn.clicked.connect(

            lambda: self.pages.setCurrentWidget(

                self.history

            )

        )

        self.about_btn.clicked.connect(

            lambda: self.pages.setCurrentWidget(

                self.about

            )

        )

        ##################################################

        self.dashboard.analysis_completed.connect(

            self.show_result

        )

    def show_result(self, result):

        self.results.update_result(result)

        self.history.refresh()

        self.pages.setCurrentWidget(

            self.results

        )
