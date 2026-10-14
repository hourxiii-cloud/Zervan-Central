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
