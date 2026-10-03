.PHONY: smoke pmc-seal pmc-admit pmc-admit-dataset \
	validate-v40-candidate test-v40-candidate \
	validate-v42-candidate test-v42-candidate \
	validate-v42-canonical test-v42-canonical \
	validate-v42-5-4 test-v42-5-4 \
	validate-spider-persona validate-observers test-observers \
	validate-current-canon test-current-canon test-repository check

# A bounded read-only check of the active release identity and Spider admission.
smoke: validate-v42-5-4

# These operational PMC commands are deliberately excluded from validation targets.
pmc-admit:
	@./tools/pmc_admit.sh

pmc-admit-dataset:
	@./tools/pmc_admit.sh --dataset "$(DATASET)"

pmc-seal:
	@./tools/pmc_seal.sh

# Historical candidate checks remain individually callable.
validate-v40-candidate:
	@PYTHONDONTWRITEBYTECODE=1 python candidate/v40/tools/validate_failure_inventory.py
	@PYTHONDONTWRITEBYTECODE=1 python candidate/v40/tools/validate_operational_contract.py
	@PYTHONDONTWRITEBYTECODE=1 python candidate/v40/tools/validate_control_plane.py
	@PYTHONDONTWRITEBYTECODE=1 python candidate/v40/tools/validate_continuity.py
	@PYTHONDONTWRITEBYTECODE=1 python candidate/v40/tools/validate_reporting_records.py
	@PYTHONDONTWRITEBYTECODE=1 python candidate/v40/tools/validate_reporting_inventories.py
	@PYTHONDONTWRITEBYTECODE=1 python candidate/v40/tools/validate_reporting_projection.py

test-v40-candidate:
	@PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -s tests -p 'test_v40_candidate_*.py' -v

validate-v42-candidate:
	@PYTHONDONTWRITEBYTECODE=1 python candidate/v42/tools/generate_artifacts.py --check
	@PYTHONDONTWRITEBYTECODE=1 python candidate/v42/tools/validate_v42.py --fixtures

test-v42-candidate:
	@PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -s candidate/v42/tests -p 'test_*.py' -v

validate-v42-canonical:
	@PYTHONDONTWRITEBYTECODE=1 python tools/validate_version_identity.py
	@PYTHONDONTWRITEBYTECODE=1 python candidate/v42/tools/generate_artifacts.py --check
	@PYTHONDONTWRITEBYTECODE=1 python candidate/v42/tools/validate_v42.py --fixtures

test-v42-canonical:
	@PYTHONDONTWRITEBYTECODE=1 python -m unittest tests.test_native_v42_entry -v
	@PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -s candidate/v42/tests -p 'test_*.py' -v

# The current vTemporal.42.5.4 release adds Spider R2 persona admission.
# This checks committed document integrity and metadata, not deployed runtime.
validate-spider-persona:
	@PYTHONDONTWRITEBYTECODE=1 python tools/validate_spider_persona_admission.py

validate-v42-5-4: validate-v42-canonical validate-spider-persona

# The frozen candidate suite includes an old assertion that VERSION equals
# the historical v42.0 release. Run its tests with the historical candidate
# target; current-release checks use the canonical entry and current controls.
test-v42-5-4:
	@PYTHONDONTWRITEBYTECODE=1 python -m unittest tests.test_native_v42_entry -v
	@PYTHONDONTWRITEBYTECODE=1 python -m unittest tests.test_version_identity -v
	@PYTHONDONTWRITEBYTECODE=1 python -m unittest tests.test_world_box_v42_5_2 tests.test_box_question_return_v42_5_2 -v

# Observer promotion verification is historical; its original post-promotion
# validator assumes the promotion commit is HEAD and cannot run on later main.
validate-observers:
	@PYTHONDONTWRITEBYTECODE=1 python tools/observers/validate_observer_capabilities.py

test-observers:
	@PYTHONDONTWRITEBYTECODE=1 python tests/observers/functional/run_observer_functional_tests.py

validate-current-canon: validate-v42-5-4 validate-observers

# Full repository regression includes preserved historical and current tests.
# Candidate v42 tests live outside tests/ and are therefore run separately.
test-repository:
	@PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -s tests -p 'test_*.py' -v

test-current-canon: test-v42-5-4 test-observers

check: validate-current-canon test-current-canon
