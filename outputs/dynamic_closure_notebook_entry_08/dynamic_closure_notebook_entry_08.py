"""
Dynamic Closure Notebook — Entry 08
Consolidation of the Dynamic Closure Theorem (DCT)

Purpose
-------
Entry 08 introduces no new physical mechanism.

It consolidates Entries 04–07 into a theorem package with explicit:
    - definitions,
    - EDF structural premises,
    - exact lemmas,
    - algebraic closure theorem,
    - arithmetic uniqueness theorem,
    - final Dynamic Closure Theorem,
    - corollaries,
    - falsification gates,
    - computational certificate.

Epistemic separation
--------------------
Exact mathematics:
    group arithmetic, operator algebra, Fibonacci arithmetic, published
    perfect-power classification.

EDF structural premises:
    P1 finite cyclic phase resolution,
    P2 homogeneous coherent primitive phase evolution,
    P3 primitive recurrence order k,
    P4 unital associative operator closure,
    P5 Fibonacci compatibility F_k = C(k).

Computational certificate:
    exact integer checks and floating-point operator diagnostics that mirror
    the theorem implementation. The code verifies the implementation; it does
    not replace the proofs.

Main theorem chain
------------------
Kernel preservation:
    Delta_phi = 2*pi*r/k.

Primitive recurrence:
    gcd(k,r) = 1.

Primitive traversal:
    U_r = X^r.

Since gcd(k,r)=1, there exists s with
    r*s = 1 mod k,
so
    (U_r)^s = X.

Phase-traversal algebra:
    Z U_r = omega_k^r U_r Z.

Because omega_k^r is primitive when gcd(k,r)=1,
    alg(U_r, Z) = M_k(C).

Therefore:
    C(k) = k^2.

Fibonacci compatibility:
    F_k = C(k) = k^2.

Bugeaud-Mignotte-Siksek perfect-power theorem:
    only Fibonacci perfect powers are 0, 1, 8, 144.

For k >= 2:
    F_k = k^2  iff  k = 12.

References
----------
Y. Bugeaud, M. Mignotte, and S. Siksek,
"Classical and modular approaches to exponential Diophantine equations I.
Fibonacci and Lucas perfect powers,"
Annals of Mathematics 163 (2006), 969-1018.
DOI: 10.4007/annals.2006.163.969

R. A. Bertlmann and P. Krammer,
"Bloch vectors for qudits,"
Journal of Physics A: Mathematical and Theoretical 41, 235303 (2008).
arXiv:0806.1174

S. M. Carroll and A. Singh,
"Quantum mereology: Factorizing Hilbert space into subsystems with
quasiclassical dynamics,"
Physical Review A 103, 022213 (2021).
DOI: 10.1103/PhysRevA.103.022213
"""

from __future__ import annotations

from dataclasses import dataclass
from math import gcd
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


@dataclass
class Config:
    exact_k_min: int = 2
    exact_k_max: int = 72

    operator_k_min: int = 2
    operator_k_max: int = 16

    fibonacci_scan_max: int = 500

    diagnostic_k: int = 12

    output_dir: str = "dynamic_closure_entry_08_output"


# ---------------------------------------------------------------------------
# Exact arithmetic utilities
# ---------------------------------------------------------------------------

def fibonacci(n: int) -> int:
    """Return F_n with F_0=0 and F_1=1 using exact integer arithmetic."""
    if n < 0:
        raise ValueError("Fibonacci index must be non-negative.")

    a, b = 0, 1

    for _ in range(n):
        a, b = b, a + b

    return a


def extended_gcd(a: int, b: int) -> tuple[int, int, int]:
    """
    Return (g, x, y) such that:
        a*x + b*y = g = gcd(a,b).
    """
    old_r, r = a, b
    old_s, s = 1, 0
    old_t, t = 0, 1

    while r != 0:
        quotient = old_r // r
        old_r, r = r, old_r - quotient * r
        old_s, s = s, old_s - quotient * s
        old_t, t = t, old_t - quotient * t

    return old_r, old_s, old_t


def modular_inverse(r: int, k: int) -> int:
    """Return s such that r*s = 1 mod k."""
    g, s, _ = extended_gcd(r, k)

    if g != 1:
        raise ValueError("r has no modular inverse modulo k.")

    return s % k


def euler_totient(k: int) -> int:
    """Return Euler's totient phi(k)."""
    return sum(
        1
        for r in range(1, k)
        if gcd(k, r) == 1
    )


def orbit_length(k: int, r: int) -> int:
    """
    Exact orbit length of repeated addition by r in Z_k:
        L = k / gcd(k,r).
    """
    return k // gcd(k, r)


# ---------------------------------------------------------------------------
# Finite Weyl operators
# ---------------------------------------------------------------------------

def clock_and_shift(k: int) -> tuple[complex, np.ndarray, np.ndarray]:
    """
    Return primitive root omega, canonical shift X, and phase operator Z.
    """
    omega = np.exp(2j * np.pi / k)

    x = np.zeros((k, k), dtype=complex)
    for m in range(k):
        x[(m + 1) % k, m] = 1.0

    z = np.diag(
        np.array(
            [omega**m for m in range(k)],
            dtype=complex,
        )
    )

    return omega, x, z


def matrix_power_mod_cycle(
    matrix: np.ndarray,
    exponent: int,
    k: int,
) -> np.ndarray:
    """Use cyclic exponent modulo k."""
    return np.linalg.matrix_power(matrix, exponent % k)


def traversal_operator(k: int, r: int) -> np.ndarray:
    """Return U_r = X^r."""
    _, x, _ = clock_and_shift(k)
    return matrix_power_mod_cycle(x, r, k)


def matrix_span_rank(matrices: list[np.ndarray]) -> int:
    """Return numerical rank after vectorizing a matrix family."""
    flattened = np.column_stack(
        [matrix.reshape(-1) for matrix in matrices]
    )
    return int(np.linalg.matrix_rank(flattened))


def phase_traversal_basis(
    k: int,
    r: int,
) -> list[np.ndarray]:
    """
    Return:
        { U_r^a Z^b : a,b in Z_k }.
    """
    _, _, z = clock_and_shift(k)
    u = traversal_operator(k, r)

    basis = []

    for a in range(k):
        ua = matrix_power_mod_cycle(u, a, k)

        for b in range(k):
            zb = matrix_power_mod_cycle(z, b, k)
            basis.append(ua @ zb)

    return basis


# ---------------------------------------------------------------------------
# Exact theorem certificate
# ---------------------------------------------------------------------------

def build_exact_traversal_certificate(
    config: Config,
) -> pd.DataFrame:
    """
    Exact integer certificate of Entries 07–08.

    For every k and every nonzero r:
        L(k,r) = k/gcd(k,r)
        full traversal iff gcd(k,r)=1
        inverse s exists iff gcd(k,r)=1
        r*s = 1 mod k
    """
    rows = []

    for k in range(config.exact_k_min, config.exact_k_max + 1):
        for r in range(1, k):
            g = gcd(k, r)
            length = orbit_length(k, r)
            transitive = g == 1

            if transitive:
                s = modular_inverse(r, k)
                inverse_check = (r * s) % k
            else:
                s = None
                inverse_check = None

            rows.append(
                {
                    "k": k,
                    "r": r,
                    "gcd_k_r": g,
                    "orbit_length": length,
                    "primitive_recurrence": length == k,
                    "transitive_full_cycle": transitive,
                    "modular_inverse_s": s,
                    "r_times_s_mod_k": inverse_check,
                    "U_power_recovers_X": (
                        inverse_check == 1
                        if transitive
                        else False
                    ),
                }
            )

    return pd.DataFrame(rows)


def build_totient_certificate(
    config: Config,
    traversal_certificate: pd.DataFrame,
) -> pd.DataFrame:
    rows = []

    for k in range(config.exact_k_min, config.exact_k_max + 1):
        subset = traversal_certificate[
            traversal_certificate["k"] == k
        ]

        measured = int(
            subset["transitive_full_cycle"].sum()
        )

        expected = euler_totient(k)

        rows.append(
            {
                "k": k,
                "measured_primitive_generators": measured,
                "euler_totient_phi_k": expected,
                "exact_agreement": measured == expected,
            }
        )

    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# Operator theorem certificate
# ---------------------------------------------------------------------------

def operator_diagnostics_for_k(k: int) -> dict:
    """
    Test every primitive traversal r for one k and retain maximum errors
    and minimum generated rank.
    """
    omega, x, z = clock_and_shift(k)

    primitive_r = [
        r
        for r in range(1, k)
        if gcd(k, r) == 1
    ]

    maximum_weyl_error = 0.0
    maximum_inverse_recovery_error = 0.0
    maximum_orthogonality_error = 0.0
    minimum_span_rank = k * k

    for r in primitive_r:
        u = traversal_operator(k, r)
        s = modular_inverse(r, k)

        primitive_root_r = omega**r

        weyl_error = np.linalg.norm(
            z @ u - primitive_root_r * u @ z,
            ord="fro",
        )

        recovered_x = matrix_power_mod_cycle(u, s, k)

        recovery_error = np.linalg.norm(
            recovered_x - x,
            ord="fro",
        )

        basis = phase_traversal_basis(k, r)
        rank = matrix_span_rank(basis)
        minimum_span_rank = min(minimum_span_rank, rank)

        # Hilbert-Schmidt normalized orthogonality.
        # For runtime efficiency, compare every operator to itself and to
        # its immediate successor in the deterministic basis ordering.
        for index, operator in enumerate(basis):
            self_value = (
                np.trace(operator.conj().T @ operator) / k
            )

            maximum_orthogonality_error = max(
                maximum_orthogonality_error,
                float(abs(self_value - 1.0)),
            )

            if index + 1 < len(basis):
                neighbor = basis[index + 1]
                cross_value = (
                    np.trace(operator.conj().T @ neighbor) / k
                )

                maximum_orthogonality_error = max(
                    maximum_orthogonality_error,
                    float(abs(cross_value)),
                )

        maximum_weyl_error = max(
            maximum_weyl_error,
            float(weyl_error),
        )

        maximum_inverse_recovery_error = max(
            maximum_inverse_recovery_error,
            float(recovery_error),
        )

    return {
        "k": k,
        "primitive_generator_count": len(primitive_r),
        "euler_totient_phi_k": euler_totient(k),
        "minimum_phase_traversal_span_rank": minimum_span_rank,
        "expected_full_operator_dimension": k * k,
        "maximum_Weyl_relation_error": maximum_weyl_error,
        "maximum_U_inverse_power_recovers_X_error":
            maximum_inverse_recovery_error,
        "maximum_sampled_HS_orthogonality_error":
            maximum_orthogonality_error,
    }


def build_operator_certificate(config: Config) -> pd.DataFrame:
    return pd.DataFrame(
        [
            operator_diagnostics_for_k(k)
            for k in range(
                config.operator_k_min,
                config.operator_k_max + 1,
            )
        ]
    )


# ---------------------------------------------------------------------------
# Fibonacci arithmetic certificate
# ---------------------------------------------------------------------------

def build_fibonacci_certificate(
    config: Config,
) -> pd.DataFrame:
    rows = []

    for k in range(2, config.fibonacci_scan_max + 1):
        fib = fibonacci(k)
        square = k * k

        if fib == square:
            rows.append(
                {
                    "k": k,
                    "F_k": fib,
                    "k_squared": square,
                    "exact_solution": True,
                }
            )

    return pd.DataFrame(
        rows,
        columns=[
            "k",
            "F_k",
            "k_squared",
            "exact_solution",
        ],
    )


def published_perfect_power_certificate() -> pd.DataFrame:
    """
    Finite classification from Bugeaud-Mignotte-Siksek.

    This function does not prove their theorem; it transparently checks the
    equation F_k=k^2 against the theorem's published Fibonacci perfect-power
    indices.
    """
    theorem_indices = [0, 1, 2, 6, 12]

    return pd.DataFrame(
        [
            {
                "k": k,
                "F_k": fibonacci(k),
                "k_squared": k * k,
                "F_k_equals_k_squared": fibonacci(k) == k * k,
            }
            for k in theorem_indices
        ]
    )


# ---------------------------------------------------------------------------
# DCT dependency registry and falsification gates
# ---------------------------------------------------------------------------

def assumption_dependency_matrix() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "result_id": "L1",
                "result": "Delta_phi = 2*pi*r/k",
                "depends_on": "P1, P2",
                "status": "Exact conditional lemma",
            },
            {
                "result_id": "L2",
                "result": "gcd(k,r)=1",
                "depends_on": "P3 + L1",
                "status": "Exact conditional lemma",
            },
            {
                "result_id": "L3",
                "result": "U_r=X^r and X=(U_r)^s",
                "depends_on": "L2",
                "status": "Exact group-theoretic lemma",
            },
            {
                "result_id": "L4",
                "result": "Z U_r = omega_k^r U_r Z",
                "depends_on": "P1 + L3",
                "status": "Exact operator identity",
            },
            {
                "result_id": "T_A",
                "result": "alg(U_r,Z)=M_k(C), C(k)=k^2",
                "depends_on": "P4 + L2 + L4",
                "status": "Exact conditional theorem",
            },
            {
                "result_id": "P_F",
                "result": "F_k=k^2",
                "depends_on": "P5 + T_A",
                "status": "Exact conditional proposition",
            },
            {
                "result_id": "T_B",
                "result": "F_k=k^2 iff k=12 for k>=2",
                "depends_on": "Published BMS perfect-power theorem",
                "status": "Exact arithmetic theorem consequence",
            },
            {
                "result_id": "DCT",
                "result": "k=12",
                "depends_on": "P1-P5 + T_A + T_B",
                "status": "Dynamic Closure Theorem",
            },
            {
                "result_id": "NUM",
                "result": "Finite computational certificate",
                "depends_on": "Implemented equations",
                "status": "Verification, not proof",
            },
            {
                "result_id": "PHYS",
                "result": "Real-world correspondence",
                "depends_on": "Later empirical tests",
                "status": "Empirical, not mathematical proof",
            },
        ]
    )


def premise_registry() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "premise_id": "P1",
                "premise": "Finite cyclic phase resolution",
                "formal_statement":
                    "EDF resolves A_k={exp(2*pi*i*m/k):m in Z_k}.",
            },
            {
                "premise_id": "P2",
                "premise": "Homogeneous coherent primitive phase evolution",
                "formal_statement":
                    "phi_(n+1)=phi_n+Delta_phi mod 2*pi.",
            },
            {
                "premise_id": "P3",
                "premise": "Primitive recurrence order k",
                "formal_statement":
                    "The first complete return occurs after exactly k updates.",
            },
            {
                "premise_id": "P4",
                "premise": "Unital associative dynamic closure",
                "formal_statement":
                    "Required EDF operations close under composition in the "
                    "smallest unital associative complex operator algebra.",
            },
            {
                "premise_id": "P5",
                "premise": "Fibonacci compatibility",
                "formal_statement":
                    "Exact EDF structural compatibility requires F_k=C(k).",
            },
        ]
    )


def falsification_gates() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "gate_id": "G1",
                "failure_condition":
                    "The finite phases of A_k are not physically resolved.",
                "consequence":
                    "Z is not forced by the EDF kernel; DCT chain stops.",
            },
            {
                "gate_id": "G2",
                "failure_condition":
                    "Primitive evolution is not homogeneous coherent phase "
                    "accumulation.",
                "consequence":
                    "Delta_phi=2*pi*r/k need not follow.",
            },
            {
                "gate_id": "G3",
                "failure_condition":
                    "The first recurrence order is smaller than k.",
                "consequence":
                    "gcd(k,r)>1 is allowed; full traversal fails.",
            },
            {
                "gate_id": "G4",
                "failure_condition":
                    "Fundamental dynamic closure is not unital/associative "
                    "under operator composition.",
                "consequence":
                    "The M_k(C) closure theorem does not apply.",
            },
            {
                "gate_id": "G5",
                "failure_condition":
                    "Fibonacci compatibility F_k=C(k) lacks independent EDF "
                    "justification.",
                "consequence":
                    "k^2 is still derived, but k=12 does not follow.",
            },
            {
                "gate_id": "G6",
                "failure_condition":
                    "A valid alternative theorem contradicts the BMS "
                    "perfect-power classification.",
                "consequence":
                    "Arithmetic uniqueness must be re-evaluated.",
            },
        ]
    )


def theorem_chain_table() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "step": 1,
                "input": "P1 + P2",
                "result":
                    "Kernel preservation quantizes Delta_phi=2*pi*r/k",
            },
            {
                "step": 2,
                "input": "P3",
                "result":
                    "Primitive recurrence implies gcd(k,r)=1",
            },
            {
                "step": 3,
                "input": "gcd(k,r)=1",
                "result":
                    "U_r=X^r and X=(U_r)^s for r*s=1 mod k",
            },
            {
                "step": 4,
                "input": "P1 + traversal",
                "result":
                    "Z U_r = omega_k^r U_r Z",
            },
            {
                "step": 5,
                "input": "P4 + Weyl pair",
                "result":
                    "alg(U_r,Z)=M_k(C), hence C(k)=k^2",
            },
            {
                "step": 6,
                "input": "P5",
                "result":
                    "F_k=C(k)=k^2",
            },
            {
                "step": 7,
                "input": "BMS theorem",
                "result":
                    "Unique nontrivial solution for k>=2 is k=12",
            },
        ]
    )


# ---------------------------------------------------------------------------
# Figures
# ---------------------------------------------------------------------------

def plot_proof_chain(output_dir: Path) -> None:
    labels = [
        "EDF premises\nP1–P3",
        "Primitive\ntraversal",
        "Weyl pair\n(U_r, Z)",
        "Full algebra\nM_k(C)",
        "C(k)=k^2",
        "F_k=k^2",
        "k=12",
    ]

    x_positions = np.arange(len(labels))

    plt.figure(figsize=(13, 4.5))

    for index, (x, label) in enumerate(zip(x_positions, labels)):
        plt.text(
            x,
            0.0,
            label,
            ha="center",
            va="center",
            bbox={
                "boxstyle": "round,pad=0.5",
                "facecolor": "none",
            },
        )

        if index < len(labels) - 1:
            plt.annotate(
                "",
                xy=(x + 0.72, 0.0),
                xytext=(x + 0.28, 0.0),
                arrowprops={"arrowstyle": "->"},
            )

    arrow_labels = [
        "L1–L3",
        "L4",
        "Theorem A",
        "dimension",
        "P5",
        "Theorem B",
    ]

    for index, label in enumerate(arrow_labels):
        plt.text(
            index + 0.5,
            0.18,
            label,
            ha="center",
            va="bottom",
            fontsize=8,
        )

    plt.xlim(-0.6, len(labels) - 0.4)
    plt.ylim(-0.6, 0.6)
    plt.axis("off")
    plt.title("Dynamic Closure Theorem — Logical Dependency Chain")
    plt.tight_layout()
    plt.savefig(
        output_dir / "dct_logical_dependency_chain.png",
        dpi=180,
    )
    plt.close()


def plot_primitive_generator_count(
    totient: pd.DataFrame,
    output_dir: Path,
) -> None:
    plt.figure(figsize=(10, 5))

    plt.plot(
        totient["k"],
        totient["measured_primitive_generators"],
        marker="o",
        label="Exact primitive-generator count",
    )

    plt.plot(
        totient["k"],
        totient["euler_totient_phi_k"],
        linestyle="--",
        label="Euler totient phi(k)",
    )

    plt.xlabel("Closure sector count k")
    plt.ylabel("Number of primitive traversal generators")
    plt.title("Primitive Traversal Multiplicity")
    plt.legend(frameon=False)
    plt.tight_layout()
    plt.savefig(
        output_dir / "primitive_generator_count.png",
        dpi=180,
    )
    plt.close()


def plot_operator_dimension(
    operator_certificate: pd.DataFrame,
    output_dir: Path,
) -> None:
    plt.figure(figsize=(9, 5))

    plt.plot(
        operator_certificate["k"],
        operator_certificate["minimum_phase_traversal_span_rank"],
        marker="o",
        label="Minimum generated rank over primitive r",
    )

    plt.plot(
        operator_certificate["k"],
        operator_certificate["expected_full_operator_dimension"],
        linestyle="--",
        label="k^2",
    )

    plt.xlabel("Closure sector count k")
    plt.ylabel("Operator-space dimension")
    plt.title("Primitive Traversals Generate the Full Weyl Operator Space")
    plt.legend(frameon=False)
    plt.tight_layout()
    plt.savefig(
        output_dir / "primitive_traversal_operator_dimension.png",
        dpi=180,
    )
    plt.close()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    config = Config()
    output_dir = Path(config.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    premises = premise_registry()
    premises.to_csv(
        output_dir / "premise_registry.csv",
        index=False,
    )

    dependencies = assumption_dependency_matrix()
    dependencies.to_csv(
        output_dir / "assumption_dependency_matrix.csv",
        index=False,
    )

    gates = falsification_gates()
    gates.to_csv(
        output_dir / "falsification_gates.csv",
        index=False,
    )

    theorem_chain = theorem_chain_table()
    theorem_chain.to_csv(
        output_dir / "dct_theorem_chain.csv",
        index=False,
    )

    traversal = build_exact_traversal_certificate(config)
    traversal.to_csv(
        output_dir / "exact_traversal_certificate.csv",
        index=False,
    )

    totient = build_totient_certificate(
        config,
        traversal,
    )
    totient.to_csv(
        output_dir / "totient_certificate.csv",
        index=False,
    )

    operator_certificate = build_operator_certificate(config)
    operator_certificate.to_csv(
        output_dir / "operator_theorem_certificate.csv",
        index=False,
    )

    fibonacci_scan = build_fibonacci_certificate(config)
    fibonacci_scan.to_csv(
        output_dir / "fibonacci_square_scan.csv",
        index=False,
    )

    perfect_power = published_perfect_power_certificate()
    perfect_power.to_csv(
        output_dir / "published_perfect_power_certificate.csv",
        index=False,
    )

    diagnostic_rows = traversal[
        traversal["k"] == config.diagnostic_k
    ].copy()

    diagnostic_rows.to_csv(
        output_dir / "diagnostic_k12_primitive_generators.csv",
        index=False,
    )

    plot_proof_chain(output_dir)
    plot_primitive_generator_count(totient, output_dir)
    plot_operator_dimension(operator_certificate, output_dir)

    # Exact Boolean certificates.
    primitive_recurrence_equivalence = bool(
        np.all(
            traversal["primitive_recurrence"]
            == traversal["transitive_full_cycle"]
        )
    )

    inverse_certificate = traversal[
        traversal["transitive_full_cycle"]
    ]

    inverse_recovery_exact = bool(
        np.all(
            inverse_certificate["r_times_s_mod_k"] == 1
        )
        and np.all(
            inverse_certificate["U_power_recovers_X"]
        )
    )

    totient_exact = bool(
        np.all(totient["exact_agreement"])
    )

    operator_dimension_exact_numerically = bool(
        np.all(
            operator_certificate[
                "minimum_phase_traversal_span_rank"
            ]
            ==
            operator_certificate[
                "expected_full_operator_dimension"
            ]
        )
    )

    k12_generators = diagnostic_rows.loc[
        diagnostic_rows["transitive_full_cycle"],
        "r",
    ].tolist()

    print()
    print("Dynamic Closure Notebook — Entry 08")
    print("Consolidation of the Dynamic Closure Theorem")
    print("-" * 60)
    print()
    print("No new physical mechanism is introduced in this entry.")
    print()
    print(
        "Primitive recurrence iff full traversal "
        f"for k={config.exact_k_min},...,{config.exact_k_max}: "
        f"{primitive_recurrence_equivalence}"
    )
    print(
        "Modular inverse recovers canonical X exactly "
        "for every primitive traversal: "
        f"{inverse_recovery_exact}"
    )
    print(
        "Primitive-generator count equals Euler phi(k) exactly: "
        f"{totient_exact}"
    )
    print(
        "Every tested primitive phase-traversal pair spans k^2: "
        f"{operator_dimension_exact_numerically}"
    )
    print()
    print(
        "Maximum numerical Weyl-relation error: "
        f"{operator_certificate['maximum_Weyl_relation_error'].max():.6e}"
    )
    print(
        "Maximum numerical X-recovery error: "
        f"{operator_certificate['maximum_U_inverse_power_recovers_X_error'].max():.6e}"
    )
    print(
        "Maximum sampled Hilbert-Schmidt orthogonality error: "
        f"{operator_certificate['maximum_sampled_HS_orthogonality_error'].max():.6e}"
    )
    print()
    print(
        f"Primitive traversal generators for k={config.diagnostic_k}: "
        + ", ".join(str(value) for value in k12_generators)
    )
    print()
    print(
        f"Computational solutions of F_k=k^2 for 2 <= k <= "
        f"{config.fibonacci_scan_max}: "
        f"{fibonacci_scan['k'].tolist()}"
    )
    print()
    print("Published BMS perfect-power classification check:")
    print(perfect_power.to_string(index=False))
    print()
    print("Theorem A — Dynamic Algebraic Closure:")
    print(
        "    P1-P4 => alg(U_r,Z)=M_k(C) => C(k)=k^2."
    )
    print()
    print("Theorem B — Arithmetic Uniqueness:")
    print(
        "    F_k=k^2 and k>=2 => k=12."
    )
    print()
    print("Dynamic Closure Theorem:")
    print(
        "    P1-P5 => k=12."
    )
    print()
    print(f"Outputs written to: {output_dir.resolve()}")


if __name__ == "__main__":
    main()
