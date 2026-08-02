from pydantic import BaseModel

from app.schemas.active_subjects import ActiveSubjectOutBasic
from app.schemas.small import DepartmentOut, SemesterOut

class SubjectOutBasic(BaseModel):
    subject_id: int
    subject_name: str
    department_id: int
    semester_id: int
    is_obligatory: bool
    opinions_count: int

class SubjectsResponseBasic(BaseModel):
    subjects: list[SubjectOutBasic]

'TODO: zrobić to'
class SubjectOut(SubjectOutBasic):
    opinions: list[str]
    department: DepartmentOut
    semester: SemesterOut
    lecturers_info: list[LecturerOutBasic]
    groups_count: int
    groups: list[int]

class SubjectsResponse(BaseModel):
    subjects: list[SubjectOut]
