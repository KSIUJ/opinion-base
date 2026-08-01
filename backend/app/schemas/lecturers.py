from pydantic import BaseModel


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
