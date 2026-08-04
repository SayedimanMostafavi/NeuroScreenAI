from desktop.services.analysis_service import AnalysisService


class AnalysisController:

    def __init__(self):

        self.service = AnalysisService()

    def analyze(self, edf_path):

        return self.service.analyze(edf_path)
