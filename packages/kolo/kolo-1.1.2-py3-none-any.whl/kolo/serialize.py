import json
from contextlib import contextmanager
from typing import Dict

from django.db.models import QuerySet


@contextmanager
def monkeypatch_queryset_repr():
    old_repr = QuerySet.__repr__

    def new_repr(queryset):
        if queryset._result_cache is None:
            return f"Unevaluated queryset for: {queryset.model}"
        return old_repr(queryset)

    QuerySet.__repr__ = new_repr  # type: ignore
    try:
        yield
    finally:
        QuerySet.__repr__ = old_repr  # type: ignore


def _serialize_local(local: object) -> object:
    try:
        json.dumps(local)
    except (TypeError, OverflowError, ValueError):
        try:
            return str(local)
        except Exception:
            return "SerializationError"
    return local


def serialize_locals(locals: Dict[str, object]) -> str:
    serialized_locals = {key: _serialize_local(value) for key, value in locals.items()}
    return json.dumps(serialized_locals, indent=2)


def serialize_potential_json(arg: object) -> str:
    if arg is None:
        return str(arg)

    try:
        return json.dumps(arg)
    except (TypeError, OverflowError, ValueError):
        return str(arg)
