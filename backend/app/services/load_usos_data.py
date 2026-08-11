import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import json

from dotenv import load_dotenv

from app.db import SessionLocal
from app.models import ActiveSubject, Lecturer, Subject

OUT_DIR = Path(__file__).resolve().parent
STAFF_FILE = OUT_DIR / "usos_staff.json"
STAFF_COURSES_FILE = OUT_DIR / "usos_staff_courses.json"
COURSES_FILE = OUT_DIR / "usos_courses.json"


def load_json(path: Path) -> list | dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def course_name(data: dict) -> str:
    name = data.get("name") or {}
    return name.get("pl") or name.get("en") or data.get("id") or "[unknown]"


def main() -> None:
    load_dotenv()

    staff = load_json(STAFF_FILE)
    staff_courses = load_json(STAFF_COURSES_FILE)
    courses = load_json(COURSES_FILE)

    db = SessionLocal()
    try:
        lecturer_ids: dict[str, int] = {}
        for person in staff:
            lecturer = Lecturer(
                name=person.get("first_name"),
                surname=person.get("last_name") or "[unknown]",
                department_id=None,
            )
            db.add(lecturer)
            db.flush()
            lecturer_ids[person["id"]] = lecturer.id

        subject_ids: dict[str, int] = {}
        for course_id, data in courses.items():
            subject = Subject(
                name=course_name(data),
                department_id=None,
                semester_id=None,
                is_obligatory=True,
            )
            db.add(subject)
            db.flush()
            subject_ids[course_id] = subject.id

        skipped = 0
        for usos_id, course_list in staff_courses.items():
            lecturer_id = lecturer_ids.get(usos_id)
            if lecturer_id is None:
                skipped += 1
                continue
            for course_id in course_list:
                subject_id = subject_ids.get(course_id)
                if subject_id is None:
                    continue
                db.add(
                    ActiveSubject(
                        lecturer_id=lecturer_id,
                        role_id=None,
                        subject_id=subject_id,
                        time_id=None,
                    )
                )

        db.commit()
        print(
            f"loaded lecturers={len(lecturer_ids)} subjects={len(subject_ids)} "
            f"active_subjects={len(staff_courses)} mappings "
            f"(skipped {skipped} staff not found)"
        )
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
