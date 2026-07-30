from sqlalchemy import Boolean, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


class Department(Base):
    __tablename__ = "department"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)

    lecturers: Mapped[list["Lecturer"]] = relationship(back_populates="department")
    subjects: Mapped[list["Subject"]] = relationship(back_populates="department")


class Semester(Base):
    __tablename__ = "semester"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    is_winter: Mapped[bool] = mapped_column(Boolean, nullable=False)

    subjects: Mapped[list["Subject"]] = relationship(back_populates="semester")


class LecturerRole(Base):
    __tablename__ = "lecturers_roles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)

    active_subjects: Mapped[list["ActiveSubject"]] = relationship(back_populates="role")


class Lecturer(Base):
    __tablename__ = "lecturers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str | None] = mapped_column(String, nullable=True)
    surname: Mapped[str] = mapped_column(String, nullable=False)
    department_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("department.id", ondelete="CASCADE"), nullable=True
    )

    department: Mapped["Department"] = relationship(back_populates="lecturers")
    active_subjects: Mapped[list["ActiveSubject"]] = relationship(back_populates="lecturer")
    opinion_relations: Mapped[list["LecturerOpinionRelation"]] = relationship(
        back_populates="lecturer"
    )


class Subject(Base):
    __tablename__ = "subjects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    department_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("department.id", ondelete="CASCADE"), nullable=True
    )
    semester_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("semester.id", ondelete="CASCADE"), nullable=True
    )
    is_obligatory: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    department: Mapped["Department"] = relationship(back_populates="subjects")
    semester: Mapped["Semester"] = relationship(back_populates="subjects")
    active_subjects: Mapped[list["ActiveSubject"]] = relationship(back_populates="subject")
    group_relations: Mapped[list["SubjectSubjectGroupRelation"]] = relationship(
        back_populates="subject"
    )
    opinion_relations: Mapped[list["SubjectOpinionRelation"]] = relationship(
        back_populates="subject"
    )


class SubjectGroup(Base):
    __tablename__ = "subject_groups"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)

    subject_relations: Mapped[list["SubjectSubjectGroupRelation"]] = relationship(
        back_populates="subject_group"
    )


class SubjectSubjectGroupRelation(Base):
    __tablename__ = "subject_subject_group_relation"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_subject: Mapped[int | None] = mapped_column(Integer, ForeignKey("subjects.id"))
    id_subject_group: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("subject_groups.id")
    )

    subject: Mapped["Subject"] = relationship(back_populates="group_relations")
    subject_group: Mapped["SubjectGroup"] = relationship(back_populates="subject_relations")


class Time(Base):
    __tablename__ = "time"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    active_subjects: Mapped[list["ActiveSubject"]] = relationship(back_populates="time")
    subject_opinion_relations: Mapped[list["SubjectOpinionRelation"]] = relationship(
        back_populates="time"
    )
    lecturer_opinion_relations: Mapped[list["LecturerOpinionRelation"]] = relationship(
        back_populates="time"
    )


class ActiveSubject(Base):
    __tablename__ = "active_subjects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    lecturer_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("lecturers.id"))
    role_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("lecturers_roles.id"))
    subject_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("subjects.id"))
    time_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("time.id"))

    lecturer: Mapped["Lecturer"] = relationship(back_populates="active_subjects")
    role: Mapped["LecturerRole"] = relationship(back_populates="active_subjects")
    subject: Mapped["Subject"] = relationship(back_populates="active_subjects")
    time: Mapped["Time"] = relationship(back_populates="active_subjects")


class Opinion(Base):
    __tablename__ = "opinions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    content: Mapped[str | None] = mapped_column(String, default="[empty opinion]")

    subject_relations: Mapped[list["SubjectOpinionRelation"]] = relationship(
        back_populates="opinion"
    )
    lecturer_relations: Mapped[list["LecturerOpinionRelation"]] = relationship(
        back_populates="opinion"
    )


class SubjectOpinionRelation(Base):
    __tablename__ = "subjects_opinion_relation"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    subject_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("subjects.id"))
    opinion_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("opinions.id"))
    time_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("time.id"))

    subject: Mapped["Subject"] = relationship(back_populates="opinion_relations")
    opinion: Mapped["Opinion"] = relationship(back_populates="subject_relations")
    time: Mapped["Time"] = relationship(back_populates="subject_opinion_relations")


class LecturerOpinionRelation(Base):
    __tablename__ = "lecturers_opinion_relation"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    lecturer_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("lecturers.id"))
    opinion_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("opinions.id"))
    time_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("time.id"))

    lecturer: Mapped["Lecturer"] = relationship(back_populates="opinion_relations")
    opinion: Mapped["Opinion"] = relationship(back_populates="lecturer_relations")
    time: Mapped["Time"] = relationship(back_populates="lecturer_opinion_relations")
