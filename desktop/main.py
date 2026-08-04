import sys

from PySide6.QtWidgets import QApplication

from desktop.ui.splash import SplashScreen
from desktop.ui.main_window import MainWindow


def main():

    app = QApplication(sys.argv)

    app.setApplicationName("NeuroScreenAI")

    splash = SplashScreen()

    splash.show()

    window = MainWindow()

    def show_main():

        window.show()

    splash.destroyed.connect(show_main)

    sys.exit(app.exec())


if __name__ == "__main__":

    main()
