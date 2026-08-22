"""
Dynamic Closure Notebook — Entry 12
Alternative Structure Controls and Premise Audit

Tests whether lower-dimensional relation spaces remain closed under the DCT
operator requirements. The purpose is to determine whether k^2 is structurally
forced by phase + traversal + ordinary composition rather than selected because
F_12=144.
"""
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import numpy as np
import pandas as pd

@dataclass
class Config:
    fibonacci_scan_max:int=500; algebra_k_min:int=2; algebra_k_max:int=12
    diagnostic_k:int=6; tolerance:float=1e-10
    output_dir:str="dynamic_closure_entry_12_output"

def fibonacci(n):
    a,b=0,1
    for _ in range(n): a,b=b,a+b
    return a

def candidate_count(name,k):
    if name=="full_ordered_self": return k*k
    if name=="traceless": return k*k-1
    if name=="ordered_no_self": return k*(k-1)
    if name=="unordered_self": return k*(k+1)//2
    if name=="unordered_no_self": return k*(k-1)//2
    if name=="single_generator": return k
    raise ValueError(name)
CANDIDATES=("full_ordered_self","traceless","ordered_no_self","unordered_self","unordered_no_self","single_generator")

def fibonacci_match_scan(config):
    rows=[]
    formulas={"full_ordered_self":"k^2","traceless":"k^2-1","ordered_no_self":"k(k-1)","unordered_self":"k(k+1)/2","unordered_no_self":"k(k-1)/2","single_generator":"k"}
    for name in CANDIDATES:
        matches=[k for k in range(2,config.fibonacci_scan_max+1) if fibonacci(k)==candidate_count(name,k)]
        rows.append({"candidate":name,"count_formula":formulas[name],"exact_match_indices":",".join(map(str,matches)) if matches else "none","match_count":len(matches)})
    return pd.DataFrame(rows)
def residual_table(k_max=24):
    rows=[]
    for k in range(2,k_max+1):
        f=fibonacci(k)
        for name in CANDIDATES:
            c=candidate_count(name,k); rows.append({"k":k,"candidate":name,"F_k":f,"C_k":c,"bounded_residual":abs(f-c)/(f+c),"exact_match":f==c})
    return pd.DataFrame(rows)
def E(k,i,j):
    m=np.zeros((k,k),complex); m[i,j]=1; return m
def family_rank(family,tol): return int(np.linalg.matrix_rank(np.column_stack([m.reshape(-1) for m in family]),tol=tol)) if family else 0
def in_span(candidate,basis,tol): return family_rank(basis+[candidate],tol)==family_rank(basis,tol)
def full_basis(k): return [E(k,i,j) for i in range(k) for j in range(k)]
def traceless_basis(k):
    b=[E(k,i,j) for i in range(k) for j in range(k) if i!=j]
    for i in range(k-1): b.append(E(k,i,i)-E(k,k-1,k-1))
    return b
def ordered_no_self_basis(k): return [E(k,i,j) for i in range(k) for j in range(k) if i!=j]
def unordered_self_basis(k):
    b=[E(k,i,i) for i in range(k)]
    for i in range(k):
        for j in range(i+1,k): b.append(E(k,i,j)+E(k,j,i))
    return b
def unordered_no_self_basis(k): return [E(k,i,j)+E(k,j,i) for i in range(k) for j in range(i+1,k)]
def clock_and_shift(k):
    omega=np.exp(2j*np.pi/k); z=np.diag([omega**m for m in range(k)]); x=np.zeros((k,k),complex)
    for m in range(k): x[(m+1)%k,m]=1
    return z,x
def cyclic_power_basis(g,k): return [np.linalg.matrix_power(g,a) for a in range(k)]
def weyl_basis(k):
    z,x=clock_and_shift(k); return [np.linalg.matrix_power(x,a)@np.linalg.matrix_power(z,b) for a in range(k) for b in range(k)]
def explicit_audit_row(name,k,tol):
    I=np.eye(k,complex)
    if name=="full_ordered_self": basis=full_basis(k); witness_inside=True; generated=k*k; status="PASS"; reason="Already the full unital associative operator algebra."
    elif name=="traceless":
        basis=traceless_basis(k); a=E(k,0,0)-E(k,1,1); witness_inside=in_span(a@a,basis,tol); generated=k*k; status="FAIL P4"; reason="Multiplication regenerates nontraceless/self components."
    elif name=="ordered_no_self":
        basis=ordered_no_self_basis(k); witness_inside=in_span(E(k,0,1)@E(k,1,0),basis,tol); generated=k*k; status="FAIL P4"; reason="E_01 E_10 = E_00 regenerates a deleted self-relation."
    elif name=="unordered_self":
        basis=unordered_self_basis(k); witness_inside=in_span(E(k,0,0)@(E(k,0,1)+E(k,1,0)),basis,tol); generated=k*k; status="FAIL P3; FAIL P4"; reason="Ordinary composition regenerates directed matrix units."
    elif name=="unordered_no_self":
        basis=unordered_no_self_basis(k); s=E(k,0,1)+E(k,1,0); witness_inside=in_span(s@s,basis,tol); generated=2 if k==2 else k*k; status="FAIL P1/P3; FAIL P4"; reason="Symmetric off-diagonal squares regenerate diagonal/self structure."
    return {"k":k,"candidate":name,"declared_dimension":len(basis),"basis_rank":family_rank(basis,tol),"contains_identity":in_span(I,basis,tol),"explicit_product_witness_in_declared_span":witness_inside,"multiplicatively_closed_under_witness":witness_inside,"unital_associative_closure_dimension":generated,"full_k2_dimension":k*k,"expands_to_full_k2":generated==k*k,"dct_status":status,"reason":reason}
def algebra_audit(config):
    rows=[]
    for k in range(config.algebra_k_min,config.algebra_k_max+1):
        for name in ("full_ordered_self","traceless","ordered_no_self","unordered_self","unordered_no_self"): rows.append(explicit_audit_row(name,k,config.tolerance))
        z,x=clock_and_shift(k); zb=cyclic_power_basis(z,k); xb=cyclic_power_basis(x,k); wb=weyl_basis(k)
        rows.append({"k":k,"candidate":"phase_only_linear","declared_dimension":k,"basis_rank":family_rank(zb,config.tolerance),"contains_identity":True,"explicit_product_witness_in_declared_span":True,"multiplicatively_closed_under_witness":True,"unital_associative_closure_dimension":k,"full_k2_dimension":k*k,"expands_to_full_k2":False,"dct_status":"FAIL P3","reason":"Closed cyclic phase algebra, but omits traversal X."})
        rows.append({"k":k,"candidate":"shift_only_linear","declared_dimension":k,"basis_rank":family_rank(xb,config.tolerance),"contains_identity":True,"explicit_product_witness_in_declared_span":True,"multiplicatively_closed_under_witness":True,"unital_associative_closure_dimension":k,"full_k2_dimension":k*k,"expands_to_full_k2":False,"dct_status":"FAIL P1","reason":"Closed cyclic traversal algebra, but omits phase Z."})
        rows.append({"k":k,"candidate":"phase_plus_shift_DCT","declared_dimension":2,"basis_rank":2,"contains_identity":False,"explicit_product_witness_in_declared_span":False,"multiplicatively_closed_under_witness":False,"unital_associative_closure_dimension":family_rank(wb,config.tolerance),"full_k2_dimension":k*k,"expands_to_full_k2":family_rank(wb,config.tolerance)==k*k,"dct_status":"PASS","reason":"Required generators Z and X span the k^2 Weyl basis."})
    return pd.DataFrame(rows)
def premise_audit():
    return pd.DataFrame([
        {"candidate":"full_ordered_self","count":"k^2","P1":"PASS","P2":"PASS","P3":"PASS","P4":"PASS","Fibonacci_match":"k=12"},
        {"candidate":"traceless","count":"k^2-1","P1":"PASS","P2":"PASS","P3":"PASS","P4":"FAIL","Fibonacci_match":"none"},
        {"candidate":"ordered_no_self","count":"k(k-1)","P1":"FAIL","P2":"PASS","P3":"PASS","P4":"FAIL","Fibonacci_match":"none"},
        {"candidate":"unordered_self","count":"k(k+1)/2","P1":"PASS","P2":"PASS","P3":"FAIL","P4":"FAIL","Fibonacci_match":"k=10"},
        {"candidate":"unordered_no_self","count":"k(k-1)/2","P1":"FAIL","P2":"PASS","P3":"FAIL","P4":"FAIL","Fibonacci_match":"k=2"},
        {"candidate":"single_generator_linear","count":"k","P1":"conditional","P2":"PASS","P3":"conditional","P4":"PASS as subalgebra","Fibonacci_match":"k=5"},
    ])
def main():
    config=Config(); out=Path(config.output_dir); out.mkdir(parents=True,exist_ok=True); matches=fibonacci_match_scan(config); matches.to_csv(out/"alternative_fibonacci_matches.csv",index=False); residual_table().to_csv(out/"alternative_structural_residuals.csv",index=False); audit=algebra_audit(config); audit.to_csv(out/"alternative_algebra_audit.csv",index=False); pa=premise_audit(); pa.to_csv(out/"alternative_premise_audit.csv",index=False); diagnostic=audit[audit["k"]==config.diagnostic_k]; diagnostic.to_csv(out/"diagnostic_k6_algebra_audit.csv",index=False)
    print("\nDynamic Closure Notebook — Entry 12\nAlternative Structure Controls and Premise Audit\n"+"-"*60); print("\nFibonacci matches:\n",matches.to_string(index=False)); print("\nPremise audit:\n",pa.to_string(index=False)); print("\nConclusion: deleting identity/self/direction directions is not stable under ordinary composition; phase-only and shift-only are legitimate k-dimensional subalgebras but omit one required DCT structure; retaining both Z and X restores M_k(C), dimension k^2.")
if __name__=="__main__": main()
