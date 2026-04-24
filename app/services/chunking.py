from langchain_text_splitters import RecursiveCharacterTextSplitter
from sqlalchemy.orm import Session
from app.models.document import Document
from app.models.document_chunk import DocumentChunk


def normalize_text(text: str) -> str:
    """
    Нормализуем текст:
    - убираем лишние пробелы по краям строк
    - удаляем полностью пустые строки
    """
    lines = [line.strip() for line in text.splitlines()]
    non_empty_lines = [line for line in lines if line]
    return "\n".join(non_empty_lines)


def build_text_splitter(
    chunk_size: int = 800,
    chunk_overlap: int = 150,
) -> RecursiveCharacterTextSplitter:
    """
    Создаём splitter LangChain.

    separators = порядок, в котором splitter пытается
    искать границы для более аккуратного разбиения.
    """
    return RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=[
            "\n\n",   # сначала пробуем резать по абзацам
            "\n",     # потом по строкам
            ". ",     # потом по предложениям
            " ",      # потом по словам
            "",       # и только потом по символам
        ],
        length_function=len,
        is_separator_regex=False,
    )


def chunk_text_with_langchain(
    text: str,
    chunk_size: int = 800,
    chunk_overlap: int = 150,
) -> list[str]:
    """
    Разбиваем текст на chunks через LangChain.
    """
    if chunk_overlap >= chunk_size:
        raise ValueError("chunk_overlap должен быть меньше chunk_size")
    
    cleaned_text = normalize_text(text)

    if not cleaned_text:
        return []

    splitter = build_text_splitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )

    chunks = splitter.split_text(cleaned_text)

    # Убираем пустые chunk'и.
    return [chunk.strip() for chunk in chunks if chunk.strip()]


def build_document_chunks(
    document_id: str,
    text: str,
    chunk_size: int = 800,
    chunk_overlap: int = 150,
) -> list[DocumentChunk]:
    """
    Превращаем список строк в список ORM-объектов DocumentChunk.
    """
    if chunk_overlap >= chunk_size:
        raise ValueError("chunk_overlap должен быть меньше chunk_size")

    raw_chunks = chunk_text_with_langchain(
        text=text,
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )

    document_chunks: list[DocumentChunk] = []

    for index, chunk_content in enumerate(raw_chunks):
        document_chunks.append(
            DocumentChunk(
                document_id=document_id,
                chunk_index=index,
                content=chunk_content,
                char_count=len(chunk_content),
            )
        )

    return document_chunks


def save_document_chunks(
    db: Session,
    document: Document,
    chunks: list[DocumentChunk],
) -> list[DocumentChunk]:
    """
    Сохраняем chunks в PostgreSQL.

    Если документ chunk'ится повторно, сначала удаляем старые chunks.
    """
    db.query(DocumentChunk).filter(DocumentChunk.document_id == document.id).delete()

    for chunk in chunks:
        db.add(chunk)

    document.status = "chunked"

    db.commit()

    for chunk in chunks:
        db.refresh(chunk)

    db.refresh(document)

    return chunks
