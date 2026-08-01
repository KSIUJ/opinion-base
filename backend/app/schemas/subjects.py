from pydantic import BaseModel


class SubjectOutBasic(BaseModel):
    subject_id: int
    subject_name: str
    department_id: int
    semester_id: int
    is_obligatory: bool
    opinions_count: int

class SubjectsResponseBasic(BaseModel):
    subjects: list[SubjectOutBasic]

'TODO: zrobić to dobrze'
class SubjectOut(SubjectOutBasic):
    opinions: list[str]

class SubjectsResponse(BaseModel):
    
    subjects: list[SubjectOut]
