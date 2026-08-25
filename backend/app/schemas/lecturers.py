from pydantic import BaseModel, Field

from app.schemas.active_subjects import ActiveSubjectOutBasic
from app.schemas.general import DepartmentOut, LecturerRoleOut


class LecturerOutBasic(BaseModel):
    id: int
    name: str
    surname: str
    department_id: int | None = None
    department: DepartmentOut | None = None
    role: LecturerRoleOut | None = None
    active_subjects: list[ActiveSubjectOutBasic] = Field(default_factory=list)



class LecturerListItem(BaseModel):
    id: int
    name: str
    surname: str
    subject_count: int


class LecturerListResponse(BaseModel):
    lecturers: list[LecturerListItem]


class SubjectSummary(BaseModel):
    id: int
    name: str
    opinions_count: int


class OpinionOut(BaseModel):
    id: int
    subject_name: str
    content: str


class LecturerOut(BaseModel):
    id: int
    name: str
    surname: str
    subjects: list[SubjectSummary] = Field(default_factory=list)
    opinions: list[OpinionOut] = Field(default_factory=list)
