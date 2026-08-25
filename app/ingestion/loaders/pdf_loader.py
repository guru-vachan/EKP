from pypdf import PdfReader

def load_pdf(file_path):
    try:
        reader = PdfReader(file_path)
    except Exception as e:
        

    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text


# for multiple pdf 
def load_multiple_pdfs(file_paths):
    documents = []

    for file_path in file_paths:
        reader = PdfReader(file_path)

        for i, page in enumerate(reader.pages):
            text = page.extract_text()

            if text:
                documents.append({
                    "text": text,
                    "source": file_path,
                    "page": i
                })

    return documents
