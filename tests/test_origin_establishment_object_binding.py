import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

VALIDATOR = (
    ROOT
    / "tools"
    / "validate_origin_establishment_object_binding.py"
)

spec = importlib.util.spec_from_file_location(
    "validate_origin_establishment_object_binding",
    VALIDATOR
)

module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

r2a = module.load_r2a()


def fixtures(
    *,
    final_status="ESTABLISHED",
    duplicate_check="CLEAR"
):
    origin_id = (
        "sha512:"
        + "1" * 128
    )

    ingress_ref = "ingress:001"
    genesis_ref = "genesis:001"
    nonce = "room-001"

    object_id = r2a.compute_object_id(
        genesis_ref,
        origin_id,
        nonce
    )

    ingress = {
        "content_identity": {
            "algorithm": "sha512",
            "value": origin_id,
        },
        "provenance": {
            "origin_reference":
                "origin:001",
        },
    }

    genesis = {
        "ingress_envelope_reference":
            ingress_ref,
        "origin_content_identity":
            origin_id,
        "provenance_origin_reference":
            "origin:001",
    }

    room = {
        "object_id":
            object_id,
        "genesis_manifest_reference":
            genesis_ref,
        "origin_content_identity":
            origin_id,
        "object_nonce":
            nonce,
        "provenance_origin_reference":
            "origin:001",
        "establishment_status":
            final_status,
    }

    checks = {
        "ingress_present": True,
        "content_identity_valid": True,
        "genesis_present": True,
        "ingress_reference_match": True,
        "content_identity_match": True,
        "provenance_continuity": True,
        "object_identity_match": True,
        "authorization_resolved": True,
    }

    decided_at = (
        "2026-08-07T18:25:00-04:00"
    )

    receipt = {
        "establishment_receipt_id": None,
        "ingress_envelope_reference":
            ingress_ref,
        "genesis_manifest_reference":
            genesis_ref,
        "object_id":
            object_id,
        "initial_status":
            "PROPOSED",
        "final_status":
            final_status,
        "duplicate_check":
            duplicate_check,
        "prerequisite_checks":
            checks,
        "authorization_reference":
            "auth:001",
        "human_gate": {
            "status":
                "REQUIRED_SATISFIED",
            "reference":
                "human-gate:001",
        },
        "provenance_route": [
            object_id,
            genesis_ref,
            ingress_ref,
            "origin:001",
        ],
        "decided_at":
            decided_at,
        "decision_reason":
            "binding validated",
    }

    receipt["establishment_receipt_id"] = (
        module.compute_receipt_id(
            ingress_ref,
            genesis_ref,
            object_id,
            final_status,
            duplicate_check,
            "auth:001",
            decided_at
        )
    )

    return (
        ingress,
        ingress_ref,
        genesis,
        genesis_ref,
        room,
        receipt,
    )


class OriginEstablishmentBindingTests(
    unittest.TestCase
):

    def test_repository_contract(self):
        self.assertEqual(
            module.validate(),
            []
        )

    def test_valid_establishment_binding(self):
        (
            ingress,
            ingress_ref,
            genesis,
            genesis_ref,
            room,
            receipt,
        ) = fixtures()

        self.assertEqual(
            module.validate_binding(
                ingress=ingress,
                ingress_reference=ingress_ref,
                genesis=genesis,
                genesis_reference=genesis_ref,
                room_object=room,
                receipt=receipt,
            ),
            []
        )

    def test_content_identity_mismatch_fails(self):
        (
            ingress,
            ingress_ref,
            genesis,
            genesis_ref,
            room,
            receipt,
        ) = fixtures()

        genesis[
            "origin_content_identity"
        ] = (
            "sha512:"
            + "9" * 128
        )

        errors = module.validate_binding(
            ingress=ingress,
            ingress_reference=ingress_ref,
            genesis=genesis,
            genesis_reference=genesis_ref,
            room_object=room,
            receipt=receipt,
        )

        self.assertTrue(
            any(
                "Genesis origin content identity"
                in error
                for error in errors
            )
        )

    def test_wrong_object_id_fails(self):
        (
            ingress,
            ingress_ref,
            genesis,
            genesis_ref,
            room,
            receipt,
        ) = fixtures()

        room["object_id"] = (
            "sha512:"
            + "8" * 128
        )

        errors = module.validate_binding(
            ingress=ingress,
            ingress_reference=ingress_ref,
            genesis=genesis,
            genesis_reference=genesis_ref,
            room_object=room,
            receipt=receipt,
        )

        self.assertTrue(
            any(
                "does not recompute"
                in error
                for error in errors
            )
        )

    def test_unresolved_duplicate_blocks_establishment(self):
        (
            ingress,
            ingress_ref,
            genesis,
            genesis_ref,
            room,
            receipt,
        ) = fixtures(
            duplicate_check="UNRESOLVED"
        )

        errors = module.validate_binding(
            ingress=ingress,
            ingress_reference=ingress_ref,
            genesis=genesis,
            genesis_reference=genesis_ref,
            room_object=room,
            receipt=receipt,
        )

        self.assertTrue(
            any(
                "duplicate check CLEAR"
                in error
                for error in errors
            )
        )

    def test_existing_object_blocks_establishment(self):
        (
            ingress,
            ingress_ref,
            genesis,
            genesis_ref,
            room,
            receipt,
        ) = fixtures(
            duplicate_check="EXISTING_OBJECT"
        )

        errors = module.validate_binding(
            ingress=ingress,
            ingress_reference=ingress_ref,
            genesis=genesis,
            genesis_reference=genesis_ref,
            room_object=room,
            receipt=receipt,
        )

        self.assertTrue(
            any(
                "duplicate check CLEAR"
                in error
                for error in errors
            )
        )

    def test_provenance_contradiction_fails(self):
        (
            ingress,
            ingress_ref,
            genesis,
            genesis_ref,
            room,
            receipt,
        ) = fixtures()

        genesis[
            "provenance_origin_reference"
        ] = "origin:other"

        errors = module.validate_binding(
            ingress=ingress,
            ingress_reference=ingress_ref,
            genesis=genesis,
            genesis_reference=genesis_ref,
            room_object=room,
            receipt=receipt,
        )

        self.assertTrue(
            any(
                "provenance"
                in error.lower()
                for error in errors
            )
        )

    def test_establishment_transition_is_one_way(self):
        self.assertTrue(
            module.validate_transition(
                "PROPOSED",
                "ESTABLISHED"
            )
        )

        self.assertTrue(
            module.validate_transition(
                "PROPOSED",
                "REJECTED"
            )
        )

        self.assertFalse(
            module.validate_transition(
                "ESTABLISHED",
                "PROPOSED"
            )
        )

        self.assertFalse(
            module.validate_transition(
                "REJECTED",
                "ESTABLISHED"
            )
        )


if __name__ == "__main__":
    unittest.main()
