
"""
Dynamic Closure Notebook — Entry 11
Robustness and Falsification Suite

This entry stress-tests the post-DCT transient-memory model. It varies:
lambda, commitment scale h0, topology, initial condition, defect
representation, commitment law, and intervention strength.

It separates two claims:

STRUCTURAL MEMORY
- transient occupancy vanishes when Q is Hurwitz;
- reachable transient states can have nonzero integrated residence;
- eliminating a coupled transient state generates nonzero Schur-complement
  boundary terms.

TARGET-SPECIFIC CAUSALITY
- soft blockade of a transient sector can change P(commit to k=12);
- this effect is allowed to weaken or change sign under model changes.

DCT itself is not modified or retested here.
"""

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
    target_k: int = 12
    lambdas: tuple = (0.0, 0.5, 1.0, 2.0, 4.0)
    h0_values: tuple = (0.02, 0.10, 0.50)
    topologies: tuple = ("path", "ring", "complete")
    initial_conditions: tuple = ("boundary_pair", "left_boundary")
    defect_names: tuple = ("log", "bounded", "symmetric")
    commitment_laws: tuple = (
        "exponential",
        "reciprocal",
        "quadratic_exponential",
    )
    block_factor: float = 0.05
    blockade_factors: tuple = (0.0, 0.01, 0.05, 0.20, 0.50, 0.80)
    attempt_frequency: float = 1.0
    tolerance: float = 1.0e-10
    output_dir: str = "dynamic_closure_entry_11_output"


def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def log_defect(k_values):
    return np.array(
        [abs(np.log(fibonacci(int(k)) / (int(k) ** 2))) for k in k_values],
        dtype=float,
    )


def defect_transform(d, name):
    if name == "log":
        x = d.copy()
    elif name == "bounded":
        x = np.tanh(d / 2.0)
    elif name == "symmetric":
        x = 2.0 * np.sinh(d / 2.0)
    else:
        raise ValueError(name)

    nonzero = x[x > 0]
    scale = float(nonzero.mean()) if len(nonzero) else 1.0
    return x / scale


def adjacency(n, topology):
    a = np.zeros((n, n), dtype=float)

    if topology == "path":
        for i in range(n - 1):
            a[i, i + 1] = a[i + 1, i] = 1.0

    elif topology == "ring":
        for i in range(n):
            j = (i + 1) % n
            a[i, j] = a[j, i] = 1.0

    elif topology == "complete":
        a[:] = 1.0
        np.fill_diagonal(a, 0.0)

    else:
        raise ValueError(topology)

    # Preserve symmetry while making mean total jump degree comparable.
    mean_degree = a.sum(axis=1).mean()
    return a * (2.0 / mean_degree)


def rates_from_defect(d, lam, nu, a):
    delta = d[None, :] - d[:, None]
    w = nu * a * np.exp(-0.5 * lam * delta)
    np.fill_diagonal(w, 0.0)
    return w


def hazards_from_defect(d, lam, h0, law):
    if law == "exponential":
        return h0 * np.exp(-lam * d)
    if law == "reciprocal":
        return h0 / (1.0 + lam * d)
    if law == "quadratic_exponential":
        return h0 * np.exp(-lam * d**2)
    raise ValueError(law)


def generator(w, h):
    q = w.copy()
    np.fill_diagonal(q, -w.sum(axis=1) - h)
    return q


def initial_distribution(n, name):
    mu = np.zeros(n)
    if name == "boundary_pair":
        mu[0] = 0.5
        mu[-1] = 0.5
    elif name == "left_boundary":
        mu[0] = 1.0
    else:
        raise ValueError(name)
    return mu


def target_absorption(q, h, mu, target):
    rhs = np.zeros(len(h))
    rhs[target] = h[target]
    b = np.linalg.solve(-q, rhs)
    return float(mu @ b)


def residence(q, mu):
    return np.linalg.solve((-q).T, mu)


def schur_footprints(q, h):
    n = len(h)
    out = np.zeros(n)

    for j in range(n):
        keep = [i for i in range(n) if i != j]
        q_aj = q[np.ix_(keep, [j])]
        q_ja = q[np.ix_([j], keep)]
        q_jj = float(q[j, j])

        delta_q = -(q_aj * (1.0 / q_jj)) @ q_ja
        delta_r_col = -(q_aj[:, 0] * (1.0 / q_jj) * h[j])

        out[j] = np.sqrt(
            np.linalg.norm(delta_q, ord="fro") ** 2
            + np.linalg.norm(delta_r_col) ** 2
        )

    return out


def block_state(w, j, factor):
    wb = w.copy()
    wb[j, :] *= factor
    wb[:, j] *= factor
    wb[j, j] = 0.0
    return wb


def causal_effects(w, h, mu, target, base_prob, factor):
    n = len(h)
    effects = []

    for j in range(n):
        if j == target or mu[j] > 0.0:
            continue

        wb = block_state(w, j, factor)
        qb = generator(wb, h)
        pb = target_absorption(qb, h, mu, target)

        effects.append(base_prob - pb)

    return np.asarray(effects, dtype=float)


def evaluate(
    k_values,
    base_d,
    lam,
    h0,
    topology,
    initial_name,
    defect_name,
    law,
    config,
    block_factor=None,
):
    d = defect_transform(base_d, defect_name)
    a = adjacency(len(k_values), topology)
    w = rates_from_defect(d, lam, config.attempt_frequency, a)
    h = hazards_from_defect(d, lam, h0, law)
    q = generator(w, h)
    mu = initial_distribution(len(k_values), initial_name)
    target = int(np.where(k_values == config.target_k)[0][0])

    p_target = target_absorption(q, h, mu, target)
    tau = residence(q, mu)
    footprints = schur_footprints(q, h)

    factor = config.block_factor if block_factor is None else block_factor
    effects = causal_effects(
        w, h, mu, target, p_target, factor
    )

    eig = np.linalg.eigvals(q)
    max_real = float(np.max(np.real(eig)))

    tol = config.tolerance

    return {
        "lambda": lam,
        "h0": h0,
        "topology": topology,
        "initial_condition": initial_name,
        "defect_representation": defect_name,
        "commitment_law": law,
        "block_factor": factor,
        "target_probability": p_target,
        "max_real_transient_eigenvalue": max_real,
        "transient_extinction_verified": max_real < -tol,
        "minimum_expected_residence": float(tau.min()),
        "all_states_positive_residence": bool(np.all(tau > 0.0)),
        "all_states_residence_above_tolerance": bool(np.all(tau > tol)),
        "minimum_schur_footprint": float(footprints.min()),
        "all_states_nonzero_schur_footprint": bool(
            np.all(footprints > tol)
        ),
        "causal_probe_count": len(effects),
        "positive_causal_count": int(np.sum(effects > tol)),
        "negative_causal_count": int(np.sum(effects < -tol)),
        "near_zero_causal_count": int(np.sum(np.abs(effects) <= tol)),
        "positive_causal_fraction": float(np.mean(effects > tol)),
        "median_causal_effect": float(np.median(effects)),
        "mean_absolute_causal_effect": float(np.mean(np.abs(effects))),
        "max_absolute_causal_effect": float(np.max(np.abs(effects))),
        "min_causal_effect": float(effects.min()),
        "max_causal_effect": float(effects.max()),
    }


def build_core_grid(k_values, base_d, config):
    rows = []

    # Broad sweep keeps the Entry 10 commitment law fixed.
    for lam in config.lambdas:
        for h0 in config.h0_values:
            for topology in config.topologies:
                for init in config.initial_conditions:
                    for defect_name in config.defect_names:
                        rows.append(
                            evaluate(
                                k_values,
                                base_d,
                                lam,
                                h0,
                                topology,
                                init,
                                defect_name,
                                "exponential",
                                config,
                            )
                        )

    return pd.DataFrame(rows)


def build_law_sensitivity(k_values, base_d, config):
    rows = []
    for lam in config.lambdas:
        for h0 in config.h0_values:
            for law in config.commitment_laws:
                rows.append(
                    evaluate(
                        k_values,
                        base_d,
                        lam,
                        h0,
                        "path",
                        "boundary_pair",
                        "log",
                        law,
                        config,
                    )
                )
    return pd.DataFrame(rows)


def build_blockade_sensitivity(k_values, base_d, config):
    rows = []
    for factor in config.blockade_factors:
        row = evaluate(
            k_values,
            base_d,
            2.0,
            0.10,
            "path",
            "boundary_pair",
            "log",
            "exponential",
            config,
            block_factor=factor,
        )
        rows.append(row)
    return pd.DataFrame(rows)


def category_summary(df, category):
    return (
        df.groupby(category, as_index=False)
        .agg(
            configurations=("target_probability", "size"),
            mean_target_probability=("target_probability", "mean"),
            mean_positive_causal_fraction=(
                "positive_causal_fraction", "mean"
            ),
            median_abs_causal_effect=(
                "mean_absolute_causal_effect", "median"
            ),
            min_schur_footprint=("minimum_schur_footprint", "min"),
            extinction_success=(
                "transient_extinction_verified", "mean"
            ),
            positive_residence_success=(
                "all_states_positive_residence", "mean"
            ),
            residence_above_tolerance_success=(
                "all_states_residence_above_tolerance", "mean"
            ),
            schur_success=(
                "all_states_nonzero_schur_footprint", "mean"
            ),
        )
    )


def baseline_grid(df):
    return df[
        (df["topology"] == "path")
        & (df["initial_condition"] == "boundary_pair")
        & (df["defect_representation"] == "log")
    ].copy()


def heatmap(table, value, title, path):
    lambdas = sorted(table["lambda"].unique())
    h0s = sorted(table["h0"].unique())

    m = np.empty((len(h0s), len(lambdas)))
    for i, h0 in enumerate(h0s):
        for j, lam in enumerate(lambdas):
            row = table[
                np.isclose(table["h0"], h0)
                & np.isclose(table["lambda"], lam)
            ]
            m[i, j] = row[value].iloc[0]

    plt.figure(figsize=(8, 5))
    im = plt.imshow(m, origin="lower", aspect="auto")
    plt.colorbar(im)
    plt.xticks(range(len(lambdas)), [f"{x:g}" for x in lambdas])
    plt.yticks(range(len(h0s)), [f"{x:g}" for x in h0s])
    plt.xlabel("Selection strength lambda")
    plt.ylabel("Commitment scale h0")
    plt.title(title)
    plt.tight_layout()
    plt.savefig(path, dpi=180)
    plt.close()


def plot_summary(summary, category, path):
    x = np.arange(len(summary))
    plt.figure(figsize=(9, 5))
    plt.bar(x, summary["mean_positive_causal_fraction"])
    plt.xticks(x, summary[category].astype(str), rotation=20)
    plt.ylim(0.0, 1.05)
    plt.ylabel("Mean positive causal fraction")
    plt.xlabel(category.replace("_", " ").title())
    plt.title("Target-Directed Causal Robustness")
    plt.tight_layout()
    plt.savefig(path, dpi=180)
    plt.close()


def plot_law_sensitivity(df, path):
    plt.figure(figsize=(9, 5))
    for law in df["commitment_law"].unique():
        s = (
            df[df["commitment_law"] == law]
            .groupby("lambda", as_index=False)
            ["positive_causal_fraction"]
            .mean()
        )
        plt.plot(
            s["lambda"],
            s["positive_causal_fraction"],
            marker="o",
            label=law,
        )
    plt.ylim(0.0, 1.05)
    plt.xlabel("Selection strength lambda")
    plt.ylabel("Mean positive causal fraction")
    plt.title("Commitment-Law Sensitivity")
    plt.legend(frameon=False)
    plt.tight_layout()
    plt.savefig(path, dpi=180)
    plt.close()


def plot_blockade(df, path):
    plt.figure(figsize=(9, 5))
    suppression = 1.0 - df["block_factor"]
    plt.plot(
        suppression,
        df["mean_absolute_causal_effect"],
        marker="o",
        label="Mean absolute effect",
    )
    plt.plot(
        suppression,
        df["max_absolute_causal_effect"],
        marker="o",
        label="Maximum absolute effect",
    )
    plt.xlabel("Suppression fraction of incident rates")
    plt.ylabel("Change in P(commit to k=12)")
    plt.title("Intervention-Strength Sensitivity")
    plt.legend(frameon=False)
    plt.tight_layout()
    plt.savefig(path, dpi=180)
    plt.close()


def main():
    config = Config()
    out = Path(config.output_dir)
    out.mkdir(parents=True, exist_ok=True)

    k_values = np.arange(config.k_min, config.k_max + 1)
    base_d = log_defect(k_values)

    core = build_core_grid(k_values, base_d, config)
    core.to_csv(out / "core_robustness_grid.csv", index=False)

    law = build_law_sensitivity(k_values, base_d, config)
    law.to_csv(out / "commitment_law_sensitivity.csv", index=False)

    blockade = build_blockade_sensitivity(k_values, base_d, config)
    blockade.to_csv(out / "blockade_strength_sensitivity.csv", index=False)

    weakening = core[
        (core["positive_causal_fraction"] < 0.75)
        | (core["mean_absolute_causal_effect"] < 1.0e-4)
        | (core["negative_causal_count"] > 0)
    ].sort_values(
        ["positive_causal_fraction", "mean_absolute_causal_effect"]
    )
    weakening.to_csv(
        out / "target_causality_weakening_regimes.csv",
        index=False,
    )

    topology_summary = category_summary(core, "topology")
    defect_summary = category_summary(core, "defect_representation")
    initial_summary = category_summary(core, "initial_condition")

    topology_summary.to_csv(
        out / "topology_robustness_summary.csv", index=False
    )
    defect_summary.to_csv(
        out / "defect_robustness_summary.csv", index=False
    )
    initial_summary.to_csv(
        out / "initial_condition_robustness_summary.csv", index=False
    )

    baseline = baseline_grid(core)
    baseline.to_csv(out / "baseline_lambda_h0_grid.csv", index=False)

    heatmap(
        baseline,
        "target_probability",
        "P(commit to k=12): Baseline Path Model",
        out / "baseline_target_probability_heatmap.png",
    )
    heatmap(
        baseline,
        "positive_causal_fraction",
        "Positive Causal Fraction: Baseline Path Model",
        out / "baseline_positive_causal_fraction_heatmap.png",
    )
    heatmap(
        baseline,
        "mean_absolute_causal_effect",
        "Mean Intervention Effect: Baseline Path Model",
        out / "baseline_mean_causal_effect_heatmap.png",
    )

    plot_summary(
        topology_summary,
        "topology",
        out / "topology_causal_robustness.png",
    )
    plot_summary(
        defect_summary,
        "defect_representation",
        out / "defect_causal_robustness.png",
    )
    plot_law_sensitivity(
        law,
        out / "commitment_law_causal_robustness.png",
    )
    plot_blockade(
        blockade,
        out / "blockade_strength_sensitivity.png",
    )

    weakest = core.loc[core["mean_absolute_causal_effect"].idxmin()]
    strongest = core.loc[core["mean_absolute_causal_effect"].idxmax()]

    print()
    print("Dynamic Closure Notebook — Entry 11")
    print("Robustness and Falsification Suite")
    print("-" * 54)
    print()
    print(f"Core configurations tested: {len(core)}")
    print(f"Commitment-law sensitivity configurations: {len(law)}")
    print()
    print(
        "Transient extinction success fraction: "
        f"{core['transient_extinction_verified'].mean():.3f}"
    )
    print(
        "All-state strictly positive residence success fraction: "
        f"{core['all_states_positive_residence'].mean():.3f}"
    )

    print(
        "All-state residence above numerical tolerance fraction: "
        f"{core['all_states_residence_above_tolerance'].mean():.3f}"
    )
    print(
        "All-state nonzero Schur-footprint success fraction: "
        f"{core['all_states_nonzero_schur_footprint'].mean():.3f}"
    )
    print()
    print(
        "Median positive causal fraction: "
        f"{core['positive_causal_fraction'].median():.3f}"
    )
    print(
        "Minimum positive causal fraction: "
        f"{core['positive_causal_fraction'].min():.3f}"
    )
    print(
        "Fraction of configurations with every probed sector positive: "
        f"{np.mean(np.isclose(core['positive_causal_fraction'], 1.0)):.3f}"
    )
    print()
    print(
        f"Target-causality weakening regimes flagged: {len(weakening)}"
    )
    print()
    print("Topology summary:")
    print(topology_summary.to_string(index=False))
    print()
    print("Defect summary:")
    print(defect_summary.to_string(index=False))
    print()
    print("Initial-condition summary:")
    print(initial_summary.to_string(index=False))
    print()

    law_summary = (
        law.groupby("commitment_law", as_index=False)
        .agg(
            mean_target_probability=("target_probability", "mean"),
            mean_positive_causal_fraction=("positive_causal_fraction", "mean"),
            median_abs_causal_effect=("mean_absolute_causal_effect", "median"),
            minimum_positive_causal_fraction=("positive_causal_fraction", "min"),
        )
    )

    print("Commitment-law sensitivity summary:")
    print(law_summary.to_string(index=False))
    print()

    print("Blockade-strength sensitivity:")
    print(
        blockade[
            [
                "block_factor",
                "positive_causal_fraction",
                "mean_absolute_causal_effect",
                "max_absolute_causal_effect",
            ]
        ].to_string(index=False)
    )
    print()
    print("Weakest mean intervention-effect configuration:")
    print(
        weakest[
            [
                "lambda",
                "h0",
                "topology",
                "initial_condition",
                "defect_representation",
                "target_probability",
                "positive_causal_fraction",
                "mean_absolute_causal_effect",
                "minimum_schur_footprint",
            ]
        ].to_string()
    )
    print()
    print("Strongest mean intervention-effect configuration:")
    print(
        strongest[
            [
                "lambda",
                "h0",
                "topology",
                "initial_condition",
                "defect_representation",
                "target_probability",
                "positive_causal_fraction",
                "mean_absolute_causal_effect",
                "minimum_schur_footprint",
            ]
        ].to_string()
    )
    print()
    print(f"Outputs written to: {out.resolve()}")


if __name__ == "__main__":
    main()
