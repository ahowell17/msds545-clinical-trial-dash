import csv
import io
from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import require_role
from app.db.session import get_db
from app.db import models

router = APIRouter(prefix="/upload", tags=["upload"])

uploader_required = require_role("uploader")

REQUIRED_COLUMNS = {"subject_id", "age", "gender", "treatment_arm", "site", "visit_date"}

@router.post("/csv")
async def upload_csv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(uploader_required),
):
    if not file.filename.lower().endswith(".csv"): # type: ignore
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only CSV files are supported.")

    raw = await file.read()
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unable to decode file as UTF-8.")

    reader = csv.DictReader(io.StringIO(text))
    header_cols = set(reader.fieldnames or [])
    missing = REQUIRED_COLUMNS - header_cols
    if missing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Missing required columns: {', '.join(sorted(missing))}",
        )

    upload = models.Upload(filename=file.filename, user_id=current_user.id)
    db.add(upload)
    db.flush()  # to populate upload.id

    records_created = 0
    for row in reader:
        try:
            age_int = int(row["age"])
        except (TypeError, ValueError):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid age value in row for subject_id {row.get('subject_id')}",
            )
        rec = models.ClinicalRecord(
            upload_id=upload.id,
            subject_id=row["subject_id"],
            age=age_int,
            gender=row["gender"],
            treatment_arm=row["treatment_arm"],
            site=row["site"],
            visit_date=row["visit_date"],
        )
        db.add(rec)
        records_created += 1

    db.commit()
    return {
        "message": "Upload successful",
        "filename": file.filename,
        "records_created": records_created,
        "upload_id": upload.id,
    }
