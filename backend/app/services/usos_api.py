import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from requests_oauthlib import OAuth1Session

from app.config import get_usos_client as get_usos_client_config


USOS_BASE = "https://apps.usos.uj.edu.pl"


class UsosApiClient:
    def __init__(self, consumer_key: str, consumer_secret: str) -> None:
        self._session = OAuth1Session(
            client_key=consumer_key,
            client_secret=consumer_secret,
        )

    def _get(self, method: str, **params: Any) -> Any:
        url = f"{USOS_BASE}/services/{method}"
        response = self._session.get(
            url,
            params={"format": "json", **params},
            timeout=30,
        )
        response.raise_for_status()
        return response.json()

    def installation(self) -> dict:
        return self._get("apisrv/installation")

    def resolve_facpattern(self, facpattern: str) -> list[str]:
        return self._get("fac/resolve_facpattern", facpattern=facpattern)

    def faculties(self, fac_ids: str, fields: str = "id|name") -> dict:
        return self._get("fac/faculties", fac_ids=fac_ids, fields=fields)

    def staff_index(self, fac_ids: str, start: int = 0, num: int = 100) -> dict:
        return self._get(
            "users/staff_index",
            fac_ids=fac_ids,
            teachers_only="true",
            start=start,
            num=num,
            fields="users[id|first_name|last_name]|next_page|total",
        )

    def staff_activities(
        self,
        user_id: str,
        start: str | None = None,
        days: int = 7,
        fields: str = "course_id|course_name|unit_id",
    ) -> list:
        params: dict[str, Any] = {"user_id": user_id, "days": days, "fields": fields}
        if start is not None:
            params["start"] = start
        return self._get("tt/staff", **params)

    def courses(self, course_ids: str, fields: str = "id|name") -> dict:
        return self._get("courses/courses", course_ids=course_ids, fields=fields)


def get_usos_client() -> UsosApiClient:
    config = get_usos_client_config()
    return UsosApiClient(
        consumer_key=config.usos_consumer_key,
        consumer_secret=config.usos_consumer_secret,
    )
