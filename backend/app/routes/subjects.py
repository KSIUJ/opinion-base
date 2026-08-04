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
def list_subjects(
    subject_id: int | None = None,
    subject_name: str | None = None,
    lecturer_id: int | None = None,
    lecturer_name: str | None = None,
    lecturer_surname: str | None = None,
    min_opinions: int | None = None,
    db: Session = Depends(get_db),
) -> SubjectsResponse:

    if min_opinions is not None and min_opinions < 0:
        raise HTTPException(status_code=422, detail="min_opinions must be >= 0")
'''
    if not any(
            value is not None
            for value in [
                subject_id,
                subject_name,
                lecturer_id,
                lecturer_name,
                lecturer_surname,
                min_opinions,
            ]
    ):
        return SubjectsResponse(subjects=SubjectsService.list_subjects_all(db=db))
'''

    
    try:
        subjects = SubjectsService.list_subjects(
            db=db,
            subject_id=subject_id,
            subject_name=subject_name,
            lecturer_id=lecturer_id,
            lecturer_name=lecturer_name,
            lecturer_surname=lecturer_surname,
            min_opinions=min_opinions,
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
    return list_subjects(subject_id=subject_id, db=db)

