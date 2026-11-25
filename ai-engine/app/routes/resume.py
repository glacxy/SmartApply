from fastapi import APIRouter, UploadFile, File, HTTPException

from app.services.resume_service import (
    extract_text_from_pdf,
    parse_resume
)

router = APIRouter()


@router.post("/upload")
async def upload_resume(file: UploadFile = File(...)):

    # Validate file type
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed"
        )

    # Read file bytes
    file_bytes = await file.read()

    # Maximum file size: 5 MB
    max_size = 5 * 1024 * 1024

    if len(file_bytes) > max_size:
        raise HTTPException(
            status_code=400,
            detail="File size must be less than 5 MB"
        )

    # Validate empty file
    if not file_bytes:
        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty"
        )

    # Validate PDF signature
    if not file_bytes.startswith(b"%PDF-"):
        raise HTTPException(
            status_code=400,
            detail="Invalid PDF file"
        )

    # Extract raw text
    text = extract_text_from_pdf(file_bytes)

    # Parse raw text into structured data
    resume_data = parse_resume(text)

    # Return response
    return {
        "filename": file.filename,
        "resume": resume_data
    }