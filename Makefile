.PHONY: smoke pmc-seal pmc-admit

smoke:

# C + A targets will be added after we create the scripts below.

pmc-admit:
	@./tools/pmc_admit.sh

pmc-admit-dataset:
	@./tools/pmc_admit.sh --dataset "$(DATASET)"

pmc-seal:
	@./tools/pmc_seal.sh
