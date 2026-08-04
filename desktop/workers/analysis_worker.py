from PySide6.QtCore import QObject
from PySide6.QtCore import Signal

from desktop.controllers.analysis_controller import AnalysisController


class AnalysisWorker(QObject):

    finished = Signal(object)

    error = Signal(str)

    progress = Signal(int)

    def __init__(self, edf_path):

        super().__init__()

        self.edf_path = edf_path

        self.controller = AnalysisController()

    def run(self):

        try:

            self.progress.emit(10)

            result = self.controller.analyze(

                self.edf_path

            )

            self.progress.emit(100)

            self.finished.emit(result)

        except Exception as e:

            self.error.emit(str(e))
