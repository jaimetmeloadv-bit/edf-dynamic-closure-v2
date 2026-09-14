"""
Dynamic Closure Notebook — Entry 02
Candidate Fibonacci Pair-Closure Functional — Vectorized Edition

Scientific status
-----------------
This notebook tests an explicit candidate closure rule. It does NOT claim that
this rule has already been uniquely derived from EDF.

No preference for k = 12 is inserted by hand.

Candidate rule
--------------
A k-sector closure has k^2 ordered pair relations. Define

    B_k = |F_k - k^2| / (F_k + k^2),

where F_k is the kth Fibonacci number.

Exact pair closure occurs when

    F_k = k^2.

The preferred sector is discovered computationally as argmin(B_k).

Predeclared controls
--------------------
1. Null:
       B_k = 0

2. Fibonacci index shift -1:
       B_k = |F_{k-1} - k^2| / (F_{k-1} + k^2)

3. Fibonacci index shift +1:
       B_k = |F_{k+1} - k^2| / (F_{k+1} + k^2)

4. Linear structural count:
       B_k = |F_k - k| / (F_k + k)

5. Cubic structural count:
       B_k = |F_k - k^3| / (F_k + k^3)

Dynamic model
-------------
Unnormalized populations q_k obey

    dq_k/dt =
        sum_{j != k} W_{j->k} q_j
        - sum_{j != k} W_{k->j} q_k
        - Gamma_eff(k,t) q_k.

Normalized occupancy:

    p_k = q_k / sum_j q_j.

Detailed-balance transition rule:

    W_{j->k} = W0 exp[-beta (B_k - B_j)/2].

Environmental fluctuations enter Gamma_eff through independent
Ornstein-Uhlenbeck processes.

Implementation note
-------------------
Ensemble realizations are vectorized. This changes runtime, not the equations.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


@dataclass
class Config:
    k_values: tuple[int, ...] = tuple(range(4, 25, 2))

    t_max: float = 30.0
    dt: float = 0.05

    base_transition_rate: float = 0.16
    base_loss_rate: float = 0.035

    environment_correlation_time: float = 1.5
    environment_noise_strength: float = 0.030

    ensemble_size: int = 1000
    random_seed: int = 271828

    beta_values: tuple[float, ...] = (0.5, 1.0, 2.0, 4.0)

    output_dir: str = "dynamic_closure_entry_02_output"


def fibonacci(n: int) -> int:
    """Return F_n with F_0 = 0 and F_1 = 1."""
    if n < 0:
        raise ValueError("Fibonacci index must be non-negative.")
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def normalized_residual(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    denominator = np.abs(a) + np.abs(b)
    result = np.zeros_like(denominator, dtype=float)
    mask = denominator > 0.0
    result[mask] = np.abs(a[mask] - b[mask]) / denominator[mask]
    return result


def build_structural_scores(k_values: np.ndarray) -> pd.DataFrame:
    fib_k = np.array([fibonacci(int(k)) for k in k_values], dtype=float)
    fib_k_minus_1 = np.array(
        [fibonacci(int(k) - 1) for k in k_values],
        dtype=float,
    )
    fib_k_plus_1 = np.array(
        [fibonacci(int(k) + 1) for k in k_values],
        dtype=float,
    )

    k_float = k_values.astype(float)
    pair_count = k_float**2
    linear_count = k_float
    cubic_count = k_float**3

    return pd.DataFrame(
        {
            "k": k_values,
            "F_k": fib_k.astype(np.int64),
            "pair_count_k2": pair_count.astype(np.int64),
            "candidate_pair_residual": normalized_residual(
                fib_k,
                pair_count,
            ),
            "control_shift_minus_1": normalized_residual(
                fib_k_minus_1,
                pair_count,
            ),
            "control_shift_plus_1": normalized_residual(
                fib_k_plus_1,
                pair_count,
            ),
            "control_linear": normalized_residual(
                fib_k,
                linear_count,
            ),
            "control_cubic": normalized_residual(
                fib_k,
                cubic_count,
            ),
            "null": np.zeros(len(k_values), dtype=float),
        }
    )


def transition_matrix_from_score(
    score: np.ndarray,
    base_rate: float,
    beta: float,
) -> np.ndarray:
    delta = score[None, :] - score[:, None]
    rates = base_rate * np.exp(-0.5 * beta * delta)
    np.fill_diagonal(rates, 0.0)
    return rates


def entropy_rows(p: np.ndarray) -> np.ndarray:
    safe = np.where(p > 0.0, p, 1.0)
    return -np.sum(np.where(p > 0.0, p * np.log(safe), 0.0), axis=1)


def batch_simulation(
    config: Config,
    score: np.ndarray,
    beta: float,
    seed: int,
    store_first_trajectory: bool = False,
) -> tuple[pd.DataFrame, dict | None]:
    """
    Simulate the complete ensemble simultaneously.

    Arrays have shape:
        q, p, environment: (ensemble_size, n_states)
    """
    rng = np.random.default_rng(seed)

    k_values = np.asarray(config.k_values, dtype=int)
    n_states = len(k_values)
    n_runs = config.ensemble_size

    W = transition_matrix_from_score(
        score,
        config.base_transition_rate,
        beta,
    )
    outgoing_rates = W.sum(axis=1)

    n_steps = int(round(config.t_max / config.dt)) + 1
    times = np.linspace(0.0, config.t_max, n_steps)

    q = np.full(
        (n_runs, n_states),
        1.0 / n_states,
        dtype=float,
    )
    environment = np.zeros_like(q)
    residence = np.zeros_like(q)

    trajectory = None
    if store_first_trajectory:
        first_p_history = np.empty((n_steps, n_states), dtype=float)
        first_entropy_history = np.empty(n_steps, dtype=float)

    dt = config.dt
    tau = config.environment_correlation_time
    sigma = config.environment_noise_strength

    diffusion_scale = (
        sigma
        * np.sqrt(2.0 / tau)
        * np.sqrt(dt)
    )

    for step in range(n_steps):
        total = q.sum(axis=1, keepdims=True)
        p = q / total

        if store_first_trajectory:
            first_p_history[step] = p[0]
            first_entropy_history[step] = entropy_rows(p[:1])[0]

        if step == n_steps - 1:
            break

        residence += p * dt

        environment += (
            -(environment / tau) * dt
            + diffusion_scale * rng.normal(size=environment.shape)
        )

        gamma_eff = np.clip(
            config.base_loss_rate + environment,
            a_min=0.0,
            a_max=None,
        )

        incoming = q @ W
        outgoing = q * outgoing_rates[None, :]

        q += dt * (incoming - outgoing - gamma_eff * q)
        np.maximum(q, 0.0, out=q)

    final_p = q / q.sum(axis=1, keepdims=True)
    selected_indices = np.argmax(final_p, axis=1)

    counts = np.bincount(
        selected_indices,
        minlength=n_states,
    )

    summary = pd.DataFrame(
        {
            "k": k_values,
            "selection_count": counts,
            "selection_probability": counts / n_runs,
            "mean_residence": residence.mean(axis=0),
            "mean_final_occupancy": final_p.mean(axis=0),
        }
    )

    if store_first_trajectory:
        trajectory = {
            "times": times,
            "p_history": first_p_history,
            "entropy_history": first_entropy_history,
        }

    return summary, trajectory


def make_score_plot(
    score_table: pd.DataFrame,
    output_dir: Path,
) -> None:
    plt.figure(figsize=(9, 5))
    plt.plot(
        score_table["k"],
        score_table["candidate_pair_residual"],
        marker="o",
        label="Pair-count candidate",
    )
    plt.plot(
        score_table["k"],
        score_table["control_shift_minus_1"],
        marker="o",
        label="Index shift -1",
    )
    plt.plot(
        score_table["k"],
        score_table["control_shift_plus_1"],
        marker="o",
        label="Index shift +1",
    )
    plt.xlabel("Closure sector k")
    plt.ylabel("Normalized structural residual")
    plt.title("Candidate Fibonacci Closure Score and Index-Shift Controls")
    plt.legend(frameon=False)
    plt.tight_layout()
    plt.savefig(
        output_dir / "structural_residuals.png",
        dpi=180,
    )
    plt.close()


def make_selection_plot(
    comparison: pd.DataFrame,
    beta: float,
    output_dir: Path,
) -> None:
    subset = comparison[np.isclose(comparison["beta"], beta)]

    model_order = [
        "null",
        "candidate_pair_residual",
        "control_shift_minus_1",
        "control_shift_plus_1",
        "control_linear",
        "control_cubic",
    ]

    plt.figure(figsize=(10, 6))
    for model_name in model_order:
        model_data = subset[subset["model"] == model_name]
        plt.plot(
            model_data["k"],
            model_data["selection_probability"],
            marker="o",
            label=model_name,
        )

    plt.xlabel("Closure sector k")
    plt.ylabel("Selection probability")
    plt.title(f"Dynamic Selection Across Structural Models (beta = {beta:g})")
    plt.legend(fontsize=8, frameon=False)
    plt.tight_layout()
    plt.savefig(
        output_dir / f"selection_comparison_beta_{beta:g}.png",
        dpi=180,
    )
    plt.close()


def make_candidate_trajectory_plot(
    config: Config,
    trajectory: dict,
    output_dir: Path,
) -> None:
    k_values = np.asarray(config.k_values, dtype=int)

    plt.figure(figsize=(10, 6))
    for index, k in enumerate(k_values):
        plt.plot(
            trajectory["times"],
            trajectory["p_history"][:, index],
            linewidth=1.0,
            label=f"k={k}",
        )
    plt.xlabel("Time")
    plt.ylabel("Normalized occupancy p_k")
    plt.title("Candidate Pair-Closure Model: Example Trajectory")
    plt.legend(ncol=3, fontsize=8, frameon=False)
    plt.tight_layout()
    plt.savefig(
        output_dir / "candidate_example_trajectory.png",
        dpi=180,
    )
    plt.close()

    plt.figure(figsize=(9, 5))
    plt.plot(
        trajectory["times"],
        trajectory["entropy_history"],
    )
    plt.xlabel("Time")
    plt.ylabel("Closure-space entropy H_K")
    plt.title("Candidate Pair-Closure Model: Closure-Space Entropy")
    plt.tight_layout()
    plt.savefig(
        output_dir / "candidate_closure_entropy.png",
        dpi=180,
    )
    plt.close()


def main() -> None:
    config = Config()
    output_dir = Path(config.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    k_values = np.asarray(config.k_values, dtype=int)
    score_table = build_structural_scores(k_values)
    score_table.to_csv(
        output_dir / "structural_scores.csv",
        index=False,
    )

    candidate_score = score_table[
        "candidate_pair_residual"
    ].to_numpy(dtype=float)

    detected_index = int(np.argmin(candidate_score))
    detected_k = int(k_values[detected_index])
    detected_residual = float(candidate_score[detected_index])

    model_columns = [
        "null",
        "candidate_pair_residual",
        "control_shift_minus_1",
        "control_shift_plus_1",
        "control_linear",
        "control_cubic",
    ]

    all_summaries = []
    representative_trajectory = None

    model_counter = 0

    for beta in config.beta_values:
        for model_name in model_columns:
            score = score_table[model_name].to_numpy(dtype=float)

            store_trajectory = (
                model_name == "candidate_pair_residual"
                and np.isclose(beta, 2.0)
            )

            summary, trajectory = batch_simulation(
                config=config,
                score=score,
                beta=beta,
                seed=config.random_seed + model_counter * 100_003,
                store_first_trajectory=store_trajectory,
            )

            model_counter += 1

            summary.insert(0, "model", model_name)
            summary.insert(1, "beta", beta)
            all_summaries.append(summary)

            if store_trajectory:
                representative_trajectory = trajectory

    comparison = pd.concat(
        all_summaries,
        ignore_index=True,
    )
    comparison.to_csv(
        output_dir / "dynamic_model_comparison.csv",
        index=False,
    )

    winner_rows = []
    for (model_name, beta), group in comparison.groupby(
        ["model", "beta"],
        sort=False,
    ):
        best_row = group.loc[
            group["selection_probability"].idxmax()
        ]
        winner_rows.append(
            {
                "model": model_name,
                "beta": beta,
                "dynamic_winner_k": int(best_row["k"]),
                "winner_selection_probability": float(
                    best_row["selection_probability"]
                ),
            }
        )

    winners = pd.DataFrame(winner_rows)
    winners.to_csv(
        output_dir / "dynamic_winners.csv",
        index=False,
    )

    gain_rows = []
    for beta in config.beta_values:
        null_group = comparison[
            (comparison["model"] == "null")
            & np.isclose(comparison["beta"], beta)
        ]
        candidate_group = comparison[
            (comparison["model"] == "candidate_pair_residual")
            & np.isclose(comparison["beta"], beta)
        ]

        null_probability = float(
            null_group.loc[
                null_group["k"] == detected_k,
                "selection_probability",
            ].iloc[0]
        )
        candidate_probability = float(
            candidate_group.loc[
                candidate_group["k"] == detected_k,
                "selection_probability",
            ].iloc[0]
        )

        gain_rows.append(
            {
                "beta": beta,
                "detected_structural_sector": detected_k,
                "null_selection_probability": null_probability,
                "candidate_selection_probability": candidate_probability,
                "selection_gain": (
                    candidate_probability / null_probability
                    if null_probability > 0.0
                    else np.inf
                ),
            }
        )

    gains = pd.DataFrame(gain_rows)
    gains.to_csv(
        output_dir / "candidate_selection_gain.csv",
        index=False,
    )

    make_score_plot(
        score_table=score_table,
        output_dir=output_dir,
    )

    for beta in config.beta_values:
        make_selection_plot(
            comparison=comparison,
            beta=beta,
            output_dir=output_dir,
        )

    if representative_trajectory is not None:
        make_candidate_trajectory_plot(
            config=config,
            trajectory=representative_trajectory,
            output_dir=output_dir,
        )

        trajectory_frame = pd.DataFrame(
            representative_trajectory["p_history"],
            columns=[f"k_{k}" for k in k_values],
        )
        trajectory_frame.insert(
            0,
            "time",
            representative_trajectory["times"],
        )
        trajectory_frame.to_csv(
            output_dir / "candidate_example_trajectory.csv",
            index=False,
        )

        entropy_frame = pd.DataFrame(
            {
                "time": representative_trajectory["times"],
                "closure_entropy": representative_trajectory[
                    "entropy_history"
                ],
            }
        )
        entropy_frame.to_csv(
            output_dir / "candidate_example_entropy.csv",
            index=False,
        )

    print()
    print("Dynamic Closure Notebook — Entry 02")
    print("Candidate Fibonacci Pair-Closure Functional")
    print("-" * 58)
    print()
    print("Candidate structural score:")
    print("    B_k = |F_k - k^2| / (F_k + k^2)")
    print()
    print(
        "Computationally detected minimum-residual sector: "
        f"k = {detected_k}"
    )
    print(
        "Minimum structural residual: "
        f"{detected_residual:.12g}"
    )
    print()
    print("Structural score table:")
    print(
        score_table[
            [
                "k",
                "F_k",
                "pair_count_k2",
                "candidate_pair_residual",
            ]
        ].to_string(index=False)
    )
    print()
    print("Candidate selection gain relative to null:")
    print(gains.to_string(index=False))
    print()
    print("Dynamic winners:")
    print(winners.to_string(index=False))
    print()
    print(f"Outputs written to: {output_dir.resolve()}")
    print()
    print(
        "Interpretation rule: this notebook tests a candidate structural "
        "criterion. It does not establish that the criterion is uniquely "
        "derived from EDF."
    )


if __name__ == "__main__":
    main()
