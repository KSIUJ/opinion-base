from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session

from app.db import SessionLocal
from app.schemas.lecturers import LecturerListResponse, LecturerOut
from app.services.lecturers_service import LecturersService
from app.dependencies.db import get_db

router = APIRouter()


@router.get("", response_model=LecturerListResponse)
def list_lecturers(db: Session = Depends(get_db)) -> LecturerListResponse:
    try:
        return LecturersService.list_lecturers(db)
    except OperationalError as exc:
        raise HTTPException(
            status_code=503,
            detail=f"Database connection failed: {exc}",
        ) from exc


@router.get("/search", response_model=LecturerListResponse)
def search_lecturers(
    surname: str | None = None,
    subject: str | None = None,
    db: Session = Depends(get_db),
) -> LecturerListResponse:
    try:
        return LecturersService.search_lecturers(
            db, surname=surname, subject=subject
        )
    except OperationalError as exc:
        raise HTTPException(
            status_code=503,
            detail=f"Database connection failed: {exc}",
        ) from exc


@router.get("/{lecturer_id}", response_model=LecturerOut)
def get_lecturer(
    lecturer_id: int,
    db: Session = Depends(get_db),
) -> LecturerOut:
    try:
        lecturer = LecturersService.get_lecturer(db, lecturer_id)
    except OperationalError as exc:
        raise HTTPException(
            status_code=503,
            detail=f"Database connection failed: {exc}",
        ) from exc

    if lecturer is None:
        raise HTTPException(status_code=404, detail="Lecturer not found")

