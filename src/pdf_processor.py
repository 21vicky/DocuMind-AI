import pymupdf


def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    """
    Extract text from an uploaded PDF document.

    Args:
        pdf_bytes: PDF file content in bytes.

    Returns:
        Extracted text from all PDF pages.
    """

    if not pdf_bytes:
        raise ValueError("The uploaded PDF is empty.")

    extracted_text = []

    try:
        # Open PDF from memory
        document = pymupdf.open(
            stream=pdf_bytes,
            filetype="pdf"
        )

        # Read every page
        for page_number, page in enumerate(document, start=1):

            text = page.get_text("text")

            if text.strip():
                extracted_text.append(
                    f"\n--- Page {page_number} ---\n{text}"
                )

        document.close()

    except Exception as error:
        raise ValueError(
            f"Unable to process PDF: {error}"
        ) from error

    if not extracted_text:
        raise ValueError(
            "No readable text found in this PDF. "
            "It may be a scanned document."
        )

    return "\n".join(extracted_text)