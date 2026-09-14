"""
Dynamic Closure Notebook — Entry 09
Closure Defect and Theorem-Compatible Selection Functional

Purpose
-------
Entry 09 begins the post-theorem phase.

The Dynamic Closure Theorem (DCT) fixes the exact closure condition

    F_k = C(k) = k^2.

DCT therefore fixes the ZERO SET of any valid closure-defect functional:

    defect(k) = 0  iff  F_k = k^2.

DCT does NOT uniquely fix how nonzero defects should be dynamically penalized.
That modeling layer must be stated separately and tested.

Canonical ratio defect
----------------------
For positive F_k and C(k)=k^2, define

    rho_k = F_k / k^2,

    D_k = |ln(rho_k)|.

Properties:
    D_k >= 0,
    D_k = 0 iff F_k = k^2,
    D(F,C) = D(C,F),
    multiplicative mismatch becomes additive in log space.

The previously used bounded residual is not independent:

    B_k = |F_k-k^2| / (F_k+k^2)
        = tanh(D_k/2).

Thus B_k and D_k have exactly the same ordering and the same unique zero.
The earlier candidate residual is therefore a bounded monotone representation
of the theorem-compatible logarithmic defect.

Maximum-entropy selection functional
------------------------------------
On a finite candidate set K, use a uniform prior and constrain only the
ensemble mean closure defect <D>. Maximizing Shannon entropy yields

    pi_k(lambda)
        = exp(-lambda D_k) / Z(lambda),

where

    Z(lambda) = sum_j exp(-lambda D_j),

and lambda >= 0 is a dimensionless selection-strength parameter.

Important:
    lambda is NOT derived by DCT.
    It controls how strongly dynamics resolves structural mismatch.

At lambda = 0:
    pi_k is uniform.

As lambda increases:
    probability concentrates on minimum-defect sectors.

Detailed-balance jump dynamics
------------------------------
For any symmetric connected adjacency A_jk, define

    W_(j->k)
      = nu A_jk exp[-lambda (D_k-D_j)/2].

Then

    W_(j->k) / W_(k->j)
      = exp[-lambda(D_k-D_j)]
      = pi_k / pi_j,

so

    pi_j W_(j->k) = pi_k W_(k->j).

Therefore pi is stationary by detailed balance.

The topology controls kinetics/pathways but not the stationary MaxEnt
distribution, provided the graph is symmetric and connected.

Scientific status
-----------------
Exact:
    D_k = 0 iff F_k=k^2.
    B_k = tanh(D_k/2).
    Detailed-balance identity for the declared rate family.

Inference principle:
    exponential weighting follows from maximum entropy under a mean-defect
    constraint and a uniform prior.

Model parameter:
    lambda is phenomenological until EDF supplies a microscopic coupling law.

This entry does not modify the DCT premises or theorem.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


@dataclass
class Config:
    k_min: int = 2
    k_max: int = 36

    lambda_values: tuple[float, ...] = (
        0.0,
        0.25,
        0.5,
        1.0,
        2.0,
        4.0,
        8.0,
    )

    attempt_frequency: float = 1.0

    diagnostic_lambda: float = 2.0
    diagnostic_k: int = 12

    output_dir: str = "dynamic_closure_entry_09_output"


def fibonacci(n: int) -> int:
    """Return F_n with F_0=0 and F_1=1 using exact integer arithmetic."""
    if n < 0:
        raise ValueError("Fibonacci index must be non-negative.")

    a, b = 0, 1

    for _ in range(n):
        a, b = b, a + b

    return a


def structural_table(config: Config) -> pd.DataFrame:
    rows = []

    for k in range(config.k_min, config.k_max + 1):
        fib = fibonacci(k)
        capacity = k * k

        signed_defect = fib - capacity
        absolute_defect = abs(signed_defect)

        ratio = fib / capacity

        log_defect = abs(np.log(ratio))

        bounded_defect = (
            absolute_defect / (fib + capacity)
        )

        symmetric_relative_defect = (
            absolute_defect / np.sqrt(fib * capacity)
        )

        bounded_from_log = np.tanh(log_defect / 2.0)
        symmetric_from_log = 2.0 * np.sinh(log_defect / 2.0)

        rows.append(
            {
                "k": k,
                "F_k": fib,
                "closure_capacity_k2": capacity,
                "signed_integer_defect": signed_defect,
                "absolute_integer_defect": absolute_defect,
                "ratio_F_over_C": ratio,
                "log_ratio_defect_D": log_defect,
                "bounded_defect_B": bounded_defect,
                "bounded_from_tanh_D_over_2": bounded_from_log,
                "bounded_identity_error": abs(
                    bounded_defect - bounded_from_log
                ),
                "symmetric_relative_defect": symmetric_relative_defect,
                "symmetric_from_2sinh_D_over_2": symmetric_from_log,
                "symmetric_identity_error": abs(
                    symmetric_relative_defect - symmetric_from_log
                ),
                "exact_DCT_closure": fib == capacity,
            }
        )

    return pd.DataFrame(rows)


def maxent_distribution(
    defects: np.ndarray,
    selection_strength: float,
) -> np.ndarray:
    """
    pi_k(lambda) = exp(-lambda D_k) / Z.

    A stable log-sum-exp style shift is used.
    """
    log_weights = -selection_strength * defects
    log_weights -= np.max(log_weights)

    weights = np.exp(log_weights)

    return weights / weights.sum()


def selection_table(
    structure: pd.DataFrame,
    config: Config,
) -> pd.DataFrame:
    defects = structure["log_ratio_defect_D"].to_numpy(dtype=float)
    k_values = structure["k"].to_numpy(dtype=int)

    rows = []

    for selection_strength in config.lambda_values:
        probabilities = maxent_distribution(
            defects,
            selection_strength,
        )

        expected_defect = float(
            np.sum(probabilities * defects)
        )

        entropy = float(
            -np.sum(
                probabilities
                * np.log(np.where(probabilities > 0.0, probabilities, 1.0))
            )
        )

        for k, defect, probability in zip(
            k_values,
            defects,
            probabilities,
        ):
            rows.append(
                {
                    "lambda": selection_strength,
                    "k": int(k),
                    "defect_D": float(defect),
                    "selection_probability": float(probability),
                    "ensemble_mean_defect": expected_defect,
                    "selection_entropy": entropy,
                }
            )

    return pd.DataFrame(rows)


def complete_adjacency(n: int) -> np.ndarray:
    adjacency = np.ones((n, n), dtype=float)
    np.fill_diagonal(adjacency, 0.0)
    return adjacency


def path_adjacency(n: int) -> np.ndarray:
    adjacency = np.zeros((n, n), dtype=float)

    for index in range(n - 1):
        adjacency[index, index + 1] = 1.0
        adjacency[index + 1, index] = 1.0

    return adjacency


def jump_rates(
    defects: np.ndarray,
    selection_strength: float,
    attempt_frequency: float,
    adjacency: np.ndarray,
) -> np.ndarray:
    """
    W[j,k] = rate j -> k.

    For symmetric adjacency:
        W[j,k]/W[k,j] = exp[-lambda(D_k-D_j)].
    """
    delta = defects[None, :] - defects[:, None]

    rates = (
        attempt_frequency
        * adjacency
        * np.exp(-0.5 * selection_strength * delta)
    )

    np.fill_diagonal(rates, 0.0)

    return rates


def generator_from_rates(rates: np.ndarray) -> np.ndarray:
    """
    Row-vector convention:
        dp/dt = p Q

    Q[j,k] = W[j,k], j != k
    Q[j,j] = -sum_{k != j} W[j,k].
    """
    generator = rates.copy()
    np.fill_diagonal(
        generator,
        -rates.sum(axis=1),
    )
    return generator


def detailed_balance_diagnostics(
    defects: np.ndarray,
    selection_strength: float,
    attempt_frequency: float,
    adjacency: np.ndarray,
) -> dict:
    pi = maxent_distribution(
        defects,
        selection_strength,
    )

    rates = jump_rates(
        defects,
        selection_strength,
        attempt_frequency,
        adjacency,
    )

    generator = generator_from_rates(rates)

    flux_error = 0.0
    ratio_error = 0.0

    n = len(defects)

    for j in range(n):
        for k in range(n):
            if j == k or adjacency[j, k] == 0.0:
                continue

            left_flux = pi[j] * rates[j, k]
            right_flux = pi[k] * rates[k, j]

            flux_error = max(
                flux_error,
                abs(left_flux - right_flux),
            )

            measured_ratio = rates[j, k] / rates[k, j]
            expected_ratio = np.exp(
                -selection_strength
                * (defects[k] - defects[j])
            )

            ratio_error = max(
                ratio_error,
                abs(measured_ratio - expected_ratio),
            )

    stationary_residual = np.linalg.norm(
        pi @ generator,
        ord=1,
    )

    # The nonzero eigenvalue closest to zero controls asymptotic relaxation.
    eigenvalues = np.linalg.eigvals(generator)

    real_parts = np.sort(
        np.real(eigenvalues)
    )

    nonzero_magnitudes = sorted(
        [
            abs(np.real(value))
            for value in eigenvalues
            if abs(value) > 1.0e-10
        ]
    )

    spectral_gap = (
        nonzero_magnitudes[0]
        if nonzero_magnitudes
        else 0.0
    )

    return {
        "maximum_detailed_balance_flux_error": float(flux_error),
        "maximum_rate_ratio_error": float(ratio_error),
        "stationary_distribution_residual_L1": float(
            stationary_residual
        ),
        "spectral_gap": float(spectral_gap),
        "minimum_generator_real_eigenvalue": float(real_parts[0]),
        "maximum_generator_real_eigenvalue": float(real_parts[-1]),
    }


def topology_diagnostics(
    structure: pd.DataFrame,
    config: Config,
) -> pd.DataFrame:
    defects = structure["log_ratio_defect_D"].to_numpy(dtype=float)
    n = len(defects)

    topologies = {
        "complete_graph": complete_adjacency(n),
        "path_graph": path_adjacency(n),
    }

    rows = []

    for selection_strength in config.lambda_values:
        for topology_name, adjacency in topologies.items():
            result = detailed_balance_diagnostics(
                defects=defects,
                selection_strength=selection_strength,
                attempt_frequency=config.attempt_frequency,
                adjacency=adjacency,
            )

            result["lambda"] = selection_strength
            result["topology"] = topology_name

            rows.append(result)

    return pd.DataFrame(rows)


def monotone_equivalence_table(
    structure: pd.DataFrame,
) -> pd.DataFrame:
    """
    Demonstrate that D, B=tanh(D/2), and the symmetric relative defect
    induce the same ordering because they are monotone transforms of D.
    """
    table = structure[
        [
            "k",
            "log_ratio_defect_D",
            "bounded_defect_B",
            "symmetric_relative_defect",
        ]
    ].copy()

    table["rank_D"] = table["log_ratio_defect_D"].rank(
        method="min",
    )
    table["rank_B"] = table["bounded_defect_B"].rank(
        method="min",
    )
    table["rank_symmetric"] = table[
        "symmetric_relative_defect"
    ].rank(
        method="min",
    )

    table["all_ranks_equal"] = (
        (table["rank_D"] == table["rank_B"])
        & (table["rank_D"] == table["rank_symmetric"])
    )

    return table


def lambda_summary(
    selection: pd.DataFrame,
    config: Config,
) -> pd.DataFrame:
    rows = []

    uniform_probability = 1.0 / (
        config.k_max - config.k_min + 1
    )

    for selection_strength in config.lambda_values:
        subset = selection[
            np.isclose(selection["lambda"], selection_strength)
        ]

        target_probability = float(
            subset.loc[
                subset["k"] == config.diagnostic_k,
                "selection_probability",
            ].iloc[0]
        )

        probabilities = subset[
            "selection_probability"
        ].to_numpy(dtype=float)

        defects = subset[
            "defect_D"
        ].to_numpy(dtype=float)

        mean_defect = float(
            subset["ensemble_mean_defect"].iloc[0]
        )

        defect_variance = float(
            np.sum(
                probabilities
                * (defects - mean_defect) ** 2
            )
        )

        highest_probability = float(
            subset["selection_probability"].max()
        )

        tied_winners = subset.loc[
            np.isclose(
                subset["selection_probability"],
                highest_probability,
                rtol=0.0,
                atol=1.0e-14,
            ),
            "k",
        ].astype(int).tolist()

        rows.append(
            {
                "lambda": selection_strength,
                "target_k": config.diagnostic_k,
                "target_probability": target_probability,
                "uniform_probability": uniform_probability,
                "target_gain_over_uniform": (
                    target_probability / uniform_probability
                ),
                "highest_probability_k": ",".join(
                    str(value) for value in tied_winners
                ),
                "highest_probability_tie_count": len(tied_winners),
                "highest_probability": highest_probability,
                "ensemble_mean_defect": mean_defect,
                "defect_variance": defect_variance,
                "analytic_d_mean_defect_d_lambda":
                    -defect_variance,
                "analytic_d_entropy_d_lambda":
                    -selection_strength * defect_variance,
                "analytic_d_log_target_probability_d_lambda":
                    mean_defect,
                "selection_entropy": float(
                    subset["selection_entropy"].iloc[0]
                ),
            }
        )

    return pd.DataFrame(rows)


def plot_defect_equivalence(
    structure: pd.DataFrame,
    output_dir: Path,
) -> None:
    plt.figure(figsize=(10, 6))

    plt.plot(
        structure["k"],
        structure["log_ratio_defect_D"],
        marker="o",
        label="Log-ratio defect D",
    )

    plt.plot(
        structure["k"],
        structure["bounded_defect_B"],
        marker="o",
        label="Bounded residual B=tanh(D/2)",
    )

    plt.xlabel("Closure sector k")
    plt.ylabel("Dimensionless closure defect")
    plt.title("DCT-Compatible Closure-Defect Representations")
    plt.legend(frameon=False)
    plt.tight_layout()
    plt.savefig(
        output_dir / "closure_defect_representations.png",
        dpi=180,
    )
    plt.close()


def plot_selection_distributions(
    selection: pd.DataFrame,
    config: Config,
    output_dir: Path,
) -> None:
    plt.figure(figsize=(10, 6))

    for selection_strength in config.lambda_values:
        subset = selection[
            np.isclose(selection["lambda"], selection_strength)
        ]

        plt.plot(
            subset["k"],
            subset["selection_probability"],
            marker="o",
            label=f"lambda={selection_strength:g}",
        )

    plt.xlabel("Closure sector k")
    plt.ylabel("Maximum-entropy selection probability")
    plt.title("DCT Defect Selection Family")
    plt.legend(frameon=False, fontsize=8)
    plt.tight_layout()
    plt.savefig(
        output_dir / "maxent_selection_family.png",
        dpi=180,
    )
    plt.close()


def plot_target_gain(
    summary: pd.DataFrame,
    config: Config,
    output_dir: Path,
) -> None:
    plt.figure(figsize=(9, 5))

    plt.plot(
        summary["lambda"],
        summary["target_probability"],
        marker="o",
        label=f"P(k={config.diagnostic_k})",
    )

    plt.plot(
        summary["lambda"],
        summary["uniform_probability"],
        linestyle="--",
        label="Uniform baseline",
    )

    plt.xlabel("Selection strength lambda")
    plt.ylabel("Selection probability")
    plt.title(
        f"Theorem-Derived Closure Preference for k={config.diagnostic_k}"
    )
    plt.legend(frameon=False)
    plt.tight_layout()
    plt.savefig(
        output_dir / "target_selection_probability.png",
        dpi=180,
    )
    plt.close()


def plot_entropy_and_mean_defect(
    summary: pd.DataFrame,
    output_dir: Path,
) -> None:
    plt.figure(figsize=(9, 5))

    plt.plot(
        summary["lambda"],
        summary["selection_entropy"],
        marker="o",
        label="Selection entropy",
    )

    plt.xlabel("Selection strength lambda")
    plt.ylabel("Shannon entropy")
    plt.title("Selection Entropy Under Increasing Closure Resolution")
    plt.legend(frameon=False)
    plt.tight_layout()
    plt.savefig(
        output_dir / "selection_entropy_vs_lambda.png",
        dpi=180,
    )
    plt.close()

    plt.figure(figsize=(9, 5))

    plt.plot(
        summary["lambda"],
        summary["ensemble_mean_defect"],
        marker="o",
    )

    plt.xlabel("Selection strength lambda")
    plt.ylabel("Mean log-ratio closure defect")
    plt.title("Mean Closure Defect Under Maximum-Entropy Selection")
    plt.tight_layout()
    plt.savefig(
        output_dir / "mean_defect_vs_lambda.png",
        dpi=180,
    )
    plt.close()


def plot_topology_spectral_gap(
    topology: pd.DataFrame,
    output_dir: Path,
) -> None:
    plt.figure(figsize=(9, 5))

    for topology_name in topology["topology"].unique():
        subset = topology[
            topology["topology"] == topology_name
        ].sort_values("lambda")

        plt.plot(
            subset["lambda"],
            subset["spectral_gap"],
            marker="o",
            label=topology_name,
        )

    plt.xlabel("Selection strength lambda")
    plt.ylabel("Generator spectral gap")
    plt.title("Topology Changes Kinetics Without Changing the Stationary Law")
    plt.legend(frameon=False)
    plt.tight_layout()
    plt.savefig(
        output_dir / "topology_spectral_gap.png",
        dpi=180,
    )
    plt.close()


def main() -> None:
    config = Config()

    output_dir = Path(config.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    structure = structural_table(config)
    structure.to_csv(
        output_dir / "closure_defect_table.csv",
        index=False,
    )

    monotone = monotone_equivalence_table(structure)
    monotone.to_csv(
        output_dir / "defect_monotone_equivalence.csv",
        index=False,
    )

    selection = selection_table(structure, config)
    selection.to_csv(
        output_dir / "maxent_selection_family.csv",
        index=False,
    )

    summary = lambda_summary(selection, config)
    summary.to_csv(
        output_dir / "selection_lambda_summary.csv",
        index=False,
    )

    topology = topology_diagnostics(structure, config)
    topology.to_csv(
        output_dir / "detailed_balance_topology_diagnostics.csv",
        index=False,
    )

    plot_defect_equivalence(
        structure,
        output_dir,
    )

    plot_selection_distributions(
        selection,
        config,
        output_dir,
    )

    plot_target_gain(
        summary,
        config,
        output_dir,
    )

    plot_entropy_and_mean_defect(
        summary,
        output_dir,
    )

    plot_topology_spectral_gap(
        topology,
        output_dir,
    )

    exact_zero_sectors = structure.loc[
        structure["exact_DCT_closure"],
        "k",
    ].tolist()

    bounded_identity_verified = bool(
        structure["bounded_identity_error"].max() < 1.0e-12
    )

    symmetric_identity_verified = bool(
        structure["symmetric_identity_error"].max() < 1.0e-12
    )

    monotone_ranking_verified = bool(
        np.all(monotone["all_ranks_equal"])
    )

    target_probability_monotone = bool(
        np.all(
            np.diff(summary["target_probability"].to_numpy(dtype=float))
            >= -1.0e-14
        )
    )

    mean_defect_monotone = bool(
        np.all(
            np.diff(summary["ensemble_mean_defect"].to_numpy(dtype=float))
            <= 1.0e-14
        )
    )

    entropy_monotone = bool(
        np.all(
            np.diff(summary["selection_entropy"].to_numpy(dtype=float))
            <= 1.0e-14
        )
    )

    detailed_balance_verified = bool(
        topology[
            "maximum_detailed_balance_flux_error"
        ].max()
        < 1.0e-12
    )

    stationarity_verified = bool(
        topology[
            "stationary_distribution_residual_L1"
        ].max()
        < 1.0e-12
    )

    print()
    print("Dynamic Closure Notebook — Entry 09")
    print("Closure Defect and Theorem-Compatible Selection Functional")
    print("-" * 72)
    print()
    print("DCT closure condition:")
    print("    F_k = C(k) = k^2")
    print()
    print("Canonical dimensionless closure defect:")
    print("    D_k = |ln(F_k/k^2)|")
    print()
    print(
        "Exact zero-defect sectors in configured range: "
        f"{exact_zero_sectors}"
    )
    print()
    print(
        "Identity B_k = tanh(D_k/2) verified: "
        f"{bounded_identity_verified}"
    )
    print(
        "Identity symmetric defect = 2*sinh(D_k/2) verified: "
        f"{symmetric_identity_verified}"
    )
    print(
        "All monotone defect representations give identical ranking: "
        f"{monotone_ranking_verified}"
    )
    print()
    print("Maximum-entropy selection law:")
    print("    pi_k(lambda) = exp(-lambda D_k) / Z(lambda)")
    print()
    print(summary.to_string(index=False))
    print()
    print(
        "Target probability nondecreasing across lambda grid: "
        f"{target_probability_monotone}"
    )
    print(
        "Mean defect nonincreasing across lambda grid: "
        f"{mean_defect_monotone}"
    )
    print(
        "Selection entropy nonincreasing across lambda grid: "
        f"{entropy_monotone}"
    )
    print()
    print(
        "Detailed balance verified for complete and path graphs: "
        f"{detailed_balance_verified}"
    )
    print(
        "MaxEnt distribution stationary for both graph topologies: "
        f"{stationarity_verified}"
    )
    print()
    print(
        "Interpretation:"
    )
    print(
        "    DCT determines where the defect is exactly zero."
    )
    print(
        "    Maximum entropy supplies the least-committal exponential "
        "selection family once only the mean defect is constrained."
    )
    print(
        "    lambda remains a model parameter until EDF supplies a "
        "microscopic coupling law."
    )
    print()
    print(f"Outputs written to: {output_dir.resolve()}")


if __name__ == "__main__":
    main()
