from types import SimpleNamespace

from app.repositories.subjects_repository import SubjectsRepository
from app.routes import subjects as subjects_route
from app.services.subjects_service import SubjectsService


def make_subject(**overrides):
    values = {
        "id": 1,
        "name": "Test subject",
        "department": None,
        "semester": None,
        "is_obligatory": True,
        "opinion_relations": [],
        "active_subjects": [],
        "group_relations": [],
    }
    values.update(overrides)
    return SimpleNamespace(**values)


def test_subject_serializer_allows_missing_department_and_semester():
    result = SubjectsService._serialize_subject(make_subject())

    assert result.subject_id == 1
    assert result.subject_name == "Test subject"
    assert result.department is None
    assert result.semester is None
    assert result.opinions == []
    assert result.lecturers_info == []


def test_search_subjects_passes_only_supported_search_parameters(monkeypatch):
    calls = {}
    db = object()

    def fake_list_subjects(**kwargs):
        calls.update(kwargs)
        return []

    monkeypatch.setattr(subjects_route.SubjectsService, "list_subjects", fake_list_subjects)

    response = subjects_route.search_subjects(
        name="Programming",
        semester_name="3",
        lecturer_surname="Smith",
        db=db,
    )

    assert response.subjects == []
    assert calls == {
        "db": db,
        "subject_name": "Programming",
        "semester_name": "3",
        "lecturer_id": None,
        "lecturer_name": None,
        "lecturer_surname": "Smith",
        "min_opinions": None,
        "sort_by": None,
        "order": "asc",
    }


def test_subject_detail_passes_subject_id_to_service(monkeypatch):
    calls = {}
    db = object()

    def fake_list_subjects(**kwargs):
        calls.update(kwargs)
        return []

    monkeypatch.setattr(subjects_route.SubjectsService, "list_subjects", fake_list_subjects)

    response = subjects_route.display_info(subject_id=42, db=db)

    assert response.subjects == []
    assert calls == {"db": db, "subject_id": 42}


def test_subject_service_forwards_search_filters(monkeypatch):
    calls = {}
    db = object()

    def fake_list_subjects(**kwargs):
        calls.update(kwargs)
        return []

    monkeypatch.setattr(SubjectsRepository, "list_subjects", fake_list_subjects)

    result = SubjectsService.list_subjects(
        db=db,
        subject_name="Programming",
        semester_name="3",
        lecturer_surname="Smith",
    )

    assert result == []
    assert calls == {
        "db": db,
        "subject_id": None,
        "subject_name": "Programming",
        "semester_name": "3",
        "lecturer_id": None,
        "lecturer_name": None,
        "lecturer_surname": "Smith",
        "min_opinions": None,
        "sort_by": None,
        "order": "asc",
    }
