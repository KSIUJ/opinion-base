from types import SimpleNamespace

import pytest
from fastapi import HTTPException

from app.repositories.lecturers_repository import LecturersRepository
from app.routes import lecturers as lecturers_route
from app.services.lecturers_service import LecturersService


def make_lecturer(**overrides):
    values = {
        "id": 1,
        "name": "Piotr",
        "surname": "Micek",
        "active_subjects": [],
        "opinion_relations": [],
    }
    values.update(overrides)
    return SimpleNamespace(**values)


def make_active_subject(subject_id, subject=None):
    return SimpleNamespace(subject_id=subject_id, subject=subject)


def test_list_lecturers_counts_distinct_subjects(monkeypatch):
    lecturer = make_lecturer(
        active_subjects=[
            make_active_subject(10),
            make_active_subject(10),
            make_active_subject(None),
            make_active_subject(11),
        ]
    )
    monkeypatch.setattr(LecturersRepository, "list_lecturers", lambda db: [lecturer])

    result = LecturersService.list_lecturers(db=object())

    assert result.lecturers[0].id == 1
    assert result.lecturers[0].subject_count == 2


def test_search_lecturers_forwards_filters(monkeypatch):
    calls = {}

    def fake_search(
        db,
        name=None,
        surname=None,
        subject=None,
        department=None,
        sort_by=None,
        order="asc",
    ):
        calls.update(
            db=db,
            name=name,
            surname=surname,
            subject=subject,
            department=department,
            sort_by=sort_by,
            order=order,
        )
        return []

    monkeypatch.setattr(LecturersRepository, "search_lecturers", fake_search)
    db = object()

    result = LecturersService.search_lecturers(db, surname="Micek", subject="Propabil")

    assert result.lecturers == []
    assert calls == {
        "db": db,
        "name": None,
        "surname": "Micek",
        "subject": "Propabil",
        "department": None,
        "sort_by": None,
        "order": "asc",
    }


def test_get_lecturer_returns_unique_subjects_and_opinions(monkeypatch):
    subject = SimpleNamespace(
        id=10,
        name="Programming",
        opinion_relations=[object(), object()],
    )
    opinion = SimpleNamespace(
        id=20,
        content="Good subject",
        subject_relations=[SimpleNamespace(subject=subject)],
    )
    lecturer = make_lecturer(
        active_subjects=[
            make_active_subject(10, subject),
            make_active_subject(10, subject),
        ],
        opinion_relations=[SimpleNamespace(opinion=opinion)],
    )
    monkeypatch.setattr(
        LecturersRepository,
        "get_lecturer",
        lambda db, lecturer_id: lecturer if lecturer_id == 1 else None,
    )

    result = LecturersService.get_lecturer(db=object(), lecturer_id=1)

    assert result.id == 1
    assert len(result.subjects) == 1
    assert result.subjects[0].opinions_count == 2
    assert result.opinions[0].subject_name == "Programming"
    assert result.opinions[0].content == "Good subject"


def test_get_lecturer_returns_none_for_unknown_id(monkeypatch):
    monkeypatch.setattr(LecturersRepository, "get_lecturer", lambda db, lecturer_id: None)

    assert LecturersService.get_lecturer(db=object(), lecturer_id=999) is None


def test_get_lecturer_route_returns_service_result(monkeypatch):
    expected = SimpleNamespace(id=1)
    monkeypatch.setattr(
        lecturers_route.LecturersService,
        "get_lecturer",
        lambda db, lecturer_id: expected,
    )

    assert lecturers_route.get_lecturer(1, object()) is expected


def test_get_lecturer_route_returns_404_for_unknown_id(monkeypatch):
    monkeypatch.setattr(
        lecturers_route.LecturersService,
        "get_lecturer",
        lambda db, lecturer_id: None,
    )

    with pytest.raises(HTTPException) as error:
        lecturers_route.get_lecturer(999, object())

    assert error.value.status_code == 404
