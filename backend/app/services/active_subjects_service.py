from sqlalchemy.orm import Session

from app.models import ActiveSubject
from app.repositories.subjects_repository import ActiveSubjectsRepository
from app.schemas.subjects import ActiveSubjectOut
from app.schemas.subjects import ActiveSubjectOutBasic


class ActiveSubjectsService:
    @staticmethod
    def _serialize_subject_basic(subject: ActiveSubject) -> ActiveSubjectOutBasic:
        return ActiveSubjectOutBasic(
            id=subject.id,
            lecturer_id=subject.lecturer_id,
            role_id=subject.role_id,
            subject_id=subject.subject_id,
            time_id=subject.time_id

            subject_name=subject.subject.name,
            lecturer_id=subject.lecturer.id,
            opinions_count=len(subject.subject.opinions),
            opinions=[opinion.content for opinion in subject.subject.opinions],
        )

    @staticmethod
    def _serialize_subject_basic(subject: ActiveSubject) -> ActiveSubjectOutBasic:
        return ActiveSubjectOut(
            subject_id=subject.id,
            subject_name=subject.name,
        )

    @staticmethod
    def list_subjects_all(db: Session) -> list[ActiveSubjectOutBasic]:
        subjects = ActiveSubjectsRepository.list_subjects_all(db=db)
        return [ActiveSubjectsService._serialize_subject_basic(subject) for subject in subjects]

    @staticmethod
    def list_subjects(
        db: Session,
        subject_id: int | None = None,
        subject_name: str | None = None,
        lecturer_id: int | None = None,
        lecturer_name: str | None = None,
        lecturer_surname: str | None = None,
        min_opinions: int | None = None,
    ) -> list[ActiveSubjectOut]:

        subjects = ActiveSubjectsRepository.list_subjects(
            db=db,
            subject_id=subject_id,
            subject_name=subject_name,
            lecturer_id=lecturer_id,
            lecturer_name=lecturer_name,
            lecturer_surname=lecturer_surname,
        )

        response = [ActiveSubjectsService._serialize_subject(subject) for subject in subjects]
        if min_opinions is not None:
            response = [
                subject for subject in response if subject.opinions_count >= min_opinions
            ]
        return response
