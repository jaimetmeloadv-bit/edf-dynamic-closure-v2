"""
Dynamic Closure Notebook — Entry 09
Closure Defect and Theorem-Compatible Selection Functional

DCT fixes the exact zero through F_k=C(k)=k^2. This entry defines equivalent
defect representations, a MaxEnt selection family, and detailed-balance jump
dynamics. The kinetic law is a model choice; the structural zero is not.
"""
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

@dataclass
class Config:
    k_min:int=2; k_max:int=36
    lambda_values:tuple[float,...]=(0.0,0.25,0.5,1.0,2.0,4.0)
    attempt_frequency:float=1.0; diagnostic_lambda:float=2.0; diagnostic_k:int=12
    output_dir:str="dynamic_closure_entry_09_output"

def fibonacci(n):
    a,b=0,1
    for _ in range(n): a,b=b,a+b
    return a

def structural_table(config):
    rows=[]
    for k in range(config.k_min,config.k_max+1):
        f=fibonacci(k); c=k*k; delta=f-c; ad=abs(delta); ratio=f/c; D=abs(np.log(ratio)); B=ad/(f+c); S=ad/np.sqrt(f*c)
        rows.append({"k":k,"F_k":f,"closure_capacity_k2":c,"signed_integer_defect":delta,"absolute_integer_defect":ad,"ratio_F_over_C":ratio,"log_ratio_defect_D":D,"bounded_defect_B":B,"bounded_from_tanh_D_over_2":np.tanh(D/2),"bounded_identity_error":abs(B-np.tanh(D/2)),"symmetric_relative_defect":S,"symmetric_from_2sinh_D_over_2":2*np.sinh(D/2),"symmetric_identity_error":abs(S-2*np.sinh(D/2)),"exact_DCT_closure":f==c})
    return pd.DataFrame(rows)

def maxent_distribution(defects,lam):
    logs=-lam*defects; logs-=np.max(logs); w=np.exp(logs); return w/w.sum()

def selection_table(structure,config):
    d=structure["log_ratio_defect_D"].to_numpy(float); kv=structure["k"].to_numpy(int); rows=[]
    for lam in config.lambda_values:
        p=maxent_distribution(d,lam); mean=float(np.sum(p*d)); H=float(-np.sum(p*np.log(np.where(p>0,p,1))))
        for k,di,pi in zip(kv,d,p): rows.append({"lambda":lam,"k":int(k),"defect_D":float(di),"selection_probability":float(pi),"ensemble_mean_defect":mean,"selection_entropy":H})
    return pd.DataFrame(rows)

def complete_adjacency(n):
    a=np.ones((n,n)); np.fill_diagonal(a,0); return a
def path_adjacency(n):
    a=np.zeros((n,n))
    for i in range(n-1): a[i,i+1]=a[i+1,i]=1
    return a

def jump_rates(defects,lam,nu,adj):
    delta=defects[None,:]-defects[:,None]; w=nu*adj*np.exp(-0.5*lam*delta); np.fill_diagonal(w,0); return w

def generator_from_rates(rates):
    q=rates.copy(); np.fill_diagonal(q,-rates.sum(axis=1)); return q

def topology_diagnostics(structure,config):
    d=structure["log_ratio_defect_D"].to_numpy(float); rows=[]
    for lam in config.lambda_values:
        p=maxent_distribution(d,lam)
        for name,adj in [("complete",complete_adjacency(len(d))),("path",path_adjacency(len(d)))]:
            w=jump_rates(d,lam,config.attempt_frequency,adj); q=generator_from_rates(w); flux=p[:,None]*w; db=float(np.max(np.abs(flux-flux.T))); stationary=float(np.sum(np.abs(p@q))); eig=np.linalg.eigvals(q); real=np.sort(np.real(eig)); gap=float(-real[-2]) if len(real)>1 else np.nan
            rows.append({"lambda":lam,"topology":name,"maximum_detailed_balance_flux_error":db,"stationary_distribution_residual_L1":stationary,"spectral_gap":gap})
    return pd.DataFrame(rows)

def monotone_equivalence_table(structure):
    a=structure.sort_values("log_ratio_defect_D")["k"].tolist(); b=structure.sort_values("bounded_defect_B")["k"].tolist(); c=structure.sort_values("symmetric_relative_defect")["k"].tolist()
    return pd.DataFrame([{"all_ranks_equal":a==b==c}])
def lambda_summary(selection,config):
    rows=[]
    for lam,g in selection.groupby("lambda"):
        t=g[g["k"]==config.diagnostic_k].iloc[0]; rows.append({"lambda":lam,"target_probability":t["selection_probability"],"ensemble_mean_defect":t["ensemble_mean_defect"],"selection_entropy":t["selection_entropy"]})
    return pd.DataFrame(rows)

def main():
    config=Config(); out=Path(config.output_dir); out.mkdir(parents=True,exist_ok=True); structure=structural_table(config); structure.to_csv(out/"closure_defect_table.csv",index=False); monotone=monotone_equivalence_table(structure); monotone.to_csv(out/"defect_monotone_equivalence.csv",index=False); selection=selection_table(structure,config); selection.to_csv(out/"maxent_selection_family.csv",index=False); summary=lambda_summary(selection,config); summary.to_csv(out/"selection_lambda_summary.csv",index=False); topology=topology_diagnostics(structure,config); topology.to_csv(out/"detailed_balance_topology_diagnostics.csv",index=False)
    exact=structure.loc[structure["exact_DCT_closure"],"k"].tolist(); print("\nDynamic Closure Notebook — Entry 09\nClosure Defect and Theorem-Compatible Selection Functional\n"+"-"*72); print("\nDCT closure condition:\n    F_k = C(k) = k^2\n\nCanonical defect:\n    D_k = |ln(F_k/k^2)|"); print(f"\nExact zero-defect sectors: {exact}\nB=tanh(D/2) verified: {structure['bounded_identity_error'].max()<1e-12}\nS=2sinh(D/2) verified: {structure['symmetric_identity_error'].max()<1e-12}\nAll defect rankings equal: {bool(monotone['all_ranks_equal'].all())}"); print(f"\nDetailed balance verified: {topology['maximum_detailed_balance_flux_error'].max()<1e-12}\nStationarity verified: {topology['stationary_distribution_residual_L1'].max()<1e-12}")

if __name__=="__main__": main()
