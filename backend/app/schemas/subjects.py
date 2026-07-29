from pydantic import BaseModel


class SubjectOut(BaseModel):
    subject_id: int
    subject_name: str
    lecturer_id: int
    lecturer_name: str
    lecturer_surname: str
    opinions_count: int
    opinions: list[str]


class SubjectsResponse(BaseModel):
    subjects: list[SubjectOut]
