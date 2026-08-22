"""
Dynamic Closure Notebook — Entry 06
Why a Cyclic Dynamic Closure Requires Phase and Shift Generators

Entry 05 established cyclic phase Z + cyclic shift X + operator composition -> M_k(C), dimension k^2. Entry 06 tests the preceding bridge: phase distinguishability supplies Z; actual cyclic traversal supplies X up to gauge. Either generator alone gives a k-dimensional commutative algebra, while both give k^2.
"""
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

@dataclass
class Config:
    k_min:int=2; k_max:int=24; gauge_trials_per_k:int=100; random_seed:int=112358
    output_dir:str="dynamic_closure_entry_06_output"

def clock_and_shift(k):
    omega=np.exp(2j*np.pi/k); x=np.zeros((k,k),complex)
    for m in range(k): x[(m+1)%k,m]=1
    z=np.diag(np.array([omega**m for m in range(k)],dtype=complex)); return omega,x,z

def discrete_fourier(k):
    omega=np.exp(2j*np.pi/k); return np.array([[omega**(m*n)/np.sqrt(k) for n in range(k)] for m in range(k)],dtype=complex)

def matrix_span_rank(matrices):
    return int(np.linalg.matrix_rank(np.column_stack([m.reshape(-1) for m in matrices])))

def single_generator_algebra_dimension(generator,k): return matrix_span_rank([np.linalg.matrix_power(generator,p) for p in range(k)])
def pair_generator_algebra_dimension(x,z,k): return matrix_span_rank([np.linalg.matrix_power(x,a)@np.linalg.matrix_power(z,b) for a in range(k) for b in range(k)])

def random_closed_traversal(k,rng):
    theta=np.empty(k,float)
    if k>1: theta[:-1]=rng.uniform(-np.pi,np.pi,size=k-1); theta[-1]=-np.sum(theta[:-1])
    else: theta[0]=0
    t=np.zeros((k,k),complex)
    for m in range(k): t[(m+1)%k,m]=np.exp(1j*theta[m])
    return theta,t

def gauge_from_traversal_phases(theta):
    alpha=np.zeros(len(theta),float)
    for m in range(len(theta)-1): alpha[m+1]=alpha[m]+theta[m]
    return np.diag(np.exp(1j*alpha))

def verify_gauge_equivalence(k,rng):
    omega,x,z=clock_and_shift(k); theta,t=random_closed_traversal(k,rng); g=gauge_from_traversal_phases(theta); I=np.eye(k,complex)
    return {"k":k,"cycle_closure_error":float(np.linalg.norm(np.linalg.matrix_power(t,k)-I,ord="fro")),"gauge_to_shift_error":float(np.linalg.norm(g.conj().T@t@g-x,ord="fro")),"gauge_phase_commutator_error":float(np.linalg.norm(g@z-z@g,ord="fro")),"dressed_weyl_relation_error":float(np.linalg.norm(z@t-omega*t@z,ord="fro")),"total_traversal_phase":float(np.sum(theta))}

def verify_fourier_duality(k):
    _,x,z=clock_and_shift(k); f=discrete_fourier(k); I=np.eye(k,dtype=complex)
    return {"k":k,"fourier_unitarity_error":float(np.linalg.norm(f.conj().T@f-I,ord="fro")),"Fdag_Z_F_minus_X_error":float(np.linalg.norm(f.conj().T@z@f-x,ord="fro")),"Fdag_X_F_minus_Zinv_error":float(np.linalg.norm(f.conj().T@x@f-z.conj().T,ord="fro"))}

def verify_phase_only_occupation_invariance(k,rng):
    _,x,z=clock_and_shift(k); psi=rng.normal(size=k)+1j*rng.normal(size=k); psi/=np.linalg.norm(psi); power=int(rng.integers(0,k)); phase=np.linalg.matrix_power(z,power)@psi; shifted=x@psi; init=np.abs(psi)**2
    return {"k":k,"phase_power":power,"phase_only_occupation_change_L1":float(np.linalg.norm(np.abs(phase)**2-init,ord=1)),"shift_permutation_error_L1":float(np.linalg.norm(np.abs(shifted)**2-np.roll(init,1),ord=1))}

def algebra_dimension_table(config):
    rows=[]
    for k in range(config.k_min,config.k_max+1):
        _,x,z=clock_and_shift(k); rows.append({"k":k,"phase_only_dimension":single_generator_algebra_dimension(z,k),"shift_only_dimension":single_generator_algebra_dimension(x,k),"phase_shift_dimension":pair_generator_algebra_dimension(x,z,k),"expected_single_generator_dimension":k,"expected_pair_dimension":k*k})
    return pd.DataFrame(rows)

def gauge_diagnostics_table(config):
    master=np.random.default_rng(config.random_seed); rows=[]
    for k in range(config.k_min,config.k_max+1):
        for trial in range(config.gauge_trials_per_k):
            seed=int(master.integers(0,2**32-1)); r=verify_gauge_equivalence(k,np.random.default_rng(seed)); r["trial"]=trial; r["seed"]=seed; rows.append(r)
    return pd.DataFrame(rows)

def phase_dynamics_table(config):
    master=np.random.default_rng(config.random_seed+1000003); rows=[]
    for k in range(config.k_min,config.k_max+1):
        seed=int(master.integers(0,2**32-1)); r=verify_phase_only_occupation_invariance(k,np.random.default_rng(seed)); r["seed"]=seed; rows.append(r)
    return pd.DataFrame(rows)

def plot_algebra_dimensions(table,output_dir):
    plt.figure(figsize=(9,5)); plt.plot(table["k"],table["phase_only_dimension"],marker="o",label="Phase generator only"); plt.plot(table["k"],table["shift_only_dimension"],marker="x",label="Shift generator only"); plt.plot(table["k"],table["phase_shift_dimension"],marker="o",label="Phase + shift generators"); plt.xlabel("Closure sector count k"); plt.ylabel("Generated algebra dimension"); plt.title("Generator Sufficiency: k versus k^2"); plt.legend(frameon=False); plt.tight_layout(); plt.savefig(output_dir/"generator_algebra_dimensions.png",dpi=180); plt.close()

def plot_dimension_ratio(table,output_dir):
    plt.figure(figsize=(9,5)); plt.plot(table["k"],table["phase_only_dimension"]/(table["k"]**2),marker="o",label="Phase only / full operator dimension"); plt.plot(table["k"],table["shift_only_dimension"]/(table["k"]**2),marker="x",label="Shift only / full operator dimension"); plt.plot(table["k"],table["phase_shift_dimension"]/(table["k"]**2),marker="o",label="Phase + shift / full operator dimension"); plt.xlabel("Closure sector count k"); plt.ylabel("Fraction of full operator space"); plt.title("Fraction of M_k(C) Generated by the Available Operators"); plt.legend(frameon=False); plt.tight_layout(); plt.savefig(output_dir/"generated_operator_fraction.png",dpi=180); plt.close()

def plot_gauge_errors(s,output_dir):
    plt.figure(figsize=(9,5)); plt.semilogy(s["k"],s["max_cycle_closure_error"]+1e-18,marker="o",label="Cycle closure error"); plt.semilogy(s["k"],s["max_gauge_to_shift_error"]+1e-18,marker="o",label="Gauge-to-shift error"); plt.semilogy(s["k"],s["max_dressed_weyl_relation_error"]+1e-18,marker="o",label="Dressed Weyl relation error"); plt.xlabel("Closure sector count k"); plt.ylabel("Maximum numerical error"); plt.title("Gauge Equivalence of Closed Cyclic Traversal"); plt.legend(frameon=False); plt.tight_layout(); plt.savefig(output_dir/"gauge_equivalence_errors.png",dpi=180); plt.close()

def plot_phase_occupation_invariance(d,output_dir):
    plt.figure(figsize=(9,5)); plt.semilogy(d["k"],d["phase_only_occupation_change_L1"]+1e-18,marker="o",label="Occupation change under phase-only action"); plt.semilogy(d["k"],d["shift_permutation_error_L1"]+1e-18,marker="x",label="Shift permutation error"); plt.xlabel("Closure sector count k"); plt.ylabel("L1 error / change"); plt.title("Phase Labeling Does Not Produce Sector Traversal"); plt.legend(frameon=False); plt.tight_layout(); plt.savefig(output_dir/"phase_only_occupation_invariance.png",dpi=180); plt.close()

def main():
    config=Config(); output_dir=Path(config.output_dir); output_dir.mkdir(parents=True,exist_ok=True)
    dimensions=algebra_dimension_table(config); dimensions.to_csv(output_dir/"generator_algebra_dimensions.csv",index=False)
    fourier=pd.DataFrame([verify_fourier_duality(k) for k in range(config.k_min,config.k_max+1)]); fourier.to_csv(output_dir/"fourier_duality_diagnostics.csv",index=False)
    gauge=gauge_diagnostics_table(config); gauge.to_csv(output_dir/"gauge_equivalence_trials.csv",index=False)
    summary=gauge.groupby("k",as_index=False).agg(max_cycle_closure_error=("cycle_closure_error","max"),max_gauge_to_shift_error=("gauge_to_shift_error","max"),max_gauge_phase_commutator_error=("gauge_phase_commutator_error","max"),max_dressed_weyl_relation_error=("dressed_weyl_relation_error","max")); summary.to_csv(output_dir/"gauge_equivalence_summary.csv",index=False)
    phase=phase_dynamics_table(config); phase.to_csv(output_dir/"phase_only_dynamics_diagnostics.csv",index=False)
    plot_algebra_dimensions(dimensions,output_dir); plot_dimension_ratio(dimensions,output_dir); plot_gauge_errors(summary,output_dir); plot_phase_occupation_invariance(phase,output_dir)
    p=bool(np.all(dimensions["phase_only_dimension"]==dimensions["expected_single_generator_dimension"])); s=bool(np.all(dimensions["shift_only_dimension"]==dimensions["expected_single_generator_dimension"])); pair=bool(np.all(dimensions["phase_shift_dimension"]==dimensions["expected_pair_dimension"]))
    print("\nDynamic Closure Notebook — Entry 06\nWhy a Cyclic Dynamic Closure Requires Phase and Shift\n"+"-"*64)
    print(f"\nPhase-only algebra dimension equals k for all tested k: {p}\nShift-only algebra dimension equals k for all tested k: {s}\nPhase + shift algebra dimension equals k^2 for all tested k: {pair}")
    print(f"\nMaximum Fourier duality error F^dagger Z F = X: {fourier['Fdag_Z_F_minus_X_error'].max():.6e}\nMaximum Fourier duality error F^dagger X F = Z^(-1): {fourier['Fdag_X_F_minus_Zinv_error'].max():.6e}")
    print(f"\nMaximum closed-traversal gauge-to-shift error across all trials: {gauge['gauge_to_shift_error'].max():.6e}\nMaximum dressed Weyl-relation error across all trials: {gauge['dressed_weyl_relation_error'].max():.6e}")
    print("\nStructural conclusion:\n    Phase distinguishability supplies Z; actual cyclic traversal supplies X up to gauge. Either generator alone spans only a k-dimensional commutative algebra; together they span M_k(C), dimension k^2.")

if __name__=="__main__": main()
