# Codespaces Application

## Preconditions

Run from the root of `hourxiii-cloud/Zervan-Central` with a clean worktree.

```bash
git fetch origin
git switch main
git pull --ff-only origin main
git rev-parse HEAD
```

The packaged candidate was built from:

```text
ae898ab803061823b36fb825e0664e3d8d255409
```

If current `main` differs, stop and compare before applying. Do not force the package
onto a changed baseline.

## Apply the patch

Upload `ZERVAN_v42_CANDIDATE_IMPLEMENTATION.patch` to the repository root, then run:

```bash
git switch -c candidate/v42-governed-development
git am --3way ZERVAN_v42_CANDIDATE_IMPLEMENTATION.patch
make validate-v42-candidate
make test-v42-candidate
git status --short
```

Expected candidate result:

```text
candidate v42 generated artifacts verified: 27
candidate v42 validation: PASS
Ran 26 tests
OK
```

Do not merge to `main` or modify `VERSION` during this step. Executable aggregate
closure and a separate final Human-Gate promotion decision remain required.

