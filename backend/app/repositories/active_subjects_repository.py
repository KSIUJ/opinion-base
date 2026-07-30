from sqlalchemy import Select, select
from sqlalchemy.orm import Session, selectinload

from app.models import Lecturer, ActiveSubject


class ActiveSubjectsRepository:
    @staticmethod
    def build_query_basic() -> Select:
        query = (select(ActiveSubject)
                 .options(
                     joininload(ActiveSubject.subject),
                     )
                 )
        return query

    @staticmethod
    def filter_query(
        subject_id: int | None = None,
        subject_name: str | None = None,
        lecturer_id: int | None = None,
        lecturer_name: str | None = None,
        lecturer_surname: str | None = None,
    ) -> Select:
        query = build_query()

        if subject_id is not None:
            query = query.where(ActiveSubject.id == subject_id)
        if subject_name:
            query = query.where(ActiveSubject.name.ilike(f"%{subject_name}%"))
        if lecturer_id is not None:
            query = query.where(ActiveSubject.lecturer == lecturer_id)

        if lecturer_name or lecturer_surname:
            query = query.join(ActiveSubject.lecturer_rel)
            if lecturer_name:
                query = query.where(Lecturer.name.ilike(f"%{lecturer_name}%"))
            if lecturer_surname:
                query = query.where(Lecturer.surname.ilike(f"%{lecturer_surname}%"))

        return query

    @staticmethod
    def list_subjects_all(
            db: Session
            ) -> list[ActiveSubject]:
        query = ActiveSubjectsRepository.build_query_basic()
        return db.execute(query).unique().scalars().all()
        
    @staticmethod
    def list_subjects(
        db: Session,
        subject_id: int | None = None,
        subject_name: str | None = None,
        lecturer_id: int | None = None,
        lecturer_name: str | None = None,
        lecturer_surname: str | None = None,
    ) -> list[ActiveSubject]:
        query = (ActiveSubjectsRepository.build_query()
                .filter_query(
                    subject_id=subject_id,
                    subject_name=subject_name,
                    lecturer_id=lecturer_id,
                    lecturer_name=lecturer_name,
                    lecturer_surname=lecturer_surname,
                    )
                 )
        return db.execute(query).unique().scalars().all()
