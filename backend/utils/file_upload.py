"""File upload utilities."""

import logging
import os
import uuid
from pathlib import Path
from typing import Optional

import aiofiles
from fastapi import HTTPException, UploadFile, status

from backend.config.settings import settings

logger = logging.getLogger(__name__)

ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/webp", "image/gif"}
ALLOWED_DOC_TYPES = {"application/pdf", "text/plain"}


def _ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


async def save_upload(
    file: UploadFile,
    subfolder: str = "misc",
    allowed_types: Optional[set] = None,
) -> str:
    """Save an uploaded file and return its relative path."""
    if allowed_types and file.content_type not in allowed_types:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"File type '{file.content_type}' is not allowed",
        )

    content = await file.read()
    if len(content) > settings.max_upload_bytes:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File exceeds maximum size of {settings.MAX_UPLOAD_SIZE_MB}MB",
        )

    ext = Path(file.filename or "file").suffix
    filename = f"{uuid.uuid4().hex}{ext}"
    upload_dir = Path(settings.UPLOAD_DIR) / subfolder
    _ensure_dir(upload_dir)
    file_path = upload_dir / filename

    async with aiofiles.open(file_path, "wb") as f:
        await f.write(content)

    relative_path = f"{subfolder}/{filename}"
    logger.info("📁 Saved upload: %s", relative_path)
    return relative_path


async def save_profile_image(file: UploadFile) -> str:
    return await save_upload(file, subfolder="profiles", allowed_types=ALLOWED_IMAGE_TYPES)


async def save_resume_file(file: UploadFile) -> str:
    return await save_upload(file, subfolder="resumes", allowed_types=ALLOWED_DOC_TYPES)


def delete_file(relative_path: str) -> None:
    full_path = Path(settings.UPLOAD_DIR) / relative_path
    if full_path.exists():
        os.remove(full_path)
        logger.info("🗑️ Deleted file: %s", relative_path)
