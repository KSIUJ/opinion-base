from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models import (
    ActiveSubject,
    Department,
    Lecturer,
    LecturerOpinionRelation,
    Opinion,
    Subject,
    SubjectOpinionRelation,
)


class LecturersRepository:
    @staticmethod
    def list_lecturers(db: Session) -> list[Lecturer]:
        query = (
            select(Lecturer)
            .options(selectinload(Lecturer.active_subjects))
            .order_by(Lecturer.id)
        )
        return db.execute(query).unique().scalars().all()

    @staticmethod
    def search_lecturers(
        db: Session,
        name: str | None = None,
        surname: str | None = None,
        subject: str | None = None,
        department: str | None = None,
        sort_by: str | None = None,
        order: str = "asc",
    ) -> list[Lecturer]:
        sort_fields = {"name": Lecturer.name, "surname": Lecturer.surname}
        column = sort_fields.get(sort_by or "surname", Lecturer.surname)
        query = (
            select(Lecturer)
            .options(
                selectinload(Lecturer.department),
                selectinload(Lecturer.active_subjects),
            )
            .order_by(
                column.desc() if order == "desc" else column.asc(),
                Lecturer.name.asc(),
            )
        )
        if name:
            query = query.where(Lecturer.name.ilike(f"%{name}%"))
        if surname:
            query = query.where(Lecturer.surname.ilike(f"%{surname}%"))
        if subject:
            query = (
                query.join(Lecturer.active_subjects)
                .join(ActiveSubject.subject)
                .where(Subject.name.ilike(f"%{subject}%"))
            )
            query = query.distinct()
        if department:
            query = query.join(Lecturer.department).where(
                Department.name.ilike(f"%{department}%")
            )
        return db.execute(query).unique().scalars().all()

    @staticmethod
    def get_lecturer(db: Session, lecturer_id: int) -> Lecturer | None:
        query = (
            select(Lecturer)
            .where(Lecturer.id == lecturer_id)
            .options(
                selectinload(Lecturer.department),
                selectinload(Lecturer.active_subjects).selectinload(
                    ActiveSubject.subject
                ),
                selectinload(Lecturer.opinion_relations)
                .selectinload(LecturerOpinionRelation.opinion)
                .selectinload(Opinion.subject_relations)
                .selectinload(SubjectOpinionRelation.subject),
            )
        )
        return db.execute(query).unique().scalars().one_or_none()
