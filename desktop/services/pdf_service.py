from pathlib import Path
from datetime import datetime

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
)


class PDFService:

    def __init__(self):

        self.output = Path("history")

        self.output.mkdir(exist_ok=True)

    def export(self, result):

        filename = datetime.now().strftime(
            "%Y-%m-%d_%H-%M-%S.pdf"
        )

        pdf = self.output / filename

        doc = SimpleDocTemplate(str(pdf))

        styles = getSampleStyleSheet()

        story = []

        story.append(
            Paragraph(
                "<b><font size=22>NeuroScreenAI</font></b>",
                styles["Title"],
            )
        )

        story.append(
            Paragraph(
                "EEG Depression Screening Report",
                styles["Heading2"],
            )
        )

        story.append(Spacer(1, 20))

        story.append(
            Paragraph(
                f"<b>Diagnosis:</b> {result.diagnosis}",
                styles["BodyText"],
            )
        )

        story.append(
            Paragraph(
                f"<b>Probability:</b> {result.probability*100:.2f} %",
                styles["BodyText"],
            )
        )

        story.append(
            Paragraph(
                f"<b>EDF File:</b> {result.file_name}",
                styles["BodyText"],
            )
        )

        story.append(
            Paragraph(
                f"<b>Channels:</b> {result.channels}",
                styles["BodyText"],
            )
        )

        story.append(
            Paragraph(
                f"<b>Sampling Rate:</b> {result.sampling_rate:.0f} Hz",
                styles["BodyText"],
            )
        )

        story.append(
            Paragraph(
                f"<b>Duration:</b> {result.duration} sec",
                styles["BodyText"],
            )
        )

        story.append(
            Paragraph(
                f"<b>Windows:</b> {result.windows}",
                styles["BodyText"],
            )
        )

        story.append(Spacer(1, 20))

        story.append(
            Paragraph(
                "<b>Model</b>",
                styles["Heading2"],
            )
        )

        story.append(
            Paragraph(
                "Subject-Level SVM",
                styles["BodyText"],
            )
        )

        story.append(
            Paragraph(
                "Approximate Validation Accuracy: 90%",
                styles["BodyText"],
            )
        )

        story.append(Spacer(1, 20))

        story.append(
            Paragraph(
                "<b>Disclaimer</b>",
                styles["Heading2"],
            )
        )

        story.append(
            Paragraph(
                "NeuroScreenAI is an AI-assisted screening tool. "
                "It is not intended to replace clinical diagnosis. "
                "All results should be interpreted by qualified healthcare professionals.",
                styles["BodyText"],
            )
        )

        story.append(Spacer(1, 20))

        story.append(
            Paragraph(
                "<b>Developed By</b>",
                styles["Heading2"],
            )
        )

        story.append(
            Paragraph(
                "Dr. Faezeh Rohani<br/>"
                "Sayediman Mostafavi",
                styles["BodyText"],
            )
        )

        doc.build(story)

        return pdf
