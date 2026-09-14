"""
Dynamic Closure Notebook — Entry 10
Transient-State Causality and Boundary Footprints

Purpose
-------
Test the hypothesis that a sector can have zero terminal transient occupancy
while still leaving a nonzero dynamical and effective-boundary contribution.

The model separates:

1. transient search/selection states labelled by closure sector k;
2. absorbing committed outcomes labelled by the same k.

All transient probability eventually vanishes:

    p_transient(t -> infinity) = 0,

but transient sectors can still have:

    - nonzero expected residence time;
    - nonzero expected transition flux;
    - nonzero intervention effect on P(commit to k=12);
    - nonzero Schur-complement boundary footprint after elimination.

This directly tests the statement:

    zero final occupancy != zero causal/dynamical contribution.

Structural defect
-----------------
Use the Entry 09 DCT-compatible log-ratio defect

    D_k = |ln(F_k/k^2)|.

Local detailed-balance pathway rates
------------------------------------
For nearest-neighbor sectors,

    W_(j->k)
      = nu A_jk exp[-lambda(D_k-D_j)/2],

with symmetric path adjacency A.

Commitment hazard
-----------------
Each transient sector k has an irreversible commitment rate

    h_k = h0 exp(-lambda D_k).

This is a declared modeling layer, not a DCT theorem. It simply makes lower
defect sectors more likely to commit once visited.

Continuous-time absorbing generator
------------------------------------
Let Q be the transient generator and R the transient-to-absorbing rate matrix:

    Q_jk = W_jk,                    j != k
    Q_jj = -sum_(k != j) W_jk - h_j
    R = diag(h_j).

Then the continuous-time fundamental matrix is

    N = (-Q)^(-1).

For initial row distribution mu:

    expected residence time in transient sector j:
        tau_j = (mu N)_j

    final absorption probabilities:
        a = mu N R.

All transient occupancy tends to zero when Q is Hurwitz
(all eigenvalues have negative real part).

Intervention measure
--------------------
To test pathway causality without changing DCT, apply a soft blockade to one
interior transient sector j by multiplying all incident transition rates by

    epsilon_block << 1.

The commitment hazard is left unchanged.

Define

    C_j = P_target(base) - P_target(block j).

For the default boundary-pair initial condition, every interior sector begins
with zero initial probability. Thus C_j measures a pathway intervention rather
than simply deleting initial mass.

Schur-complement boundary footprint
-----------------------------------
Partition one transient state j from all retained transient states A.

Eliminate j algebraically:

    Q_eff = Q_AA - Q_Aj Q_jj^(-1) Q_jA

    R_eff = R_A  - Q_Aj Q_jj^(-1) R_j.

The eliminated state no longer appears explicitly, yet it induces:

    Delta_Q = Q_eff - Q_AA
    Delta_R = R_eff - R_A.

These are its effective boundary footprints.

The absorption matrix is exactly preserved on retained starting states:

    B = (-Q)^(-1) R

    B_eff = (-Q_eff)^(-1) R_eff

    B_eff = B_A.

Therefore eliminating a zero-terminal transient state does not erase its
dynamical influence; the influence is transferred into effective boundary
couplings and sink terms.

Scientific status
-----------------
Standard mathematics:
    absorbing continuous-time Markov chains, fundamental matrix,
    Schur-complement elimination.

EDF-specific input:
    the DCT defect D_k.

Model choices:
    local path topology,
    commitment hazard form,
    lambda, nu, h0,
    intervention strength.

Failure of this pathway model would not invalidate DCT.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

try:
    from scipy.linalg import expm
except ImportError as exc:
    raise ImportError(
        "Entry 10 requires scipy.linalg.expm for finite-time verification."
    ) from exc


@dataclass
class Config:
    k_min: int = 2
    k_max: int = 36

    selection_strength: float = 2.0
    attempt_frequency: float = 1.0
    commitment_rate_scale: float = 0.10

    target_k: int = 12

    # Soft pathway blockade: 0.05 means 95% suppression of incident rates.
    block_factor: float = 0.05

    # Initial probability is placed only on the two outer boundaries.
    boundary_pair_initial_condition: bool = True

    # Long-time numerical check for transient extinction.
    long_time: float = 1000.0

    output_dir: str = "dynamic_closure_entry_10_output"


def fibonacci(n: int) -> int:
    """Return F_n with F_0=0 and F_1=1."""
    if n < 0:
        raise ValueError("Fibonacci index must be non-negative.")

    a, b = 0, 1

    for _ in range(n):
        a, b = b, a + b

    return a


def closure_defect(k_values: np.ndarray) -> np.ndarray:
    """D_k = |ln(F_k/k^2)|."""
    values = []

    for k in k_values:
        fib = fibonacci(int(k))
        capacity = int(k) ** 2
        values.append(abs(np.log(fib / capacity)))

    return np.asarray(values, dtype=float)


def path_adjacency(n: int) -> np.ndarray:
    """Nearest-neighbor symmetric path graph."""
    adjacency = np.zeros((n, n), dtype=float)

    for index in range(n - 1):
        adjacency[index, index + 1] = 1.0
        adjacency[index + 1, index] = 1.0

    return adjacency


def detailed_balance_rates(
    defects: np.ndarray,
    selection_strength: float,
    attempt_frequency: float,
    adjacency: np.ndarray,
) -> np.ndarray:
    """Return W[j,k] = transient jump rate j -> k."""
    delta = defects[None, :] - defects[:, None]

    rates = (
        attempt_frequency
        * adjacency
        * np.exp(-0.5 * selection_strength * delta)
    )

    np.fill_diagonal(rates, 0.0)

    return rates


def commitment_hazards(
    defects: np.ndarray,
    selection_strength: float,
    commitment_rate_scale: float,
) -> np.ndarray:
    """
    Irreversible commitment rate for each transient sector.

        h_k = h0 exp(-lambda D_k).
    """
    return (
        commitment_rate_scale
        * np.exp(-selection_strength * defects)
    )


def absorbing_matrices(
    rates: np.ndarray,
    hazards: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    """
    Return transient generator Q and transient-to-absorbing rate matrix R.
    """
    q = rates.copy()

    np.fill_diagonal(
        q,
        -rates.sum(axis=1) - hazards,
    )

    r = np.diag(hazards)

    return q, r


def initial_distribution(
    k_values: np.ndarray,
    config: Config,
) -> np.ndarray:
    """Default: equal mass on the two outer k boundaries."""
    n = len(k_values)
    mu = np.zeros(n, dtype=float)

    if config.boundary_pair_initial_condition:
        mu[0] = 0.5
        mu[-1] = 0.5
    else:
        mu[:] = 1.0 / n

    return mu


def absorption_analysis(
    q: np.ndarray,
    r: np.ndarray,
    mu: np.ndarray,
) -> dict:
    """
    Continuous-time absorbing-chain quantities.

    Fundamental matrix:
        N = (-Q)^(-1)

    Absorption matrix:
        B = N R
    """
    fundamental = np.linalg.inv(-q)

    absorption_matrix = fundamental @ r

    residence = mu @ fundamental
    absorption_probabilities = mu @ absorption_matrix

    eigenvalues = np.linalg.eigvals(q)

    return {
        "fundamental": fundamental,
        "absorption_matrix": absorption_matrix,
        "residence": residence,
        "absorption_probabilities": absorption_probabilities,
        "generator_eigenvalues": eigenvalues,
        "max_real_eigenvalue": float(np.max(np.real(eigenvalues))),
        "absorption_probability_sum": float(
            absorption_probabilities.sum()
        ),
    }


def expected_fluxes(
    residence: np.ndarray,
    rates: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    """
    Expected transition counts before absorption.

        J_jk = tau_j W_jk.

    Return edge flux matrix and node throughflow.
    """
    edge_flux = residence[:, None] * rates

    outgoing = edge_flux.sum(axis=1)
    incoming = edge_flux.sum(axis=0)

    throughflow = incoming + outgoing

    return edge_flux, throughflow


def finite_time_transient_distribution(
    mu: np.ndarray,
    q: np.ndarray,
    time_value: float,
) -> np.ndarray:
    """p_transient(t) = mu exp(Q t)."""
    return mu @ expm(q * time_value)


def apply_soft_blockade(
    rates: np.ndarray,
    state_index: int,
    block_factor: float,
) -> np.ndarray:
    """
    Suppress all transition rates into and out of one transient sector.

    The diagonal is rebuilt later from the modified off-diagonal rates.
    """
    modified = rates.copy()

    modified[state_index, :] *= block_factor
    modified[:, state_index] *= block_factor

    modified[state_index, state_index] = 0.0

    return modified


def causal_intervention_table(
    k_values: np.ndarray,
    defects: np.ndarray,
    base_rates: np.ndarray,
    hazards: np.ndarray,
    mu: np.ndarray,
    base_target_probability: float,
    config: Config,
) -> pd.DataFrame:
    """
    Soft-block every interior non-target transient sector.

    Boundary sectors are excluded because the default initial distribution
    places probability mass there, which would confound pathway blockade with
    initial-condition intervention.
    """
    rows = []

    for index, k in enumerate(k_values):
        is_boundary = index in (0, len(k_values) - 1)
        is_target = int(k) == config.target_k

        if is_boundary or is_target:
            continue

        blocked_rates = apply_soft_blockade(
            base_rates,
            index,
            config.block_factor,
        )

        q_block, r_block = absorbing_matrices(
            blocked_rates,
            hazards,
        )

        blocked = absorption_analysis(
            q_block,
            r_block,
            mu,
        )

        target_index = int(
            np.where(k_values == config.target_k)[0][0]
        )

        blocked_target_probability = float(
            blocked["absorption_probabilities"][target_index]
        )

        rows.append(
            {
                "k": int(k),
                "defect_D": float(defects[index]),
                "blocked_target_probability": blocked_target_probability,
                "causal_effect_on_target": (
                    base_target_probability
                    - blocked_target_probability
                ),
                "relative_causal_effect": (
                    (
                        base_target_probability
                        - blocked_target_probability
                    )
                    / base_target_probability
                    if base_target_probability > 0.0
                    else np.nan
                ),
            }
        )

    return pd.DataFrame(rows)


def schur_eliminate_one(
    q: np.ndarray,
    r: np.ndarray,
    eliminate_index: int,
) -> dict:
    """
    Eliminate one transient state exactly by Schur complement.

    Partition:
        retained states A
        eliminated scalar state j

    Q_eff = Q_AA - Q_Aj Q_jj^(-1) Q_jA
    R_eff = R_A  - Q_Aj Q_jj^(-1) R_j
    """
    n = q.shape[0]

    retained = np.array(
        [index for index in range(n) if index != eliminate_index],
        dtype=int,
    )

    q_aa = q[np.ix_(retained, retained)]

    q_aj = q[np.ix_(retained, [eliminate_index])]
    q_ja = q[np.ix_([eliminate_index], retained)]
    q_jj = float(q[eliminate_index, eliminate_index])

    r_a = r[retained, :]
    r_j = r[[eliminate_index], :]

    correction_q = (
        q_aj
        * (1.0 / q_jj)
        @ q_ja
    )

    # Q_eff = Q_AA - correction_q.
    q_eff = q_aa - correction_q

    correction_r = (
        q_aj
        * (1.0 / q_jj)
        @ r_j
    )

    r_eff = r_a - correction_r

    delta_q = q_eff - q_aa
    delta_r = r_eff - r_a

    return {
        "retained_indices": retained,
        "q_eff": q_eff,
        "r_eff": r_eff,
        "delta_q": delta_q,
        "delta_r": delta_r,
        "transition_footprint_norm": float(
            np.linalg.norm(delta_q, ord="fro")
        ),
        "absorption_footprint_norm": float(
            np.linalg.norm(delta_r, ord="fro")
        ),
        "total_boundary_footprint": float(
            np.sqrt(
                np.linalg.norm(delta_q, ord="fro") ** 2
                + np.linalg.norm(delta_r, ord="fro") ** 2
            )
        ),
        "maximum_induced_transition": float(
            np.max(np.abs(delta_q))
        ),
        "maximum_induced_absorption": float(
            np.max(np.abs(delta_r))
        ),
    }


def schur_footprint_table(
    k_values: np.ndarray,
    q: np.ndarray,
    r: np.ndarray,
    full_absorption_matrix: np.ndarray,
) -> pd.DataFrame:
    rows = []

    for index, k in enumerate(k_values):
        eliminated = schur_eliminate_one(
            q,
            r,
            index,
        )

        retained = eliminated["retained_indices"]

        reduced_absorption_matrix = (
            np.linalg.inv(-eliminated["q_eff"])
            @ eliminated["r_eff"]
        )

        exact_reference = full_absorption_matrix[
            retained,
            :
        ]

        preservation_error = float(
            np.linalg.norm(
                reduced_absorption_matrix - exact_reference,
                ord="fro",
            )
        )

        rows.append(
            {
                "k": int(k),
                "transition_boundary_footprint": eliminated[
                    "transition_footprint_norm"
                ],
                "absorption_boundary_footprint": eliminated[
                    "absorption_footprint_norm"
                ],
                "total_boundary_footprint": eliminated[
                    "total_boundary_footprint"
                ],
                "maximum_induced_transition": eliminated[
                    "maximum_induced_transition"
                ],
                "maximum_induced_absorption": eliminated[
                    "maximum_induced_absorption"
                ],
                "absorption_statistics_preservation_error": (
                    preservation_error
                ),
            }
        )

    return pd.DataFrame(rows)


def safe_correlation(x: np.ndarray, y: np.ndarray) -> float:
    """Pearson correlation when both vectors have nonzero variance."""
    if len(x) < 2:
        return np.nan

    if np.std(x) == 0.0 or np.std(y) == 0.0:
        return np.nan

    return float(np.corrcoef(x, y)[0, 1])


def plot_transient_memory(
    sector_table: pd.DataFrame,
    config: Config,
    output_dir: Path,
) -> None:
    plt.figure(figsize=(10, 6))

    plt.plot(
        sector_table["k"],
        sector_table["expected_residence_time"],
        marker="o",
        label="Expected residence time",
    )

    plt.plot(
        sector_table["k"],
        sector_table["expected_throughflow"],
        marker="o",
        label="Expected pathway throughflow",
    )

    plt.xlabel("Transient closure sector k")
    plt.ylabel("Integrated pathway measure")
    plt.title(
        "Transient Sectors Retain Dynamical Memory Despite Zero Final Occupancy"
    )
    plt.legend(frameon=False)
    plt.tight_layout()
    plt.savefig(
        output_dir / "transient_pathway_memory.png",
        dpi=180,
    )
    plt.close()


def plot_causal_effect(
    causal: pd.DataFrame,
    output_dir: Path,
) -> None:
    plt.figure(figsize=(10, 5))

    plt.bar(
        causal["k"],
        causal["causal_effect_on_target"],
    )

    plt.xlabel("Soft-blocked transient sector k")
    plt.ylabel("Decrease in P(commit to k=12)")
    plt.title("Intervention-Based Pathway Contribution to k=12 Closure")
    plt.tight_layout()
    plt.savefig(
        output_dir / "causal_intervention_effect.png",
        dpi=180,
    )
    plt.close()


def plot_boundary_footprint(
    footprint: pd.DataFrame,
    output_dir: Path,
) -> None:
    plt.figure(figsize=(10, 5))

    plt.plot(
        footprint["k"],
        footprint["transition_boundary_footprint"],
        marker="o",
        label="Induced transition footprint",
    )

    plt.plot(
        footprint["k"],
        footprint["absorption_boundary_footprint"],
        marker="o",
        label="Induced absorption footprint",
    )

    plt.xlabel("Eliminated transient sector k")
    plt.ylabel("Schur-complement footprint norm")
    plt.title(
        "Eliminated Sectors Survive as Effective Boundary Terms"
    )
    plt.legend(frameon=False)
    plt.tight_layout()
    plt.savefig(
        output_dir / "schur_boundary_footprints.png",
        dpi=180,
    )
    plt.close()


def plot_absorption_probabilities(
    sector_table: pd.DataFrame,
    config: Config,
    output_dir: Path,
) -> None:
    plt.figure(figsize=(10, 5))

    plt.plot(
        sector_table["k"],
        sector_table["final_absorption_probability"],
        marker="o",
    )

    plt.axvline(
        config.target_k,
        linestyle="--",
        label=f"DCT target k={config.target_k}",
    )

    plt.xlabel("Committed closure outcome k")
    plt.ylabel("Final absorption probability")
    plt.title("Final Committed Outcome Distribution")
    plt.legend(frameon=False)
    plt.tight_layout()
    plt.savefig(
        output_dir / "final_absorption_probabilities.png",
        dpi=180,
    )
    plt.close()


def main() -> None:
    config = Config()
    output_dir = Path(config.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    k_values = np.arange(
        config.k_min,
        config.k_max + 1,
        dtype=int,
    )

    defects = closure_defect(k_values)

    adjacency = path_adjacency(len(k_values))

    rates = detailed_balance_rates(
        defects=defects,
        selection_strength=config.selection_strength,
        attempt_frequency=config.attempt_frequency,
        adjacency=adjacency,
    )

    hazards = commitment_hazards(
        defects=defects,
        selection_strength=config.selection_strength,
        commitment_rate_scale=config.commitment_rate_scale,
    )

    q, r = absorbing_matrices(
        rates,
        hazards,
    )

    mu = initial_distribution(
        k_values,
        config,
    )

    baseline = absorption_analysis(
        q,
        r,
        mu,
    )

    residence = baseline["residence"]
    absorption_probabilities = baseline[
        "absorption_probabilities"
    ]

    edge_flux, throughflow = expected_fluxes(
        residence,
        rates,
    )

    long_time_transient = finite_time_transient_distribution(
        mu,
        q,
        config.long_time,
    )

    target_index = int(
        np.where(k_values == config.target_k)[0][0]
    )

    target_probability = float(
        absorption_probabilities[target_index]
    )

    sector_table = pd.DataFrame(
        {
            "k": k_values,
            "defect_D": defects,
            "initial_transient_probability": mu,
            "expected_residence_time": residence,
            "expected_throughflow": throughflow,
            "long_time_transient_occupancy": long_time_transient,
            "commitment_hazard": hazards,
            "final_absorption_probability": absorption_probabilities,
        }
    )

    sector_table.to_csv(
        output_dir / "transient_sector_memory_table.csv",
        index=False,
    )

    pd.DataFrame(
        edge_flux,
        index=[f"k_{k}" for k in k_values],
        columns=[f"k_{k}" for k in k_values],
    ).to_csv(
        output_dir / "expected_transition_flux_matrix.csv",
    )

    causal = causal_intervention_table(
        k_values=k_values,
        defects=defects,
        base_rates=rates,
        hazards=hazards,
        mu=mu,
        base_target_probability=target_probability,
        config=config,
    )

    causal.to_csv(
        output_dir / "causal_pathway_interventions.csv",
        index=False,
    )

    footprint = schur_footprint_table(
        k_values=k_values,
        q=q,
        r=r,
        full_absorption_matrix=baseline["absorption_matrix"],
    )

    footprint.to_csv(
        output_dir / "schur_boundary_footprints.csv",
        index=False,
    )

    merged = (
        sector_table
        .merge(
            footprint,
            on="k",
            how="left",
        )
        .merge(
            causal[
                [
                    "k",
                    "causal_effect_on_target",
                    "relative_causal_effect",
                ]
            ],
            on="k",
            how="left",
        )
    )

    merged.to_csv(
        output_dir / "entry10_combined_diagnostics.csv",
        index=False,
    )

    plot_transient_memory(
        sector_table,
        config,
        output_dir,
    )

    plot_causal_effect(
        causal,
        output_dir,
    )

    plot_boundary_footprint(
        footprint,
        output_dir,
    )

    plot_absorption_probabilities(
        sector_table,
        config,
        output_dir,
    )

    interior_causal = merged.dropna(
        subset=["causal_effect_on_target"]
    )

    correlations = pd.DataFrame(
        [
            {
                "comparison":
                    "causal effect vs expected residence",
                "pearson_correlation": safe_correlation(
                    interior_causal[
                        "causal_effect_on_target"
                    ].to_numpy(),
                    interior_causal[
                        "expected_residence_time"
                    ].to_numpy(),
                ),
            },
            {
                "comparison":
                    "causal effect vs pathway throughflow",
                "pearson_correlation": safe_correlation(
                    interior_causal[
                        "causal_effect_on_target"
                    ].to_numpy(),
                    interior_causal[
                        "expected_throughflow"
                    ].to_numpy(),
                ),
            },
            {
                "comparison":
                    "causal effect vs Schur boundary footprint",
                "pearson_correlation": safe_correlation(
                    interior_causal[
                        "causal_effect_on_target"
                    ].to_numpy(),
                    interior_causal[
                        "total_boundary_footprint"
                    ].to_numpy(),
                ),
            },
        ]
    )

    correlations.to_csv(
        output_dir / "pathway_correlation_summary.csv",
        index=False,
    )

    asymptotic_extinction_verified = bool(
        baseline["max_real_eigenvalue"] < 0.0
    )

    finite_time_extinction_residual = float(
        np.sum(long_time_transient)
    )

    absorption_normalization_error = abs(
        baseline["absorption_probability_sum"] - 1.0
    )

    maximum_schur_preservation_error = float(
        footprint[
            "absorption_statistics_preservation_error"
        ].max()
    )

    nonzero_residence_count = int(
        np.sum(residence > 1.0e-12)
    )

    nonzero_footprint_count = int(
        np.sum(
            footprint["total_boundary_footprint"]
            > 1.0e-12
        )
    )

    positive_causal_count = int(
        np.sum(
            causal["causal_effect_on_target"]
            > 1.0e-12
        )
    )

    top_causal = causal.sort_values(
        "causal_effect_on_target",
        ascending=False,
    ).head(10)

    top_footprint = footprint.sort_values(
        "total_boundary_footprint",
        ascending=False,
    ).head(10)

    print()
    print("Dynamic Closure Notebook — Entry 10")
    print("Transient-State Causality and Boundary Footprints")
    print("-" * 66)
    print()
    print(
        "All transient states asymptotically vanish: "
        f"{asymptotic_extinction_verified}"
    )
    print(
        "Total transient probability at finite long-time check "
        f"t={config.long_time:g}: "
        f"{finite_time_extinction_residual:.6e}"
    )
    print()
    print(
        "Absorption-probability normalization error: "
        f"{absorption_normalization_error:.6e}"
    )
    print()
    print(
        f"Baseline P(commit to k={config.target_k}): "
        f"{target_probability:.6f}"
    )
    print()
    print(
        "Transient sectors with nonzero expected residence: "
        f"{nonzero_residence_count}/{len(k_values)}"
    )
    print(
        "Transient sectors with nonzero Schur boundary footprint: "
        f"{nonzero_footprint_count}/{len(k_values)}"
    )
    print(
        "Interior non-target sectors with positive soft-block causal effect: "
        f"{positive_causal_count}/{len(causal)}"
    )
    print()
    print(
        "Maximum Schur absorption-statistics preservation error: "
        f"{maximum_schur_preservation_error:.6e}"
    )
    print()
    print("Top intervention-based pathway contributors:")
    print(
        top_causal[
            [
                "k",
                "causal_effect_on_target",
                "relative_causal_effect",
            ]
        ].to_string(index=False)
    )
    print()
    print("Largest effective boundary footprints:")
    print(
        top_footprint[
            [
                "k",
                "transition_boundary_footprint",
                "absorption_boundary_footprint",
                "total_boundary_footprint",
            ]
        ].to_string(index=False)
    )
    print()
    print("Pathway correlations:")
    print(correlations.to_string(index=False))
    print()
    print("Interpretation:")
    print(
        "    Terminal transient occupancy goes to zero, but residence, flux, "
        "intervention effects, and Schur-complement boundary terms remain "
        "nonzero."
    )
    print(
        "    Eliminating a transient state transfers its influence into "
        "effective couplings and sink terms rather than erasing it."
    )
    print()
    print(f"Outputs written to: {output_dir.resolve()}")


if __name__ == "__main__":
    main()
