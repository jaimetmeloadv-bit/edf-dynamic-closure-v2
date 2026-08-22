"""
Dynamic Closure Notebook — Entry 14
Theorem Repair and Prediction Reconstruction
Computational certificate for the repaired mathematical statements.

The script verifies:
1. Exact CRT factorization H_12 ~= H_3 tensor H_4.
2. Three orthogonal Z3 character projectors (not only the invariant average).
3. A norm-preserving three-branch isometric embedding.
4. Twelve-event alternating B3 bookkeeping and pairwise linking numbers.
5. The distinction between pairwise-link sum (=6) and a ribbon self-linking
   number, which is not computed or assumed by this certificate.
6. Representative UV convergence/divergence for the repaired soft-regulator
   power-counting criterion.
"""

import math
from pathlib import Path
import numpy as np
import pandas as pd

OUT = Path("dynamic_closure_entry_14_output")
OUT.mkdir(parents=True, exist_ok=True)
TOL = 1e-11


def shift(k):
    x = np.zeros((k, k), dtype=complex)
    for m in range(k):
        x[(m + 1) % k, m] = 1.0
    return x


def clock(k):
    omega = np.exp(2j * np.pi / k)
    return np.diag([omega**m for m in range(k)])


def crt_permutation_12_to_3x4():
    p = np.zeros((12, 12), dtype=complex)
    for m in range(12):
        a = m % 3
        b = m % 4
        p[a * 4 + b, m] = 1.0
    return p


def crt_certificate():
    p = crt_permutation_12_to_3x4()
    x12 = shift(12)
    z12 = clock(12)
    x_expected = np.kron(shift(3), shift(4))
    z_expected = np.kron(clock(3), np.linalg.matrix_power(clock(4), 3))
    x_mapped = p @ x12 @ p.conj().T
    z_mapped = p @ z12 @ p.conj().T
    return pd.DataFrame([{
        "X_factorization_max_error": float(np.max(np.abs(x_mapped - x_expected))),
        "Z_factorization_max_error": float(np.max(np.abs(z_mapped - z_expected))),
        "dim_H12": 12,
        "dim_H3_times_dim_H4": 3 * 4,
        "dim_M12": 12**2,
        "dim_M3_times_dim_M4": (3**2) * (4**2),
    }])


def z3_character_projectors():
    r = shift(3)
    omega = np.exp(2j * np.pi / 3)
    projectors = []
    for s in range(3):
        pi = np.zeros((3, 3), dtype=complex)
        for n in range(3):
            pi += (omega ** (-s * n)) * np.linalg.matrix_power(r, n)
        pi /= 3.0
        projectors.append(pi)
    identity = np.eye(3, dtype=complex)
    rows = []
    for s, pi_s in enumerate(projectors):
        rows.append({
            "sector_s": s,
            "idempotence_max_error": float(np.max(np.abs(pi_s @ pi_s - pi_s))),
            "hermiticity_max_error": float(np.max(np.abs(pi_s.conj().T - pi_s))),
            "rank": int(np.linalg.matrix_rank(pi_s, tol=TOL)),
        })
    orth_errors = []
    for s in range(3):
        for t in range(3):
            target = projectors[s] if s == t else np.zeros((3, 3), dtype=complex)
            orth_errors.append(np.max(np.abs(projectors[s] @ projectors[t] - target)))
    summary = pd.DataFrame([{
        "projector_sum_identity_error": float(np.max(np.abs(sum(projectors) - identity))),
        "max_orthogonality_error": float(max(orth_errors)),
        "ranks_sum": sum(int(np.linalg.matrix_rank(p, tol=TOL)) for p in projectors),
    }])
    return pd.DataFrame(rows), summary, projectors


def triplication_isometry_certificate():
    rng = np.random.default_rng(1401)
    dim = 4
    psi = rng.normal(size=dim) + 1j * rng.normal(size=dim)
    psi = psi / np.linalg.norm(psi)
    unitaries = []
    for _ in range(3):
        a = rng.normal(size=(dim, dim)) + 1j * rng.normal(size=(dim, dim))
        q, rr = np.linalg.qr(a)
        phases = np.diag(rr)
        phases = np.where(np.abs(phases) > 0, phases / np.abs(phases), 1.0)
        q = q @ np.diag(np.conj(phases))
        unitaries.append(q)
    theta = np.array([0.0, 0.37, -0.91])
    out = np.zeros(3 * dim, dtype=complex)
    branch_norms = []
    for a in range(3):
        branch = np.exp(1j * theta[a]) * (unitaries[a] @ psi) / math.sqrt(3)
        out[a * dim:(a + 1) * dim] = branch
        branch_norms.append(float(np.vdot(branch, branch).real))
    return pd.DataFrame([{
        "input_norm_sq": float(np.vdot(psi, psi).real),
        "output_norm_sq": float(np.vdot(out, out).real),
        "norm_sq_error": abs(float(np.vdot(out, out).real - np.vdot(psi, psi).real)),
        "branch_0_norm_sq": branch_norms[0],
        "branch_1_norm_sq": branch_norms[1],
        "branch_2_norm_sq": branch_norms[2],
        "sum_branch_norm_sq": sum(branch_norms),
    }])


def braid_certificate():
    positions = [1, 2, 3]
    pair_counts = {(1, 2): 0, (1, 3): 0, (2, 3): 0}
    events = []
    event = 0
    for repeat in range(1, 7):
        for generator, left in [("sigma1", 0), ("sigma2", 1)]:
            event += 1
            before = positions.copy()
            a, b = positions[left], positions[left + 1]
            pair = tuple(sorted((a, b)))
            pair_counts[pair] += 1
            positions[left], positions[left + 1] = positions[left + 1], positions[left]
            events.append({
                "event": event,
                "repeat": repeat,
                "generator": generator,
                "pair": f"{pair[0]}-{pair[1]}",
                "crossing_sign": 1,
                "positions_before": "-".join(map(str, before)),
                "positions_after": "-".join(map(str, positions)),
            })
    pair_rows = []
    for pair, n_cross in sorted(pair_counts.items()):
        pair_rows.append({
            "component_pair": f"{pair[0]}-{pair[1]}",
            "positive_crossings": n_cross,
            "pairwise_linking_number": n_cross / 2.0,
        })
    events_df = pd.DataFrame(events)
    pairs_df = pd.DataFrame(pair_rows)
    summary_df = pd.DataFrame([{
        "word": "(sigma1 sigma2)^6",
        "word_length": len(events),
        "final_permutation_identity": positions == [1, 2, 3],
        "number_closed_components": 3 if positions == [1, 2, 3] else np.nan,
        "pairwise_link_sum": float(pairs_df["pairwise_linking_number"].sum()),
        "ribbon_self_linking_computed": False,
    }])
    return events_df, pairs_df, summary_df


def uv_power_counting_certificate():
    cases = [
        {"name": "convergent", "D": 4, "sigma": 0.0, "n": 2, "alpha": 2.5},
        {"name": "borderline_log", "D": 4, "sigma": 0.0, "n": 2, "alpha": 2.0},
        {"name": "divergent", "D": 4, "sigma": 0.0, "n": 2, "alpha": 1.5},
    ]
    rmax_values = [10.0, 1e2, 1e3, 1e4]
    rows = []
    for case in cases:
        exponent = case["D"] - 1 + case["sigma"] - case["n"] * case["alpha"]
        q = exponent + 1.0
        vals = []
        for rmax in rmax_values:
            integral = math.log(rmax) if abs(q) < 1e-14 else (rmax**q - 1.0) / q
            vals.append(integral)
        rows.append({
            **case,
            "radial_exponent": exponent,
            "criterion_nalpha_gt_DplusSigma": case["n"] * case["alpha"] > case["D"] + case["sigma"],
            "I_R10": vals[0],
            "I_R100": vals[1],
            "I_R1000": vals[2],
            "I_R10000": vals[3],
        })
    return pd.DataFrame(rows)


def main():
    crt = crt_certificate()
    crt.to_csv(OUT / "crt_factorization.csv", index=False)
    proj, proj_summary, _ = z3_character_projectors()
    proj.to_csv(OUT / "z3_character_projectors.csv", index=False)
    proj_summary.to_csv(OUT / "z3_projector_summary.csv", index=False)
    trip = triplication_isometry_certificate()
    trip.to_csv(OUT / "triplication_isometry.csv", index=False)
    events, pairs, braid_summary = braid_certificate()
    events.to_csv(OUT / "braid_events.csv", index=False)
    pairs.to_csv(OUT / "braid_pairwise_linking.csv", index=False)
    braid_summary.to_csv(OUT / "braid_summary.csv", index=False)
    uv = uv_power_counting_certificate()
    uv.to_csv(OUT / "uv_power_counting.csv", index=False)
    print("ENTRY 14 — THEOREM REPAIR CERTIFICATE")
    print("-------------------------------------")
    print("\nCRT factorization:")
    print(crt.to_string(index=False))
    print("\nZ3 character projectors:")
    print(proj.to_string(index=False))
    print(proj_summary.to_string(index=False))
    print("\nTriplication isometry:")
    print(trip.to_string(index=False))
    print("\nBraid closure:")
    print(braid_summary.to_string(index=False))
    print(pairs.to_string(index=False))
    print("\nUV power-counting examples:")
    print(uv.to_string(index=False))


if __name__ == "__main__":
    main()
