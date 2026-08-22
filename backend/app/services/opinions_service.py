from dataclasses import dataclass
from enum import Enum
from typing import Type

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models import (
    Lecturer,
    LecturerOpinionRelation,
    Opinion,
    Subject,
    SubjectOpinionRelation,
)


class OpinionTarget(str, Enum):
    lecturer = "lecturer"
    subject = "subject"


class OpinionServiceError(Exception):
    def __init__(self, message: str, status_code: int = 400):
        super().__init__(message)
        self.status_code = status_code


@dataclass(frozen=True)
class TargetSpec:
    target_model: Type[Lecturer] | Type[Subject]
    relation_model: Type[LecturerOpinionRelation] | Type[SubjectOpinionRelation]
    relation_fk_field: str  # "lecturer_id" albo "subject_id"


TARGET_SPECS = {
    OpinionTarget.lecturer: TargetSpec(
        target_model=Lecturer,
        relation_model=LecturerOpinionRelation,
        relation_fk_field="lecturer_id",
    ),
    OpinionTarget.subject: TargetSpec(
        target_model=Subject,
        relation_model=SubjectOpinionRelation,
        relation_fk_field="subject_id",
    ),
}


class OpinionsService:
    @staticmethod
    def write_opinion(
        target_id: int,
        target_type: str,
        content: str,
        db: Session,
    ) -> None:
        try:
            normalized_target_type = OpinionTarget(target_type)
        except ValueError as exc:
            raise OpinionServiceError(
                f"Unsupported opinion target type: {target_type}",
                status_code=400,
            ) from exc

        spec = TARGET_SPECS[normalized_target_type]
        target = db.get(spec.target_model, target_id)
        if not target:
            raise OpinionServiceError(
                f"Target not found for type={normalized_target_type.value}, id={target_id}",
                status_code=404,
            )

        try:
            opinion = Opinion(content=content)
            db.add(opinion)
            db.flush()

            relation = spec.relation_model(opinion_id=opinion.id, time_id=1)
            setattr(relation, spec.relation_fk_field, target_id)
            db.add(relation)
            db.commit()

        except SQLAlchemyError as exc:
            db.rollback()
            raise OpinionServiceError(
                "Database operation failed while saving opinion",
                status_code=503,
            ) from exc
