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


class LecturerRoleOut(BaseModel):
    id: int
    name: str


# Backward-compatible alias for older typoed imports.
LectrurerRoleOut = LecturerRoleOut
