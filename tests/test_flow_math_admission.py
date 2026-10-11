import json
import tempfile
import unittest
from pathlib import Path
from tools.validate_flow_math_admission import ROOT, validate


class AdmissionTests(unittest.TestCase):
    def copy_bound_objects(self, dest):
        a = json.loads((ROOT / 'canonical/geometry/FLOW_MATH_ADMISSION.json').read_text())
        version = json.loads((ROOT / 'VERSION.json').read_text())
        paths = ['VERSION.json', 'canonical/geometry/FLOW_MATH_ADMISSION.json',
                 version['canonical_entry'], a['frozen_parent']['path'],
                 *[x['path'] for x in a['payloads']]]
        for rel in paths:
            p = dest / rel; p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes((ROOT / rel).read_bytes())

    def test_actual_admission(self):
        self.assertEqual(validate()['authority'], 'NONE')

    def test_tampered_math_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            dest = Path(temp); self.copy_bound_objects(dest)
            p = dest / 'canonical/geometry/RELATIONAL_FLOW_MATHEMATICS.md'
            p.write_bytes(p.read_bytes() + b'zero drift guaranteed\n')
            with self.assertRaisesRegex(ValueError, 'artifact mismatch'):
                validate(dest)

    def test_removed_load_dependency_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            dest = Path(temp); self.copy_bound_objects(dest)
            p = dest / 'canonical/ZERVAN_v42_5_4_CANONICAL_ENTRY.md'
            p.write_text(p.read_text().replace('/canonical/geometry/RELATIONAL_FLOW_MATHEMATICS.md', '/missing'))
            with self.assertRaisesRegex(ValueError, 'load missing'):
                validate(dest)

    def test_frozen_parent_edit_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            dest = Path(temp); self.copy_bound_objects(dest)
            p = dest / 'canonical/geometry/RELATIONAL_FLOW_PRESSURE_VORTEX_CROSS_SCALE_GEOMETRY.md'
            p.write_bytes(p.read_bytes() + b'rewritten origin\n')
            with self.assertRaisesRegex(ValueError, 'artifact mismatch'):
                validate(dest)
