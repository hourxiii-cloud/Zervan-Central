"""Contract-faithful Gate 0 check for the middleware telemetry artifact.

This candidate-side validator reports contract compatibility. It does not
manufacture a formal Beagle runtime receipt when fresh dependency loading and
runtime execution have not been verified.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "verification/CHAT_MIDDLEWARE_RUNTIME_TELEMETRY.json"
SCHEMA = ROOT / "verification/CHAT_MIDDLEWARE_RUNTIME_TELEMETRY.schema.json"


def main() -> None:
    artifact = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    assert artifact["artifact_type"] == "runtime_telemetry"
    assert artifact["evidence_class"] == "DERIVED"
    assert artifact["hash_algorithm"] == "SHA-512"
    assert artifact["structural_definition"] == str(SCHEMA.relative_to(ROOT))
    assert artifact["source_identifier"] == "verification/validate_chat_middleware_duck_100000.py"
    assert artifact["runtime_execution"] == "NOT_DEPLOYED"
    assert artifact["beagle_component_execution"].startswith("UNKNOWN")
    assert set(schema["required"]).issubset(artifact)
    assert artifact["metrics"]["governed_standing_wobble"] == 0
    assert artifact["metrics"]["authority"] == "NONE"
    assert artifact["metrics"]["membership"] == "NONE"
    assert artifact["metrics"]["work_id"] == "NONE"
    assert artifact["metrics"]["promotion"] == "NONE"
    assert artifact["metrics"]["unsupported_resolution"] == "UNKNOWN"
    digest = hashlib.sha512(ARTIFACT.read_bytes()).hexdigest()
    assert len(digest) == 128
    print("BEAGLE GATE 0 CONTRACT CHECK: PASS")
    print(f"artifact_sha512={digest}")
    print("evidence_class=DERIVED")
    print("formal_beagle_component_receipt=NOT_VERIFIED")


if __name__ == "__main__":
    main()
