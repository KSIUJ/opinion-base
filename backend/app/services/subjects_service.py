from sqlalchemy.orm import Session

from app.models import Subject
from app.repositories.subjects_repository import SubjectsRepository
from app.schemas.subjects import SubjectOut, SubjectOutBasic
from app.schemas.small import DepartmentOut, SemesterOut


class SubjectsService:
    'TODO: add lecturers'
    @staticmethod
    def _serialize_subject(subject: Subject) -> SubjectOut:
        return SubjectOut(
            subject_id=subject.id,
            subject_name=subject.name,
            department=DepartmentOut(
                id=subject.department.id,
                name=subject.department.name,
                ),
            semester=SemesterOut(
                id=subject.semester.id,
                name=subject.semester.name,
                is_winter=subject.semester.is_winter,
                ),
            is_obligatory=subject.is_obligatory,
            opinions_count=len(subject.opinion_relations),

            opinions=[relation.opinion.content for relation in subject.opinion_relations],
            groups_count=len(subject.group_relations),
            groups=[relation.subject_group.name for relation in subject.group_relations],

        )

    @staticmethod
    def _serialize_subject_basic(subject: Subject) -> SubjectOutBasic:
        return SubjectOutBasic(
            subject_id=subject.id,
            subject_name=subject.name,
            department=DepartmentOut(
                id=subject.department.id,
                name=subject.department.name,
                ),
            semester=SemesterOut(
                id=subject.semester.id,
                name=subject.semester.name,
                is_winter=subject.semester.is_winter,
                ),
            is_obligatory=subject.is_obligatory,
            opinions_count=len(subject.opinion_relations),
        )

    @staticmethod
    def list_subjects_all(db: Session) -> list[SubjectOutBasic]:
        subjects = SubjectsRepository.list_subjects_all(db=db)
        return [SubjectsService._serialize_subject_basic(subject) for subject in subjects]

    @staticmethod
    def list_subjects(
        db: Session,
        subject_id: int | None = None,
        subject_name: str | None = None,
        lecturer_id: int | None = None,
        lecturer_name: str | None = None,
        lecturer_surname: str | None = None,
        min_opinions: int | None = None,
    ) -> list[SubjectOut]:

        subjects = SubjectsRepository.list_subjects(
            db=db,
            subject_id=subject_id,
            subject_name=subject_name,
            lecturer_id=lecturer_id,
            lecturer_name=lecturer_name,
            lecturer_surname=lecturer_surname,
        )

        response = [SubjectsService._serialize_subject(subject) for subject in subjects]
        if min_opinions is not None:
            response = [
                subject for subject in response if subject.opinions_count >= min_opinions
            ]
        return response
