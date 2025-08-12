import pymupdf


def process_pdf(input_path: str) -> list[str]:
    try:
        with pymupdf.open(input_path) as pdf:
            text_by_page = [page.get_text() for page in pdf]

    except Exception as e:
        raise Exception(f"PDF file processing failed. Please ensure that the file path is correct and that the file is not corrupted. Full Error: {e}")
    
    return text_by_page

# def process_word() -> ...