from sqlalchemy import Select, and_, select
from sqlalchemy.orm import Session, joinedload, selectinload

from app.models import ActiveSubject, Lecturer, Subject


class SubjectsRepository:
    @staticmethod
    def build_query_basic() -> Select:
        query = (select(Subject)
                 .options(
                        selectinload(Subject.active_subjects),
                     )
                 )
        return query

    @staticmethod
    def list_subjects_all(
            db: Session
            ) -> list[Subject]:
        query = SubjectsRepository.build_query_basic()
        return db.execute(query).unique().scalars().all()


    @staticmethod
    def build_query() -> Select:
        query = (select(Subject)
                 .options(
                     joinedload(Subject.department),
                     joinedload(Subject.semester),
                     selectinload(Subject.active_subjects),
                     selectinload(Subject.group_relations),
                     selectinload(Subject.opinion_relations),
                 )
                )
        return query


    @staticmethod
    def filter_query(
        query: Select,
        subject_id: int | None = None,
        subject_name: str | None = None,
        lecturer_id: int | None = None,
        lecturer_name: str | None = None,
        lecturer_surname: str | None = None,
    ) -> Select:

        if subject_id is not None:
            query = query.where(Subject.id == subject_id)
        if subject_name:
            query = query.where(Subject.name.ilike(f"%{subject_name}%"))
        if lecturer_id is not None:
            query = query.where(
                Subject.active_subjects.any(ActiveSubject.lecturer_id == lecturer_id)
            )

        if lecturer_name or lecturer_surname:
            lecturer_filters = []
            if lecturer_name:
                lecturer_filters.append(Lecturer.name.ilike(f"%{lecturer_name}%"))
            if lecturer_surname:
                lecturer_filters.append(Lecturer.surname.ilike(f"%{lecturer_surname}%"))
            query = query.where(
                Subject.active_subjects.any(
                    ActiveSubject.lecturer.has(and_(*lecturer_filters))
                )
            )

        return query

        
    @staticmethod
    def list_subjects(
        db: Session,
        subject_id: int | None = None,
        subject_name: str | None = None,
        lecturer_id: int | None = None,
        lecturer_name: str | None = None,
        lecturer_surname: str | None = None,
    ) -> list[Subject]:
        query = SubjectsRepository.filter_query(
                    subject_id=subject_id,
                    subject_name=subject_name,
                    lecturer_id=lecturer_id,
                    lecturer_name=lecturer_name,
                    lecturer_surname=lecturer_surname,
                    query=SubjectsRepository.build_query()
                    )
                 
        return db.execute(query).unique().scalars().all()
