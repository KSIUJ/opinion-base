from sqlalchemy.orm import Session

from app.models import Subject
from app.repositories.subjects_repository import SubjectsRepository
from app.schemas.active_subjects import ActiveSubjectFromSubjectOut
from app.schemas.general import DepartmentOut, SemesterOut, LecturerRoleOut
from app.schemas.subjects import SubjectOut, SubjectOutBasic


class SubjectsService:
    @staticmethod
    def _serialize_subject(subject: Subject) -> SubjectOut:
        return SubjectOut(
            subject_id=subject.id,
            subject_name=subject.name,
            department=DepartmentOut(
                id=subject.department.id,
                name=subject.department.name,
            ) if subject.department else DepartmentOut(id=-1, name="Nieznany"),
            semester=SemesterOut(
                id=subject.semester.id,
                name=subject.semester.name,
                is_winter=subject.semester.is_winter,
            ) if subject.semester else SemesterOut(id=-1, name="Nieznany", is_winter=False),
            is_obligatory=subject.is_obligatory,
            opinions_count=len(subject.opinion_relations),

            opinions=[relation.opinion.content for relation in subject.opinion_relations if relation.opinion],
            groups_count=len(subject.group_relations),
            groups=[relation.subject_group.name for relation in subject.group_relations if relation.subject_group],

            lecturers_info=[ActiveSubjectFromSubjectOut(
                lecturer_name=activeSubject.lecturer.name,
                lecturer_surname=activeSubject.lecturer.surname,
                role=LecturerRoleOut(
                    id=activeSubject.role.id,
                    name=activeSubject.role.name,
                ) if activeSubject.role else LecturerRoleOut(id=-1, name="Nieznana"),
            ) for activeSubject in subject.active_subjects if activeSubject.lecturer],

        )

    @staticmethod
    def _serialize_subject_basic(subject: Subject) -> SubjectOutBasic:
        return SubjectOutBasic(
            subject_id=subject.id,
            subject_name=subject.name,
            department=DepartmentOut(
                id=subject.department.id,
                name=subject.department.name,
            ) if subject.department else DepartmentOut(id=-1, name="Nieznany"),
            semester=SemesterOut(
                id=subject.semester.id,
                name=subject.semester.name,
                is_winter=subject.semester.is_winter,
            ) if subject.semester else SemesterOut(id=-1, name="Nieznany", is_winter=False),
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
        semester_name: str | None = None,
        lecturer_id: int | None = None,
        lecturer_name: str | None = None,
        lecturer_surname: str | None = None,
        min_opinions: int | None = None,
        sort_by: str | None = None,
        order: str = "asc",
    ) -> list[SubjectOut]:

        subjects = SubjectsRepository.list_subjects(
            db=db,
            subject_id=subject_id,
            subject_name=subject_name,
            semester_name=semester_name,
            lecturer_id=lecturer_id,
            lecturer_name=lecturer_name,
            lecturer_surname=lecturer_surname,
            min_opinions=min_opinions,
            sort_by=sort_by,
            order=order,
        )

        return [SubjectsService._serialize_subject(subject) for subject in subjects]
