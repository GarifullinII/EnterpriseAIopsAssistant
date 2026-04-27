from fastapi import APIRouter, Depends, File, Form, UploadFile, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.document import Document
from app.models.document_chunk import DocumentChunk
from app.schemas.document import DocumentCreate, DocumentResponse
from pathlib import Path
import shutil
from app.schemas.document_chunk import DocumentChunkResponse
from app.services.chunking import build_document_chunks, save_document_chunks
from app.services.extraction import extract_text_from_file
from app.services.indexing import index_document_chunks


router = APIRouter(prefix="/documents", tags=["documents"])

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@router.post("/", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
def create_document(payload: DocumentCreate, db: Session = Depends(get_db)) -> Document:
    document = Document(
        title=payload.title,
        source=payload.source,
        status="uploaded",
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    return document

@router.post("/upload", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
def upload_document(
    title: str = Form(...),
    source: str = Form("manual"),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
) -> Document:
    # 1. создаем запись
    document = Document(
        title=title,
        source=source,
        status="uploaded",
        original_filename=file.filename,
        mime_type=file.content_type,
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    suffix = Path(file.filename).suffix if file.filename else ""
    saved_path = UPLOAD_DIR / f"{document.id}{suffix}"

    try:
        # 2. сохраняем файл
        with saved_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # 3. обновляем запись
        document.file_path = str(saved_path)
        document.status = "stored"

        db.commit()
        db.refresh(document)

    except Exception as e:
        # откат + очистка
        db.rollback()

        # удалить запись из БД
        db.delete(document)
        db.commit()

        # удалить файл, если он частично создался
        if saved_path.exists():
            saved_path.unlink(missing_ok=True)

        raise HTTPException(
            status_code=500,
            detail=f"Ошибка сохранения файла: {str(e)}"
        )

    finally:
        file.file.close()

    return document

@router.post("/{document_id}/process", response_model=DocumentResponse)
def process_document(document_id: str, db: Session = Depends(get_db)) -> Document:
    document = db.get(Document, document_id)

    if document is None:
        raise HTTPException(status_code=404, detail="Document not found")

    if not document.file_path:
        raise HTTPException(status_code=400, detail="Document has no file path")

    try:
        document.status = "processing"
        db.commit()
        db.refresh(document)

        extracted_text = extract_text_from_file(document.file_path)

        document.extracted_text = extracted_text
        document.status = "processed"

        db.commit()
        db.refresh(document)

        return document

    except Exception as e:
        document.status = "failed"
        db.commit()
        db.refresh(document)

        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")
    

@router.post("/{document_id}/chunk", response_model=DocumentResponse)
def chunk_document(document_id: str, db: Session = Depends(get_db)) -> Document:
    document = db.get(Document, document_id)

    if document is None:
        raise HTTPException(status_code=404, detail="Document not found")

    if not document.extracted_text:
        raise HTTPException(
            status_code=400,
            detail="Document has no extracted_text. Run /process first."
        )

    try:
        document.status = "chunking"
        db.commit()
        db.refresh(document)

        chunks = build_document_chunks(
            document_id=document.id,
            text=document.extracted_text,
            chunk_size=800,
            chunk_overlap=150,
        )

        if not chunks:
            raise HTTPException(
                status_code=400,
                detail="Extracted text is empty after normalization"
            )

        save_document_chunks(db=db, document=document, chunks=chunks)

        db.refresh(document)
        return document

    except HTTPException:
        document.status = "failed"
        db.commit()
        db.refresh(document)
        raise

    except Exception as e:
        document.status = "failed"
        db.commit()
        db.refresh(document)

        raise HTTPException(status_code=500, detail=f"Chunking failed: {str(e)}")


@router.get("/{document_id}/chunks", response_model=list[DocumentChunkResponse])
def get_document_chunks(document_id: str, db: Session = Depends(get_db)) -> list[DocumentChunk]:
    document = db.get(Document, document_id)

    if document is None:
        raise HTTPException(status_code=404, detail="Document not found")

    return document.chunks


@router.post("/{document_id}/index", response_model=DocumentResponse)
def index_document(document_id: str, db: Session = Depends(get_db)) -> Document:
    document = db.get(Document, document_id)

    if document is None:
        raise HTTPException(status_code=404, detail="Document not found")

    if document.status != "chunked":
        raise HTTPException(
            status_code=400,
            detail="Document must be chunked before indexing"
        )

    try:
        document.status = "indexing"
        db.commit()
        db.refresh(document)

        index_document_chunks(db=db, document=document)

        db.refresh(document)
        return document

    except HTTPException:
        db.rollback()
        raise

    except Exception as e:
        db.rollback()
        document.status = "failed"
        db.commit()
        db.refresh(document)

        raise HTTPException(status_code=500, detail=f"Indexing failed: {str(e)}")
