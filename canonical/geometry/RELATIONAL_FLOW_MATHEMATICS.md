# Relational Flow Mathematics — additive formal successor

Standing: CANONICAL MATHEMATICAL SUPPLEMENT upon the Human-authorized main publication.
Authority NONE. Human Gate ACTIVE. No Compression Out ACTIVE.
Source authorization: Human, 2026-10-05 America/New_York: “we need to patch the MATHS!!! Then restack and redeploy!!!”
Source candidate baseline: main `bf8c82dfb911ba4eac4b984c77ace741c4e81c6f`, vTemporal.42.5.4. Port baseline: vTemporal.47.8.0 main `1e2847133eb69c925dcb85fa91bf1fe17919e4b2`.

## 1. Source, operation, and claim boundaries

Load the complete frozen `canonical/geometry/RELATIONAL_FLOW_PRESSURE_VORTEX_CROSS_SCALE_GEOMETRY.md` before this supplement. Its bytes, original qualification receipts, and unresolved historical definitions remain unchanged. This is new formal development, not recovery of historical equations. The operation is additive formalization, synthetic calculation, qualification, load-path integration, and publication. Producer: Codex middleware; no independently credentialed Tech, Spider, or Audit invocation is asserted. Chat WORK_ID NONE; component WORK IDs UNKNOWN / NOT RETRIEVED.

The formulas below define scoped models. A model identity, receipt match, arithmetic pass, or publication does not validate a physical mechanism. Real applications must qualify variable meanings, observations, units, lineage, parameter estimates, assumptions, uncertainty, and applicability. Unknown observations remain unknown. Do not turn an empty measurement set into zero flow.

## 2. Typed inventory and transport

For a declared domain and observation interval, let G=(N,E) be a directed multigraph. Each edge has a fixed reference orientation, source/target, material type, transfer rule, access condition, and capacity. Let B have -1 at the edge's source and +1 at its target. An amount s_i has unit U; a signed rate q_e has U/T. Distinguish external addition a_i, actual removal d_i, and a net transformation term r_i. Then

    ds/dt = B q + a - d + r.
    s(t1)-s(t0) = B integral(q dt) + integral((a-d+r) dt).

The executable checker accepts actual interval totals, not instantaneous rates silently multiplied by duration. For constant rates, interval total is q*Delta_t. For sampled rates use a declared quadrature/interpolation rule and its error; timestamps alone do not establish interval coverage.

Internal edges cancel in the total: 1^T B=0. Thus total inventory changes by admitted external additions, removals, and transformations. This is an accounting identity only for the declared quantity. Information copying is not conserved byte inventory: represent duplication as a transformation or use separately typed source/derived inventories with lineage. Do not add messages, bytes, joules, confidence, and people in one stock vector. Multiple material types require separate balances and explicit conversion relations.

Drain is a declared removal boundary d. Pipe is an admissible transport edge/path, possibly with delay and capacity. Flow is the measured transfer q or interval total. They are distinct objects. For delayed transfer, model in-transit stock explicitly; arrival and departure cannot be asserted simultaneous. Capacity K bounds admissible |q| for a bidirectional edge; directed-only edges separately prohibit negative q.

## 3. Constraint, driving potential, and pressure development

Declare a potential p with unit P and edge conductance k with U/(T*P). A conditional linear constitutive model is

    q_e = k_e (p_source-p_target), k_e >= 0.

It is a model choice, not a universal law. Holding k and the potential difference fixed gives fixed q. Changing k changes flow even with unchanged source capability. A zero conductance blocks modeled transport; it does not prove a real observed obstruction. Saturation, inertia, valves, feedback, nonlinear conductance, and path-dependent effects need their own equations.

For a locally qualified storage relation s=C*p with constant C>0, C has U/P and

    C dp/dt = net inflow + addition - drain + transformation.

A reservoir with inflow 2 U/T, drain 1 U/T, C=2 U/P has dp/dt=0.5 P/T without a newly introduced external forcing event. That calculation demonstrates possibility under the chosen assumptions. It does not establish internal force origin: the initial/boundary conditions and earlier inflow remain attributable. If C changes, d(Cp)/dt=C dp/dt+p dC/dt; omit no term. Pressure may mean physical pressure only in a qualified physical model; computational potential/backlog is separately typed.

## 4. Backflow and back-pressure

Fix reference orientation before examining the return. A measured interval total v<0 establishes reverse net transfer on that edge over that interval; mixed positive/negative subintervals can cancel, so zero net transfer does not establish stagnation. Let qualified uncertainty be [v_lo,v_hi]. If v_hi<0 the interval supports net backflow; if v_lo>0 it supports forward flow; [0,0] supports zero net transfer; otherwise sign is unresolved. An interval crossing zero is not absence or backflow. The range is supplied evidence, not an invented confidence interval.

Under the conditional conductance law with k>0, a reversed potential difference gives reversed modeled rate. A pressure rise alone does not establish backflow: a closed valve can have q=0 at nonzero pressure. A measured backflow can also have inertial or external forcing terms outside this simple law. The historical Back-pressure↔Backflow relation remains unresolved. This supplement supplies a conditional pressure/transport relation rather than retroactively declaring those terms synonyms.

## 5. Circulation and vortex discrimination

Graph cycle existence is structural possibility. A declared oriented cycle c satisfies Bc=0. A cycle-rate component alpha*c therefore changes no node inventory while retaining nonzero circulation. Example: three nodes A→B→C→A, each edge rate 1, give Bq=0 and sum |q|=3. Equal stocks and zero net accumulation do not imply no movement.

The checker verifies a simple oriented cycle from observed interval transfers and their lineage references: each signed transfer follows the proposed traversal, and the minimum absolute transfer is a possible common circulation component. Subtracting that component leaves an attributable residual. This is a decomposition of aggregate interval totals, not proof that the same item traversed the whole loop, that legs were simultaneous, that information was trapped, or that a fluid vortex existed. Such claims require item identity and event ordering, interval overlap, residence/escape observations, and a relevant dynamical model. A cycle with no qualified transfer evidence remains unverified.

For a qualified physical velocity field u(x,t), vorticity is omega=curl(u), and circulation around a declared contour is Gamma=integral(u dot dl). Nonzero local vorticity alone does not identify a coherent vortex: steady shear can have nonzero curl. Required additional evidence includes spatial/temporal structure and the chosen vortex criterion. Graph circulation is not fluid vorticity and neither is automatically the canonical historical Vortex definition. That definition remains a separate qualification surface.

## 6. Burst and stability

A separately qualified burst model can declare failure at p>=p_crit, or s>=s_crit, with an explicit transition/output and uncertainty. A threshold is a supplied model parameter; crossing it does not establish a real rupture. Backflow need not reach it. A reservoir with dp/dt=0 or a stable equilibrium supplies a counterexample to burst inevitability. For dynamics dx/dt=f(x), a local stability calculation requires an identified equilibrium f(x*)=0 and Jacobian; its eigenvalues describe the local linearization within its assumptions, not global stability or actor intent.

## 7. Cross-scale qualification and physical branch

The graph accounting identity can transfer between systems only after independently mapping units, stocks, boundaries, transformations, timing, and uncertainty. Constitutive/dynamical laws do not transfer by analogy. In a qualified fluid branch, mass continuity is partial_t rho + div(rho*u)=0 without mass sources. For steady fully developed incompressible Newtonian laminar flow in a circular pipe with no-slip walls, Q=pi*r^4*Delta_p/(8*mu*L). Changing radius by one half gives Q/16 at fixed pressure difference, viscosity, and length. These conditions do not apply automatically to information or interacting solar systems.

Physical references (primary teaching materials; equations paraphrased, not a claim of validation): MIT OCW, 8.09 Classical Mechanics III, Chapter 6, https://ocw.mit.edu/courses/8-09-classical-mechanics-iii-fall-2014/3bfed6897483f5c55bf615ed583af603_MIT8_09F14_Chapter_6.pdf ; MIT OCW, 2.25 Advanced Fluid Mechanics, Couette & Poiseuille Flows, https://ocw.mit.edu/courses/2-25-advanced-fluid-mechanics-fall-2013/resources/mit2_25f13_couet_and_pois/ . The discrete graph and interval derivations here are newly developed for this supplement.

Cosmology remains the source counterobject. No collision simulation, cosmological equivalence, universal fluid equation, or agency inference is supplied. A qualified split into accounting geometry and distinct system dynamics is the present mathematical disposition.

## 8. Q1–Q14 disposition and remaining work

| Source test | Formal contribution | Standing |
| --- | --- | --- |
| Q1 Path | Conductance/capacity and typed graph change | Synthetic model calculation |
| Q2 Pressure | Storage imbalance with constant earlier input | Synthetic model calculation |
| Q3 Origin | Preserve initial/boundary/forcing lineage | Attribution requirement; actual origin unmeasured |
| Q4 Vortex | Separate graph cycle, observed transfer, curl, coherent vortex | Discrimination requirement; historical definition unresolved |
| Q5 Backflow | Signed measured interval and uncertainty against fixed orientation | Executable interval classification |
| Q6 Back-pressure | Conditional constitutive relation, blocked-edge counterexample | Historical relation unresolved |
| Q7 Burst | Separate threshold dynamics; non-burst counterexample | Model-only; empirical threshold unresolved |
| Q8 Agency | No actor variable inferred from structure | Preserved exclusion |
| Q9 Scale | Typed accounting relation may transfer | Conditional mapping requirement |
| Q10 Scale failure | Constitutive physics does not transfer by resemblance | Explicit qualified split |
| Q11 Primitives | No invented Slam/Collapse/Expansion/Reduction definition | Unresolved preserved |
| Q12 Economy | No invented Economy-1/Economy-2 definition | Unresolved preserved |
| Q13 Composition | Shared accounting, distinct constitutive dynamics | Bounded mathematical composition |
| Q14 Split | Graph transport versus physical fluids versus cosmology | Split retained with common source lineage |

This table is not full empirical execution of the source test program. Implemented checks cover interval balance, conductance, uncertainty-aware backflow, and qualified simple-cycle decomposition. Remaining real-system work: observations and error bounds, dimensional mappings, parameter fitting and holdout validation, delayed/inertial dynamics, physical vortex discrimination, empirical burst thresholds, cross-scale counterobject runs, and historical definition retrieval. No ROC/AUROC or detection statistic is estimable from these synthetic cases.

## 9. Return and re-inspection

Return the original question, exact input snapshot, declared model, units, source references, calculations, residuals, uncertainty, alternatives, and actual scope. Separate receipt integrity from semantic qualification. `FLOW_MATH_ADMISSION.json` binds this full supplement, the executable checker, tests, and the unchanged frozen parent. Re-inspection verifies those bytes, then checks the interpretation against their actual statements and assumptions. A failed interpretation changes its dependent findings without altering origin bytes. Entry loading is integration, not independently executed persona return. End each bounded run after its attributable return.
