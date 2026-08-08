from sqlalchemy import Select, and_, func, select
from sqlalchemy.orm import Session, joinedload, selectinload

from app.models import ActiveSubject, Lecturer, Subject, SubjectOpinionRelation, SubjectSubjectGroupRelation


class SubjectsRepository:
    @staticmethod
    def build_query_basic() -> Select:
        query = (select(Subject)
                 .options(
                        joinedload(Subject.department),
                        joinedload(Subject.semester),
                        selectinload(Subject.opinion_relations),
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
                     selectinload(Subject.active_subjects).options(
                        joinedload(ActiveSubject.lecturer),
                        joinedload(ActiveSubject.role),        
                     ),
                     selectinload(Subject.group_relations).
                     joinedload(SubjectSubjectGroupRelation.subject_group),
                     selectinload(Subject.opinion_relations).
                     joinedload(SubjectOpinionRelation.opinion),
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
        min_opinions: int | None = None,
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

        if min_opinions is not None:
            opinions_count_subquery = (
                select(func.count(SubjectOpinionRelation.id))
                .where(SubjectOpinionRelation.subject_id == Subject.id)
                .scalar_subquery()
            )
            query = query.where(opinions_count_subquery >= min_opinions)

        return query

        
    @staticmethod
    def list_subjects(
        db: Session,
        subject_id: int | None = None,
        subject_name: str | None = None,
        lecturer_id: int | None = None,
        lecturer_name: str | None = None,
        lecturer_surname: str | None = None,
        min_opinions: int | None = None,
    ) -> list[Subject]:
        query = SubjectsRepository.filter_query(
                    subject_id=subject_id,
                    subject_name=subject_name,
                    lecturer_id=lecturer_id,
                    lecturer_name=lecturer_name,
                    lecturer_surname=lecturer_surname,
                    min_opinions=min_opinions,
                    query=SubjectsRepository.build_query()
                    )
                 
        return db.execute(query).unique().scalars().all()
