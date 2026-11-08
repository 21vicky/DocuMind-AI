import pymupdf

from src.pdf_processor import extract_text_from_pdf


# Create a sample PDF
pdf = pymupdf.open()

page = pdf.new_page()

page.insert_text(
    (50, 50),
    "Welcome to DocuMind AI!"
)

page.insert_text(
    (50, 100),
    "This is our first PDF extraction test."
)

pdf_bytes = pdf.tobytes()

pdf.close()


# Extract text
result = extract_text_from_pdf(pdf_bytes)

print("\n===== EXTRACTED PDF TEXT =====")
print(result)

print("\n===== TEST SUCCESSFUL =====")