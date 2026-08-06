import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import date, timedelta
from typing import Any

from dotenv import load_dotenv

from app.services.usos_api import get_usos_client

OUT_DIR = Path(__file__).resolve().parent
FACULTY = "UJ.WMI"
TERM_START = date(2026, 2, 16)
TERM_END = date(2026, 6, 30)
WORKERS = 12


def load_env() -> None:
    load_dotenv()


def fetch_staff(client: Any, fac_ids: str) -> list[dict]:
    staff: list[dict] = []
    start = 0
    while True:
        page = client.staff_index(fac_ids, start=start, num=100)
        staff.extend(page.get("users", []))
        if not page.get("next_page"):
            break
        start += 100
    return staff


def semester_weeks() -> list[str]:
    weeks: list[str] = []
    d = TERM_START
    while d <= TERM_END:
        weeks.append(d.isoformat())
        d += timedelta(days=7)
    return weeks


def fetch_staff_courses(client: Any, user_id: str) -> list[str]:
    course_ids: list[str] = []
    seen: set[str] = set()
    for start in semester_weeks():
        try:
            activities = client.staff_activities(user_id, start=start, days=7)
        except Exception:
            continue
        for act in activities:
            cid = act.get("course_id")
            if cid and cid not in seen:
                seen.add(cid)
                course_ids.append(cid)
    return course_ids


def fetch_courses(client: Any, course_ids: list[str], batch: int = 50) -> dict:
    courses: dict[str, Any] = {}
    for i in range(0, len(course_ids), batch):
        chunk = course_ids[i : i + batch]
        result = client.courses("|".join(chunk), fields="id|name")
        for cid, data in result.items():
            if data is not None:
                courses[cid] = data
    return courses


def main() -> None:
    load_env()
    client = get_usos_client()

    print(f"pracowanicy {FACULTY}...", flush=True)
    staff = fetch_staff(client, FACULTY)
    staff_file = OUT_DIR / "usos_staff.json"
    staff_file.write_text(
        json.dumps(staff, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"prowadzący (semestr {TERM_START}..{TERM_END})...", flush=True)
    staff_courses: dict[str, list[str]] = {}
    all_course_ids: list[str] = []
    seen: set[str] = set()
    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        future_to_user = {
            pool.submit(fetch_staff_courses, client, u["id"]): u for u in staff
        }
        for i, future in enumerate(as_completed(future_to_user), start=1):
            user = future_to_user[future]
            try:
                ids = future.result()
            except Exception as exc:
                print(f"  [{i}/{len(staff)}] {user.get('last_name')} ERROR: {exc}")
                ids = []
            staff_courses[user["id"]] = ids
            for cid in ids:
                if cid not in seen:
                    seen.add(cid)
                    all_course_ids.append(cid)
    staff_courses_file = OUT_DIR / "usos_staff_courses.json"
    staff_courses_file.write_text(
        json.dumps(staff_courses, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f" prowadzący->przedmioty -> {staff_courses_file.name}", flush=True)
    courses = fetch_courses(client, all_course_ids)
    courses_file = OUT_DIR / "usos_courses.json"
    courses_file.write_text(
        json.dumps(courses, ensure_ascii=False, indent=2), encoding="utf-8"
    )


if __name__ == "__main__":
    main()
