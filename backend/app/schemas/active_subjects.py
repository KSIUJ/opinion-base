from pydantic import BaseModel

from app.schemas.subjects import SubjectOutBasic

class ActiveSubjectOutBasic(SubjectOutBasic):
    id: int
    lecturer_id: int
    role_id: int
    subject_id: int
    time_id: int


