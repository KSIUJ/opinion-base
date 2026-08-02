from pydantic import BaseModel

from app.schemas.small import LecturerRoleOut

class LecturerOutBasic(BaseModel):
    id: int
    name: str
    surname: str
    department_id: int
    role: LecturerRoleOut
    active_subjects: list[ActiveSubjectOutBasic]



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
    subjects: list[SubjectSummary]
    opinions: list[OpinionOut]
