"""
Dynamic Closure Notebook — Entry 03
Local Pathway Dynamics and Robustness Scan

Purpose
-------
Entry 02 showed that an all-to-all transition network makes the structural
minimum dominate too easily. Entry 03 tests a less trivial dynamical topology:

    k <-> k +/- 2

for the even-sector set k = 4, 6, 8, ..., 24.

The structural candidate remains

    B_k = |F_k - k^2| / (F_k + k^2),

but no sector number is hard-coded as the target. The minimum-residual sector is
detected computationally.
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
    t_max: float = 12.0
    dt: float = 0.04
    base_transition_rate: float = 0.25
    base_loss_rate: float = 0.035
    environment_correlation_time: float = 1.5
    ensemble_size: int = 1500
    random_seed: int = 1618033
    beta_values: tuple[float, ...] = (0.0, 0.25, 0.5, 1.0, 2.0)
    noise_values: tuple[float, ...] = (0.0, 0.03, 0.06, 0.10, 0.15)
    representative_beta: float = 0.5
    representative_noise: float = 0.10
    output_dir: str = "dynamic_closure_entry_03_output"

def fibonacci(n: int) -> int:
    if n < 0: raise ValueError("Fibonacci index must be non-negative.")
    a,b=0,1
    for _ in range(n): a,b=b,a+b
    return a

def normalized_residual(a,b):
    denominator=np.abs(a)+np.abs(b); result=np.zeros_like(denominator,dtype=float); mask=denominator>0
    result[mask]=np.abs(a[mask]-b[mask])/denominator[mask]; return result

def candidate_score(k_values):
    fib=np.array([fibonacci(int(k)) for k in k_values],dtype=float); return normalized_residual(fib,k_values.astype(float)**2)

def local_transition_matrix(score,beta,base_rate):
    n=len(score); rates=np.zeros((n,n),dtype=float)
    for i in range(n-1):
        j=i+1
        rates[i,j]=base_rate*np.exp(-0.5*beta*(score[j]-score[i])); rates[j,i]=base_rate*np.exp(-0.5*beta*(score[i]-score[j]))
    return rates

def entropy_rows(p):
    safe=np.where(p>0,p,1.0); return -np.sum(np.where(p>0,p*np.log(safe),0.0),axis=1)

def simulate_grid_point(config,score,beta,noise_strength,seed,store_first_trajectory=False):
    rng=np.random.default_rng(seed); k_values=np.asarray(config.k_values,dtype=int); n_states=len(k_values); n_runs=config.ensemble_size
    W=local_transition_matrix(score,beta,config.base_transition_rate); outgoing_rates=W.sum(axis=1)
    n_steps=int(round(config.t_max/config.dt))+1; times=np.linspace(0,config.t_max,n_steps)
    q=rng.dirichlet(alpha=np.ones(n_states),size=n_runs); environment=np.zeros_like(q); residence=np.zeros_like(q)
    dt=config.dt; tau=config.environment_correlation_time; diffusion_scale=noise_strength*np.sqrt(2.0/tau)*np.sqrt(dt)
    if store_first_trajectory: first_p_history=np.empty((n_steps,n_states)); first_entropy_history=np.empty(n_steps)
    initial_entropy=None
    for step in range(n_steps):
        p=q/q.sum(axis=1,keepdims=True)
        if step==0: initial_entropy=entropy_rows(p)
        if store_first_trajectory: first_p_history[step]=p[0]; first_entropy_history[step]=entropy_rows(p[:1])[0]
        if step==n_steps-1: break
        residence+=p*dt
        environment+=-(environment/tau)*dt+diffusion_scale*rng.normal(size=environment.shape)
        gamma_eff=np.clip(config.base_loss_rate+environment,0,None)
        q+=dt*(q@W-q*outgoing_rates[None,:]-gamma_eff*q); np.maximum(q,0,out=q)
    final_p=q/q.sum(axis=1,keepdims=True); final_entropy=entropy_rows(final_p); winner_indices=np.argmax(final_p,axis=1); winner_counts=np.bincount(winner_indices,minlength=n_states)
    summary=pd.DataFrame({"k":k_values,"mean_terminal_occupancy":final_p.mean(axis=0),"argmax_frequency":winner_counts/n_runs,"mean_residence":residence.mean(axis=0)})
    diagnostics={"mean_initial_entropy":float(np.mean(initial_entropy)),"mean_final_entropy":float(np.mean(final_entropy)),"mean_entropy_change":float(np.mean(final_entropy)-np.mean(initial_entropy))}
    trajectory={}
    if store_first_trajectory: trajectory={"times":times,"p_history":first_p_history,"entropy_history":first_entropy_history}
    return summary,{"diagnostics":diagnostics,"trajectory":trajectory}

def save_structural_table(k_values,score,output_dir):
    fib=np.array([fibonacci(int(k)) for k in k_values],dtype=np.int64); pair=k_values.astype(np.int64)**2
    table=pd.DataFrame({"k":k_values,"F_k":fib,"pair_count_k2":pair,"candidate_score_Bk":score}); table.to_csv(output_dir/"structural_score.csv",index=False); return table

def plot_target_probability_heatmap(phase_summary,config,output_dir):
    pivot=phase_summary.pivot(index="noise_strength",columns="beta",values="target_terminal_probability").reindex(index=config.noise_values,columns=config.beta_values)
    plt.figure(figsize=(8,5)); im=plt.imshow(pivot.to_numpy(),origin="lower",aspect="auto"); plt.colorbar(im,label="Target terminal probability")
    plt.xticks(np.arange(len(config.beta_values)),[str(v) for v in config.beta_values]); plt.yticks(np.arange(len(config.noise_values)),[str(v) for v in config.noise_values]); plt.xlabel("Structural coupling beta"); plt.ylabel("Environmental noise strength"); plt.title("Local Dynamics: Target Closure Probability"); plt.tight_layout(); plt.savefig(output_dir/"target_probability_heatmap.png",dpi=180); plt.close()

def plot_target_argmax_heatmap(phase_summary,config,output_dir):
    pivot=phase_summary.pivot(index="noise_strength",columns="beta",values="target_argmax_frequency").reindex(index=config.noise_values,columns=config.beta_values)
    plt.figure(figsize=(8,5)); im=plt.imshow(pivot.to_numpy(),origin="lower",aspect="auto"); plt.colorbar(im,label="Target argmax frequency")
    plt.xticks(np.arange(len(config.beta_values)),[str(v) for v in config.beta_values]); plt.yticks(np.arange(len(config.noise_values)),[str(v) for v in config.noise_values]); plt.xlabel("Structural coupling beta"); plt.ylabel("Environmental noise strength"); plt.title("Local Dynamics: Winner-Take-All Target Frequency"); plt.tight_layout(); plt.savefig(output_dir/"target_argmax_heatmap.png",dpi=180); plt.close()

def plot_target_probability_vs_noise(phase_summary,config,uniform_probability,output_dir):
    plt.figure(figsize=(9,5))
    for beta in config.beta_values:
        s=phase_summary[np.isclose(phase_summary["beta"],beta)].sort_values("noise_strength"); plt.plot(s["noise_strength"],s["target_terminal_probability"],marker="o",label=f"beta={beta:g}")
    plt.axhline(uniform_probability,linestyle="--",label="Uniform baseline"); plt.xlabel("Environmental noise strength"); plt.ylabel("Target terminal probability"); plt.title("Target Closure Robustness Under Environmental Noise"); plt.legend(frameon=False); plt.tight_layout(); plt.savefig(output_dir/"target_probability_vs_noise.png",dpi=180); plt.close()

def plot_representative_trajectory(trajectory,k_values,beta,noise_strength,output_dir):
    plt.figure(figsize=(10,6))
    for i,k in enumerate(k_values): plt.plot(trajectory["times"],trajectory["p_history"][:,i],linewidth=1,label=f"k={k}")
    plt.xlabel("Time"); plt.ylabel("Normalized occupancy p_k"); plt.title(f"Representative Local-Pathway Trajectory (beta={beta:g}, noise={noise_strength:g})"); plt.legend(ncol=3,fontsize=8,frameon=False); plt.tight_layout(); plt.savefig(output_dir/"representative_trajectory.png",dpi=180); plt.close()
    plt.figure(figsize=(9,5)); plt.plot(trajectory["times"],trajectory["entropy_history"]); plt.xlabel("Time"); plt.ylabel("Closure-space entropy H_K"); plt.title(f"Representative Closure-Space Entropy (beta={beta:g}, noise={noise_strength:g})"); plt.tight_layout(); plt.savefig(output_dir/"representative_entropy.png",dpi=180); plt.close()

def main():
    config=Config(); output_dir=Path(config.output_dir); output_dir.mkdir(parents=True,exist_ok=True); k_values=np.asarray(config.k_values,dtype=int); score=candidate_score(k_values)
    structural_table=save_structural_table(k_values,score,output_dir); target_index=int(np.argmin(score)); target_k=int(k_values[target_index]); target_score=float(score[target_index]); uniform_probability=1.0/len(k_values)
    grid_frames=[]; phase_rows=[]; representative_trajectory=None; combo_index=0
    for beta in config.beta_values:
        for noise_strength in config.noise_values:
            store=np.isclose(beta,config.representative_beta) and np.isclose(noise_strength,config.representative_noise)
            summary,extra=simulate_grid_point(config,score,beta,noise_strength,config.random_seed+combo_index*100003,store); combo_index+=1
            summary.insert(0,"beta",beta); summary.insert(1,"noise_strength",noise_strength); grid_frames.append(summary); target_row=summary[summary["k"]==target_k].iloc[0]; d=extra["diagnostics"]
            phase_rows.append({"beta":beta,"noise_strength":noise_strength,"detected_target_k":target_k,"target_terminal_probability":float(target_row["mean_terminal_occupancy"]),"target_argmax_frequency":float(target_row["argmax_frequency"]),"target_gain_over_uniform":float(target_row["mean_terminal_occupancy"])/uniform_probability,"mean_initial_entropy":d["mean_initial_entropy"],"mean_final_entropy":d["mean_final_entropy"],"mean_entropy_change":d["mean_entropy_change"]})
            if store: representative_trajectory=extra["trajectory"]
    pd.concat(grid_frames,ignore_index=True).to_csv(output_dir/"local_dynamics_grid.csv",index=False); phase_summary=pd.DataFrame(phase_rows); phase_summary.to_csv(output_dir/"phase_summary.csv",index=False)
    plot_target_probability_heatmap(phase_summary,config,output_dir); plot_target_argmax_heatmap(phase_summary,config,output_dir); plot_target_probability_vs_noise(phase_summary,config,uniform_probability,output_dir)
    if representative_trajectory is not None:
        plot_representative_trajectory(representative_trajectory,k_values,config.representative_beta,config.representative_noise,output_dir)
        f=pd.DataFrame(representative_trajectory["p_history"],columns=[f"k_{k}" for k in k_values]); f.insert(0,"time",representative_trajectory["times"]); f.to_csv(output_dir/"representative_trajectory.csv",index=False)
        pd.DataFrame({"time":representative_trajectory["times"],"closure_entropy":representative_trajectory["entropy_history"]}).to_csv(output_dir/"representative_entropy.csv",index=False)
    print("\nDynamic Closure Notebook — Entry 03\nLocal Pathway Dynamics and Robustness Scan\n"+"-"*54)
    print(f"\nComputationally detected structural target: k = {target_k}\nTarget structural residual: {target_score:.12g}\nUniform terminal-probability baseline: {uniform_probability:.6f}")
    print("\nPhase summary:\n",phase_summary[["beta","noise_strength","target_terminal_probability","target_argmax_frequency","target_gain_over_uniform","mean_entropy_change"]].to_string(index=False))
    print(f"\nOutputs written to: {output_dir.resolve()}")
    print("\nInterpretation: beta = 0 is the unbiased dynamical control. Increasing beta tests how strongly the independently specified structural score biases local closure pathways under environmental fluctuations.")

if __name__=="__main__": main()
