#!/usr/bin/env python3

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
import hashlib
import json
from typing import Any, Iterable, Mapping, Sequence


CLEAN = "CLEAN"
COLLISION = "COLLISION"
UNRESOLVED_CONTEXT = "UNRESOLVED_CONTEXT"

AUTHORITY_STATE = "NONE"
HUMAN_GATE_STATE = "ACTIVE"


@dataclass(frozen=True)
class CollisionGroup:
    collision_group_id: str
    measurable_body_sha512: str
    member_count: int
    distinct_labels: tuple[str, ...]
    member_references: tuple[str, ...]
    feature_identity_surface: tuple[str, ...]


@dataclass(frozen=True)
class CollisionBoundaryResult:
    total_source_rows: int
    clean_rows: int
    collision_rows: int
    unresolved_context_rows: int
    collision_groups: tuple[CollisionGroup, ...]
    row_dispositions: tuple[dict[str, Any], ...]

    def supervised_member_references(self) -> tuple[str, ...]:
        return tuple(
            record["member_reference"]
            for record in self.row_dispositions
            if record["population_disposition"] == CLEAN
        )

    def reconcile(self) -> bool:
        return self.total_source_rows == (
            self.clean_rows
            + self.collision_rows
            + self.unresolved_context_rows
        )


def _canonical_json(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def _sha512_identity(value: Any) -> str:
    return "sha512:" + hashlib.sha512(
        _canonical_json(value)
    ).hexdigest()


def validate_feature_surface(
    feature_identity_surface: Sequence[str],
    *,
    label_field: str,
    member_reference_field: str,
) -> tuple[str, ...]:
    surface = tuple(feature_identity_surface)

    if not surface:
        raise ValueError(
            "feature identity surface must not be empty"
        )

    if len(surface) != len(set(surface)):
        raise ValueError(
            "feature identity surface contains duplicates"
        )

    if label_field in surface:
        raise ValueError(
            "reviewed target label must not participate "
            "in measurable-body identity"
        )

    if member_reference_field in surface:
        raise ValueError(
            "member/row reference must not participate "
            "in measurable-body identity"
        )

    return surface


def measurable_body_identity(
    row: Mapping[str, Any],
    feature_identity_surface: Sequence[str],
    *,
    label_field: str = "reviewed_label",
    member_reference_field: str = "member_reference",
) -> str:
    surface = validate_feature_surface(
        feature_identity_surface,
        label_field=label_field,
        member_reference_field=member_reference_field,
    )

    missing = [
        field
        for field in surface
        if field not in row
    ]

    if missing:
        raise KeyError(
            "missing measurable fields: "
            + ", ".join(sorted(missing))
        )

    body = {
        field: row[field]
        for field in sorted(surface)
    }

    return _sha512_identity(
        {
            "feature_identity_surface": sorted(surface),
            "measurable_body": body,
        }
    )


def collision_group_identity(
    measurable_body_sha512: str,
    distinct_labels: Iterable[str],
    feature_identity_surface: Sequence[str],
) -> str:
    return _sha512_identity(
        {
            "measurable_body_sha512":
                measurable_body_sha512,
            "distinct_labels":
                sorted(set(distinct_labels)),
            "feature_identity_surface":
                sorted(feature_identity_surface),
        }
    )


def analyze_collision_boundary(
    rows: Sequence[Mapping[str, Any]],
    feature_identity_surface: Sequence[str],
    *,
    label_field: str = "reviewed_label",
    member_reference_field: str = "member_reference",
    provenance_field: str = "provenance_reference",
) -> CollisionBoundaryResult:
    surface = validate_feature_surface(
        feature_identity_surface,
        label_field=label_field,
        member_reference_field=member_reference_field,
    )

    prepared: list[dict[str, Any]] = []
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)

    seen_members: set[str] = set()

    for position, row in enumerate(rows):
        member = row.get(member_reference_field)

        if member is None or str(member) == "":
            member = f"source-position:{position}"
            member_resolved = False
        else:
            member = str(member)
            member_resolved = True

        if member in seen_members:
            raise ValueError(
                f"duplicate member reference: {member}"
            )

        seen_members.add(member)

        label = row.get(label_field)

        unresolved_reasons: list[str] = []

        if not member_resolved:
            unresolved_reasons.append(
                "MEMBER_REFERENCE_UNRESOLVED"
            )

        if label is None or str(label) == "":
            unresolved_reasons.append(
                "REVIEWED_LABEL_UNRESOLVED"
            )

        try:
            body_sha = measurable_body_identity(
                row,
                surface,
                label_field=label_field,
                member_reference_field=member_reference_field,
            )
        except (KeyError, TypeError, ValueError):
            body_sha = None
            unresolved_reasons.append(
                "MEASURABLE_BODY_UNRESOLVED"
            )

        record = {
            "member_reference": member,
            "reviewed_label":
                None if label is None else str(label),
            "measurable_body_sha512": body_sha,
            "collision_group_id": None,
            "feature_identity_surface": surface,
            "provenance_reference":
                row.get(provenance_field),
            "population_disposition":
                UNRESOLVED_CONTEXT
                if unresolved_reasons
                else CLEAN,
            "unresolved_reasons":
                tuple(sorted(set(unresolved_reasons))),
        }

        prepared.append(record)

        if not unresolved_reasons and body_sha is not None:
            groups[body_sha].append(record)

    collision_groups: list[CollisionGroup] = []

    for body_sha, members in groups.items():
        labels = tuple(sorted({
            str(member["reviewed_label"])
            for member in members
        }))

        if len(labels) <= 1:
            continue

        group_id = collision_group_identity(
            body_sha,
            labels,
            surface,
        )

        member_refs = tuple(sorted(
            member["member_reference"]
            for member in members
        ))

        collision_group = CollisionGroup(
            collision_group_id=group_id,
            measurable_body_sha512=body_sha,
            member_count=len(members),
            distinct_labels=labels,
            member_references=member_refs,
            feature_identity_surface=surface,
        )

        collision_groups.append(collision_group)

        for member in members:
            member["population_disposition"] = COLLISION
            member["collision_group_id"] = group_id

    collision_groups.sort(
        key=lambda group: group.collision_group_id
    )

    clean_rows = sum(
        record["population_disposition"] == CLEAN
        for record in prepared
    )

    collision_rows = sum(
        record["population_disposition"] == COLLISION
        for record in prepared
    )

    unresolved_rows = sum(
        record["population_disposition"]
        == UNRESOLVED_CONTEXT
        for record in prepared
    )

    result = CollisionBoundaryResult(
        total_source_rows=len(prepared),
        clean_rows=clean_rows,
        collision_rows=collision_rows,
        unresolved_context_rows=unresolved_rows,
        collision_groups=tuple(collision_groups),
        row_dispositions=tuple(prepared),
    )

    if not result.reconcile():
        raise RuntimeError(
            "collision-boundary population reconciliation failed"
        )

    supervised = set(
        result.supervised_member_references()
    )

    for record in result.row_dispositions:
        if (
            record["population_disposition"] != CLEAN
            and record["member_reference"] in supervised
        ):
            raise RuntimeError(
                "ineligible row entered supervised population"
            )

    return result
