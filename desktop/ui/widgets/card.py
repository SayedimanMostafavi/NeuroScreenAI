from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel


class Card(QFrame):

    def __init__(self, title):
        super().__init__()

        self.setObjectName("card")

        self.layout = QVBoxLayout(self)

        title_label = QLabel(title)
        title_label.setObjectName("cardTitle")

        self.layout.addWidget(title_label)

    def addWidget(self, widget):
        self.layout.addWidget(widget)
