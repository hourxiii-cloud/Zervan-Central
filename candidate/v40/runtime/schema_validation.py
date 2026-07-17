"""Dependency-free validation for the closed JSON Schema subset used by v40."""

from __future__ import annotations

import json
import re
from datetime import datetime
from typing import Any


class SchemaValidationError(ValueError):
    """A candidate record failed its declared closed schema."""


def _schema_type_matches(value: Any, expected: str) -> bool:
    if expected == "null":
        return value is None
    if expected == "boolean":
        return isinstance(value, bool)
    if expected == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if expected == "string":
        return isinstance(value, str)
    if expected == "array":
        return isinstance(value, list)
    if expected == "object":
        return isinstance(value, dict)
    raise SchemaValidationError(f"unsupported schema type: {expected}")


def _resolve_local_ref(root_schema: dict[str, Any], ref: str) -> dict[str, Any]:
    if not ref.startswith("#/"):
        raise SchemaValidationError(f"unsupported non-local reference: {ref}")
    value: Any = root_schema
    for raw_part in ref[2:].split("/"):
        part = raw_part.replace("~1", "/").replace("~0", "~")
        try:
            value = value[part]
        except (KeyError, TypeError) as exc:
            raise SchemaValidationError(f"unresolved schema reference: {ref}") from exc
    if not isinstance(value, dict):
        raise SchemaValidationError(f"schema reference is not an object: {ref}")
    return value


def _is_date_time(value: str) -> bool:
    candidate = value[:-1] + "+00:00" if value.endswith("Z") else value
    try:
        parsed = datetime.fromisoformat(candidate)
    except ValueError:
        return False
    return "T" in value and parsed.tzinfo is not None


def validate_schema(
    instance: Any,
    schema: dict[str, Any],
    *,
    root_schema: dict[str, Any] | None = None,
    path: str = "$",
) -> None:
    """Validate one value against the dependency-free schema subset."""

    root = root_schema or schema

    if "$ref" in schema:
        validate_schema(instance, _resolve_local_ref(root, schema["$ref"]), root_schema=root, path=path)
        return

    for branch in schema.get("allOf", []):
        validate_schema(instance, branch, root_schema=root, path=path)

    if "anyOf" in schema:
        for branch in schema["anyOf"]:
            try:
                validate_schema(instance, branch, root_schema=root, path=path)
            except SchemaValidationError:
                continue
            break
        else:
            raise SchemaValidationError(f"{path}: no anyOf branch matched")

    if "if" in schema:
        try:
            validate_schema(instance, schema["if"], root_schema=root, path=path)
        except SchemaValidationError:
            branch = schema.get("else")
        else:
            branch = schema.get("then")
        if branch is not None:
            validate_schema(instance, branch, root_schema=root, path=path)

    expected_types = schema.get("type")
    if expected_types is not None:
        if isinstance(expected_types, str):
            expected_types = [expected_types]
        if not any(_schema_type_matches(instance, expected) for expected in expected_types):
            raise SchemaValidationError(f"{path}: expected type {expected_types}")

    if "const" in schema and instance != schema["const"]:
        raise SchemaValidationError(f"{path}: value does not match const")
    if "enum" in schema and instance not in schema["enum"]:
        raise SchemaValidationError(f"{path}: value is not in enum")

    if isinstance(instance, str):
        if len(instance) < schema.get("minLength", 0):
            raise SchemaValidationError(f"{path}: string is too short")
        if "pattern" in schema and re.fullmatch(schema["pattern"], instance) is None:
            raise SchemaValidationError(f"{path}: string does not match pattern")
        if schema.get("format") == "date-time" and not _is_date_time(instance):
            raise SchemaValidationError(f"{path}: invalid date-time")

    if isinstance(instance, (int, float)) and not isinstance(instance, bool):
        if "minimum" in schema and instance < schema["minimum"]:
            raise SchemaValidationError(f"{path}: value is below minimum")

    if isinstance(instance, list):
        if len(instance) < schema.get("minItems", 0):
            raise SchemaValidationError(f"{path}: array has fewer than minItems")
        if "maxItems" in schema and len(instance) > schema["maxItems"]:
            raise SchemaValidationError(f"{path}: array has more than maxItems")
        if schema.get("uniqueItems"):
            canonical_items = [json.dumps(item, sort_keys=True, separators=(",", ":")) for item in instance]
            if len(canonical_items) != len(set(canonical_items)):
                raise SchemaValidationError(f"{path}: array items are not unique")
        if "items" in schema:
            for index, item in enumerate(instance):
                validate_schema(item, schema["items"], root_schema=root, path=f"{path}[{index}]")

    if isinstance(instance, dict):
        missing = [name for name in schema.get("required", []) if name not in instance]
        if missing:
            raise SchemaValidationError(f"{path}: missing required properties {missing}")
        properties = schema.get("properties", {})
        if schema.get("additionalProperties") is False:
            extras = sorted(set(instance) - set(properties))
            if extras:
                raise SchemaValidationError(f"{path}: unexpected properties {extras}")
        for name, child_schema in properties.items():
            if name in instance:
                validate_schema(instance[name], child_schema, root_schema=root, path=f"{path}.{name}")
