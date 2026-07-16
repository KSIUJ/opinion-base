from sqlalchemy.orm import Session

from app.models import Subject
from app.repositories.subjects_repository import SubjectsRepository
from app.schemas.subjects import SubjectOut


class SubjectsService:
    @staticmethod
    def _serialize_subject(subject: Subject) -> SubjectOut:
        return SubjectOut(
            subject_id=subject.id,
            subject_name=subject.name,
            lecturer_id=subject.lecturer_rel.id,
            lecturer_name=subject.lecturer_rel.name,
            lecturer_surname=subject.lecturer_rel.surname,
            opinions_count=len(subject.opinions),
            opinions=[opinion.content for opinion in subject.opinions],
        )

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
