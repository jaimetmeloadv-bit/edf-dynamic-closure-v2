"""
Dynamic Closure Notebook — Entry 08
Consolidation of the Dynamic Closure Theorem (DCT)

This entry introduces no new physical mechanism. It consolidates Entries 04–07:

    Delta_phi = 2*pi*r/k
    primitive recurrence <=> gcd(k,r)=1
    U_r = X^r
    alg(U_r,Z) = M_k(C)
    C(k)=k^2
    Fibonacci compatibility F_k=C(k)
    => F_k=k^2
    => unique nontrivial k=12.

The code is an implementation certificate; it does not replace the proofs.
"""
from __future__ import annotations
from dataclasses import dataclass
from math import gcd
from pathlib import Path
import numpy as np
import pandas as pd

@dataclass
class Config:
    exact_k_min:int=2; exact_k_max:int=72
    operator_k_min:int=2; operator_k_max:int=16
    fibonacci_scan_max:int=500; diagnostic_k:int=12
    output_dir:str="dynamic_closure_entry_08_output"

def fibonacci(n):
    a,b=0,1
    for _ in range(n): a,b=b,a+b
    return a

def extended_gcd(a,b):
    old_r,r=a,b; old_s,s=1,0; old_t,t=0,1
    while r:
        q=old_r//r; old_r,r=r,old_r-q*r; old_s,s=s,old_s-q*s; old_t,t=t,old_t-q*t
    return old_r,old_s,old_t

def modular_inverse(r,k):
    g,s,_=extended_gcd(r,k)
    if g!=1: raise ValueError("r has no modular inverse modulo k")
    return s%k

def euler_totient(k): return sum(1 for r in range(1,k) if gcd(k,r)==1)
def orbit_length(k,r): return k//gcd(k,r)

def clock_and_shift(k):
    omega=np.exp(2j*np.pi/k); x=np.zeros((k,k),complex)
    for m in range(k): x[(m+1)%k,m]=1
    z=np.diag([omega**m for m in range(k)]); return omega,x,z

def traversal_operator(k,r):
    _,x,_=clock_and_shift(k); return np.linalg.matrix_power(x,r%k)
def matrix_span_rank(matrices): return int(np.linalg.matrix_rank(np.column_stack([m.reshape(-1) for m in matrices])))
def phase_traversal_basis(k,r):
    _,_,z=clock_and_shift(k); u=traversal_operator(k,r)
    return [np.linalg.matrix_power(u,a)@np.linalg.matrix_power(z,b) for a in range(k) for b in range(k)]

def build_exact_traversal_certificate(config):
    rows=[]
    for k in range(config.exact_k_min,config.exact_k_max+1):
        for r in range(1,k):
            g=gcd(k,r); length=orbit_length(k,r); transitive=g==1
            s=modular_inverse(r,k) if transitive else None
            rows.append({"k":k,"r":r,"gcd_k_r":g,"orbit_length":length,"primitive_recurrence":length==k,"transitive_full_cycle":transitive,"modular_inverse_s":s,"r_times_s_mod_k":((r*s)%k if transitive else None),"U_power_recovers_X":(((r*s)%k)==1 if transitive else False)})
    return pd.DataFrame(rows)

def build_totient_certificate(config,traversal):
    rows=[]
    for k in range(config.exact_k_min,config.exact_k_max+1):
        measured=int(traversal[traversal["k"]==k]["transitive_full_cycle"].sum()); expected=euler_totient(k)
        rows.append({"k":k,"measured_primitive_generators":measured,"euler_totient_phi_k":expected,"exact_agreement":measured==expected})
    return pd.DataFrame(rows)

def operator_diagnostics_for_k(k):
    omega,x,z=clock_and_shift(k); primitive=[r for r in range(1,k) if gcd(k,r)==1]
    max_weyl=max_recovery=max_orth=0.0; min_rank=k*k
    for r in primitive:
        u=traversal_operator(k,r); s=modular_inverse(r,k); max_weyl=max(max_weyl,float(np.linalg.norm(z@u-(omega**r)*u@z,ord="fro"))); max_recovery=max(max_recovery,float(np.linalg.norm(np.linalg.matrix_power(u,s)-x,ord="fro"))); basis=phase_traversal_basis(k,r); min_rank=min(min_rank,matrix_span_rank(basis))
        for i,op in enumerate(basis):
            max_orth=max(max_orth,float(abs(np.trace(op.conj().T@op)/k-1)))
            if i+1<len(basis): max_orth=max(max_orth,float(abs(np.trace(op.conj().T@basis[i+1])/k)))
    return {"k":k,"primitive_generator_count":len(primitive),"euler_totient_phi_k":euler_totient(k),"minimum_phase_traversal_span_rank":min_rank,"expected_full_operator_dimension":k*k,"maximum_Weyl_relation_error":max_weyl,"maximum_U_inverse_power_recovers_X_error":max_recovery,"maximum_sampled_HS_orthogonality_error":max_orth}

def build_operator_certificate(config): return pd.DataFrame([operator_diagnostics_for_k(k) for k in range(config.operator_k_min,config.operator_k_max+1)])
def build_fibonacci_certificate(config): return pd.DataFrame([{"k":k,"F_k":fibonacci(k),"k_squared":k*k,"exact_match":fibonacci(k)==k*k} for k in range(2,config.fibonacci_scan_max+1)])
def published_perfect_power_certificate():
    return pd.DataFrame([{"k":k,"F_k":fibonacci(k),"k_squared":k*k,"F_k_equals_k_squared":fibonacci(k)==k*k} for k in [0,1,2,6,12]])

def premise_registry():
    return pd.DataFrame([
        {"premise":"P1","statement":"finite cyclic phase resolution","status":"EDF structural premise"},
        {"premise":"P2","statement":"homogeneous coherent phase evolution","status":"EDF structural premise"},
        {"premise":"P3","statement":"primitive recurrence order k","status":"EDF structural premise"},
        {"premise":"P4","statement":"operator composition closure","status":"EDF structural premise"},
        {"premise":"FC","statement":"Fibonacci compatibility F_k=C(k)","status":"separate EDF compatibility condition"},
    ])

def main():
    config=Config(); out=Path(config.output_dir); out.mkdir(parents=True,exist_ok=True)
    traversal=build_exact_traversal_certificate(config); traversal.to_csv(out/"exact_traversal_certificate.csv",index=False)
    totient=build_totient_certificate(config,traversal); totient.to_csv(out/"totient_certificate.csv",index=False)
    operator=build_operator_certificate(config); operator.to_csv(out/"operator_theorem_certificate.csv",index=False)
    fib=build_fibonacci_certificate(config); fib.to_csv(out/"fibonacci_square_scan.csv",index=False)
    pub=published_perfect_power_certificate(); pub.to_csv(out/"published_perfect_power_certificate.csv",index=False)
    premise_registry().to_csv(out/"premise_registry.csv",index=False)
    diagnostic=traversal[traversal["k"]==config.diagnostic_k].copy(); diagnostic.to_csv(out/"diagnostic_k12_primitive_generators.csv",index=False)
    exact_k=fib.loc[fib["exact_match"],"k"].tolist()
    traversal_ok=bool(np.all(traversal.loc[traversal["transitive_full_cycle"],"U_power_recovers_X"]))
    totient_ok=bool(np.all(totient["exact_agreement"])); operator_ok=bool(np.all(operator["minimum_phase_traversal_span_rank"]==operator["expected_full_operator_dimension"]))
    print("\nDynamic Closure Notebook — Entry 08\nDynamic Closure Theorem consolidation\n"+"-"*58)
    print(f"\nPrimitive traversal certificate: {traversal_ok}\nEuler-totient certificate: {totient_ok}\nFull M_k(C) operator dimension certificate: {operator_ok}")
    print(f"\nExact computational solutions of F_k=k^2 for 2<=k<={config.fibonacci_scan_max}: {exact_k}")
    print("\nDCT chain:\n    finite phase kernel -> Delta_phi=2*pi*r/k\n    primitive recurrence -> gcd(k,r)=1 -> U_r=X^r\n    phase + traversal -> M_k(C), C(k)=k^2\n    FC: F_k=C(k) -> F_k=k^2\n    published perfect-power theorem -> k=12")

if __name__=="__main__": main()
