#!/usr/bin/env bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel 2>/dev/null)" || {
  echo "Run this from inside the Zervan Codespaces Git repository." >&2
  exit 2
}
cd "$ROOT"

VERSION_VALUE="$(tr -d '\r\n' < VERSION)"
if [[ "$VERSION_VALUE" != "vTemporal.47.8.0" ]]; then
  echo "Stopped: expected VERSION vTemporal.47.8.0; found ${VERSION_VALUE:-<empty>}." >&2
  exit 2
fi

for target in tools/jumping_spider_spatial.py tests/test_jumping_spider_spatial.py; do
  if [[ -e "$target" ]]; then
    echo "Stopped: refusing to overwrite existing $target" >&2
    exit 2
  fi
done

mkdir -p tools tests
cat > tools/jumping_spider_spatial.py <<'JUMPING_SPIDER_MODULE'
"""Deterministic, modeled-only Jumping Spider spatial approach operation.

This module computes a route through an explicitly validated graph map to one
of a candidate's declared observation points. It never moves a real observer,
infers missing map geometry, or alters its inputs.
"""

from __future__ import annotations

import hashlib
import heapq
import json
import math
from copy import deepcopy
from typing import Any, Mapping


SCHEMA = "zervan-jumping-spider-route/v1"
OPERATION = "JUMPING_SPIDER_SPATIAL_APPROACH"


def _digest(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _valid_map(spatial_map: Mapping[str, Any]) -> bool:
    if spatial_map.get("validated") is not True:
        return False
    if not all(isinstance(spatial_map.get(k), str) and spatial_map[k] for k in ("map_id", "map_version")):
        return False
    nodes = spatial_map.get("nodes")
    edges = spatial_map.get("edges")
    if not isinstance(nodes, dict) or not nodes or not isinstance(edges, list):
        return False
    for node_id, node in nodes.items():
        coords = node.get("coordinates") if isinstance(node, dict) else None
        if not isinstance(node_id, str) or not node_id or not isinstance(coords, list) or len(coords) != 3:
            return False
        if any(isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v) for v in coords):
            return False
    for edge in edges:
        if not isinstance(edge, dict):
            return False
        source, target, cost = edge.get("from"), edge.get("to"), edge.get("cost")
        if (
            not isinstance(source, str)
            or not isinstance(target, str)
            or source not in nodes
            or target not in nodes
            or source == target
        ):
            return False
        if isinstance(cost, bool) or not isinstance(cost, (int, float)) or not math.isfinite(cost) or cost <= 0:
            return False
        if "blocked" in edge and not isinstance(edge["blocked"], bool):
            return False
    return True


def _shortest_path(spatial_map: Mapping[str, Any], start: str, goal: str) -> tuple[float, tuple[str, ...]] | None:
    nodes = spatial_map["nodes"]
    if start not in nodes or goal not in nodes:
        return None
    adjacency: dict[str, list[tuple[str, float]]] = {node_id: [] for node_id in nodes}
    for edge in spatial_map["edges"]:
        if edge.get("blocked", False):
            continue
        a, b, cost = edge["from"], edge["to"], float(edge["cost"])
        adjacency[a].append((b, cost))
        adjacency[b].append((a, cost))
    for neighbors in adjacency.values():
        neighbors.sort(key=lambda pair: pair[0])

    # Path tuple is part of the heap key to make equal-cost routes repeatable.
    queue: list[tuple[float, tuple[str, ...], str]] = [(0.0, (start,), start)]
    best: dict[str, tuple[float, tuple[str, ...]]] = {start: (0.0, (start,))}
    while queue:
        distance, path, node_id = heapq.heappop(queue)
        if best.get(node_id) != (distance, path):
            continue
        if node_id == goal:
            return distance, path
        for neighbor, cost in adjacency[node_id]:
            next_value = (distance + cost, path + (neighbor,))
            if neighbor not in best or next_value < best[neighbor]:
                best[neighbor] = next_value
                heapq.heappush(queue, (next_value[0], next_value[1], neighbor))
    return None


def route_to_observation_point(
    spatial_map: Mapping[str, Any], candidate: Mapping[str, Any], origin_node_id: str
) -> dict[str, Any]:
    """Return a modeled route receipt or a fail-closed status.

    The map must carry ``validated: true`` and explicit 3D node coordinates and
    positive edge costs. A candidate must declare an ordered set of valid
    ``observation_node_ids``. The chosen point is the reachable point with the
    lowest graph cost, with node ID and complete path as deterministic ties.
    """
    try:
        source_map = deepcopy(dict(spatial_map))
        source_candidate = deepcopy(dict(candidate))
        source_digest = _digest({"map": source_map, "candidate": source_candidate, "origin": origin_node_id})
    except (TypeError, ValueError):
        return {"schema": SCHEMA, "operation": OPERATION, "status": "INSUFFICIENT_MAP", "observer_motion": "MODELED_ONLY"}

    base: dict[str, Any] = {
        "schema": SCHEMA,
        "operation": OPERATION,
        "observer_motion": "MODELED_ONLY",
        "candidate_id": source_candidate.get("candidate_id"),
        "provenance": {
            "map": source_map,
            "candidate": source_candidate,
            "origin_node_id": origin_node_id,
            "input_sha256": source_digest,
        },
    }
    observation_ids = source_candidate.get("observation_node_ids")
    if (
        not _valid_map(source_map)
        or not isinstance(source_candidate.get("candidate_id"), str)
        or not source_candidate["candidate_id"]
        or not isinstance(observation_ids, list)
        or not observation_ids
        or any(not isinstance(node_id, str) for node_id in observation_ids)
        or not isinstance(origin_node_id, str)
    ):
        return {**base, "status": "INSUFFICIENT_MAP"}

    reachable: list[tuple[float, str, tuple[str, ...]]] = []
    for observation_id in set(observation_ids):
        found = _shortest_path(source_map, origin_node_id, observation_id)
        if found is not None:
            cost, path = found
            reachable.append((cost, observation_id, path))
    if not reachable:
        return {**base, "status": "NO_ROUTE"}

    cost, observation_id, path = min(reachable, key=lambda item: (item[0], item[1], item[2]))
    result = {
        **base,
        "status": "ROUTE_FOUND",
        "observation_node_id": observation_id,
        "route_node_ids": list(path),
        "route_cost": cost,
    }
    result["receipt_sha256"] = _digest(result)
    return result
JUMPING_SPIDER_MODULE
cat > tests/test_jumping_spider_spatial.py <<'JUMPING_SPIDER_TESTS'
import copy
import unittest

from tools.jumping_spider_spatial import route_to_observation_point


def fixture_map():
    return {
        "map_id": "synthetic-map-1",
        "map_version": "fixture-v1",
        "validated": True,
        "nodes": {
            "start": {"coordinates": [0, 0, 0]},
            "junction": {"coordinates": [1, 0, 0]},
            "near": {"coordinates": [2, 0, 0]},
            "far": {"coordinates": [1, 1, 0]},
            "blocked": {"coordinates": [9, 9, 0]},
        },
        "edges": [
            {"from": "start", "to": "junction", "cost": 1},
            {"from": "junction", "to": "near", "cost": 1},
            {"from": "junction", "to": "far", "cost": 2},
            {"from": "near", "to": "blocked", "cost": 1, "blocked": True},
        ],
    }


class JumpingSpiderSpatialTests(unittest.TestCase):
    def test_selects_lowest_cost_reachable_observation_point(self):
        result = route_to_observation_point(
            fixture_map(),
            {"candidate_id": "candidate-7", "observation_node_ids": ["far", "near"]},
            "start",
        )
        self.assertEqual(result["status"], "ROUTE_FOUND")
        self.assertEqual(result["operation"], "JUMPING_SPIDER_SPATIAL_APPROACH")
        self.assertEqual(result["observer_motion"], "MODELED_ONLY")
        self.assertEqual(result["observation_node_id"], "near")
        self.assertEqual(result["route_node_ids"], ["start", "junction", "near"])
        self.assertEqual(result["route_cost"], 2)
        self.assertEqual(len(result["receipt_sha256"]), 64)

    def test_unvalidated_map_fails_closed_as_insufficient(self):
        spatial_map = fixture_map()
        spatial_map["validated"] = False
        result = route_to_observation_point(
            spatial_map, {"candidate_id": "candidate-7", "observation_node_ids": ["near"]}, "start"
        )
        self.assertEqual(result["status"], "INSUFFICIENT_MAP")
        self.assertNotIn("route_node_ids", result)

    def test_disconnected_candidate_returns_no_route(self):
        result = route_to_observation_point(
            fixture_map(), {"candidate_id": "candidate-7", "observation_node_ids": ["blocked"]}, "start"
        )
        self.assertEqual(result["status"], "NO_ROUTE")
        self.assertNotIn("route_node_ids", result)

    def test_preserves_full_input_and_does_not_mutate_it(self):
        spatial_map = fixture_map()
        candidate = {"candidate_id": "candidate-7", "observation_node_ids": ["near"], "source_record": {"event": 12}}
        original_map, original_candidate = copy.deepcopy(spatial_map), copy.deepcopy(candidate)
        result = route_to_observation_point(spatial_map, candidate, "start")
        self.assertEqual(spatial_map, original_map)
        self.assertEqual(candidate, original_candidate)
        self.assertEqual(result["provenance"]["map"], original_map)
        self.assertEqual(result["provenance"]["candidate"], original_candidate)

    def test_malformed_geometry_returns_insufficient_map(self):
        spatial_map = fixture_map()
        spatial_map["nodes"]["near"]["coordinates"] = [float("nan"), 0, 0]
        result = route_to_observation_point(
            spatial_map, {"candidate_id": "candidate-7", "observation_node_ids": ["near"]}, "start"
        )
        self.assertEqual(result["status"], "INSUFFICIENT_MAP")

    def test_malformed_edge_returns_insufficient_map(self):
        spatial_map = fixture_map()
        spatial_map["edges"].append({"from": ["start"], "to": "near", "cost": 1})
        result = route_to_observation_point(
            spatial_map, {"candidate_id": "candidate-7", "observation_node_ids": ["near"]}, "start"
        )
        self.assertEqual(result["status"], "INSUFFICIENT_MAP")


if __name__ == "__main__":
    unittest.main()
JUMPING_SPIDER_TESTS

python3 -m unittest discover -s tests -p 'test_jumping_spider_spatial.py' -v
