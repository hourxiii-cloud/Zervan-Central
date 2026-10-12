#!/usr/bin/env python3
"""Bind v47.8 to its inherited frozen components and push one registry commit.

This deliberately does not run tests. Run from the Zervan-Central repository
root on a synchronized main branch. It preserves all frozen component payloads.
"""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path.cwd()
REGISTRY_PATH = "canonical/v47.8/COMPONENT_REGISTRY.json"
FILES = {
    "VERSION.json",
    "VERSION_REFERENCES.json",
    "VERSION_AUTHORITY.md",
    "call/INITIATION_STATEMENT_V47_8.md",
    "canonical/ZERVAN_v47_8_CANONICAL_ENTRY.md",
    REGISTRY_PATH,
    "tools/validate_version_identity.py",
    "tools/regenerate_version_references.py",
    "tools/validate_spider_persona_admission.py",
    "tools/validate_middleware_admission.py",
    "tools/validate_flow_math_admission.py",
}


def git(*args: str, check: bool = True) -> str:
    p = subprocess.run(["git", *args], cwd=ROOT, text=True, capture_output=True)
    if check and p.returncode:
        raise RuntimeError(p.stderr.strip() or p.stdout.strip())
    return p.stdout.strip()


def sha256(path: str) -> str:
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()


def replace_once(text: str, old: str, new: str, label: str) -> str:
    if new in text:
        return text
    if text.count(old) != 1:
        raise RuntimeError(f"Cannot safely update {label}; expected one source block.")
    return text.replace(old, new, 1)


def read_json(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def main() -> int:
    if git("branch", "--show-current") != "main":
        raise RuntimeError("STOP: check out main first; nothing changed.")
    git("fetch", "origin", "main")
    head = git("rev-parse", "HEAD")
    remote = git("rev-parse", "origin/main")
    if head != remote:
        raise RuntimeError(f"STOP: local main ({head}) is not origin/main ({remote}); nothing changed.")
    staged = subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=ROOT)
    if staged.returncode == 1:
        raise RuntimeError("STOP: staged changes already exist; nothing changed.")
    if staged.returncode > 1:
        raise RuntimeError("STOP: could not inspect staged changes; nothing changed.")

    version_text = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    identity = read_json("VERSION.json")
    if version_text != "vTemporal.47.8.0" or identity.get("version") != version_text:
        raise RuntimeError("STOP: expected the active v47.8 release; nothing changed.")

    # Refuse to bless any altered historical or origin-bound artifact.
    expected_hashes = {
        "canonical/Spider/SPIDER_R2_PERSONA_ADMISSION.json": "a1708800ed59ef3d379f2d530ec4fd2c2a27e2658a46251701d6256e8b69aa09",
        "verification/v42.5.4/SPIDER_PERSONA_STANDING_CORRECTION.json": "c356606cbb3829c3398b77665db45f9484364c789b3ac0fca140d852ad494023",
        "canonical/middleware/ZERVAN_MIDDLEWARE_ADMISSION.json": "ec6eb146e2bbbf55f33caf8c89f8238e65dcbfce1e3194968ebbd42b7b3911a0",
        "canonical/geometry/FLOW_MATH_ADMISSION.json": "4221c67a03b76a64f247b076db37fc43b1f86db28b13944b1b4b5a89def040c1",
        "canonical/geometry/FLOW_MATH_ORIGIN_CONTRACT.md": "27ec46f561c2d1680039f0a92e32f7a713b377ddaeac9c08fb82cfa5c0b0e1ce",
        "verification/v47.8/PROMOTION_RECEIPT.json": "eff7cb60604c31cfdcd258a7a2310f16376065fa8fb10125a8f09ee27b673f45",
        "verification/v47.8/FLOW_MATH_PORT_RECEIPT.md": "b09edc1626bc32c816114a72dec94bf42f7efb005c131f06c8e50e282914a986",
    }
    for path, expected in expected_hashes.items():
        actual = sha256(path)
        if actual != expected:
            raise RuntimeError(f"STOP: origin/frozen SHA mismatch for {path}; nothing changed.")

    spider_admission = "canonical/Spider/SPIDER_R2_PERSONA_ADMISSION.json"
    spider_standing = "verification/v42.5.4/SPIDER_PERSONA_STANDING_CORRECTION.json"
    middleware_admission = "canonical/middleware/ZERVAN_MIDDLEWARE_ADMISSION.json"
    flow_admission = "canonical/geometry/FLOW_MATH_ADMISSION.json"
    flow_contract = "canonical/geometry/FLOW_MATH_ORIGIN_CONTRACT.md"
    flow_receipt = "verification/v47.8/PROMOTION_RECEIPT.json"
    flow_port = "verification/v47.8/FLOW_MATH_PORT_RECEIPT.md"

    registry = {
        "schema": "zervan-component-release-registry/v1",
        "active_release": version_text,
        "canonical_branch": "main",
        "parent_release": identity["parent_canonical_identity"],
        "canonical_parent_commit": identity["parent_canonical_commit"],
        "package_source_baseline": {
            "release": "vTemporal.42.5.4",
            "commit": "bf8c82dfb911ba4eac4b984c77ace741c4e81c6f",
        },
        "human_gate_decision": identity["human_gate_decision_reference"],
        "components": {
            "spider_persona": {
                "standing": "INHERITED_FROZEN_CANONICAL_COMPONENT",
                "source_release": "vTemporal.42.5.4",
                "admission": {"path": spider_admission, "sha256": sha256(spider_admission)},
                "standing_record": {"path": spider_standing, "sha256": sha256(spider_standing)},
                "inheritance_rule": "Retains the admitted v42.5.4 identity under active v47.8; source records and payload hashes remain unchanged.",
            },
            "middleware": {
                "standing": "INHERITED_FROZEN_CANONICAL_COMPONENT",
                "source_release": "vTemporal.42.5.4",
                "admission": {"path": middleware_admission, "sha256": sha256(middleware_admission)},
                "promotion_receipt": "verification/middleware/MIDDLEWARE_PROMOTION_RECEIPT.json",
                "inheritance_rule": "Retains the admitted v42.5.4 identity under active v47.8; frozen source, dependencies, receipt, and payload hashes remain unchanged.",
            },
            "relational_flow_math": {
                "standing": "APPROVED_CANONICAL_ADDITIVE_SUPPLEMENT",
                "source_release": version_text,
                "admission": {"path": flow_admission, "sha256": sha256(flow_admission)},
                "origin_contract": {"path": flow_contract, "sha256": sha256(flow_contract)},
                "promotion_receipt": {"path": flow_receipt, "sha256": sha256(flow_receipt)},
                "port_record": {"path": flow_port, "sha256": sha256(flow_port)},
                "originating_candidate_commit": "249a62f631f661ae688fb6e21bb8302969385e4f",
                "transport_artifact_sha256": "b9f25ee53f604ec731412bc72db56bb4870c880633e835137efbbb788729f330",
                "runtime_validation": "NOT PERFORMED",
                "independent_component_execution": False,
            },
        },
    }

    updates: dict[str, str] = {}
    identity["component_registry"] = REGISTRY_PATH
    updates["VERSION.json"] = json.dumps(identity, indent=2) + "\n"
    updates[REGISTRY_PATH] = json.dumps(registry, indent=2) + "\n"

    authority_path = "VERSION_AUTHORITY.md"
    authority = (ROOT / authority_path).read_text(encoding="utf-8")
    lineage_note = (
        "Component lineage is registered in `canonical/v47.8/COMPONENT_REGISTRY.json`. "
        "The Spider and middleware admissions retain their frozen v42.5.4 source identities; "
        "the v47.8 relational-flow supplement is bound to its originating candidate SHA and transport digest."
    )
    if lineage_note not in authority:
        anchor = "The promotion commit is recorded in `verification/v47.8/PROMOTION_RECEIPT.json`."
        if authority.count(anchor) != 1:
            raise RuntimeError("Cannot locate the active v47.8 authority section; nothing changed.")
        authority = authority.replace(anchor, anchor + "\n" + lineage_note, 1)
    updates[authority_path] = authority

    entry_path = "canonical/ZERVAN_v47_8_CANONICAL_ENTRY.md"
    entry = (ROOT / entry_path).read_text(encoding="utf-8")
    entry = replace_once(
        entry,
        "## Additive relational-flow mathematical supplement",
        "## Release component registry\n\nThe active v47.8 release-to-component lineage is recorded in `/canonical/v47.8/COMPONENT_REGISTRY.json`. It preserves the v42.5.4 identities and frozen hashes of inherited Spider and middleware components while binding the approved v47.8 flow-math supplement to its originating candidate and transport digest.\n\n## Additive relational-flow mathematical supplement",
        "canonical entry",
    )
    updates[entry_path] = entry

    call_path = "call/INITIATION_STATEMENT_V47_8.md"
    call = (ROOT / call_path).read_text(encoding="utf-8")
    call = replace_once(
        call,
        "Load `/VERSION`, `/VERSION.json`, `/VERSION_AUTHORITY.md`, this statement,\nand `/canonical/ZERVAN_v47_8_CANONICAL_ENTRY.md`.",
        "Load `/VERSION`, `/VERSION.json`, the component registry named by `VERSION.json`,\n`/VERSION_AUTHORITY.md`, this statement, and `/canonical/ZERVAN_v47_8_CANONICAL_ENTRY.md`.",
        "initiation statement",
    )
    updates[call_path] = call

    # The historical reference index must be based on tracked repository files,
    # not scratch/untracked package artifacts in a Codespace.
    for path in ("tools/validate_version_identity.py", "tools/regenerate_version_references.py"):
        text = (ROOT / path).read_text(encoding="utf-8")
        text = replace_once(
            text,
            '            "--cached",\n            "--others",\n            "--exclude-standard",',
            '            "--cached",',
            path + " tracked-file scan",
        )
        text = text.replace("vTemporal\\.(?:39|40|41|42)", "vTemporal\\.(?:39|40|41|42|47)")
        text = text.replace("v(?:39|40|41|42)", "v(?:39|40|41|42|47)")
        if "vTemporal\\.(?:39|40|41|42)" in text:
            raise RuntimeError(f"Could not extend version scanner in {path}; nothing changed.")
        text = text.replace('    if normalized == "v42" or normalized.startswith("v42.") or normalized.startswith("vTemporal.42"):\n        return "CURRENT_V42_FAMILY"',
                            '    if normalized.startswith("vTemporal.47.8") or normalized == "v47.8" or normalized.startswith("v47.8."):\n        return "CURRENT_V47_FAMILY"\n    if normalized.startswith("vTemporal.47") or normalized == "v47" or normalized.startswith("v47."):\n        return "HISTORICAL_V47_FAMILY"\n    if normalized == "v42" or normalized.startswith("v42.") or normalized.startswith("vTemporal.42"):\n        return "PARENT_CANONICAL_FAMILY"')
        if path.endswith("validate_version_identity.py"):
            text = text.replace('"HISTORICAL_V40",\n            "CANDIDATE_BRIDGE_HISTORY",', '"HISTORICAL_V40",\n            "CANDIDATE_BRIDGE_HISTORY",\n            "HISTORICAL_V47_FAMILY",')
            text = text.replace(
                "# Active control surfaces may reference the native version or v41\n    # family, but may not assert v39/v40 or v41.1.x as active identity.",
                "# Active controls may name the v47.8 native release and its v42.5.4\n    # parent; historical and unrelated release families are not active identity.",
            )
        text = text.replace("for v39/v40/v41/v42 families", "for v39/v40/v41/v42/v47 families")
        if "PARENT_CANONICAL_FAMILY" not in text or "CURRENT_V47_FAMILY" not in text:
            raise RuntimeError(f"Could not update release classification in {path}; nothing changed.")
        if path.endswith("regenerate_version_references.py") and "for v39/v40/v41/v42/v47 families" not in text:
            raise RuntimeError("Could not update version inventory scope; nothing changed.")
        updates[path] = text

    # Make release lineage a first-class admission: v42.5.4 components remain
    # hash-bound historical inputs, not mismatched v47.8 releases.
    spider_path = "tools/validate_spider_persona_admission.py"
    spider = (ROOT / spider_path).read_text(encoding="utf-8")
    spider = re.sub(r"(?m)^\s*(?:SPIDER_)?RELEASE\s*=.*\n", "", spider)
    spider = spider.replace('        correction = read_json(STANDING)\n', '        correction = read_json(STANDING)\n        registry = read_json(identity["component_registry"])\n        component = registry["components"]["spider_persona"]\n')
    spider = re.sub(r"\bSPIDER_RELEASE\b", "spider_release", spider)
    spider = re.sub(r"\bRELEASE\b", "version", spider)
    spider = re.sub(r"(?m)^\s*release_suffix\s*=.*$", '    release_suffix = version.removeprefix("vTemporal.").replace(".", "_")', spider)
    spider = re.sub(r'(?m)^(\s*)check_equal\(r2\.get\("target_release"\), [^,\n]+, "R2 [^"]*release", errors\)$',
                    r'\1check_equal(r2.get("target_release"), spider_release, "R2 registered source release", errors)', spider)
    spider = re.sub(r'(?m)^(\s*)check_equal\(correction\.get\("release"\), [^,\n]+, "correction [^"]*release", errors\)$',
                    r'\1check_equal(correction.get("release"), spider_release, "correction source release", errors)', spider)
    check = '    check_equal(identity.get("version"), version, "VERSION.json version", errors)'
    registry_checks = (
        '\n    check_equal(registry.get("active_release"), version, "component registry active release", errors)'
        '\n    check_equal(registry.get("canonical_branch"), identity.get("canonical_branch"), "component registry branch", errors)'
        '\n    spider_release = component.get("source_release")'
        '\n    check_equal(component.get("admission", {}).get("path"), R2, "registered Spider admission", errors)'
        '\n    check_equal(component.get("admission", {}).get("sha256"), hashlib.sha256((ROOT / R2).read_bytes()).hexdigest(), "registered Spider admission SHA-256", errors)'
        '\n    check_equal(component.get("standing_record", {}).get("path"), STANDING, "registered Spider standing record", errors)'
        '\n    check_equal(component.get("standing_record", {}).get("sha256"), hashlib.sha256((ROOT / STANDING).read_bytes()).hexdigest(), "registered Spider standing SHA-256", errors)'
    )
    if 'registry.get("active_release")' not in spider:
        spider = replace_once(spider, check, check + registry_checks, "Spider registry checks")
    if "RELEASE" in spider or 'registry.get("active_release")' not in spider or 'r2.get("target_release"), spider_release' not in spider:
        raise RuntimeError("Cannot safely adapt Spider validator; nothing changed.")
    updates[spider_path] = spider

    middleware_path = "tools/validate_middleware_admission.py"
    middleware = (ROOT / middleware_path).read_text(encoding="utf-8")
    middleware = replace_once(
        middleware,
        "    receipt = json.loads((ROOT / admission['promotion_receipt']).read_text())\n    assert admission['release'] == identity['version'] == (ROOT / 'VERSION').read_text().strip()",
        "    receipt = json.loads((ROOT / admission['promotion_receipt']).read_text())\n"
        "    registry = json.loads((ROOT / identity['component_registry']).read_text())\n"
        "    component = registry['components']['middleware']\n"
        "    assert registry['active_release'] == identity['version'] == (ROOT / 'VERSION').read_text().strip()\n"
        "    assert registry['canonical_branch'] == identity['canonical_branch'] == 'main'\n"
        "    assert component['source_release'] == admission['release']\n"
        "    assert component['admission']['path'] == admission_path\n"
        "    assert component['admission']['sha256'] == hashlib.sha256((ROOT / admission_path).read_bytes()).hexdigest()",
        "middleware validator",
    )
    updates[middleware_path] = middleware

    flow_path = "tools/validate_flow_math_admission.py"
    flow = (ROOT / flow_path).read_text(encoding="utf-8")
    flow = replace_once(
        flow,
        "    version = json.loads((root / 'VERSION.json').read_text())\n    if a['release'] != version['version'] or version['flow_math_admission'] != admission_path:",
        "    version = json.loads((root / 'VERSION.json').read_text())\n"
        "    registry = json.loads((root / version['component_registry']).read_text())\n"
        "    component = registry['components']['relational_flow_math']\n"
        "    if registry.get('active_release') != version['version']:\n        raise ValueError('component registry active release mismatch')\n"
        "    if component['source_release'] != a['release'] or component['admission']['path'] != admission_path:\n        raise ValueError('flow-math component registry lineage mismatch')\n"
        "    for key in ('admission', 'origin_contract', 'promotion_receipt', 'port_record'):\n"
        "        item = component[key]\n        actual = hashlib.sha256((root / item['path']).read_bytes()).hexdigest()\n"
        "        if actual != item['sha256']:\n            raise ValueError(f'registered flow-math {key} hash mismatch')\n"
        "    if component['originating_candidate_commit'] != a['originating_candidate_commit'] or component['transport_artifact_sha256'] != a['transport_artifact_sha256']:\n        raise ValueError('originating candidate or transport digest registry mismatch')\n"
        "    if a['release'] != version['version'] or version['flow_math_admission'] != admission_path:",
        "flow-math validator",
    )
    updates[flow_path] = flow

    # Ensure the identity validator actually validates the registry pointer.
    identity_path = "tools/validate_version_identity.py"
    identity_tool = updates[identity_path]
    identity_tool = replace_once(
        identity_tool,
        '    if metadata.get("authority_contract") != "VERSION_AUTHORITY.md":',
        '    registry_rel = metadata.get("component_registry")\n'
        '    if not isinstance(registry_rel, str) or not registry_rel or Path(registry_rel).is_absolute() or ".." in Path(registry_rel).parts:\n'
        '        errors.append("VERSION.json component_registry is missing or unsafe")\n'
        '    else:\n'
        '        try:\n'
        '            registry = json.loads((root / registry_rel).read_text(encoding="utf-8"))\n'
        '            if registry.get("active_release") != native_version:\n'
        '                errors.append("component registry active_release does not match VERSION")\n'
        '            if registry.get("canonical_branch") != metadata.get("canonical_branch"):\n'
        '                errors.append("component registry canonical_branch does not match VERSION.json")\n'
        '        except Exception as exc:\n'
        '            errors.append(f"component registry invalid: {exc}")\n\n'
        '    if metadata.get("authority_contract") != "VERSION_AUTHORITY.md":',
        "version identity validator",
    )
    updates[identity_path] = identity_tool

    # Preflight every patch before writing any file.
    for path, text in updates.items():
        if path not in FILES:
            raise RuntimeError(f"Unexpected file in update set: {path}")
    for path, text in updates.items():
        dest = ROOT / path
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(text, encoding="utf-8")

    # Stage before generation so the tracked-file inventory includes the new registry.
    git("add", *sorted(FILES))
    # Regenerate only the index. This is not a test run.
    git("add", "VERSION_REFERENCES.json")
    subprocess.run([sys.executable, "tools/regenerate_version_references.py"], cwd=ROOT, check=True)
    git("add", "VERSION_REFERENCES.json")

    git("commit", "-m", "fix: register v47.8 component lineage", "--", *sorted(FILES))
    git("push", "origin", "main")
    print(f"PUSHED {git('rev-parse', 'HEAD')} to origin/main")
    print("Registry records v42.5.4 Spider/middleware inheritance and v47.8 flow-math origin hashes.")
    print("No tests were run.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"REGISTRY UPDATE STOPPED: {exc}", file=sys.stderr)
        raise SystemExit(1)
