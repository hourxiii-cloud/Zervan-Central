from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

FORBIDDEN_ACTIVE_EXPANSIONS = (
    "Potential Mission Commitment",
    "Mission Commitment",
)

CANONICAL_FILES = (
    ROOT / "Doctrine" / "PMC.md",
    ROOT / "Doctrine" / "MC.md",
    ROOT / "Doctrine" / "PMC_MC_INTERFACE.md",
    ROOT / "ZERVAN #U2014 EQUATIONS WIRE MAP (PASS 1 + PASS 2.md",
)


def test_reserved_expansions_are_present():
    pmc = (ROOT / "Doctrine" / "PMC.md").read_text(encoding="utf-8")
    mc = (ROOT / "Doctrine" / "MC.md").read_text(encoding="utf-8")
    lock = (ROOT / "Doctrine" / "PMC_MC_NAMING_LOCK.md").read_text(encoding="utf-8")
    assert "Probabilistic Multiverse Computation" in pmc
    assert "Meta Collapse" in mc
    assert "Canonical Commitment Record" in lock


def test_forbidden_active_expansions_absent():
    for path in CANONICAL_FILES:
        text = path.read_text(encoding="utf-8")
        for forbidden in FORBIDDEN_ACTIVE_EXPANSIONS:
            assert forbidden not in text, f"{forbidden!r} found in {path}"


def test_mc_is_not_commitment_construction_in_wire_map():
    text = CANONICAL_FILES[-1].read_text(encoding="utf-8")
    assert "Eq3.CCR" in text
    assert "Meta Collapse Response-Admissibility Gate" in text
    assert "MC1_commitment_record.json" not in text
