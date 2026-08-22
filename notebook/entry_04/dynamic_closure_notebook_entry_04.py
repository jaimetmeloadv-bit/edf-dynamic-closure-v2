"""
Dynamic Closure Notebook — Entry 04
Pair-Space Derivation, Combinatorial Controls, and Arithmetic Uniqueness

This notebook investigates the structural meaning of k^2. No target sector is hard-coded.
It compares full ordered pair space k^2, traceless k^2-1, ordered/no-self,
unordered counts, and a linear count. Exact structural closure is F_k=C(k).
The published Bugeaud–Mignotte–Siksek classification of Fibonacci perfect
powers implies that, conditional on C(k)=k^2, k=12 is the unique nontrivial
solution for k>=2.
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
    k_min:int=2; k_max_table:int=30; k_max_verification:int=500
    plot_k_min:int=4; plot_k_max:int=24
    output_dir:str="dynamic_closure_entry_04_output"

def fibonacci(n):
    if n<0: raise ValueError("Fibonacci index must be non-negative.")
    a,b=0,1
    for _ in range(n): a,b=b,a+b
    return a

def normalized_residual(f,c):
    d=f+c
    return 0.0 if d==0 else abs(f-c)/d

def full_ordered_with_self(k): return k*k
def full_traceless(k): return k*k-1
def ordered_without_self(k): return k*(k-1)
def unordered_with_self(k): return k*(k+1)//2
def unordered_without_self(k): return k*(k-1)//2
def linear_count(k): return k
COUNT_MODELS={"full_ordered_with_self_k2":full_ordered_with_self,"full_traceless_k2_minus_1":full_traceless,"ordered_without_self":ordered_without_self,"unordered_with_self":unordered_with_self,"unordered_without_self":unordered_without_self,"linear_count":linear_count}

def verify_hermitian_real_dimension(k):
    diagonal=k; off=k*(k-1); return diagonal,off,diagonal+off

def build_model_table(config):
    rows=[]
    for k in range(config.k_min,config.k_max_table+1):
        fib=fibonacci(k); diagonal,off,total=verify_hermitian_real_dimension(k)
        row={"k":k,"F_k":fib,"hermitian_diagonal_real_components":diagonal,"hermitian_off_diagonal_real_components":off,"hermitian_total_real_dimension":total}
        for name,func in COUNT_MODELS.items():
            count=func(k); row[f"{name}_count"]=count; row[f"{name}_residual"]=normalized_residual(fib,count); row[f"{name}_exact"]=fib==count
        rows.append(row)
    return pd.DataFrame(rows)

def find_exact_solutions(config):
    rows=[]
    for name,func in COUNT_MODELS.items():
        for k in range(config.k_min,config.k_max_verification+1):
            fib=fibonacci(k); count=func(k)
            if fib==count: rows.append({"model":name,"k":k,"F_k":fib,"structural_count":count})
    return pd.DataFrame(rows,columns=["model","k","F_k","structural_count"])

def find_minimum_residuals(table):
    rows=[]
    for name in COUNT_MODELS:
        col=f"{name}_residual"; idx=table[col].idxmin(); r=table.loc[idx]
        rows.append({"model":name,"best_k_in_table_range":int(r["k"]),"minimum_residual":float(r[col]),"exact_in_table_range":bool(r[f"{name}_exact"])})
    return pd.DataFrame(rows)

def perfect_power_theorem_certificate():
    return pd.DataFrame([{"k":k,"F_k":fibonacci(k),"k_squared":k*k,"F_k_equals_k_squared":fibonacci(k)==k*k} for k in [0,1,2,6,12]])

def make_residual_plot(table,config,output_dir):
    s=table[(table["k"]>=config.plot_k_min)&(table["k"]<=config.plot_k_max)]
    models=["full_ordered_with_self_k2","full_traceless_k2_minus_1","ordered_without_self","unordered_with_self","unordered_without_self"]
    labels={"full_ordered_with_self_k2":"Ordered + self: k^2","full_traceless_k2_minus_1":"Traceless: k^2 - 1","ordered_without_self":"Ordered, no self: k(k-1)","unordered_with_self":"Unordered + self: k(k+1)/2","unordered_without_self":"Unordered, no self: k(k-1)/2"}
    plt.figure(figsize=(10,6))
    for name in models: plt.plot(s["k"],s[f"{name}_residual"],marker="o",label=labels[name])
    plt.xlabel("Closure sector k"); plt.ylabel("Normalized structural residual"); plt.title("Fibonacci Residual Across Pair-Space Hypotheses"); plt.legend(fontsize=8,frameon=False); plt.tight_layout(); plt.savefig(output_dir/"pair_space_residual_comparison.png",dpi=180); plt.close()

def make_k2_vs_traceless_plot(table,config,output_dir):
    s=table[(table["k"]>=config.plot_k_min)&(table["k"]<=config.plot_k_max)]
    plt.figure(figsize=(9,5)); plt.plot(s["k"],s["full_ordered_with_self_k2_residual"],marker="o",label="Full operator space: k^2"); plt.plot(s["k"],s["full_traceless_k2_minus_1_residual"],marker="o",label="Traceless state coordinates: k^2 - 1")
    plt.xlabel("Closure sector k"); plt.ylabel("Normalized structural residual"); plt.title("Full Operator Space vs Traceless Subspace"); plt.legend(frameon=False); plt.tight_layout(); plt.savefig(output_dir/"k2_vs_k2_minus_1.png",dpi=180); plt.close()

def make_exact_solution_plot(exact_solutions,output_dir):
    if exact_solutions.empty:return
    counts=exact_solutions.groupby("model").size().reindex(COUNT_MODELS.keys(),fill_value=0)
    plt.figure(figsize=(10,5)); plt.bar(np.arange(len(counts)),counts.to_numpy()); plt.xticks(np.arange(len(counts)),["k^2","k^2-1","k(k-1)","k(k+1)/2","k(k-1)/2","k"],rotation=25,ha="right"); plt.ylabel("Number of exact solutions"); plt.title("Exact Fibonacci-Closure Solutions for 2 <= k <= 500"); plt.tight_layout(); plt.savefig(output_dir/"exact_solution_counts.png",dpi=180); plt.close()

def main():
    config=Config(); output_dir=Path(config.output_dir); output_dir.mkdir(parents=True,exist_ok=True)
    table=build_model_table(config); table.to_csv(output_dir/"pair_space_model_table.csv",index=False)
    exact=find_exact_solutions(config); exact.to_csv(output_dir/"exact_solutions_to_k500.csv",index=False)
    minima=find_minimum_residuals(table); minima.to_csv(output_dir/"minimum_residuals.csv",index=False)
    theorem=perfect_power_theorem_certificate(); theorem.to_csv(output_dir/"perfect_power_theorem_certificate.csv",index=False)
    make_residual_plot(table,config,output_dir); make_k2_vs_traceless_plot(table,config,output_dir); make_exact_solution_plot(exact,output_dir)
    ok=bool(np.all(table["hermitian_total_real_dimension"]==table["k"]**2))
    print("\nDynamic Closure Notebook — Entry 04\nPair-Space Derivation and Arithmetic Uniqueness\n"+"-"*60)
    print(f"\nHermitian dimension identity verified over table range: {ok}")
    print("\nExact computational solutions for 2 <= k <= 500:\n",exact.to_string(index=False))
    print("\nMinimum normalized residuals for 2 <= k <= 30:\n",minima.to_string(index=False))
    print("\nPublished perfect-power theorem certificate:\n",theorem.to_string(index=False))
    print("\nConditional uniqueness statement:\n    If complete EDF closure requires the full ordered operator pair space C(k)=k^2 and Fibonacci compatibility F_k=C(k), then k=12 is the unique nontrivial solution for k>=2.")
    print("\nImportant distinction:\n    k^2 counts the full operator space including the identity direction; k^2-1 counts normalized traceless state coordinates.")
    print(f"\nOutputs written to: {output_dir.resolve()}")

if __name__=="__main__": main()
