from app.schemas.metadata import Metadata

class Document:
    id: int
    source: str
    file_name: str
    file_path: str
    content: str
    metadata: Metadata