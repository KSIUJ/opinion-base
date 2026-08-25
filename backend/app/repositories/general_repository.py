from sqlalchemy import Select, select
from sqlalchemy.orm import Session

from app.models import Department, Semester


class DepartmentsRepository:
    @staticmethod
    def build_query_basic() -> Select:
        query = select(Department)
        return query

    @staticmethod
    def list_departments_all_basic(db: Session) -> list[Department]:
        query = DepartmentsRepository.build_query_basic()
        return db.execute(query).unique().scalars().all()


class SemestersRepository:
    @staticmethod
    def build_query_basic() -> Select:
        query = select(Semester)
        return query

    @staticmethod
    def list_semesters_all_basic(db: Session) -> list[Semester]:
        query = SemestersRepository.build_query_basic()
        return db.execute(query).unique().scalars().all()
