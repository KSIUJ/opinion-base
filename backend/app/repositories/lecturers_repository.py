from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models import ActiveSubject, Lecturer, Subject


class LecturersRepository:
    @staticmethod
    def list_lecturers(db: Session) -> list[Lecturer]:
        query = (
            select(Lecturer)
            .options(selectinload(Lecturer.subjects))
            .order_by(Lecturer.id)
        )
        return db.execute(query).unique().scalars().all()

    @staticmethod
    def search_lecturers(
        db: Session,
        surname: str | None = None,
        subject: str | None = None,
    ) -> list[Lecturer]:
        query = (
            select(Lecturer)
            .options(
                selectinload(Lecturer.department),
                selectinload(Lecturer.active_subjects),
            )
            .order_by(Lecturer.surname, Lecturer.name)
        )
        if surname:
            query = query.where(Lecturer.surname.ilike(f"%{surname}%"))
        if subject:
            query = (
                query.join(Lecturer.active_subjects)
                .join(ActiveSubject.subject)
                .where(Subject.name.ilike(f"%{subject}%"))
            )
            query = query.distinct()
        return db.execute(query).unique().scalars().all()

    @staticmethod
    def get_lecturer(db: Session, lecturer_id: int) -> Lecturer | None:
        query = (
            select(Lecturer)
            .where(Lecturer.id == lecturer_id)
            .options(
                selectinload(Lecturer.subjects).selectinload(Subject.opinions),
            )
        )
        return db.execute(query).unique().scalars().one_or_none()
