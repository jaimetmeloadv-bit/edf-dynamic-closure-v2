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
1. Null: B_k = 0
2. Fibonacci index shift -1
3. Fibonacci index shift +1
4. Linear structural count
5. Cubic structural count
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
    if n < 0: raise ValueError("Fibonacci index must be non-negative.")
    a,b=0,1
    for _ in range(n): a,b=b,a+b
    return a

def normalized_residual(a,b):
    denominator=np.abs(a)+np.abs(b)
    result=np.zeros_like(denominator,dtype=float)
    mask=denominator>0
    result[mask]=np.abs(a[mask]-b[mask])/denominator[mask]
    return result

def build_structural_scores(k_values):
    fib_k=np.array([fibonacci(int(k)) for k in k_values],dtype=float)
    fib_m=np.array([fibonacci(int(k)-1) for k in k_values],dtype=float)
    fib_p=np.array([fibonacci(int(k)+1) for k in k_values],dtype=float)
    kf=k_values.astype(float)
    pair=kf**2
    return pd.DataFrame({
        "k":k_values,"F_k":fib_k.astype(np.int64),"pair_count_k2":pair.astype(np.int64),
        "candidate_pair_residual":normalized_residual(fib_k,pair),
        "control_shift_minus_1":normalized_residual(fib_m,pair),
        "control_shift_plus_1":normalized_residual(fib_p,pair),
        "control_linear":normalized_residual(fib_k,kf),
        "control_cubic":normalized_residual(fib_k,kf**3),
        "null":np.zeros(len(k_values),dtype=float)})

def transition_matrix_from_score(score,base_rate,beta):
    delta=score[None,:]-score[:,None]
    rates=base_rate*np.exp(-0.5*beta*delta)
    np.fill_diagonal(rates,0.0)
    return rates

def entropy_rows(p):
    safe=np.where(p>0,p,1.0)
    return -np.sum(np.where(p>0,p*np.log(safe),0.0),axis=1)

def batch_simulation(config,score,beta,seed,store_first_trajectory=False):
    rng=np.random.default_rng(seed)
    k_values=np.asarray(config.k_values,dtype=int); n_states=len(k_values); n_runs=config.ensemble_size
    W=transition_matrix_from_score(score,config.base_transition_rate,beta); outgoing_rates=W.sum(axis=1)
    n_steps=int(round(config.t_max/config.dt))+1; times=np.linspace(0,config.t_max,n_steps)
    q=np.full((n_runs,n_states),1.0/n_states); environment=np.zeros_like(q); residence=np.zeros_like(q)
    if store_first_trajectory:
        first_p_history=np.empty((n_steps,n_states)); first_entropy_history=np.empty(n_steps)
    dt=config.dt; tau=config.environment_correlation_time; sigma=config.environment_noise_strength
    diffusion_scale=sigma*np.sqrt(2.0/tau)*np.sqrt(dt)
    for step in range(n_steps):
        p=q/q.sum(axis=1,keepdims=True)
        if store_first_trajectory:
            first_p_history[step]=p[0]; first_entropy_history[step]=entropy_rows(p[:1])[0]
        if step==n_steps-1: break
        residence+=p*dt
        environment+=-(environment/tau)*dt+diffusion_scale*rng.normal(size=environment.shape)
        gamma_eff=np.clip(config.base_loss_rate+environment,0,None)
        q+=dt*(q@W-q*outgoing_rates[None,:]-gamma_eff*q)
        np.maximum(q,0,out=q)
    final_p=q/q.sum(axis=1,keepdims=True); selected_indices=np.argmax(final_p,axis=1)
    counts=np.bincount(selected_indices,minlength=n_states)
    summary=pd.DataFrame({"k":k_values,"selection_count":counts,"selection_probability":counts/n_runs,
                          "mean_residence":residence.mean(axis=0),"mean_final_occupancy":final_p.mean(axis=0)})
    trajectory=None
    if store_first_trajectory: trajectory={"times":times,"p_history":first_p_history,"entropy_history":first_entropy_history}
    return summary,trajectory

def make_score_plot(score_table,output_dir):
    plt.figure(figsize=(9,5))
    for col,label in [("candidate_pair_residual","Pair-count candidate"),("control_shift_minus_1","Index shift -1"),("control_shift_plus_1","Index shift +1")]:
        plt.plot(score_table["k"],score_table[col],marker="o",label=label)
    plt.xlabel("Closure sector k"); plt.ylabel("Normalized structural residual"); plt.title("Candidate Fibonacci Closure Score and Index-Shift Controls")
    plt.legend(frameon=False); plt.tight_layout(); plt.savefig(output_dir/"structural_residuals.png",dpi=180); plt.close()

def make_selection_plot(comparison,beta,output_dir):
    subset=comparison[np.isclose(comparison["beta"],beta)]
    model_order=["null","candidate_pair_residual","control_shift_minus_1","control_shift_plus_1","control_linear","control_cubic"]
    plt.figure(figsize=(10,6))
    for model_name in model_order:
        d=subset[subset["model"]==model_name]; plt.plot(d["k"],d["selection_probability"],marker="o",label=model_name)
    plt.xlabel("Closure sector k"); plt.ylabel("Selection probability"); plt.title(f"Dynamic Selection Across Structural Models (beta = {beta:g})")
    plt.legend(fontsize=8,frameon=False); plt.tight_layout(); plt.savefig(output_dir/f"selection_comparison_beta_{beta:g}.png",dpi=180); plt.close()

def make_candidate_trajectory_plot(config,trajectory,output_dir):
    kv=np.asarray(config.k_values,dtype=int); plt.figure(figsize=(10,6))
    for i,k in enumerate(kv): plt.plot(trajectory["times"],trajectory["p_history"][:,i],linewidth=1,label=f"k={k}")
    plt.xlabel("Time"); plt.ylabel("Normalized occupancy p_k"); plt.title("Candidate Pair-Closure Model: Example Trajectory")
    plt.legend(ncol=3,fontsize=8,frameon=False); plt.tight_layout(); plt.savefig(output_dir/"candidate_example_trajectory.png",dpi=180); plt.close()
    plt.figure(figsize=(9,5)); plt.plot(trajectory["times"],trajectory["entropy_history"]); plt.xlabel("Time"); plt.ylabel("Closure-space entropy H_K")
    plt.title("Candidate Pair-Closure Model: Closure-Space Entropy"); plt.tight_layout(); plt.savefig(output_dir/"candidate_closure_entropy.png",dpi=180); plt.close()

def main():
    config=Config(); output_dir=Path(config.output_dir); output_dir.mkdir(parents=True,exist_ok=True)
    k_values=np.asarray(config.k_values,dtype=int); score_table=build_structural_scores(k_values); score_table.to_csv(output_dir/"structural_scores.csv",index=False)
    candidate_score=score_table["candidate_pair_residual"].to_numpy(float); detected_index=int(np.argmin(candidate_score)); detected_k=int(k_values[detected_index]); detected_residual=float(candidate_score[detected_index])
    model_columns=["null","candidate_pair_residual","control_shift_minus_1","control_shift_plus_1","control_linear","control_cubic"]
    all_summaries=[]; representative_trajectory=None; model_counter=0
    for beta in config.beta_values:
        for model_name in model_columns:
            store=model_name=="candidate_pair_residual" and np.isclose(beta,2.0)
            summary,trajectory=batch_simulation(config,score_table[model_name].to_numpy(float),beta,config.random_seed+model_counter*100003,store)
            model_counter+=1; summary.insert(0,"model",model_name); summary.insert(1,"beta",beta); all_summaries.append(summary)
            if store: representative_trajectory=trajectory
    comparison=pd.concat(all_summaries,ignore_index=True); comparison.to_csv(output_dir/"dynamic_model_comparison.csv",index=False)
    winner_rows=[]
    for (model_name,beta),group in comparison.groupby(["model","beta"],sort=False):
        best=group.loc[group["selection_probability"].idxmax()]
        winner_rows.append({"model":model_name,"beta":beta,"dynamic_winner_k":int(best["k"]),"winner_selection_probability":float(best["selection_probability"])})
    pd.DataFrame(winner_rows).to_csv(output_dir/"dynamic_winners.csv",index=False)
    gain_rows=[]
    for beta in config.beta_values:
        ng=comparison[(comparison["model"]=="null")&np.isclose(comparison["beta"],beta)]
        cg=comparison[(comparison["model"]=="candidate_pair_residual")&np.isclose(comparison["beta"],beta)]
        pn=float(ng.loc[ng["k"]==detected_k,"selection_probability"].iloc[0]); pc=float(cg.loc[cg["k"]==detected_k,"selection_probability"].iloc[0])
        gain_rows.append({"beta":beta,"detected_structural_sector":detected_k,"null_selection_probability":pn,"candidate_selection_probability":pc,"selection_gain":pc/pn if pn>0 else np.inf})
    gains=pd.DataFrame(gain_rows); gains.to_csv(output_dir/"candidate_selection_gain.csv",index=False)
    make_score_plot(score_table,output_dir)
    for beta in config.beta_values: make_selection_plot(comparison,beta,output_dir)
    if representative_trajectory is not None:
        make_candidate_trajectory_plot(config,representative_trajectory,output_dir)
        frame=pd.DataFrame(representative_trajectory["p_history"],columns=[f"k_{k}" for k in k_values]); frame.insert(0,"time",representative_trajectory["times"]); frame.to_csv(output_dir/"candidate_example_trajectory.csv",index=False)
        pd.DataFrame({"time":representative_trajectory["times"],"closure_entropy":representative_trajectory["entropy_history"]}).to_csv(output_dir/"candidate_example_entropy.csv",index=False)
    print("\nDynamic Closure Notebook — Entry 02\nCandidate Fibonacci Pair-Closure Functional\n"+"-"*58)
    print(f"\nComputationally detected minimum-residual sector: k = {detected_k}\nMinimum structural residual: {detected_residual:.12g}")
    print("\nCandidate selection gain relative to null:\n",gains.to_string(index=False))
    print(f"\nOutputs written to: {output_dir.resolve()}")
    print("\nInterpretation rule: this notebook tests a candidate structural criterion. It does not establish that the criterion is uniquely derived from EDF.")

if __name__=="__main__": main()
