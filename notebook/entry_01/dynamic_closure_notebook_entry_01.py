"""
Dynamic Closure Notebook — Entry 01
Null-model baseline for closure-sector dynamics.

Purpose
-------
This script establishes the unbiased control experiment before any EDF-specific
closure functional B_k is introduced.

Important methodological rule
-----------------------------
k = 12 is NOT hard-coded as a preferred state here.

The current EDF manuscript states that a Golden/Fibonacci-inspired construction
selects k = 12, but the explicit algebraic residue functional / uniqueness proof
has not yet been supplied. Therefore this baseline uses B_k = 0 for every k.

When the exact EDF structural functional is derived, replace `closure_score_edf`
with that equation and set `score_mode="edf"`.

State equations
---------------
Unnormalized sector populations q_k:

    dq_k/dt =
        sum_{j != k} W_{j->k} q_j
        - sum_{j != k} W_{k->j} q_k
        - Gamma_eff(k,t) q_k

Normalized occupancies:

    p_k = q_k / sum_j q_j

Closure-space entropy:

    H_K = -sum_k p_k ln(p_k)

Residence:

    R_k = integral p_k(t) dt
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


@dataclass
class Config:
    k_min: int = 2
    k_max: int = 24
    t_max: float = 30.0
    dt: float = 0.02
    base_transition_rate: float = 0.18
    beta: float = 1.0
    base_loss_rate: float = 0.035
    environment_correlation_time: float = 1.5
    environment_noise_strength: float = 0.035
    ensemble_size: int = 500
    random_seed: int = 314159
    score_mode: str = "null"
    output_dir: str = "dynamic_closure_entry_01_output"


def closure_score_null(k_values: np.ndarray) -> np.ndarray:
    return np.zeros_like(k_values, dtype=float)


def closure_score_edf(k_values: np.ndarray) -> np.ndarray:
    raise NotImplementedError(
        "The exact EDF Golden/Fibonacci closure functional has not yet been "
        "derived explicitly. Keep score_mode='null' until B_k is defined."
    )


def get_closure_score(k_values: np.ndarray, mode: str) -> np.ndarray:
    if mode == "null":
        return closure_score_null(k_values)
    if mode == "edf":
        return closure_score_edf(k_values)
    raise ValueError(f"Unknown score mode: {mode!r}")


def transition_matrix_from_score(score: np.ndarray, base_rate: float, beta: float) -> np.ndarray:
    delta = score[None, :] - score[:, None]
    rates = base_rate * np.exp(-0.5 * beta * delta)
    np.fill_diagonal(rates, 0.0)
    return rates


def entropy(p: np.ndarray) -> float:
    positive = p > 0.0
    return float(-np.sum(p[positive] * np.log(p[positive])))


def ou_update(environment, dt, correlation_time, noise_strength, rng):
    drift = -(environment / correlation_time) * dt
    diffusion = (
        noise_strength
        * np.sqrt(2.0 / correlation_time)
        * np.sqrt(dt)
        * rng.normal(size=environment.size)
    )
    return environment + drift + diffusion


def simulate_one(config: Config, rng: np.random.Generator, store_trajectory: bool = False) -> dict:
    k_values = np.arange(config.k_min, config.k_max + 1)
    n_states = len(k_values)
    score = get_closure_score(k_values, config.score_mode)
    W = transition_matrix_from_score(score, config.base_transition_rate, config.beta)
    n_steps = int(round(config.t_max / config.dt)) + 1
    times = np.linspace(0.0, config.t_max, n_steps)
    q = np.ones(n_states, dtype=float)
    q /= q.sum()
    environment = np.zeros(n_states, dtype=float)
    residence = np.zeros(n_states, dtype=float)
    if store_trajectory:
        p_history = np.empty((n_steps, n_states), dtype=float)
        entropy_history = np.empty(n_steps, dtype=float)
    for step, _ in enumerate(times):
        total = q.sum()
        if total <= 0.0:
            raise RuntimeError("All unnormalized populations vanished.")
        p = q / total
        if store_trajectory:
            p_history[step] = p
            entropy_history[step] = entropy(p)
        if step == n_steps - 1:
            break
        residence += p * config.dt
        environment = ou_update(
            environment,
            config.dt,
            config.environment_correlation_time,
            config.environment_noise_strength,
            rng,
        )
        gamma_eff = np.clip(config.base_loss_rate + environment, a_min=0.0, a_max=None)
        incoming = q @ W
        outgoing = q * W.sum(axis=1)
        dq = incoming - outgoing - gamma_eff * q
        q = np.maximum(q + config.dt * dq, 0.0)
    final_p = q / q.sum()
    selected_index = int(np.argmax(final_p))
    result = {
        "k_values": k_values,
        "score": score,
        "selected_k": int(k_values[selected_index]),
        "final_p": final_p,
        "residence": residence,
    }
    if store_trajectory:
        result["times"] = times
        result["p_history"] = p_history
        result["entropy_history"] = entropy_history
    return result


def run_ensemble(config: Config):
    master_rng = np.random.default_rng(config.random_seed)
    k_values = np.arange(config.k_min, config.k_max + 1)
    counts = np.zeros(len(k_values), dtype=int)
    residence_sum = np.zeros(len(k_values), dtype=float)
    final_p_sum = np.zeros(len(k_values), dtype=float)
    example_seed = int(master_rng.integers(0, 2**32 - 1))
    example = simulate_one(config, np.random.default_rng(example_seed), store_trajectory=True)
    run_rows = []
    for run_index in range(config.ensemble_size):
        seed = int(master_rng.integers(0, 2**32 - 1))
        result = simulate_one(config, np.random.default_rng(seed), store_trajectory=False)
        selected_index = result["selected_k"] - config.k_min
        counts[selected_index] += 1
        residence_sum += result["residence"]
        final_p_sum += result["final_p"]
        run_rows.append({"run": run_index, "seed": seed, "selected_k": result["selected_k"]})
    summary = pd.DataFrame({
        "k": k_values,
        "selection_count": counts,
        "selection_probability": counts / config.ensemble_size,
        "mean_residence": residence_sum / config.ensemble_size,
        "mean_final_occupancy": final_p_sum / config.ensemble_size,
    })
    return summary, pd.DataFrame(run_rows), example


def save_example_trajectory(example: dict, output_dir: Path) -> None:
    trajectory = pd.DataFrame(
        example["p_history"], columns=[f"k_{k}" for k in example["k_values"]]
    )
    trajectory.insert(0, "time", example["times"])
    trajectory.to_csv(output_dir / "example_trajectory.csv", index=False)
    pd.DataFrame({
        "time": example["times"],
        "closure_entropy": example["entropy_history"],
    }).to_csv(output_dir / "example_entropy.csv", index=False)


def make_plots(config, summary, example, output_dir):
    plt.figure(figsize=(9, 5))
    plt.bar(summary["k"], summary["selection_probability"])
    plt.xlabel("Closure sector k")
    plt.ylabel("Selection probability")
    plt.title("Null Model: Selection Probability by Closure Sector")
    plt.tight_layout()
    plt.savefig(output_dir / "selection_probability.png", dpi=180)
    plt.close()

    plt.figure(figsize=(9, 5))
    plt.plot(summary["k"], summary["mean_residence"], marker="o")
    plt.xlabel("Closure sector k")
    plt.ylabel("Mean residence")
    plt.title("Null Model: Mean Integrated Residence by Closure Sector")
    plt.tight_layout()
    plt.savefig(output_dir / "mean_residence.png", dpi=180)
    plt.close()

    plt.figure(figsize=(10, 6))
    for index, k in enumerate(example["k_values"]):
        plt.plot(example["times"], example["p_history"][:, index], linewidth=0.9, label=f"k={k}")
    plt.xlabel("Time")
    plt.ylabel("Normalized occupancy p_k")
    plt.title("Null Model: Example Closure-Sector Trajectory")
    plt.legend(ncol=3, fontsize=7, frameon=False)
    plt.tight_layout()
    plt.savefig(output_dir / "example_trajectory.png", dpi=180)
    plt.close()

    plt.figure(figsize=(9, 5))
    plt.plot(example["times"], example["entropy_history"])
    plt.xlabel("Time")
    plt.ylabel("Closure-space entropy H_K")
    plt.title("Null Model: Closure-Space Entropy")
    plt.tight_layout()
    plt.savefig(output_dir / "closure_entropy.png", dpi=180)
    plt.close()


def main() -> None:
    config = Config()
    output_dir = Path(config.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    summary, runs, example = run_ensemble(config)
    summary.to_csv(output_dir / "ensemble_summary.csv", index=False)
    runs.to_csv(output_dir / "ensemble_runs.csv", index=False)
    save_example_trajectory(example, output_dir)
    make_plots(config, summary, example, output_dir)
    expected_uniform = 1.0 / len(summary)
    print("\nDynamic Closure Notebook — Entry 01")
    print("Null-model baseline")
    print("-" * 42)
    print(f"Closure sectors: {config.k_min} ... {config.k_max}")
    print(f"Number of sectors: {len(summary)}")
    print(f"Ensemble size: {config.ensemble_size}")
    print(f"Expected uniform selection probability: {expected_uniform:.6f}\n")
    print(summary.to_string(index=False))
    print(f"\nOutputs written to: {output_dir.resolve()}\n")
    print(
        "Interpretation: any apparent preference in this null model "
        "must arise from finite-sample stochastic fluctuations, because "
        "B_k = 0 for every sector."
    )


if __name__ == "__main__":
    main()
