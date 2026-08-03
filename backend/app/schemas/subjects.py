from pydantic import BaseModel, Field

from app.schemas.active_subjects import ActiveSubjectOut, ActiveSubjectOutBasic
from app.schemas.small import DepartmentOut, SemesterOut


class SubjectOutBasic(BaseModel):
    subject_id: int
    subject_name: str
    department_id: int | None = None
    semester_id: int | None = None
    is_obligatory: bool
    opinions_count: int


class SubjectsResponseBasic(BaseModel):
    subjects: list[SubjectOutBasic]


class SubjectOut(SubjectOutBasic):
    opinions: list[str] = Field(default_factory=list)
    department: DepartmentOut | None = None
    semester: SemesterOut | None = None
    lecturers_info: list[ActiveSubjectOutBasic] = Field(default_factory=list)
    groups_count: int = 0
    groups: list[int] = Field(default_factory=list)


class SubjectsResponse(BaseModel):
    subjects: list[SubjectOut]
