"""Adversarial admission checks using isolated copies of bound documents."""
import contextlib
import io
import json
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from tools import validate_middleware_admission as validator


class MiddlewareAdmissionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        identity = json.loads((validator.ROOT / 'VERSION.json').read_text())
        admission_path = identity['middleware_admission']
        admission = json.loads((validator.ROOT / admission_path).read_text())
        self.admission = admission
        paths = ['VERSION', 'VERSION.json', identity['canonical_entry'], admission_path, admission['promotion_receipt']]
        paths += [x['path'] for x in admission['payloads'] + admission['frozen_dependencies'] + [admission['preserved_source']]]
        for relative in paths:
            target = self.root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(validator.ROOT / relative, target)

    def run_validation(self):
        with patch.object(validator, 'ROOT', self.root), contextlib.redirect_stdout(io.StringIO()):
            validator.main()

    def test_valid_bound_tree(self):
        self.run_validation()

    def test_changed_payload_rejected(self):
        target = self.root / self.admission['payloads'][0]['path']
        target.write_bytes(target.read_bytes() + b'changed')
        with self.assertRaises(AssertionError):
            self.run_validation()

    def test_frozen_mutation_rejected(self):
        target = self.root / self.admission['frozen_dependencies'][0]['path']
        target.write_bytes(target.read_bytes() + b'changed')
        with self.assertRaises(AssertionError):
            self.run_validation()

    def test_missing_entry_route_rejected(self):
        identity = json.loads((self.root / 'VERSION.json').read_text())
        target = self.root / identity['canonical_entry']
        target.write_text(target.read_text().replace('/' + identity['middleware_admission'], '/removed'))
        with self.assertRaises(AssertionError):
            self.run_validation()
