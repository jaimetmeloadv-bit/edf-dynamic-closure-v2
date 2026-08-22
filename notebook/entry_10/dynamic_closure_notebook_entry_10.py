"""
Dynamic Closure Notebook — Entry 10
Transient-State Causality and Boundary Footprints

EDF-specific input: the DCT defect D_k. Model choices: local path topology,
commitment hazard form, lambda, nu, h0, and intervention strength. Failure of
this pathway model would not invalidate DCT.

The exact reduced-dynamics identities are
    N=(-Q)^(-1), B=NR,
    Q_eff=Q_AA-Q_Aj Q_jj^(-1) Q_jA,
    R_eff=R_A-Q_Aj Q_jj^(-1) R_j.
"""
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import numpy as np
import pandas as pd
try:
    from scipy.linalg import expm
except ImportError as exc:
    raise ImportError("Entry 10 requires scipy.linalg.expm") from exc

@dataclass
class Config:
    k_min:int=2; k_max:int=36; selection_strength:float=2.0
    attempt_frequency:float=1.0; commitment_rate_scale:float=0.10
    target_k:int=12; block_factor:float=0.05
    boundary_pair_initial_condition:bool=True; long_time:float=1000.0
    output_dir:str="dynamic_closure_entry_10_output"

def fibonacci(n):
    a,b=0,1
    for _ in range(n): a,b=b,a+b
    return a

def closure_defect(k_values): return np.asarray([abs(np.log(fibonacci(int(k))/(int(k)**2))) for k in k_values],float)
def path_adjacency(n):
    a=np.zeros((n,n))
    for i in range(n-1): a[i,i+1]=a[i+1,i]=1
    return a

def detailed_balance_rates(defects,selection_strength,attempt_frequency,adjacency):
    delta=defects[None,:]-defects[:,None]; w=attempt_frequency*adjacency*np.exp(-0.5*selection_strength*delta); np.fill_diagonal(w,0); return w

def commitment_hazards(defects,selection_strength,commitment_rate_scale): return commitment_rate_scale*np.exp(-selection_strength*defects)
def absorbing_matrices(rates,hazards):
    q=rates.copy(); np.fill_diagonal(q,-rates.sum(axis=1)-hazards); return q,np.diag(hazards)
def initial_distribution(k_values,config):
    mu=np.zeros(len(k_values))
    if config.boundary_pair_initial_condition: mu[0]=mu[-1]=0.5
    else: mu[:]=1.0/len(mu)
    return mu

def absorption_analysis(q,r,mu):
    fundamental=np.linalg.inv(-q); B=fundamental@r; residence=mu@fundamental; probs=mu@B; eig=np.linalg.eigvals(q)
    return {"fundamental":fundamental,"absorption_matrix":B,"residence":residence,"absorption_probabilities":probs,"generator_eigenvalues":eig,"max_real_eigenvalue":float(np.max(np.real(eig))),"absorption_probability_sum":float(probs.sum())}
def expected_fluxes(residence,rates):
    edge=residence[:,None]*rates; return edge,edge.sum(axis=1)+edge.sum(axis=0)
def finite_time_transient_distribution(mu,q,time_value): return mu@expm(q*time_value)
def apply_soft_blockade(rates,state_index,block_factor):
    w=rates.copy(); w[state_index,:]*=block_factor; w[:,state_index]*=block_factor; w[state_index,state_index]=0; return w

def causal_intervention_table(k_values,defects,base_rates,hazards,mu,base_target_probability,config):
    rows=[]; target_index=int(np.where(k_values==config.target_k)[0][0])
    for index,k in enumerate(k_values):
        if index in (0,len(k_values)-1) or int(k)==config.target_k: continue
        wb=apply_soft_blockade(base_rates,index,config.block_factor); qb,rb=absorbing_matrices(wb,hazards); blocked=absorption_analysis(qb,rb,mu); pb=float(blocked["absorption_probabilities"][target_index]); effect=base_target_probability-pb
        rows.append({"k":int(k),"defect_D":float(defects[index]),"blocked_target_probability":pb,"causal_effect_on_target":effect,"relative_causal_effect":effect/base_target_probability if base_target_probability>0 else np.nan})
    return pd.DataFrame(rows)

def schur_eliminate_one(q,r,eliminate_index):
    n=q.shape[0]; retained=np.array([i for i in range(n) if i!=eliminate_index],int); qaa=q[np.ix_(retained,retained)]; qaj=q[np.ix_(retained,[eliminate_index])]; qja=q[np.ix_([eliminate_index],retained)]; qjj=float(q[eliminate_index,eliminate_index]); ra=r[retained,:]; rj=r[[eliminate_index],:]
    qeff=qaa-qaj@(qja/qjj); reff=ra-qaj@(rj/qjj); return retained,qeff,reff

def boundary_footprint_table(k_values,q,r):
    rows=[]; full_B=np.linalg.inv(-q)@r
    for j,k in enumerate(k_values):
        retained,qeff,reff=schur_eliminate_one(q,r,j); reduced_B=np.linalg.inv(-qeff)@reff; preservation=float(np.max(np.abs(reduced_B-full_B[retained,:]))); qaj=q[np.ix_(retained,[j])]; qja=q[np.ix_([j],retained)]; qjj=float(q[j,j]); rj=r[[j],:]; dq=-(qaj/qjj)@qja; dr=-(qaj/qjj)@rj; tq=float(np.linalg.norm(dq,ord="fro")); ar=float(np.linalg.norm(dr,ord="fro")); rows.append({"k":int(k),"transition_boundary_footprint":tq,"absorption_boundary_footprint":ar,"total_boundary_footprint":float(np.sqrt(tq*tq+ar*ar)),"absorption_statistics_preservation_error":preservation})
    return pd.DataFrame(rows)

def main():
    config=Config(); out=Path(config.output_dir); out.mkdir(parents=True,exist_ok=True); k_values=np.arange(config.k_min,config.k_max+1,dtype=int); defects=closure_defect(k_values); rates=detailed_balance_rates(defects,config.selection_strength,config.attempt_frequency,path_adjacency(len(k_values))); hazards=commitment_hazards(defects,config.selection_strength,config.commitment_rate_scale); q,r=absorbing_matrices(rates,hazards); mu=initial_distribution(k_values,config); base=absorption_analysis(q,r,mu); residence=base["residence"]; probs=base["absorption_probabilities"]; target_index=int(np.where(k_values==config.target_k)[0][0]); target_probability=float(probs[target_index]); edge_flux,throughflow=expected_fluxes(residence,rates); causal=causal_intervention_table(k_values,defects,rates,hazards,mu,target_probability,config); footprint=boundary_footprint_table(k_values,q,r); long_time=finite_time_transient_distribution(mu,q,config.long_time)
    pd.DataFrame({"k":k_values,"defect_D":defects,"expected_residence":residence,"final_absorption_probability":probs,"throughflow":throughflow}).to_csv(out/"transient_sector_memory_table.csv",index=False); causal.to_csv(out/"causal_pathway_interventions.csv",index=False); footprint.to_csv(out/"schur_boundary_footprints.csv",index=False); pd.DataFrame(edge_flux,index=k_values,columns=k_values).to_csv(out/"expected_transition_flux_matrix.csv")
    extinction=base["max_real_eigenvalue"]<0; residual=float(np.sum(long_time)); normerr=abs(base["absorption_probability_sum"]-1); preserve=float(footprint["absorption_statistics_preservation_error"].max()); nonzero_res=int(np.sum(residence>1e-12)); nonzero_foot=int(np.sum(footprint["total_boundary_footprint"]>1e-12)); positive=int(np.sum(causal["causal_effect_on_target"]>1e-12))
    print("\nDynamic Closure Notebook — Entry 10\nTransient-State Causality and Boundary Footprints\n"+"-"*66); print(f"\nAll transient states asymptotically vanish: {extinction}\nTotal transient probability at t={config.long_time:g}: {residual:.6e}\nAbsorption normalization error: {normerr:.6e}\nBaseline P(commit to k={config.target_k}): {target_probability:.6f}\nTransient sectors with nonzero expected residence: {nonzero_res}/{len(k_values)}\nTransient sectors with nonzero Schur boundary footprint: {nonzero_foot}/{len(k_values)}\nInterior non-target sectors with positive soft-block causal effect: {positive}/{len(causal)}\nMaximum Schur absorption-statistics preservation error: {preserve:.6e}")
    print("\nInterpretation: terminal transient occupancy goes to zero, but residence, flux, intervention effects, and Schur-complement boundary terms remain nonzero. Eliminating a transient state transfers its influence into effective couplings and sink terms rather than erasing it.")

if __name__=="__main__": main()
