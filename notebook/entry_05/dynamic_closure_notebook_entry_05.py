# Dynamic Closure Notebook — Entry 05
# Weyl-Generated Closure Algebra
#
# Purpose: derive the k^2 closure capacity from cyclic phase-and-shift dynamics.

from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

@dataclass
class Config:
    k_min:int=2; k_max:int=24; arithmetic_search_max:int=500
    output_dir:str="dynamic_closure_entry_05_output"

def fibonacci(n):
    if n<0: raise ValueError("Fibonacci index must be non-negative.")
    a,b=0,1
    for _ in range(n): a,b=b,a+b
    return a

def detect_fibonacci_square_closure(k_max):
    return [k for k in range(2,k_max+1) if fibonacci(k)==k*k]

def clock_and_shift(k):
    omega=np.exp(2j*np.pi/k); z=np.diag(np.array([omega**m for m in range(k)],dtype=complex)); x=np.zeros((k,k),dtype=complex)
    for m in range(k): x[(m+1)%k,m]=1.0
    return omega,x,z

def weyl_operator(x,z,a,b,k): return np.linalg.matrix_power(x,a%k)@np.linalg.matrix_power(z,b%k)
def build_weyl_basis(k):
    _,x,z=clock_and_shift(k); return [(a,b,weyl_operator(x,z,a,b,k)) for a in range(k) for b in range(k)]

def analyze_dimension(k):
    omega,x,z=clock_and_shift(k); relation_error=np.linalg.norm(z@x-omega*x@z,ord="fro"); basis=build_weyl_basis(k)
    flattened=np.column_stack([op.reshape(-1) for _,_,op in basis]); rank=int(np.linalg.matrix_rank(flattened)); max_orth=0.0; max_trace=0.0
    for i,(_,_,wi) in enumerate(basis):
        for j,(_,_,wj) in enumerate(basis):
            value=np.trace(wi.conj().T@wj)/k; max_orth=max(max_orth,float(abs(value-(1.0 if i==j else 0.0))))
    for a,b,op in basis:
        if a or b: max_trace=max(max_trace,float(abs(np.trace(op))))
    return {"k":k,"k_squared":k*k,"weyl_basis_count":len(basis),"numerical_span_rank":rank,"weyl_relation_error":float(relation_error),"maximum_orthogonality_error":max_orth,"maximum_nonidentity_trace":max_trace}

def verify_multiplication_law(k):
    omega,x,z=clock_and_shift(k); max_error=0.0
    for a in range(k):
        for b in range(k):
            wab=weyl_operator(x,z,a,b,k)
            for c in range(k):
                for d in range(k):
                    lhs=wab@weyl_operator(x,z,c,d,k); rhs=omega**(b*c)*weyl_operator(x,z,a+c,b+d,k); max_error=max(max_error,float(np.linalg.norm(lhs-rhs,ord="fro")))
    return max_error

def verify_adjoint_law(k):
    omega,x,z=clock_and_shift(k); max_error=0.0
    for a in range(k):
        for b in range(k):
            lhs=weyl_operator(x,z,a,b,k).conj().T; rhs=omega**(a*b)*weyl_operator(x,z,-a,-b,k); max_error=max(max_error,float(np.linalg.norm(lhs-rhs,ord="fro")))
    return max_error

def verify_traceless_nonclosure(k):
    omega,x,z=clock_and_shift(k); identity=np.eye(k,dtype=complex); tested=regenerated=0; max_error=0.0
    for a in range(k):
        for b in range(k):
            if a==0 and b==0: continue
            product=weyl_operator(x,z,a,b,k)@weyl_operator(x,z,-a,-b,k); expected=omega**(-a*b)*identity; error=float(np.linalg.norm(product-expected,ord="fro")); tested+=1; max_error=max(max_error,error); regenerated+=error<1e-10
    return {"k":k,"nonidentity_elements_tested":tested,"products_regenerating_identity":regenerated,"identity_regeneration_fraction":regenerated/tested,"maximum_identity_regeneration_error":max_error}

def verify_off_diagonal_nonclosure(k):
    tested=regenerated=0; max_error=0.0
    for i in range(k):
        for j in range(k):
            if i==j: continue
            eij=np.zeros((k,k),complex); eji=np.zeros((k,k),complex); eii=np.zeros((k,k),complex); eij[i,j]=1; eji[j,i]=1; eii[i,i]=1
            error=float(np.linalg.norm(eij@eji-eii,ord="fro")); tested+=1; max_error=max(max_error,error); regenerated+=error<1e-12
    return {"k":k,"off_diagonal_inverse_pairs_tested":tested,"products_generating_self_relation":regenerated,"self_relation_regeneration_fraction":regenerated/tested,"maximum_matrix_unit_error":max_error}

def make_weyl_lattice_table(k):
    rows=[]
    for a in range(k):
        for b in range(k):
            if a==0 and b==0: category,code="identity",0
            elif a!=0 and b==0: category,code="pure_shift",1
            elif a==0: category,code="pure_phase",2
            else: category,code="mixed_phase_shift",3
            rows.append({"shift_index_a":a,"phase_index_b":b,"category":category,"category_code":code})
    return pd.DataFrame(rows)

def plot_dimension_scaling(diagnostics,output_dir):
    plt.figure(figsize=(9,5)); plt.plot(diagnostics["k"],diagnostics["weyl_basis_count"],marker="o",label="Weyl basis count"); plt.plot(diagnostics["k"],diagnostics["numerical_span_rank"],marker="x",label="Numerical span rank"); plt.plot(diagnostics["k"],diagnostics["k_squared"],linestyle="--",label="k^2"); plt.xlabel("Closure sector count k"); plt.ylabel("Operator-space dimension"); plt.title("Weyl-Generated Operator Dimension"); plt.legend(frameon=False); plt.tight_layout(); plt.savefig(output_dir/"weyl_dimension_scaling.png",dpi=180); plt.close()

def plot_errors(diagnostics,output_dir):
    plt.figure(figsize=(9,5)); plt.semilogy(diagnostics["k"],diagnostics["weyl_relation_error"]+1e-18,marker="o",label="Weyl relation error"); plt.semilogy(diagnostics["k"],diagnostics["maximum_orthogonality_error"]+1e-18,marker="o",label="Orthogonality error"); plt.xlabel("Closure sector count k"); plt.ylabel("Numerical error"); plt.title("Numerical Verification of the Finite Weyl Algebra"); plt.legend(frameon=False); plt.tight_layout(); plt.savefig(output_dir/"weyl_numerical_errors.png",dpi=180); plt.close()

def plot_lattice(lattice,k,output_dir):
    matrix=np.empty((k,k),float)
    for _,row in lattice.iterrows(): matrix[int(row["phase_index_b"]),int(row["shift_index_a"])]=int(row["category_code"])
    plt.figure(figsize=(7,6)); image=plt.imshow(matrix,origin="lower",aspect="equal"); cb=plt.colorbar(image,ticks=[0,1,2,3]); cb.ax.set_yticklabels(["Identity","Pure shift","Pure phase","Mixed"]); plt.xlabel("Shift index a"); plt.ylabel("Phase index b"); plt.title(f"Weyl Closure Lattice for Detected Fibonacci-Square Sector k={k}"); plt.tight_layout(); plt.savefig(output_dir/"detected_closure_weyl_lattice.png",dpi=180); plt.close()

def main():
    config=Config(); output_dir=Path(config.output_dir); output_dir.mkdir(parents=True,exist_ok=True)
    diagnostics=pd.DataFrame([analyze_dimension(k) for k in range(config.k_min,config.k_max+1)]); diagnostics.to_csv(output_dir/"weyl_dimension_diagnostics.csv",index=False)
    traceless=pd.DataFrame([verify_traceless_nonclosure(k) for k in range(config.k_min,config.k_max+1)]); traceless.to_csv(output_dir/"traceless_nonclosure_diagnostics.csv",index=False)
    off=pd.DataFrame([verify_off_diagonal_nonclosure(k) for k in range(config.k_min,config.k_max+1)]); off.to_csv(output_dir/"matrix_unit_nonclosure_diagnostics.csv",index=False)
    solutions=detect_fibonacci_square_closure(config.arithmetic_search_max); pd.DataFrame({"k":solutions,"F_k":[fibonacci(k) for k in solutions],"k_squared":[k*k for k in solutions]}).to_csv(output_dir/"fibonacci_square_closure_scan.csv",index=False)
    pd.DataFrame([{"k":k,"maximum_multiplication_law_error":verify_multiplication_law(k)} for k in range(2,13)]).to_csv(output_dir/"multiplication_closure_diagnostics.csv",index=False)
    pd.DataFrame([{"k":k,"maximum_adjoint_law_error":verify_adjoint_law(k)} for k in range(2,13)]).to_csv(output_dir/"adjoint_closure_diagnostics.csv",index=False)
    plot_dimension_scaling(diagnostics,output_dir); plot_errors(diagnostics,output_dir)
    detected_k=solutions[0] if solutions else None
    if detected_k is not None:
        lattice=make_weyl_lattice_table(detected_k); lattice.to_csv(output_dir/"detected_closure_weyl_lattice.csv",index=False); plot_lattice(lattice,detected_k,output_dir)
    dimension_verified=bool(np.all(diagnostics["weyl_basis_count"]==diagnostics["k_squared"]) and np.all(diagnostics["numerical_span_rank"]==diagnostics["k_squared"]))
    traceless_verified=bool(np.allclose(traceless["identity_regeneration_fraction"],1.0)); off_verified=bool(np.allclose(off["self_relation_regeneration_fraction"],1.0))
    print("\nDynamic Closure Notebook — Entry 05\nWeyl-Generated Closure Algebra\n"+"-"*50)
    print(f"\nWeyl basis dimension k^2 verified for k={config.k_min},...,{config.k_max}: {dimension_verified}")
    print(f"\nTraceless k^2-1 sector fails multiplicative closure for every inverse pair: {traceless_verified}")
    print(f"\nOff-diagonal matrix-unit sector regenerates self-relations E_ii for every inverse pair: {off_verified}")
    print(f"\nComputational solutions of F_k = k^2 for 2 <= k <= {config.arithmetic_search_max}: {solutions}")
    print("\nConditional algebraic conclusion:\n    Cyclic phase + cyclic shift + unital associative composition closure => M_k(C), dimension k^2.")
    print("\nCombined with Entry 04:\n    F_k = k^2 => unique nontrivial closure k = 12 using the published Fibonacci perfect-power theorem.")

if __name__=="__main__": main()
