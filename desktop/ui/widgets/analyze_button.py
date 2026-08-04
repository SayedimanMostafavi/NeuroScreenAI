from PySide6.QtWidgets import QPushButton


class AnalyzeButton(QPushButton):

    def __init__(self):

        super().__init__("🧠 Analyze EEG")

        self.setMinimumHeight(60)

        self.setEnabled(False)
