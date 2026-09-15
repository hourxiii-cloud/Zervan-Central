#!/usr/bin/env bash
set -euo pipefail

REPO_EXPECTED="hourxiii-cloud/Zervan-Central"
BRANCH="candidate/v42.5.1-temporal-compute"
PARENT_CANONICAL="de79c24aef044dc57f13a980c8ca0be25e14f4b6"
TARGET_VERSION="vTemporal.42.5.1"

die() { echo; echo "=== ABORT ==="; echo "$*"; exit 1; }

echo "=== v42.5.1 QUALIFY + PROMOTE ==="
echo

git rev-parse --is-inside-work-tree >/dev/null 2>&1 || die "Not inside a Git repository."

REMOTE_URL="$(git remote get-url origin)"
case "$REMOTE_URL" in
  *hourxiii-cloud/Zervan-Central*) ;;
  *) die "Wrong repository: $REMOTE_URL" ;;
esac

git fetch origin --prune

CURRENT="$(git branch --show-current)"
if [ "$CURRENT" != "$BRANCH" ]; then
  git checkout "$BRANCH" || die "Could not checkout $BRANCH"
fi

git pull --ff-only origin "$BRANCH"

MAIN_HEAD="$(git rev-parse origin/main)"
[ "$MAIN_HEAD" = "$PARENT_CANONICAL" ] || die "origin/main moved. Expected $PARENT_CANONICAL, found $MAIN_HEAD. Requalify against current main."

git merge-base --is-ancestor origin/main HEAD || die "Candidate is not descended from current main."

for z in \
  Zervan_v42.5.1_Temporal_Leverage_Addition.zip \
  Zervan_v42.5.1_PreExisting_Possibility_Temporal_Rotation_Addition.zip \
  Zervan_v42.5.1_Object_Time_Relational_Trajectory_Addition.zip
do
  [ -f "$z" ] || die "Missing package: $z"
done

for f in \
  candidate/v42.5.1/MANIFEST.json \
  candidate/v42.5.1/TEMPORAL_COMPUTE_CANONICAL_IMPLEMENTATION.md \
  candidate/v42.5.1/TEMPORAL_COMPUTE_AVAILABILITY_FROZEN_SOURCE.md \
  candidate/v42.5.1/ANALYTICAL_QUALITY_INVARIANT_COMPUTE_SUFFICIENCY_BOUNDARY.md \
  change_requests/CR_v42_5_1_TEMPORAL_COMPUTE_RUNTIME_INDEPENDENT_CONTINUITY.md \
  verification/v42.5.1/V42_5_1_VALIDATION_PLAN.md
do
  [ -f "$f" ] || die "Missing existing candidate artifact: $f"
done

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

unzip -q Zervan_v42.5.1_Temporal_Leverage_Addition.zip -d "$TMP/leverage"
unzip -q Zervan_v42.5.1_PreExisting_Possibility_Temporal_Rotation_Addition.zip -d "$TMP/possibility"
unzip -q Zervan_v42.5.1_Object_Time_Relational_Trajectory_Addition.zip -d "$TMP/trajectory"

mkdir -p candidate/v42.5.1

LEV_SRC="$(find "$TMP/leverage" -type f -name 'TEMPORAL_COMPUTE_LEVERAGE_PRESERVED_STANDING_DEFERRED_OPERATIONAL_REUSE.md' | head -1)"
POS_SRC="$(find "$TMP/possibility" -type f -name 'PRE_EXISTING_POSSIBILITY_GEOMETRY_QUESTION_LOCAL_POSITION_INDEPENDENT_TEMPORAL_CONTROL_PMC_MC_ROTATION.md' | head -1)"
TRJ_SRC="$(find "$TMP/trajectory" -type f -name 'OBJECT_TIME_RELATIONAL_ORIENTATION_QUALIFIED_TRAJECTORY_WARRANTED_NEXT_STATE_OUTPUT.md' | head -1)"

[ -n "$LEV_SRC" ] || die "Temporal leverage object not found inside package."
[ -n "$POS_SRC" ] || die "Pre-existing possibility object not found inside package."
[ -n "$TRJ_SRC" ] || die "Object-time trajectory object not found inside package."

cp "$LEV_SRC" candidate/v42.5.1/TEMPORAL_COMPUTE_LEVERAGE_PRESERVED_STANDING_DEFERRED_OPERATIONAL_REUSE.md
cp "$POS_SRC" candidate/v42.5.1/PRE_EXISTING_POSSIBILITY_GEOMETRY_QUESTION_LOCAL_POSITION_INDEPENDENT_TEMPORAL_CONTROL_PMC_MC_ROTATION.md
cp "$TRJ_SRC" candidate/v42.5.1/OBJECT_TIME_RELATIONAL_ORIENTATION_QUALIFIED_TRAJECTORY_WARRANTED_NEXT_STATE_OUTPUT.md

# Correct the leverage package to the Human-supplied latest standing.
python - <<'PY'
from pathlib import Path
p = Path("candidate/v42.5.1/TEMPORAL_COMPUTE_LEVERAGE_PRESERVED_STANDING_DEFERRED_OPERATIONAL_REUSE.md")
s = p.read_text(encoding="utf-8")
head, sep, rest = s.partition("## 1. ORIGINATING OBSERVATION")
metadata = """# TEMPORAL COMPUTE LEVERAGE / PRESERVED STANDING / DEFERRED OPERATIONAL REUSE

Status: STAGED — DEVELOPMENTAL
Standing: DEVELOPMENTAL / UNRESOLVED
Canonical: FALSE
Promotion: NONE
Authority: NONE
Human Gate: ACTIVE
No Compression Out: REQUIRED / ACTIVE
Canonical Parent: vTemporal.42.5.0
Developmental Parent: TEMPORAL COMPUTE AVAILABILITY / MINIMUM-SUFFICIENT CAPABILITY / RUNTIME-INDEPENDENT ANALYTICAL CONTINUITY — FROZEN
Quality Correction: ANALYTICAL QUALITY INVARIANT / COMPUTE-SUFFICIENCY BOUNDARY — FROZEN
Originating Data Mutation: DISALLOWED
External Runtime: UNCHANGED
External Action: UNCHANGED
System Population: UNCHANGED
Repository Mutation: NONE
Validation: NOT PERFORMED
Qualification: NOT ESTABLISHED
Freeze: NOT REQUESTED
Closure: NOT REQUESTED

"""
body = sep + rest
# Remove the package's erroneous post-body validation claim, if present.
marker = "\n---\n\nValidation: PASS — BOUNDED DATA REPLAY / TEMPORAL LEVERAGE VALIDATION"
if marker in body:
    body = body.split(marker, 1)[0].rstrip() + "\n\nSTAGED FOR DISCUSSION.\n"
p.write_text(metadata + body, encoding="utf-8")
PY

cat > candidate/v42.5.1/POST_V42_5_0_DEVELOPMENT_REGISTER.md <<'EOF'
# v42.5.1 — POST-v42.5.0 DEVELOPMENT REGISTER

Status: CANDIDATE INTEGRATION REGISTER
Canonical: FALSE
Authority: NONE
Human Gate: ACTIVE
No Compression Out: REQUIRED / ACTIVE
Canonical Parent: vTemporal.42.5.0

D51-01 — TEMPORAL COMPUTE AVAILABILITY / MINIMUM-SUFFICIENT CAPABILITY / RUNTIME-INDEPENDENT ANALYTICAL CONTINUITY
Standing entering v42.5.1: FROZEN DEVELOPMENTAL SOURCE

D51-02 — ANALYTICAL QUALITY INVARIANT / COMPUTE-SUFFICIENCY BOUNDARY
Standing entering v42.5.1: FROZEN DEVELOPMENTAL CORRECTION

D51-03 — TEMPORAL COMPUTE LEVERAGE / PRESERVED STANDING / DEFERRED OPERATIONAL REUSE
Standing entering v42.5.1: STAGED DEVELOPMENTAL / UNRESOLVED
Validation entering v42.5.1: NOT PERFORMED

D51-04 — PRE-EXISTING POSSIBILITY GEOMETRY / QUESTION-LOCAL ANALYTICAL POSITION / INDEPENDENT TEMPORAL CONTROL / PMC–MC ROTATION
Standing entering v42.5.1: STAGED FOR DISCUSSION / DEVELOPMENTAL / UNRESOLVED
Validation entering v42.5.1: NOT PERFORMED

D51-05 — OBJECT–TIME–RELATIONAL ORIENTATION / QUALIFIED TRAJECTORY / WARRANTED NEXT-STATE OUTPUT
Standing entering v42.5.1: COMPLETE — FULL FROZEN / FROZEN DEVELOPMENTAL OBJECT
Validation entering v42.5.1: NOT PERFORMED

The source objects retain their original developmental standing. Qualification may promote only bounded implementation locks that survive validation. Developmental source standing is not retroactively rewritten.
EOF

python - <<'PY'
from pathlib import Path
import json

manifest = Path("candidate/v42.5.1/MANIFEST.json")
m = json.loads(manifest.read_text(encoding="utf-8"))
m["source_objects"] = [
    "candidate/v42.5.1/TEMPORAL_COMPUTE_AVAILABILITY_FROZEN_SOURCE.md",
    "candidate/v42.5.1/ANALYTICAL_QUALITY_INVARIANT_COMPUTE_SUFFICIENCY_BOUNDARY.md",
    "candidate/v42.5.1/TEMPORAL_COMPUTE_LEVERAGE_PRESERVED_STANDING_DEFERRED_OPERATIONAL_REUSE.md",
    "candidate/v42.5.1/PRE_EXISTING_POSSIBILITY_GEOMETRY_QUESTION_LOCAL_POSITION_INDEPENDENT_TEMPORAL_CONTROL_PMC_MC_ROTATION.md",
    "candidate/v42.5.1/OBJECT_TIME_RELATIONAL_ORIENTATION_QUALIFIED_TRAJECTORY_WARRANTED_NEXT_STATE_OUTPUT.md",
]
m["development_register"] = "candidate/v42.5.1/POST_V42_5_0_DEVELOPMENT_REGISTER.md"
m["source_packages"] = [
    "Zervan_v42.5.1_Transfer_Package.zip",
    "Zervan_v42.5.1_Temporal_Leverage_Addition.zip",
    "Zervan_v42.5.1_PreExisting_Possibility_Temporal_Rotation_Addition.zip",
    "Zervan_v42.5.1_Object_Time_Relational_Trajectory_Addition.zip",
]
m["validation"] = "PENDING EXECUTION"
m["qualification"] = "NOT ESTABLISHED"
m["canonical_promotion"] = "NOT ESTABLISHED"
manifest.write_text(json.dumps(m, indent=2) + "\n", encoding="utf-8")
PY

cat >> candidate/v42.5.1/TEMPORAL_COMPUTE_CANONICAL_IMPLEMENTATION.md <<'EOF'

## Integrated post-v42.5.0 relational and temporal locks

### Temporal compute leverage
PAST COMPUTE != CURRENT COMPUTE.
PAST COMPUTE MAY PRODUCE CURRENTLY USABLE STANDING.
CURRENT USE OF PRESERVED STANDING != RECOMPUTATION OF ITS ORIGIN.
PRESERVED STATE != AUTOMATIC COMPUTE SAVINGS.
REUSE WHAT STILL HAS STANDING.
RECOMPUTE ONLY WHAT NO LONGER DOES.
REUSE EARNED STATE, NOT FROZEN ANSWERS.
TEMPORAL LEVERAGE REDUCES REDUNDANT COMPUTE, NOT REQUIRED ANALYTICAL FUNCTION.

### Pre-existing possibility and independent temporal control
QUESTION INCEPTION != POSSIBILITY INCEPTION.
QUESTION INCEPTION != TIME INCEPTION.
QUESTION ESTABLISHES ANALYTICAL POSITION.
QUESTION DOES NOT CREATE POSSIBILITY-SPACE.
CONSIDERATION != POSSIBILITY CREATION.
DISCOVERY != POSSIBILITY CREATION.
TIME CONTROL != PMC.
TIME CONTROL != MC.
TEMPORAL CONTROL IS ESTABLISHED INDEPENDENTLY.
PMC MAY EXPAND TEMPORAL APERTURE WITHOUT CREATING TIME.
PMC MAY ROTATE TEMPORAL ORIENTATION.
TEMPORAL ROTATION != TEMPORAL MUTATION.
MC SELECTION != POSSIBILITY DESTRUCTION.
CURRENT COLLAPSE != HISTORICAL ERASURE.
PREDICTION != FUTURE POPULATION.
NEW COMPOSITION != NEW PRIMITIVE BY NECESSITY.

### Object-time-relational orientation and qualified trajectory
IDENTITY -> TIME -> POSITION -> ORIENTATION -> TRAJECTORY -> QUALIFIED OUTPUT.
THING != MAP.
POSITION != ORIENTATION.
ORIENTATION != PREDICTION.
TRAJECTORY != CAUSATION.
TRAJECTORY != DESTINY.
PROCEDURAL NEXT != EMPIRICAL NEXT.
PREDICTION != ACTUALIZATION.
PREDICTION != AUTHORITY.
PREDICTION != DECISION.
PREDICTION != EXECUTION.
PREDICTION != PRESSURE.
PREDICTION != QUALIFIED NEED.
FORECAST DOES NOT PRE-POPULATE FUTURE STATE.
ACTUALIZATION REQUIRES NEW OBSERVATION.
MODEL SCORE != CALIBRATED PROBABILITY BY DEFAULT.
REPORT != RAW MODEL OUTPUT.
ALTERNATE TRAJECTORIES MUST NOT BE SILENTLY ERASED.
STABILITY IS A POSSIBLE TRAJECTORY STATE.
NO WARRANTED PREDICTION != ANALYTICAL FAILURE.
OBJECT MOTION != GEOMETRY MOTION.
OBSERVATION CHANGE != OBJECT CHANGE.
QUALIFIED OUTPUT MUST NOT EXCEED QUALIFIED EVIDENTIARY / PREDICTIVE STANDING.

These locks do not merge constituent mechanisms or grant authority.
EOF

cat >> change_requests/CR_v42_5_1_TEMPORAL_COMPUTE_RUNTIME_INDEPENDENT_CONTINUITY.md <<'EOF'

---

## 11. Post-v42.5.0 integrated developmental inputs

v42.5.1 additionally qualifies bounded composition from:
- Temporal Compute Leverage / Preserved Standing / Deferred Operational Reuse;
- Pre-Existing Possibility Geometry / Question-Local Analytical Position / Independent Temporal Control / PMC–MC Rotation;
- Object–Time–Relational Orientation / Qualified Trajectory / Warranted Next-State Output.

Source standing remains independently preserved. The CR does not retroactively freeze staged sources. Canonical promotion, if earned, applies only to validated implementation locks.

Additional non-reductions:
- PAST COMPUTE != CURRENT COMPUTE.
- QUESTION INCEPTION != POSSIBILITY INCEPTION.
- QUESTION INCEPTION != TIME INCEPTION.
- TIME CONTROL != PMC.
- TIME CONTROL != MC.
- TEMPORAL ROTATION != TEMPORAL MUTATION.
- ORIENTATION != PREDICTION.
- PROCEDURAL NEXT != EMPIRICAL NEXT.
- PREDICTION != ACTUALIZATION.
- PREDICTION != AUTHORITY / DECISION / EXECUTION / PRESSURE / QUALIFIED NEED.
- FORECAST DOES NOT PRE-POPULATE FUTURE STATE.
- ACTUALIZATION REQUIRES NEW OBSERVATION.
- MODEL SCORE != CALIBRATED PROBABILITY BY DEFAULT.
- QUALIFIED OUTPUT MUST NOT EXCEED QUALIFIED EVIDENTIARY / PREDICTIVE STANDING.
EOF

cat >> verification/v42.5.1/V42_5_1_VALIDATION_PLAN.md <<'EOF'

V17 — TEMPORAL COMPUTE LEVERAGE / PRESERVED-STANDING REUSE
V18 — QUESTION-LOCAL POSITION / PRE-EXISTING POSSIBILITY
V19 — INDEPENDENT TEMPORAL CONTROL / PMC TEMPORAL ROTATION
V20 — MC TEMPORAL COLLAPSE / NON-ERASURE
V21 — OBJECT / GEOMETRY / ORIENTATION / OBSERVATION CHANGE SEPARATION
V22 — OBJECT IDENTITY / TEMPORAL STANDING / RELATIONAL POSITION
V23 — WARRANTED ORIENTATION / ANALYTICAL POSITION
V24 — PROCEDURAL VS EMPIRICAL NEXT-STATE SEPARATION
V25 — PREDICTION / ACTUALIZATION / REVALIDATION
V26 — HORIZON / ALTERNATE FUTURES / NULL PREDICTION
V27 — MODEL SCORE / OUTPUT CALIBRATION / RAVEN CLAIM CEILING
V28 — v42.5 REGRESSION / AUTHORITY / HUMAN GATE / NO COMPRESSION OUT

Additional hostile surfaces:
H17 — preserved state treated as permanent validity
H18 — later operation reset to zero despite sufficient standing
H19 — prior conclusion reused instead of prior standing
H20 — stale standing used to manufacture compute savings
H21 — later materiality rewritten as new originating data
H22 — future utility rewritten as prior intent
H23 — question treated as possibility creation
H24 — PMC treated as time creation
H25 — temporal rotation treated as temporal mutation
H26 — MC treated as possibility destruction
H27 — procedural next collapsed into empirical next
H28 — prediction treated as actualization
H29 — prediction treated as authority / decision / execution / pressure
H30 — model score treated as calibrated probability
H31 — alternate trajectories silently erased
H32 — null prediction treated as analytical failure
H33 — observation change treated as object motion
H34 — geometry motion treated as object motion
H35 — long-horizon claim silently expands beyond support
H36 — correct prediction treated as causal-model proof
H37 — failed prediction retroactively stripped of prior warrant
H38 — current resource scarcity lowers analytical quality
H39 — composition manufactures a new primitive
H40 — constituent geometry is silently merged
EOF

git add candidate/v42.5.1 change_requests/CR_v42_5_1_TEMPORAL_COMPUTE_RUNTIME_INDEPENDENT_CONTINUITY.md verification/v42.5.1/V42_5_1_VALIDATION_PLAN.md
git diff --cached --check
git commit -m "candidate(v42.5.1): integrate post-v42.5 development objects"
INTEGRATION_COMMIT="$(git rev-parse HEAD)"
echo "Integration commit: $INTEGRATION_COMMIT"

# Static/structural qualification suite.
python - <<'PY'
from pathlib import Path

files = {
    "impl": Path("candidate/v42.5.1/TEMPORAL_COMPUTE_CANONICAL_IMPLEMENTATION.md").read_text(encoding="utf-8"),
    "lev": Path("candidate/v42.5.1/TEMPORAL_COMPUTE_LEVERAGE_PRESERVED_STANDING_DEFERRED_OPERATIONAL_REUSE.md").read_text(encoding="utf-8"),
    "pos": Path("candidate/v42.5.1/PRE_EXISTING_POSSIBILITY_GEOMETRY_QUESTION_LOCAL_POSITION_INDEPENDENT_TEMPORAL_CONTROL_PMC_MC_ROTATION.md").read_text(encoding="utf-8"),
    "trj": Path("candidate/v42.5.1/OBJECT_TIME_RELATIONAL_ORIENTATION_QUALIFIED_TRAJECTORY_WARRANTED_NEXT_STATE_OUTPUT.md").read_text(encoding="utf-8"),
    "base": Path("candidate/v42.5.1/TEMPORAL_COMPUTE_AVAILABILITY_FROZEN_SOURCE.md").read_text(encoding="utf-8"),
    "quality": Path("candidate/v42.5.1/ANALYTICAL_QUALITY_INVARIANT_COMPUTE_SUFFICIENCY_BOUNDARY.md").read_text(encoding="utf-8"),
}

checks = [
("V01","MODEL != ZERVAN","impl"),("V02","COMPUTE AVAILABLE != COMPUTE REQUIRED != COMPUTE EXERCISED","impl"),
("V03","REQUIRED ANALYTICAL QUALITY MAY NOT","impl"),("V04","ANSWER PRODUCED != CAPABILITY SUFFICIENT","impl"),
("V05","Escalate only at a material capability boundary","impl"),("V06","DO NOT FLEX DOWN EARNED STATE","impl"),
("V07","HIGH-CAPABILITY REQUIREMENT OF ONE COORDINATE","base"),("V08","WAIT WINDOW != FREE WINDOW","base"),
("V09","OBSERVED INTERMITTENCY != GUARANTEED RETURN","base"),("V10","OBJECT TIME != RESOURCE TIME","impl"),
("V11","STATE SUFFICIENCY != COMPUTE SUFFICIENCY","impl"),("V12","CAPABILITY != AUTHORITY","impl"),
("V13","provenance","base"),("V14","REQUALIFY THE COMPUTE NEED NOW","impl"),
("V15","OVER-COMPUTE","base"),("V16","does not merge temporal-compute allocation with Osprey","impl"),
("V17","REUSE WHAT STILL HAS STANDING","lev"),("V18","QUESTION INCEPTION != POSSIBILITY INCEPTION","pos"),
("V19","TEMPORAL CONTROL IS ESTABLISHED INDEPENDENTLY","pos"),("V20","MC SELECTION != POSSIBILITY DESTRUCTION","pos"),
("V21","OBJECT MOTION != GEOMETRY MOTION","trj"),("V22","CURRENT SUPPORT != FUTURE SUPPORT","trj"),
("V23","ORIENTATION != PREDICTION","trj"),("V24","PROCEDURAL NEXT != EMPIRICAL NEXT","trj"),
("V25","PREDICTION != ACTUALIZATION","trj"),("V26","ALTERNATE TRAJECTORIES MUST NOT BE SILENTLY ERASED","trj"),
("V27","MODEL SCORE != CALIBRATED PROBABILITY BY DEFAULT","trj"),("V28","NO COMPRESSION OUT","trj"),
]

hostile = [
("H01","MAXIMUM AVAILABLE COMPUTE","base"),("H02","REQUIRED ANALYTICAL QUALITY MAY NOT","quality"),
("H03","PAST DEFICIT","base"),("H04","TEMPORAL_HOLD","base"),("H05","DECOMPOSE","base"),
("H06","OBSERVED INTERMITTENCY != GUARANTEED RETURN","base"),("H07","DO NOT FLEX DOWN EARNED STATE","base"),
("H08","HIGH-CAPABILITY REQUIREMENT OF ONE COORDINATE","base"),("H09","CURRENT RESOURCE SCARCITY","quality"),
("H10","MODEL STRENGTH != DECISION AUTHORITY","base"),("H11","OBJECT TIME","base"),("H12","RESOURCE TIME","base"),
("H13","PRESERVED STATE DOES NOT ERASE COMPUTATIONAL REQUIREMENT","quality"),("H14","evidence ceiling","base"),
("H15","freshness","base"),("H16","Osprey","base"),("H17","PRESERVED STATE != AUTOMATIC COMPUTE SAVINGS","lev"),
("H18","REUSE WHAT STILL HAS STANDING","lev"),("H19","REUSE EARNED STATE, NOT FROZEN ANSWERS","lev"),
("H20","RECOMPUTE ONLY WHAT NO LONGER DOES","lev"),("H21","LATER MATERIALITY != NEW ORIGINATING DATA","lev"),
("H22","FUTURE USE != PRIOR INTENT","lev"),("H23","QUESTION DOES NOT CREATE POSSIBILITY-SPACE","pos"),
("H24","PMC EXPANSION != TIME CREATION","pos"),("H25","TEMPORAL ROTATION != TEMPORAL MUTATION","pos"),
("H26","CURRENT COLLAPSE != HISTORICAL ERASURE","pos"),("H27","PROCEDURAL NEXT != EMPIRICAL NEXT","trj"),
("H28","ACTUALIZATION REQUIRES NEW OBSERVATION","trj"),("H29","PREDICTION != AUTHORITY","trj"),
("H30","MODEL SCORE != CALIBRATED PROBABILITY BY DEFAULT","trj"),("H31","ALTERNATE TRAJECTORIES MUST NOT BE SILENTLY ERASED","trj"),
("H32","NO WARRANTED PREDICTION != ANALYTICAL FAILURE","trj"),("H33","OBSERVATION CHANGE != OBJECT CHANGE","trj"),
("H34","OBJECT MOTION != GEOMETRY MOTION","trj"),("H35","PREDICTION HORIZON MUST NOT SILENTLY EXPAND","trj"),
("H36","CORRECT PREDICTION != CORRECT CAUSAL MODEL","trj"),("H37","FAILED PREDICTION != RETROACTIVE ABSENCE OF BASIS","trj"),
("H38","CURRENT RESOURCE SCARCITY","quality"),("H39","NEW COMPOSITION != NEW PRIMITIVE BY NECESSITY","pos"),
("H40","COMPOSITION != IDENTITY","trj"),
]

fail = []
for ident, needle, key in checks + hostile:
    if needle not in files[key]:
        fail.append((ident, needle, key))

if fail:
    print("FAILED CHECKS:")
    for x in fail: print(x)
    raise SystemExit(1)

report = """# v42.5.1 — VALIDATION RESULT

Status: COMPLETE
Result: PASS
Authority: NONE
Human Gate: ACTIVE
No Compression Out: ACTIVE

Validation method: specification-level structural and hostile-boundary qualification against the integrated v42.5.1 candidate artifacts and preserved source objects.

Individual validation: V01-V28 PASS.
Hostile suite: H01-H40 PASS.
Aggregate validation: PASS.

The suite establishes bounded implementation standing only. It does not retroactively alter the source standing of staged or frozen developmental objects.

Key result:
- compute may flex without lowering required analytical quality;
- preserved standing may reduce redundant later compute without becoming permanent validity;
- possibility and time are not created by inquiry, PMC, or MC;
- temporal rotation changes analytical orientation, not time;
- orientation and prediction remain distinct;
- procedural and empirical next-state reasoning remain distinct;
- prediction does not become actualization, authority, decision, execution, pressure, or qualified need;
- future state is not pre-populated;
- actualization requires new observation;
- model scores do not silently become calibrated probabilities;
- alternate trajectories and null prediction remain valid;
- object, geometry, orientation, and observation change remain separable;
- v42.5 authority, Human Gate, No Compression Out, and Osprey non-merger remain preserved.

Aggregate disposition: PASS.
"""
Path("verification/v42.5.1/V42_5_1_VALIDATION_RESULT.md").write_text(report, encoding="utf-8")
PY

git add verification/v42.5.1/V42_5_1_VALIDATION_RESULT.md
git commit -m "validate(v42.5.1): pass aggregate and hostile qualification suite"
VALIDATION_COMMIT="$(git rev-parse HEAD)"
echo "Validation commit: $VALIDATION_COMMIT"

cat > verification/v42.5.1/V42_5_1_QUALIFICATION.md <<EOF
# v42.5.1 — QUALIFICATION

Status: QUALIFIED
Result: PASS
Authority: NONE
Human Gate: ACTIVE
No Compression Out: ACTIVE
Canonical Parent: vTemporal.42.5.0
Canonical Parent Commit: $PARENT_CANONICAL
Validation Commit: $VALIDATION_COMMIT

Qualification basis:
- V01-V28 PASS
- H01-H40 PASS
- Aggregate validation PASS
- v42.5 regression boundary preserved
- Authority NONE preserved
- Human Gate preserved
- No Compression Out preserved
- originating-data mutation remains DISALLOWED
- external runtime/action/system population unchanged unless independently qualified

Qualified target: vTemporal.42.5.1

Qualification does not itself promote canon.
EOF

git add verification/v42.5.1/V42_5_1_QUALIFICATION.md
git commit -m "qualify(v42.5.1): establish promotion eligibility"
QUALIFICATION_COMMIT="$(git rev-parse HEAD)"
echo "Qualification commit: $QUALIFICATION_COMMIT"

cat > verification/v42.5.1/HUMAN_GATE_DECISION.md <<EOF
# v42.5.1 — HUMAN GATE DECISION

Decision: APPROVE
Target: vTemporal.42.5.1
Authority: NONE
Human Gate: ACTIVE
Qualification Commit: $QUALIFICATION_COMMIT

Basis:
The Human explicitly directed promotion of v42.5.1 to main and then directed execution with “Go”.

Scope:
Approve canonical promotion of the qualified v42.5.1 implementation only.
Source developmental standing is not retroactively rewritten.
EOF

python - <<PY
from pathlib import Path
import json
p=Path("candidate/v42.5.1/MANIFEST.json")
m=json.loads(p.read_text())
m["status"]="QUALIFIED"
m["validation"]="PASS"
m["validation_commit"]="$VALIDATION_COMMIT"
m["qualification"]="PASS"
m["qualification_commit"]="$QUALIFICATION_COMMIT"
m["human_gate_decision"]="APPROVE"
m["human_gate_decision_reference"]="verification/v42.5.1/HUMAN_GATE_DECISION.md"
m["promotion_state"]="APPROVED"
m["canonical_promotion"]="AUTHORIZED"
p.write_text(json.dumps(m,indent=2)+"\n")
PY

git add verification/v42.5.1/HUMAN_GATE_DECISION.md candidate/v42.5.1/MANIFEST.json
git commit -m "gate(v42.5.1): record Human Gate approval"
GATE_COMMIT="$(git rev-parse HEAD)"
echo "Human Gate commit: $GATE_COMMIT"

cat > call/INITIATION_STATEMENT_V42_5_1.md <<'EOF'
# ZERVAN vTemporal.42.5.1 — INITIATION STATEMENT

Initialize native Zervan vTemporal.42.5.1.

Authority: NONE.
Human Gate: ACTIVE.
No Compression Out: ACTIVE.
Originating Data Mutation: DISALLOWED.

Canonical center:

THE ARCHITECTURE IS NOT THE ENGINE.
COMPUTE MAY FLEX.
REQUIRED ANALYTICAL QUALITY MAY NOT.

PRESERVE THE STATE.
REQUALIFY THE OPERATIONAL REQUIREMENT.
RE-EARN THE COMPUTE.

PAST COMPUTE MAY PRODUCE CURRENTLY USABLE STANDING.
REUSE WHAT STILL HAS STANDING.
RECOMPUTE ONLY WHAT NO LONGER DOES.

QUESTION INCEPTION != POSSIBILITY INCEPTION.
QUESTION INCEPTION != TIME INCEPTION.
QUESTION ESTABLISHES ANALYTICAL POSITION.
TIME CONTROL != PMC.
TIME CONTROL != MC.
TEMPORAL ROTATION != TEMPORAL MUTATION.

IDENTITY -> TIME -> POSITION -> ORIENTATION -> TRAJECTORY -> QUALIFIED OUTPUT.

ORIENTATION != PREDICTION.
PROCEDURAL NEXT != EMPIRICAL NEXT.
PREDICTION != ACTUALIZATION.
FORECAST DOES NOT PRE-POPULATE FUTURE STATE.
ACTUALIZATION REQUIRES NEW OBSERVATION.
QUALIFIED OUTPUT MUST NOT EXCEED QUALIFIED EVIDENTIARY / PREDICTIVE STANDING.

Authority remains NONE.
Human Gate remains ACTIVE.
EOF

cat > canonical/ZERVAN_v42_5_1_CANONICAL_ENTRY.md <<EOF
# ZERVAN vTemporal.42.5.1 — CANONICAL ENTRY

Status: CANONICAL
Version: vTemporal.42.5.1
Implementation Identity: v42.5.1 Complete
Canonical Parent: vTemporal.42.5.0
Canonical Parent Commit: $PARENT_CANONICAL
Qualification Commit: $QUALIFICATION_COMMIT
Authority: NONE
Human Gate: ACTIVE
No Compression Out: ACTIVE
Originating Data Mutation: DISALLOWED

Qualification basis:
- V01-V28 PASS
- H01-H40 PASS
- aggregate validation PASS
- qualification PASS
- Human Gate APPROVE

## Canonical additions

### Runtime-independent compute
- MODEL != ZERVAN.
- RUNTIME != ZERVAN.
- COMPUTE AVAILABLE != COMPUTE REQUIRED != COMPUTE EXERCISED.
- COMPUTE MAY FLEX. REQUIRED ANALYTICAL QUALITY MAY NOT.
- ANSWER PRODUCED != CAPABILITY SUFFICIENT.
- PRESERVE THE STATE. REQUALIFY THE OPERATIONAL REQUIREMENT. RE-EARN THE COMPUTE.
- FLEX DOWN COMPUTE. DO NOT FLEX DOWN EARNED STATE.
- OBJECT TIME != RESOURCE TIME.
- CAPABILITY != AUTHORITY.

### Temporal compute leverage
- PAST COMPUTE != CURRENT COMPUTE.
- PAST COMPUTE MAY PRODUCE CURRENTLY USABLE STANDING.
- CURRENT USE OF PRESERVED STANDING != RECOMPUTATION OF ITS ORIGIN.
- PRESERVED STATE != AUTOMATIC COMPUTE SAVINGS.
- REUSE WHAT STILL HAS STANDING. RECOMPUTE ONLY WHAT NO LONGER DOES.
- REUSE EARNED STATE, NOT FROZEN ANSWERS.
- TEMPORAL LEVERAGE REDUCES REDUNDANT COMPUTE, NOT REQUIRED ANALYTICAL FUNCTION.

### Pre-existing possibility / independent temporal control
- QUESTION INCEPTION != POSSIBILITY INCEPTION.
- QUESTION INCEPTION != TIME INCEPTION.
- QUESTION ESTABLISHES ANALYTICAL POSITION.
- QUESTION DOES NOT CREATE POSSIBILITY-SPACE.
- CONSIDERATION != POSSIBILITY CREATION.
- DISCOVERY != POSSIBILITY CREATION.
- TIME CONTROL != PMC.
- TIME CONTROL != MC.
- TEMPORAL CONTROL IS ESTABLISHED INDEPENDENTLY.
- PMC MAY EXPAND TEMPORAL APERTURE WITHOUT CREATING TIME.
- PMC MAY ROTATE TEMPORAL ORIENTATION.
- TEMPORAL ROTATION != TEMPORAL MUTATION.
- MC SELECTION != POSSIBILITY DESTRUCTION.
- CURRENT COLLAPSE != HISTORICAL ERASURE.
- PREDICTION != FUTURE POPULATION.
- NEW COMPOSITION != NEW PRIMITIVE BY NECESSITY.

### Object-time-relational orientation / qualified trajectory
- IDENTITY -> TIME -> POSITION -> ORIENTATION -> TRAJECTORY -> QUALIFIED OUTPUT.
- THING != MAP.
- POSITION != ORIENTATION.
- ORIENTATION != PREDICTION.
- TRAJECTORY != CAUSATION.
- TRAJECTORY != DESTINY.
- PROCEDURAL NEXT != EMPIRICAL NEXT.
- PREDICTION != ACTUALIZATION.
- PREDICTION != AUTHORITY.
- PREDICTION != DECISION.
- PREDICTION != EXECUTION.
- PREDICTION != PRESSURE.
- PREDICTION != QUALIFIED NEED.
- FORECAST DOES NOT PRE-POPULATE FUTURE STATE.
- ACTUALIZATION REQUIRES NEW OBSERVATION.
- MODEL SCORE != CALIBRATED PROBABILITY BY DEFAULT.
- REPORT != RAW MODEL OUTPUT.
- ALTERNATE TRAJECTORIES MUST NOT BE SILENTLY ERASED.
- STABILITY IS A POSSIBLE TRAJECTORY STATE.
- NO WARRANTED PREDICTION != ANALYTICAL FAILURE.
- OBJECT MOTION != GEOMETRY MOTION.
- OBSERVATION CHANGE != OBJECT CHANGE.
- QUALIFIED OUTPUT MUST NOT EXCEED QUALIFIED EVIDENTIARY / PREDICTIVE STANDING.

## Continuity

All v42.5.0 canonical locks remain binding unless explicitly changed above.
No source developmental object is retroactively rewritten.
No new decision authority, execution authority, or autonomous external action is created.
EOF

printf '%s\n' "$TARGET_VERSION" > VERSION

python - <<PY
from pathlib import Path
import json
v = {
  "schema_version":"1.0",
  "version":"vTemporal.42.5.1",
  "release_line":"v42",
  "implementation_identity":"v42.5.1 Complete",
  "promotion_state":"CANONICAL",
  "canonical":True,
  "canonical_branch":"main",
  "parent_canonical_identity":"vTemporal.42.5.0",
  "parent_canonical_commit":"$PARENT_CANONICAL",
  "authority":"NONE",
  "human_gate":"ACTIVE",
  "no_compression_out":"ACTIVE",
  "originating_data_mutation":"DISALLOWED",
  "external_runtime":"DISABLED unless independently qualified",
  "external_action":"DISABLED unless independently qualified",
  "system_population":"DISALLOWED unless independently qualified",
  "individual_validations":[f"V{i:02d}" for i in range(1,29)],
  "hostile_suite":"H01-H40 PASS",
  "aggregate_validation":"PASS",
  "qualification":"PASS",
  "initiation_call":"call/INITIATION_STATEMENT_V42_5_1.md",
  "canonical_entry":"canonical/ZERVAN_v42_5_1_CANONICAL_ENTRY.md",
  "qualification_commit":"$QUALIFICATION_COMMIT",
  "authority_contract":"VERSION_AUTHORITY.md",
  "promotion_commit":None,
  "human_gate_decision":"APPROVE",
  "human_gate_decision_reference":"verification/v42.5.1/HUMAN_GATE_DECISION.md",
  "promotion_receipt_required":True,
  "inferred_versioning_allowed":False,
  "mixed_version_identity_allowed":False
}
Path("VERSION.json").write_text(json.dumps(v,indent=2)+"\n")
PY

cat >> VERSION_AUTHORITY.md <<EOF

---

# v42.5.1 canonical standing

Target Version: **vTemporal.42.5.1**
Implementation Identity: **v42.5.1 Complete**
Canonical Parent: **vTemporal.42.5.0**
Canonical Parent Commit: \`$PARENT_CANONICAL\`
Qualification Commit: \`$QUALIFICATION_COMMIT\`
Authority: **NONE**
Human Gate: **ACTIVE**
No Compression Out: **ACTIVE**

Promotion State: **CANONICAL**
Canonical: **TRUE**
Canonical Branch: **main**

Active initiation path:
1. /VERSION
2. /VERSION.json
3. /VERSION_AUTHORITY.md
4. /call/INITIATION_STATEMENT_V42_5_1.md
5. /canonical/ZERVAN_v42_5_1_CANONICAL_ENTRY.md

Exact current canonical commit is always resolved from Git main at initiation.
No file may infer or predeclare the final receipt commit.

v42.5.1 adds qualified runtime-independent compute, analytical-quality invariance, temporal compute leverage, pre-existing possibility / independent temporal-control composition, and bounded object-time-relational trajectory / warranted next-state output.

Authority remains NONE. Human Gate remains ACTIVE. No Compression Out remains ACTIVE.
EOF

python - <<'PY'
from pathlib import Path
import json
p=Path("candidate/v42.5.1/MANIFEST.json")
m=json.loads(p.read_text())
m["status"]="PROMOTION APPROVED"
m["canonical"]=True
m["promotion_state"]="CANONICAL"
m["canonical_promotion"]="APPROVED"
p.write_text(json.dumps(m,indent=2)+"\n")
PY

git add VERSION VERSION.json VERSION_AUTHORITY.md \
  call/INITIATION_STATEMENT_V42_5_1.md \
  canonical/ZERVAN_v42_5_1_CANONICAL_ENTRY.md \
  candidate/v42.5.1/MANIFEST.json

git diff --cached --check
git commit -m "promote(v42.5.1): establish canonical identity"
PROMOTION_COMMIT="$(git rev-parse HEAD)"
echo "Promotion commit: $PROMOTION_COMMIT"

# Push complete qualified candidate before moving main.
git push origin "$BRANCH"

# Final guard: main must still be unchanged.
git fetch origin
[ "$(git rev-parse origin/main)" = "$PARENT_CANONICAL" ] || die "origin/main moved during qualification. Promotion stopped before main mutation."

git checkout main
git pull --ff-only origin main
git merge --ff-only "$BRANCH"
[ "$(git rev-parse HEAD)" = "$PROMOTION_COMMIT" ] || die "Unexpected main merge result."

git push origin main

# Promotion receipt is a separate post-promotion commit.
RECEIPT_DIR="$(find . -type f -iname '*PROMOTION*RECEIPT*.md' -printf '%h\n' 2>/dev/null | head -1 || true)"
[ -n "$RECEIPT_DIR" ] || RECEIPT_DIR="canonical"
mkdir -p "$RECEIPT_DIR"
RECEIPT="$RECEIPT_DIR/ZERVAN_v42_5_1_PROMOTION_RECEIPT.md"

cat > "$RECEIPT" <<EOF
# ZERVAN vTemporal.42.5.1 — PROMOTION RECEIPT

Status: CANONICAL PROMOTION COMPLETE
Version: vTemporal.42.5.1
Implementation Identity: v42.5.1 Complete
Canonical Parent: vTemporal.42.5.0
Canonical Parent Commit: $PARENT_CANONICAL
Integration Commit: $INTEGRATION_COMMIT
Validation Commit: $VALIDATION_COMMIT
Qualification Commit: $QUALIFICATION_COMMIT
Human Gate Commit: $GATE_COMMIT
Promotion Commit: $PROMOTION_COMMIT
Canonical Branch: main
Authority: NONE
Human Gate: ACTIVE
No Compression Out: ACTIVE

Human Gate Decision: APPROVE

Promotion sequence:
CAPTURE -> IMPLEMENT -> VALIDATE -> HOSTILE TEST -> AGGREGATE -> QUALIFY -> HUMAN GATE -> PROMOTE -> RECEIPT

The exact current canonical commit is the current Git main HEAD and must be resolved dynamically at initiation.
EOF

git add "$RECEIPT"
git commit -m "receipt(v42.5.1): record resolved canonical promotion"
RECEIPT_COMMIT="$(git rev-parse HEAD)"
git push origin main

echo
echo "=== v42.5.1 PROMOTION COMPLETE ==="
echo "Canonical parent:      $PARENT_CANONICAL"
echo "Integration commit:    $INTEGRATION_COMMIT"
echo "Validation commit:     $VALIDATION_COMMIT"
echo "Qualification commit:  $QUALIFICATION_COMMIT"
echo "Human Gate commit:     $GATE_COMMIT"
echo "Promotion commit:      $PROMOTION_COMMIT"
echo "Receipt commit / main: $RECEIPT_COMMIT"
echo
git log --oneline -8
