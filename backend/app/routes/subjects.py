from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session

from app.dependencies.db import get_db
from app.schemas.subjects import SubjectsResponse
from app.schemas.subjects import SubjectsResponseBasic
from app.services.subjects_service import SubjectsService

router = APIRouter()


@router.get("/all", response_model=SubjectsResponseBasic)
def list_subjects_all(db: Session = Depends(get_db)) -> SubjectsResponseBasic:
    subjects = SubjectsService.list_subjects_all(db=db)
    return SubjectsResponseBasic(subjects=subjects)


@router.get("/", response_model=SubjectsResponse)
def list_subjects(db: Session = Depends(get_db)) -> SubjectsResponse:
    try:
        subjects = SubjectsService.list_subjects(db=db)
        return SubjectsResponse(subjects=subjects)
    except OperationalError as exc:
        raise HTTPException(
            status_code=503,
            detail=f"Database connection failed: {exc}",
        ) from exc


@router.get("/search", response_model=SubjectsResponse)
def search_subjects(
    name: str | None = None,
    semester_name: str | None = None,
    lecturer_surname: str | None = None,
    db: Session = Depends(get_db),
) -> SubjectsResponse:
    try:
        subjects = SubjectsService.list_subjects(
            db=db,
            subject_name=name,
            semester_name=semester_name,
            lecturer_surname=lecturer_surname,
        )
        return SubjectsResponse(subjects=subjects)
    except OperationalError as exc:
        raise HTTPException(
            status_code=503,
            detail=f"Database connection failed: {exc}",
        ) from exc


@router.get("/{subject_id}", response_model=SubjectsResponse)
def display_info(
    subject_id: int,
    db: Session = Depends(get_db),
) -> SubjectsResponse:
    try:
        subjects = SubjectsService.list_subjects(db=db, subject_id=subject_id)
        return SubjectsResponse(subjects=subjects)
    except OperationalError as exc:
        raise HTTPException(
            status_code=503,
            detail=f"Database connection failed: {exc}",
        ) from exc

