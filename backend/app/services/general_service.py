from sqlalchemy.orm import Session

from app.repositories.general_repository import (
    DepartmentsRepository,
    SemestersRepository,
)


class DepartmentsService:
    @staticmethod
    def list_departments_all_basic(db: Session) -> list[str]:
        departments = DepartmentsRepository.list_departments_all_basic(db=db)
        return [department.name for department in departments]


class SemestersService:
    @staticmethod
    def list_semesters_all_basic(db: Session) -> list[str]:
        semesters = SemestersRepository.list_semesters_all_basic(db=db)
        return [semester.name for semester in semesters]
