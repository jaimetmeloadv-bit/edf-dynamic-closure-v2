"""
Dynamic Closure Notebook — Entry 07
Primitive EDF Phase Evolution and the Traversal Theorem

Purpose
-------
Derive the cyclic traversal operator from a primitive coherent phase-evolution
law, rather than postulating the shift operator X afterward.

Primitive EDF timing law
------------------------
Let tau_* denote one primitive timing step and Omega_* the corresponding
coherent phase rate. Sampling once per primitive timing step gives

    phi_(n+1) = phi_n + Delta_phi  (mod 2*pi),

where Delta_phi = Omega_* tau_*.

The finite k-sector phase kernel is

    A_k = {exp[i(phi_0 + 2*pi*m/k)] : m in Z_k}.

Exact preservation of A_k forces

    Delta_phi = 2*pi*r/k  (mod 2*pi)

for some r in Z_k. The induced sector map is

    m -> m+r (mod k),

with operator U_r = X^r.

The orbit has length k/gcd(k,r). If k is the primitive recurrence order—meaning
the first return occurs only after k updates—then the orbit length must equal k.
Therefore gcd(k,r)=1, and full traversal follows rather than being assumed.

For each transitive r, P_r|m> = |r*m mod k> is an invertible permutation and

    P_r^dagger X^r P_r = X.

Thus every homogeneous full-cycle traversal is relabeling-equivalent to the
canonical shift X.
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
    k_min: int = 2
    k_max: int = 36
    diagnostic_k: int = 12
    output_dir: str = "dynamic_closure_entry_07_output"


def roots_of_unity(k: int, phi_0: float = 0.0) -> np.ndarray:
    m = np.arange(k)
    return np.exp(1j * (phi_0 + 2.0 * np.pi * m / k))


def canonical_shift(k: int) -> np.ndarray:
    x = np.zeros((k, k), dtype=complex)
    for m in range(k):
        x[(m + 1) % k, m] = 1.0
    return x


def step_operator(k: int, r: int) -> np.ndarray:
    return np.linalg.matrix_power(canonical_shift(k), r % k)


def direct_step_permutation(k: int, r: int) -> np.ndarray:
    u = np.zeros((k, k), dtype=complex)
    for m in range(k):
        u[(m + r) % k, m] = 1.0
    return u


def relabeling_permutation(k: int, r: int) -> np.ndarray:
    if gcd(k, r) != 1:
        raise ValueError("r must be coprime to k for invertible relabeling.")
    p = np.zeros((k, k), dtype=complex)
    for m in range(k):
        p[(r * m) % k, m] = 1.0
    return p


def cycle_decomposition(k: int, r: int) -> list[list[int]]:
    unvisited = set(range(k))
    cycles = []
    while unvisited:
        start = min(unvisited)
        cycle = []
        current = start
        while current not in cycle:
            cycle.append(current)
            unvisited.discard(current)
            current = (current + r) % k
        cycles.append(cycle)
    return cycles


def kernel_preservation_error(k: int, r: int) -> float:
    roots = roots_of_unity(k)
    multiplier = np.exp(2j * np.pi * r / k)
    rotated = multiplier * roots
    target = np.array([roots[(m + r) % k] for m in range(k)], dtype=complex)
    return float(np.max(np.abs(rotated - target)))


def operator_step_error(k: int, r: int) -> float:
    return float(
        np.linalg.norm(
            direct_step_permutation(k, r) - step_operator(k, r),
            ord="fro",
        )
    )


def conjugacy_to_canonical_shift_error(k: int, r: int) -> float:
    if gcd(k, r) != 1:
        return np.nan
    x = canonical_shift(k)
    xr = step_operator(k, r)
    p = relabeling_permutation(k, r)
    return float(np.linalg.norm(p.conj().T @ xr @ p - x, ord="fro"))


def euler_totient(k: int) -> int:
    return sum(1 for r in range(1, k) if gcd(k, r) == 1)


def build_step_table(config: Config) -> pd.DataFrame:
    rows = []
    for k in range(config.k_min, config.k_max + 1):
        for r in range(k):
            divisor = gcd(k, r)
            cycles = cycle_decomposition(k, r)
            rows.append(
                {
                    "k": k,
                    "r": r,
                    "delta_phi_over_2pi": r / k,
                    "gcd_k_r": divisor,
                    "orbit_length": k // divisor,
                    "cycle_count": divisor,
                    "transitive_full_cycle": divisor == 1,
                    "kernel_preservation_error": kernel_preservation_error(k, r),
                    "operator_X_power_error": operator_step_error(k, r),
                    "conjugacy_to_X_error": conjugacy_to_canonical_shift_error(k, r),
                    "cycle_decomposition": " | ".join(
                        "-".join(str(value) for value in cycle)
                        for cycle in cycles
                    ),
                }
            )
    return pd.DataFrame(rows)


def build_totient_summary(config: Config, step_table: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for k in range(config.k_min, config.k_max + 1):
        subset = step_table[step_table["k"] == k]
        measured = int(subset["transitive_full_cycle"].sum())
        expected = euler_totient(k)
        rows.append(
            {
                "k": k,
                "measured_transitive_steps": measured,
                "euler_totient_phi_k": expected,
                "agreement": measured == expected,
                "fraction_of_nonzero_steps_transitive": measured / (k - 1),
            }
        )
    return pd.DataFrame(rows)


def plot_orbit_length(diagnostic: pd.DataFrame, config: Config, output_dir: Path) -> None:
    plt.figure(figsize=(9, 5))
    plt.plot(diagnostic["r"], diagnostic["orbit_length"], marker="o")
    plt.axhline(config.diagnostic_k, linestyle="--", label="Full kernel size")
    plt.xlabel("Phase-step index r")
    plt.ylabel("Orbit length")
    plt.title(f"Primitive Phase-Step Orbit Length for k={config.diagnostic_k}")
    plt.legend(frameon=False)
    plt.tight_layout()
    plt.savefig(output_dir / "diagnostic_orbit_length.png", dpi=180)
    plt.close()


def plot_cycle_count(diagnostic: pd.DataFrame, config: Config, output_dir: Path) -> None:
    plt.figure(figsize=(9, 5))
    plt.bar(diagnostic["r"], diagnostic["cycle_count"])
    plt.xlabel("Phase-step index r")
    plt.ylabel("Number of disjoint cycles")
    plt.title(f"Cycle Decomposition of Homogeneous Traversal for k={config.diagnostic_k}")
    plt.tight_layout()
    plt.savefig(output_dir / "diagnostic_cycle_count.png", dpi=180)
    plt.close()


def plot_totient_count(summary: pd.DataFrame, output_dir: Path) -> None:
    plt.figure(figsize=(10, 5))
    plt.plot(
        summary["k"],
        summary["measured_transitive_steps"],
        marker="o",
        label="Measured transitive phase steps",
    )
    plt.plot(
        summary["k"],
        summary["euler_totient_phi_k"],
        linestyle="--",
        label="Euler totient phi(k)",
    )
    plt.xlabel("Closure sector count k")
    plt.ylabel("Number of full-cycle step generators")
    plt.title("Transitive Primitive Steps Equal Euler's Totient Function")
    plt.legend(frameon=False)
    plt.tight_layout()
    plt.savefig(output_dir / "transitive_steps_vs_totient.png", dpi=180)
    plt.close()


def plot_phase_kernel(diagnostic: pd.DataFrame, config: Config, output_dir: Path) -> None:
    k = config.diagnostic_k
    roots = roots_of_unity(k)
    plt.figure(figsize=(7, 7))
    plt.scatter(roots.real, roots.imag, s=60)
    for m, root in enumerate(roots):
        plt.text(1.08 * root.real, 1.08 * root.imag, str(m), ha="center", va="center")
    angle = np.linspace(0.0, 2.0 * np.pi, 400)
    plt.plot(np.cos(angle), np.sin(angle), linewidth=1.0)
    transitive_steps = diagnostic.loc[
        diagnostic["transitive_full_cycle"], "r"
    ].tolist()
    plt.text(
        0.0,
        -1.30,
        "Full-cycle step indices: " + ", ".join(str(v) for v in transitive_steps),
        ha="center",
    )
    plt.xlabel("Real part")
    plt.ylabel("Imaginary part")
    plt.title(f"Finite Phase Kernel A_k for k={k}")
    plt.axis("equal")
    plt.xlim(-1.4, 1.4)
    plt.ylim(-1.4, 1.4)
    plt.tight_layout()
    plt.savefig(output_dir / "diagnostic_phase_kernel.png", dpi=180)
    plt.close()


def main() -> None:
    config = Config()
    output_dir = Path(config.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    step_table = build_step_table(config)
    step_table.to_csv(output_dir / "primitive_phase_step_table.csv", index=False)

    totient_summary = build_totient_summary(config, step_table)
    totient_summary.to_csv(
        output_dir / "transitive_step_totient_summary.csv",
        index=False,
    )

    diagnostic = (
        step_table[step_table["k"] == config.diagnostic_k]
        .copy()
        .reset_index(drop=True)
    )
    diagnostic.to_csv(output_dir / "diagnostic_k_step_table.csv", index=False)

    plot_orbit_length(diagnostic, config, output_dir)
    plot_cycle_count(diagnostic, config, output_dir)
    plot_totient_count(totient_summary, output_dir)
    plot_phase_kernel(diagnostic, config, output_dir)

    maximum_kernel_error = float(step_table["kernel_preservation_error"].max())
    maximum_operator_error = float(step_table["operator_X_power_error"].max())
    maximum_conjugacy_error = float(step_table["conjugacy_to_X_error"].dropna().max())
    totient_verified = bool(np.all(totient_summary["agreement"]))

    diagnostic_transitive = diagnostic.loc[
        diagnostic["transitive_full_cycle"], "r"
    ].tolist()

    print()
    print("Dynamic Closure Notebook — Entry 07")
    print("Primitive EDF Phase Evolution and the Traversal Theorem")
    print("-" * 68)
    print()
    print("Kernel-preserving homogeneous phase step:")
    print("    Delta_phi = 2*pi*r/k  (mod 2*pi)")
    print()
    print("Induced sector evolution:")
    print("    m -> m+r (mod k),    U_r = X^r")
    print()
    print("Primitive recurrence / full traversal criterion:")
    print("    first return after k updates <=> gcd(k,r) = 1")
    print()
    print(
        f"Euler-totient criterion verified for every "
        f"k={config.k_min},...,{config.k_max}: {totient_verified}"
    )
    print()
    print(f"Maximum kernel-preservation error: {maximum_kernel_error:.6e}")
    print(f"Maximum direct-step versus X^r error: {maximum_operator_error:.6e}")
    print(f"Maximum transitive-step conjugacy-to-X error: {maximum_conjugacy_error:.6e}")
    print()
    print(f"For diagnostic k={config.diagnostic_k}, the full-cycle step indices are:")
    print("    " + ", ".join(str(value) for value in diagnostic_transitive))
    print()
    print("Primitive Traversal Theorem:")
    print("    coherent homogeneous phase accumulation")
    print("    + exact finite-kernel preservation")
    print("    + primitive recurrence order k (no earlier return)")
    print("        => gcd(k,r)=1 and full k-sector traversal")
    print("        => U_r = X^r")
    print("        => U_r is relabeling-equivalent to X.")
    print()
    print(f"Outputs written to: {output_dir.resolve()}")


if __name__ == "__main__":
    main()
