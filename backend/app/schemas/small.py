from pydantic import BaseModel


class DepartmentOut(BaseModel):
    id: int
    name: str

class TimeOut(BaseModel):
    id: int

class SemesterOut(BaseModel):
    id: int
    name: str
    is_winter: bool

class LectrurerRoleOut(BaseModel):
    id: int
    name: str
