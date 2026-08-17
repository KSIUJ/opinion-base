from sqlalchemy.orm import Session

from app.models import Lecturer
from app.repositories.lecturers_repository import LecturersRepository
from app.schemas.lecturers import (
    LecturerListItem,
    LecturerListResponse,
    LecturerOut,
    OpinionOut,
    SubjectSummary,
)


class LecturersService:
    @staticmethod
    def list_lecturers(db: Session) -> LecturerListResponse:
        lecturers = LecturersRepository.list_lecturers(db)
        items = [
            LecturerListItem(
                id=lecturer.id,
                name=lecturer.name,
                surname=lecturer.surname,
                subject_count=len(lecturer.subjects),
            )
            for lecturer in lecturers
        ]
        return LecturerListResponse(lecturers=items)

    @staticmethod
    def search_lecturers(
        db: Session,
        surname: str | None = None,
        subject: str | None = None,
    ) -> LecturerListResponse:
        lecturers = LecturersRepository.search_lecturers(
            db, surname=surname, subject=subject
        )
        items = [
            LecturerListItem(
                id=lecturer.id,
                name=lecturer.name,
                surname=lecturer.surname,
                subject_count=len(
                    {
                        active.subject_id
                        for active in lecturer.active_subjects
                        if active.subject_id is not None
                    }
                ),
            )
            for lecturer in lecturers
        ]
        return LecturerListResponse(lecturers=items)

    @staticmethod
    def get_lecturer(db: Session, lecturer_id: int) -> LecturerOut | None:
        lecturer = LecturersRepository.get_lecturer(db, lecturer_id)
        if lecturer is None:
            return None

        subjects_list = []
        seen: set[int] = set()
        for active in lecturer.active_subjects:
            subject = active.subject
            if subject is None or subject.id in seen:
                continue
            seen.add(subject.id)
            subjects_list.append(
                SubjectSummary(
                    id=subject.id,
                    name=subject.name,
                    opinions_count=len(subject.opinion_relations),
                )
            )

        opinions_list = []
        for rel in lecturer.opinion_relations:
            opinion = rel.opinion
            if opinion is None:
                continue
            subject_rel = (
                opinion.subject_relations[0] if opinion.subject_relations else None
            )
            subject_name = (
                subject_rel.subject.name
                if subject_rel is not None and subject_rel.subject is not None
                else None
            )
            opinions_list.append(
                OpinionOut(
                    id=opinion.id,
                    subject_name=subject_name or "",
                    content=opinion.content or "",
                )
            )

        return LecturerOut(
            id=lecturer.id,
            name=lecturer.name,
            surname=lecturer.surname,
            subjects=subjects_list,
            opinions=opinions_list,
        )
