.PHONY: smoke pmc-seal pmc-admit validate-v40-candidate test-v40-candidate

smoke:

# C + A targets will be added after we create the scripts below.

pmc-admit:
	@./tools/pmc_admit.sh

pmc-admit-dataset:
	@./tools/pmc_admit.sh --dataset "$(DATASET)"

pmc-seal:
	@./tools/pmc_seal.sh

validate-v40-candidate:
	@python candidate/v40/tools/validate_failure_inventory.py
	@python candidate/v40/tools/validate_operational_contract.py

test-v40-candidate:
	@python -m unittest discover -s tests -p 'test_v40_candidate_*.py' -v
