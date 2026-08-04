from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from PySide6.QtGui import QPainter
from PySide6.QtGui import QPen
from PySide6.QtWidgets import QWidget


class ProbabilityGauge(QWidget):

    def __init__(self):

        super().__init__()

        self.value = 0

        self.setMinimumSize(220, 220)

    def setValue(self, value):

        self.value = value

        self.update()

    def paintEvent(self, event):

        painter = QPainter(self)

        painter.setRenderHint(QPainter.Antialiasing)

        rect = self.rect().adjusted(20,20,-20,-20)

        pen = QPen(QColor("#2D333B"))

        pen.setWidth(15)

        painter.setPen(pen)

        painter.drawEllipse(rect)

        pen.setColor(QColor("#00B4D8"))

        painter.setPen(pen)

        span = int(360 * 16 * self.value)

        painter.drawArc(
            rect,
            90*16,
            -span
        )

        painter.setPen(Qt.white)

        painter.drawText(
            rect,
            Qt.AlignCenter,
            f"{self.value*100:.1f}%"
        )
