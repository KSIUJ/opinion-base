from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


class Lecturer(Base):
    __tablename__ = "lecturers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    surname: Mapped[str] = mapped_column(String)

    subjects: Mapped[list["Subject"]] = relationship(back_populates="lecturer_rel")


class Subject(Base):
    __tablename__ = "subjects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    lecturer: Mapped[int] = mapped_column(
        Integer, ForeignKey("lecturers.id", ondelete="CASCADE")
    )

    lecturer_rel: Mapped["Lecturer"] = relationship(back_populates="subjects")
    opinions: Mapped[list["Opinion"]] = relationship(back_populates="subject_rel")


class Opinion(Base):
    __tablename__ = "opinions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    subject: Mapped[int] = mapped_column(
        Integer, ForeignKey("subjects.id", ondelete="CASCADE")
    )
    content: Mapped[str] = mapped_column(String)

    subject_rel: Mapped["Subject"] = relationship(back_populates="opinions")

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    name: Mapped[str] = mapped_column(String)
    surname: Mapped[str] = mapped_column(String)

    subjects: Mapped[list["Subject"]] = relationship(back_populates="lecturer_rel")
