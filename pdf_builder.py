from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from PyPDF2 import PdfMerger

def generate_compliance_letter(filename, deviations):

    doc = SimpleDocTemplate(filename)
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph("Compliance Letter", styles["Heading1"]))

    for dev in deviations:
        elements.append(Paragraph(
            f"{dev['requirement_id']} - {dev['reasoning']}",
            styles["Normal"]
        ))

    doc.build(elements)


def merge_pdfs(output_path, pdf_list):

    merger = PdfMerger()

    for pdf in pdf_list:
        merger.append(pdf)

    merger.write(output_path)
    merger.close()
