from typing import Any

from backend.db import reports


def save_interview(interview_data: dict[str, Any]) -> str:
    result = reports.insert_one(interview_data)
    return str(result.inserted_id)


def get_interview(interview_id: str) -> dict[str, Any] | None:
    from bson import ObjectId

    try:
        document = reports.find_one({"_id": ObjectId(interview_id)})
    except Exception:
        return None

    if document is None:
        return None

    document["_id"] = str(document["_id"])
    return document
