from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session

from app.dependencies.db import get_db
from app.schemas.general import DepartmentResponse, SemesterResponse
from app.services.general_service import DepartmentsService, SemestersService

router = APIRouter()


@router.get("/departments/list", response_model=DepartmentResponse)
def list_departments_all_basic(
    db: Session = Depends(get_db),
) -> DepartmentResponse:
    try:
        departments = DepartmentsService.list_departments_all_basic(db=db)
        return DepartmentResponse(names=departments)
    except OperationalError as exc:
        raise HTTPException(
            status_code=503,
            detail=f"Database connection failed: {exc}",
        ) from exc


@router.get("/semesters/list", response_model=SemesterResponse)
def list_semesters_all_basic(
    db: Session = Depends(get_db),
) -> SemesterResponse:
    try:
        semesters = SemestersService.list_semesters_all_basic(db=db)
        return SemesterResponse(names=semesters)
    except OperationalError as exc:
        raise HTTPException(
            status_code=503,
            detail=f"Database connection failed: {exc}",
        ) from exc
