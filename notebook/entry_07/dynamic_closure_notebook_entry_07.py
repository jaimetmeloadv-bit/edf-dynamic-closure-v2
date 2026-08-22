"""
Dynamic Closure Notebook — Entry 07
Primitive EDF Phase Evolution and the Traversal Theorem

A homogeneous phase step preserving the finite k-sector kernel must satisfy
Delta_phi=2*pi*r/k. The induced traversal is U_r=X^r. Its orbit length is
k/gcd(k,r), so primitive recurrence after exactly k steps is equivalent to
gcd(k,r)=1. Every such traversal is relabeling-equivalent to X.
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
    k_min:int=2; k_max:int=36; diagnostic_k:int=12
    output_dir:str="dynamic_closure_entry_07_output"

def roots_of_unity(k,phi_0=0.0): return np.exp(1j*(phi_0+2*np.pi*np.arange(k)/k))
def canonical_shift(k):
    x=np.zeros((k,k),complex)
    for m in range(k): x[(m+1)%k,m]=1
    return x

def step_operator(k,r): return np.linalg.matrix_power(canonical_shift(k),r%k)
def direct_step_permutation(k,r):
    u=np.zeros((k,k),complex)
    for m in range(k): u[(m+r)%k,m]=1
    return u

def relabeling_permutation(k,r):
    if gcd(k,r)!=1: raise ValueError("r must be coprime to k for invertible relabeling.")
    p=np.zeros((k,k),complex)
    for m in range(k): p[(r*m)%k,m]=1
    return p

def cycle_decomposition(k,r):
    unvisited=set(range(k)); cycles=[]
    while unvisited:
        start=min(unvisited); cycle=[]; current=start
        while current not in cycle:
            cycle.append(current); unvisited.discard(current); current=(current+r)%k
        cycles.append(cycle)
    return cycles

def kernel_preservation_error(k,r):
    roots=roots_of_unity(k); rotated=np.exp(2j*np.pi*r/k)*roots; target=np.array([roots[(m+r)%k] for m in range(k)],complex); return float(np.max(np.abs(rotated-target)))
def operator_step_error(k,r): return float(np.linalg.norm(direct_step_permutation(k,r)-step_operator(k,r),ord="fro"))
def conjugacy_to_canonical_shift_error(k,r):
    if gcd(k,r)!=1:return np.nan
    x=canonical_shift(k); xr=step_operator(k,r); p=relabeling_permutation(k,r); return float(np.linalg.norm(p.conj().T@xr@p-x,ord="fro"))
def euler_totient(k): return sum(1 for r in range(1,k) if gcd(k,r)==1)

def build_step_table(config):
    rows=[]
    for k in range(config.k_min,config.k_max+1):
        for r in range(k):
            d=gcd(k,r); cycles=cycle_decomposition(k,r)
            rows.append({"k":k,"r":r,"delta_phi_over_2pi":r/k,"gcd_k_r":d,"orbit_length":k//d,"cycle_count":d,"transitive_full_cycle":d==1,"kernel_preservation_error":kernel_preservation_error(k,r),"operator_X_power_error":operator_step_error(k,r),"conjugacy_to_X_error":conjugacy_to_canonical_shift_error(k,r),"cycle_decomposition":" | ".join("-".join(str(v) for v in c) for c in cycles)})
    return pd.DataFrame(rows)

def build_totient_summary(config,step_table):
    rows=[]
    for k in range(config.k_min,config.k_max+1):
        subset=step_table[step_table["k"]==k]; measured=int(subset["transitive_full_cycle"].sum()); expected=euler_totient(k)
        rows.append({"k":k,"measured_transitive_steps":measured,"euler_totient_phi_k":expected,"agreement":measured==expected,"fraction_of_nonzero_steps_transitive":measured/(k-1)})
    return pd.DataFrame(rows)

def plot_orbit_length(diagnostic,config,output_dir):
    plt.figure(figsize=(9,5)); plt.plot(diagnostic["r"],diagnostic["orbit_length"],marker="o"); plt.axhline(config.diagnostic_k,linestyle="--",label="Full kernel size"); plt.xlabel("Phase-step index r"); plt.ylabel("Orbit length"); plt.title(f"Primitive Phase-Step Orbit Length for k={config.diagnostic_k}"); plt.legend(frameon=False); plt.tight_layout(); plt.savefig(output_dir/"diagnostic_orbit_length.png",dpi=180); plt.close()
def plot_cycle_count(diagnostic,config,output_dir):
    plt.figure(figsize=(9,5)); plt.bar(diagnostic["r"],diagnostic["cycle_count"]); plt.xlabel("Phase-step index r"); plt.ylabel("Number of disjoint cycles"); plt.title(f"Cycle Decomposition of Homogeneous Traversal for k={config.diagnostic_k}"); plt.tight_layout(); plt.savefig(output_dir/"diagnostic_cycle_count.png",dpi=180); plt.close()
def plot_totient_count(summary,output_dir):
    plt.figure(figsize=(10,5)); plt.plot(summary["k"],summary["measured_transitive_steps"],marker="o",label="Measured transitive phase steps"); plt.plot(summary["k"],summary["euler_totient_phi_k"],linestyle="--",label="Euler totient phi(k)"); plt.xlabel("Closure sector count k"); plt.ylabel("Number of full-cycle step generators"); plt.title("Transitive Primitive Steps Equal Euler's Totient Function"); plt.legend(frameon=False); plt.tight_layout(); plt.savefig(output_dir/"transitive_steps_vs_totient.png",dpi=180); plt.close()
def plot_phase_kernel(diagnostic,config,output_dir):
    k=config.diagnostic_k; roots=roots_of_unity(k); plt.figure(figsize=(7,7)); plt.scatter(roots.real,roots.imag,s=60)
    for m,root in enumerate(roots): plt.text(1.08*root.real,1.08*root.imag,str(m),ha="center",va="center")
    angle=np.linspace(0,2*np.pi,400); plt.plot(np.cos(angle),np.sin(angle),linewidth=1); trans=diagnostic.loc[diagnostic["transitive_full_cycle"],"r"].tolist(); plt.text(0,-1.30,"Full-cycle step indices: "+", ".join(str(v) for v in trans),ha="center"); plt.xlabel("Real part"); plt.ylabel("Imaginary part"); plt.title(f"Finite Phase Kernel A_k for k={k}"); plt.axis("equal"); plt.xlim(-1.4,1.4); plt.ylim(-1.4,1.4); plt.tight_layout(); plt.savefig(output_dir/"diagnostic_phase_kernel.png",dpi=180); plt.close()

def main():
    config=Config(); output_dir=Path(config.output_dir); output_dir.mkdir(parents=True,exist_ok=True); step=build_step_table(config); step.to_csv(output_dir/"primitive_phase_step_table.csv",index=False); tot=build_totient_summary(config,step); tot.to_csv(output_dir/"transitive_step_totient_summary.csv",index=False); diagnostic=step[step["k"]==config.diagnostic_k].copy().reset_index(drop=True); diagnostic.to_csv(output_dir/"diagnostic_k_step_table.csv",index=False); plot_orbit_length(diagnostic,config,output_dir); plot_cycle_count(diagnostic,config,output_dir); plot_totient_count(tot,output_dir); plot_phase_kernel(diagnostic,config,output_dir)
    print("\nDynamic Closure Notebook — Entry 07\nPrimitive EDF Phase Evolution and the Traversal Theorem\n"+"-"*68); print("\nKernel-preserving homogeneous phase step:\n    Delta_phi = 2*pi*r/k  (mod 2*pi)\n\nInduced sector evolution:\n    m -> m+r (mod k),    U_r = X^r\n\nPrimitive recurrence / full traversal criterion:\n    first return after k updates <=> gcd(k,r) = 1"); print(f"\nEuler-totient criterion verified for every k={config.k_min},...,{config.k_max}: {bool(np.all(tot['agreement']))}"); print(f"\nFor diagnostic k={config.diagnostic_k}, the full-cycle step indices are:\n    "+", ".join(str(v) for v in diagnostic.loc[diagnostic['transitive_full_cycle'],'r'].tolist())); print("\nPrimitive Traversal Theorem:\n    coherent homogeneous phase accumulation + exact finite-kernel preservation + primitive recurrence order k => gcd(k,r)=1, U_r=X^r, and full k-sector traversal.")

if __name__=="__main__": main()
