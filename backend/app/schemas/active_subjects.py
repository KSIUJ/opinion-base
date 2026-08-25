from pydantic import BaseModel, Field

from app.schemas.small import LecturerRoleOut, TimeOut


class ActiveSubjectOutBasic(BaseModel):
    id: int
    lecturer_id: int
    role_id: int
    subject_id: int
    time_id: int


class ActiveSubjectOut(ActiveSubjectOutBasic):
    lecturer_name: str | None = None
    lecturer_surname: str | None = None
    role: LecturerRoleOut | None = None
    time: TimeOut | None = None
    opinions_count: int = 0
    opinions: list[str] = Field(default_factory=list)


class ActiveSubjectFromSubjectOut(BaseModel):
    lecturer_name: str | None = None
    lecturer_surname: str | None = None
    role: LecturerRoleOut


class ActiveSubjectsResponseBasic(BaseModel):
    subjects: list[ActiveSubjectOutBasic]


class ActiveSubjectsResponse(BaseModel):
    subjects: list[ActiveSubjectOut]
