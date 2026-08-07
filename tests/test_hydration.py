import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

VALIDATOR = (
    ROOT
    / "tools"
    / "validate_hydration.py"
)

spec = importlib.util.spec_from_file_location(
    "validate_hydration",
    VALIDATOR
)

module = importlib.util.module_from_spec(
    spec
)

spec.loader.exec_module(
    module
)


def make_request():
    object_id = (
        "sha512:"
        + "4" * 128
    )

    record = {
        "schema_version":
            "1.0",
        "object_id":
            object_id,
        "active_question":
            "what verified territory is required?",
        "capability_mission_request_reference":
            "mission:test",
        "formation_selection_reference":
            "formation:test",
        "occupancy_witness_reference":
            "occupancy:test",
        "zone_reference":
            "zone:test",
        "space_reference":
            "space:test",
        "orientation_reference":
            "orientation:test",
        "territory_reference":
            "territory:test",
        "requested_verified_territory_references": [
            "territory:verified:test"
        ],
        "requested_payload_references": [
            "payload:a",
            "payload:b"
        ],
        "payload_scope":
            "MISSION_REQUIRED",
        "mission_necessity_basis": [
            "requested payload directly supports the active question"
        ],
        "evidence_boundary": {
            "scope": "bounded"
        },
        "evidence_ceiling":
            "CEILING:TEST",
        "restriction_references": [],
        "stick_reference":
            "stick:test",
        "governance_reference":
            "governance:test",
        "authorization_reference":
            "authorization:test",
        "human_gate_reference":
            "human-gate:test",
        "provenance_route": [
            object_id,
            "mission:test",
            "territory:verified:test"
        ],
        "requested_at":
            "2026-08-07T19:46:00-04:00",
    }

    record[
        "hydration_request_id"
    ] = module.compute_request_id(
        record
    )

    return record


def make_release(
    request,
    state="RELEASED",
):
    record = {
        "schema_version":
            "1.0",
        "hydration_request_reference":
            request[
                "hydration_request_id"
            ],
        "object_id":
            request["object_id"],
        "release_state":
            state,
        "restored_verified_territory_references": [
            "territory:verified:test"
        ],
        "restored_payload_references": [
            "payload:a"
        ],
        "denied_or_blocked_references": [],
        "retained_at_rest_references": [
            "payload:b"
        ],
        "released_from_active_payload_references": [],
        "release_basis": [
            "mission-required bounded hydration"
        ],
        "restriction_findings": [],
        "evidence_boundary":
            request["evidence_boundary"],
        "evidence_ceiling":
            request["evidence_ceiling"],
        "room_state_reference":
            "room-state:test",
        "representation_state_reference":
            "representation-state:test",
        "stick_reference":
            request["stick_reference"],
        "final_active_payload_scope":
            "MISSION_REQUIRED",
        "provenance_route": [
            request["object_id"],
            request[
                "hydration_request_id"
            ],
        ],
        "released_at":
            "2026-08-07T19:46:00-04:00",
    }

    if state == "BLOCKED":
        record[
            "restored_verified_territory_references"
        ] = []

        record[
            "restored_payload_references"
        ] = []

        record[
            "denied_or_blocked_references"
        ] = [
            "payload:a"
        ]

    record[
        "hydration_release_id"
    ] = module.compute_release_id(
        record
    )

    return record


class HydrationTests(
    unittest.TestCase
):

    def test_repository_contract(self):
        self.assertEqual(
            module.validate(),
            []
        )

    def test_valid_request(self):
        request = make_request()

        self.assertEqual(
            module.validate_request(
                request
            ),
            []
        )

    def test_valid_release(self):
        request = make_request()
        release = make_release(
            request
        )

        self.assertEqual(
            module.validate_release(
                release,
                request,
            ),
            []
        )

    def test_release_states(self):
        request = make_request()

        for state in (
            "RELEASED",
            "PARTIAL",
            "BLOCKED",
        ):
            release = make_release(
                request,
                state,
            )

            self.assertEqual(
                module.validate_release(
                    release,
                    request,
                ),
                []
            )

    def test_full_payload_scope_rejected(self):
        request = make_request()

        request[
            "payload_scope"
        ] = "FULL_PAYLOAD"

        request[
            "hydration_request_id"
        ] = module.compute_request_id(
            request
        )

        errors = module.validate_request(
            request
        )

        self.assertTrue(
            any(
                "MISSION_REQUIRED"
                in error
                for error in errors
            )
        )

    def test_load_everything_basis_rejected(self):
        request = make_request()

        request[
            "mission_necessity_basis"
        ] = [
            "load everything for completeness"
        ]

        request[
            "hydration_request_id"
        ] = module.compute_request_id(
            request
        )

        errors = module.validate_request(
            request
        )

        self.assertTrue(
            any(
                "full-payload"
                in error
                for error in errors
            )
        )

    def test_release_cannot_restore_unrequested_payload(self):
        request = make_request()
        release = make_release(
            request
        )

        release[
            "restored_payload_references"
        ].append(
            "payload:not-requested"
        )

        release[
            "hydration_release_id"
        ] = module.compute_release_id(
            release
        )

        errors = module.validate_release(
            release,
            request,
        )

        self.assertTrue(
            any(
                "outside request"
                in error
                for error in errors
            )
        )

    def test_release_cannot_restore_unrequested_territory(self):
        request = make_request()
        release = make_release(
            request
        )

        release[
            "restored_verified_territory_references"
        ].append(
            "territory:not-requested"
        )

        release[
            "hydration_release_id"
        ] = module.compute_release_id(
            release
        )

        errors = module.validate_release(
            release,
            request,
        )

        self.assertTrue(
            any(
                "outside request"
                in error
                for error in errors
            )
        )

    def test_material_request_change_changes_identity(self):
        first = make_request()

        changed = dict(
            first
        )

        changed[
            "active_question"
        ] = "which second verified surface is required?"

        changed[
            "hydration_request_id"
        ] = module.compute_request_id(
            changed
        )

        self.assertNotEqual(
            first[
                "hydration_request_id"
            ],
            changed[
                "hydration_request_id"
            ]
        )

    def test_request_and_release_ids_are_distinct(self):
        request = make_request()
        release = make_release(
            request
        )

        self.assertNotEqual(
            request[
                "hydration_request_id"
            ],
            release[
                "hydration_release_id"
            ]
        )

        self.assertNotEqual(
            request[
                "object_id"
            ],
            request[
                "hydration_request_id"
            ]
        )

    def test_schema_does_not_pull_downstream_semantics_forward(self):
        request_schema = module.load(
            module.REQUEST_SCHEMA
        )

        release_schema = module.load(
            module.RELEASE_SCHEMA
        )

        forbidden = {
            "full_payload",
            "load_everything",
            "lifecycle_mutation",
            "occupancy_mutation",
            "formation_mutation",
            "landing_witness_id",
            "replay_envelope_id",
            "restriction_transition_id",
            "canonical_mutation_authority",
        }

        self.assertFalse(
            set(
                request_schema["properties"]
            )
            & forbidden
        )

        self.assertFalse(
            set(
                release_schema["properties"]
            )
            & forbidden
        )


if __name__ == "__main__":
    unittest.main()
