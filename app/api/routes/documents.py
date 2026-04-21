from fastapi import APIRouter, Depends, File, Form, UploadFile, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.document import Document
from app.schemas.document import DocumentCreate, DocumentResponse
from pathlib import Path
import shutil


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