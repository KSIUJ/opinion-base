from sqlalchemy import Select, select
from sqlalchemy.orm import Session, selectinload

from app.models import Lecturer, Subject


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
                     joininload(Subject.department),
                     joininload(Subject.semester),
                     selectinload(Subject.active_subjects),
                     selectinload(Subject.group_relations),
                     selectinload(Subject.opinion_relations),
                 )
                )
                 


    @staticmethod
    def filter_query(
        subject_id: int | None = None,
        subject_name: str | None = None,
        lecturer_id: int | None = None,
        lecturer_name: str | None = None,
        lecturer_surname: str | None = None,
        query: Select
    ) -> Select:

        if subject_id is not None:
            query = query.where(Subject.id == subject_id)
        if subject_name:
            query = query.where(Subject.name.ilike(f"%{subject_name}%"))
        if lecturer_id is not None:
            query = query.where(Subject.lecturer == lecturer_id)

        if lecturer_name or lecturer_surname:
            query = query.join(Subject.lecturer_rel)
            if lecturer_name:
                query = query.where(Lecturer.name.ilike(f"%{lecturer_name}%"))
            if lecturer_surname:
                query = query.where(Lecturer.surname.ilike(f"%{lecturer_surname}%"))

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
