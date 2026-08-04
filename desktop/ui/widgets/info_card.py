from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QFormLayout,
)


class InfoCard(QWidget):

    def __init__(self):

        super().__init__()

        layout = QFormLayout(self)

        self.file = QLabel("--")

        self.channels = QLabel("--")

        self.fs = QLabel("--")

        self.duration = QLabel("--")

        self.status = QLabel("Waiting")

        layout.addRow("File", self.file)

        layout.addRow("Channels", self.channels)

        layout.addRow("Sampling Rate", self.fs)

        layout.addRow("Duration", self.duration)

        layout.addRow("Status", self.status)

    def update(self,
               filename,
               channels,
               fs,
               duration,
               status):

        self.file.setText(filename)

        self.channels.setText(str(channels))

        self.fs.setText(str(fs))

        self.duration.setText(str(duration))

        self.status.setText(status)
