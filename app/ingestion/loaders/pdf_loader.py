from pypdf import PdfReader

def load_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""

    for page in reader.pages:
        text += page.extract_text()

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
