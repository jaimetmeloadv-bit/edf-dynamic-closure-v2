"""
Dynamic Closure Notebook — Entry 11
Robustness and Falsification Suite

Stress-tests the post-DCT transient-memory model over selection strength,
commitment scale, topology, initial condition, defect representation,
commitment law, and intervention strength.

STRUCTURAL MEMORY tested here:
- transient occupancy vanishes when Q is Hurwitz;
- reachable transient states retain positive integrated residence;
- eliminating a coupled state produces Schur-complement boundary terms.

TARGET-SPECIFIC CAUSALITY is deliberately allowed to change sign. DCT itself
is not modified or retested by this entry.
"""
from dataclasses import dataclass
from pathlib import Path
import numpy as np
import pandas as pd

@dataclass
class Config:
    k_min:int=2; k_max:int=36; target_k:int=12
    lambdas:tuple=(0.0,0.5,1.0,2.0,4.0); h0_values:tuple=(0.02,0.10,0.50)
    topologies:tuple=("path","ring","complete"); initial_conditions:tuple=("boundary_pair","left_boundary")
    defect_names:tuple=("log","bounded","symmetric"); commitment_laws:tuple=("exponential","reciprocal","quadratic_exponential")
    block_factor:float=0.05; blockade_factors:tuple=(0.0,0.01,0.05,0.20,0.50,0.80)
    attempt_frequency:float=1.0; tolerance:float=1e-10
    output_dir:str="dynamic_closure_entry_11_output"

def fibonacci(n):
    a,b=0,1
    for _ in range(n): a,b=b,a+b
    return a

def log_defect(k_values): return np.array([abs(np.log(fibonacci(int(k))/(int(k)**2))) for k in k_values],float)
def defect_transform(d,name):
    if name=="log": x=d.copy()
    elif name=="bounded": x=np.tanh(d/2)
    elif name=="symmetric": x=2*np.sinh(d/2)
    else: raise ValueError(name)
    nz=x[x>0]; scale=float(nz.mean()) if len(nz) else 1.0; return x/scale

def adjacency(n,topology):
    a=np.zeros((n,n),float)
    if topology=="path":
        for i in range(n-1): a[i,i+1]=a[i+1,i]=1
    elif topology=="ring":
        for i in range(n): j=(i+1)%n; a[i,j]=a[j,i]=1
    elif topology=="complete": a[:]=1; np.fill_diagonal(a,0)
    else: raise ValueError(topology)
    return a*(2.0/a.sum(axis=1).mean())
def rates_from_defect(d,lam,nu,a):
    delta=d[None,:]-d[:,None]; w=nu*a*np.exp(-0.5*lam*delta); np.fill_diagonal(w,0); return w
def hazards_from_defect(d,lam,h0,law):
    if law=="exponential": return h0*np.exp(-lam*d)
    if law=="reciprocal": return h0/(1+lam*d)
    if law=="quadratic_exponential": return h0*np.exp(-lam*d**2)
    raise ValueError(law)
def generator(w,h):
    q=w.copy(); np.fill_diagonal(q,-w.sum(axis=1)-h); return q
def initial_distribution(n,name):
    mu=np.zeros(n)
    if name=="boundary_pair": mu[0]=mu[-1]=0.5
    elif name=="left_boundary": mu[0]=1
    else: raise ValueError(name)
    return mu
def target_absorption(q,h,mu,target):
    rhs=np.zeros(len(h)); rhs[target]=h[target]; return float(mu@np.linalg.solve(-q,rhs))
def residence(q,mu): return np.linalg.solve((-q).T,mu)
def schur_footprints(q,h):
    n=len(h); out=np.zeros(n)
    for j in range(n):
        keep=[i for i in range(n) if i!=j]; qaj=q[np.ix_(keep,[j])]; qja=q[np.ix_([j],keep)]; qjj=float(q[j,j]); dq=-(qaj*(1/qjj))@qja; dr=-(qaj[:,0]*(1/qjj)*h[j]); out[j]=np.sqrt(np.linalg.norm(dq,ord="fro")**2+np.linalg.norm(dr)**2)
    return out
def block_state(w,j,factor):
    wb=w.copy(); wb[j,:]*=factor; wb[:,j]*=factor; wb[j,j]=0; return wb
def causal_effects(w,h,mu,target,base_prob,factor):
    effects=[]
    for j in range(len(h)):
        if j==target or mu[j]>0: continue
        qb=generator(block_state(w,j,factor),h); effects.append(base_prob-target_absorption(qb,h,mu,target))
    return np.asarray(effects,float)
def evaluate(k_values,base_d,lam,h0,topology,initial_name,defect_name,law,config,block_factor=None):
    d=defect_transform(base_d,defect_name); a=adjacency(len(k_values),topology); w=rates_from_defect(d,lam,config.attempt_frequency,a); h=hazards_from_defect(d,lam,h0,law); q=generator(w,h); mu=initial_distribution(len(k_values),initial_name); target=int(np.where(k_values==config.target_k)[0][0]); p=target_absorption(q,h,mu,target); tau=residence(q,mu); footprints=schur_footprints(q,h); factor=config.block_factor if block_factor is None else block_factor; effects=causal_effects(w,h,mu,target,p,factor); max_real=float(np.max(np.real(np.linalg.eigvals(q)))); tol=config.tolerance
    return {"lambda":lam,"h0":h0,"topology":topology,"initial_condition":initial_name,"defect_representation":defect_name,"commitment_law":law,"block_factor":factor,"target_probability":p,"max_real_transient_eigenvalue":max_real,"transient_extinction_verified":max_real<-tol,"minimum_expected_residence":float(tau.min()),"all_states_positive_residence":bool(np.all(tau>0)),"all_states_residence_above_tolerance":bool(np.all(tau>tol)),"minimum_schur_footprint":float(footprints.min()),"all_states_nonzero_schur_footprint":bool(np.all(footprints>tol)),"causal_probe_count":len(effects),"positive_causal_count":int(np.sum(effects>tol)),"negative_causal_count":int(np.sum(effects<-tol)),"near_zero_causal_count":int(np.sum(np.abs(effects)<=tol)),"positive_causal_fraction":float(np.mean(effects>tol)),"median_causal_effect":float(np.median(effects)),"mean_absolute_causal_effect":float(np.mean(np.abs(effects))),"max_absolute_causal_effect":float(np.max(np.abs(effects))),"min_causal_effect":float(effects.min()),"max_causal_effect":float(effects.max())}
def build_core_grid(k_values,base_d,config):
    rows=[]
    for lam in config.lambdas:
        for h0 in config.h0_values:
            for topology in config.topologies:
                for init in config.initial_conditions:
                    for defect in config.defect_names: rows.append(evaluate(k_values,base_d,lam,h0,topology,init,defect,"exponential",config))
    return pd.DataFrame(rows)
def build_law_sensitivity(k_values,base_d,config): return pd.DataFrame([evaluate(k_values,base_d,lam,h0,"path","boundary_pair","log",law,config) for lam in config.lambdas for h0 in config.h0_values for law in config.commitment_laws])
def build_blockade_sensitivity(k_values,base_d,config): return pd.DataFrame([evaluate(k_values,base_d,2.0,0.10,"path","boundary_pair","log","exponential",config,block_factor=f) for f in config.blockade_factors])
def category_summary(df,category):
    return df.groupby(category,as_index=False).agg(configurations=("target_probability","size"),mean_target_probability=("target_probability","mean"),mean_positive_causal_fraction=("positive_causal_fraction","mean"),median_abs_causal_effect=("mean_absolute_causal_effect","median"),min_schur_footprint=("minimum_schur_footprint","min"),extinction_success=("transient_extinction_verified","mean"),positive_residence_success=("all_states_positive_residence","mean"),residence_above_tolerance_success=("all_states_residence_above_tolerance","mean"),schur_success=("all_states_nonzero_schur_footprint","mean"))
def main():
    config=Config(); out=Path(config.output_dir); out.mkdir(parents=True,exist_ok=True); k_values=np.arange(config.k_min,config.k_max+1); base_d=log_defect(k_values); core=build_core_grid(k_values,base_d,config); core.to_csv(out/"core_robustness_grid.csv",index=False); laws=build_law_sensitivity(k_values,base_d,config); laws.to_csv(out/"commitment_law_sensitivity.csv",index=False); blockade=build_blockade_sensitivity(k_values,base_d,config); blockade.to_csv(out/"blockade_strength_sensitivity.csv",index=False); category_summary(core,"topology").to_csv(out/"topology_robustness_summary.csv",index=False); category_summary(core,"defect_representation").to_csv(out/"defect_robustness_summary.csv",index=False); category_summary(core,"initial_condition").to_csv(out/"initial_condition_robustness_summary.csv",index=False); weak=core.sort_values("positive_causal_fraction").head(30); weak.to_csv(out/"target_causality_weakening_regimes.csv",index=False)
    print("\nDynamic Closure Notebook — Entry 11\nRobustness and Falsification Suite\n"+"-"*52); print(f"\nCore configurations: {len(core)}\nAll extinction verified: {bool(core['transient_extinction_verified'].all())}\nAll positive residence: {bool(core['all_states_positive_residence'].all())}\nAll nonzero Schur footprints: {bool(core['all_states_nonzero_schur_footprint'].all())}\nMedian positive target-causal fraction: {core['positive_causal_fraction'].median():.6f}\nMinimum positive target-causal fraction: {core['positive_causal_fraction'].min():.6f}"); print("\nRobust conclusion: p_j(infinity)=0 does not imply dynamical irrelevance. The sign of target-conditioned intervention is topology/path/model dependent.")
if __name__=="__main__": main()
