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
    def get_lecturer(db: Session, lecturer_id: int) -> LecturerOut | None:
        lecturer = LecturersRepository.get_lecturer(db, lecturer_id)
        if lecturer is None:
            return None

        subjects_list = [
            SubjectSummary(
                id=subject.id,
                name=subject.name,
                opinions_count=len(subject.opinions),
            )
            for subject in lecturer.subjects
        ]

        opinions_list = [
            OpinionOut(
                id=opinion.id,
                subject_name=opinion.subject_rel.name,
                content=opinion.content,
            )
            for subject in lecturer.subjects
            for opinion in subject.opinions
        ]

        return LecturerOut(
            id=lecturer.id,
            name=lecturer.name,
            surname=lecturer.surname,
            subjects=subjects_list,
            opinions=opinions_list,
        )
