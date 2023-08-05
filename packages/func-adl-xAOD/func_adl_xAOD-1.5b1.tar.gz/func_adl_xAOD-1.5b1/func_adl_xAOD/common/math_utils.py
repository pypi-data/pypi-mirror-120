# Some math utilities
import ast
from typing import Callable, Dict
import func_adl_xAOD.common.cpp_ast as cpp_ast


DeltaRSpec = cpp_ast.CPPCodeSpecification(
    'DeltaR',
    ['TVector2.h', 'math.h'],
    ['eta1', 'phi1', 'eta2', 'phi2'],
    [
        'auto d_eta = eta1 - eta2;',
        'auto d_phi = TVector2::Phi_mpi_pi(phi1-phi2);',
        'auto result = sqrt(d_eta*d_eta + d_phi*d_phi);'
    ],
    'result',
    'double'
)


# def DeltaRAst(call_node):
#     r'''
#     User is trying to call DeltaR (eta1, phi1, eta2, phi2). We turn this into a call
#     into a call into ROOT that does the phi subtraction (I can never get that crap right).
#     '''

#     if len(call_node.args) != 4:
#         raise ValueError("Calling DeltaR(eta1, phi1, eta2, phi2) has incorrect number of arguments")

#     # Create an AST to hold onto all of this.
#     r = cpp_ast.CPPCodeValue()
#     # We need TVector2 included here
#     r.include_files += ['TVector2.h', 'math.h']

#     # We need all four arguments pushed through.
#     r.args = ['eta1', 'phi1', 'eta2', 'phi2']

#     # The code is three steps
#     r.running_code += ['auto d_eta = eta1 - eta2;']
#     r.running_code += ['auto d_phi = TVector2::Phi_mpi_pi(phi1-phi2);']
#     r.running_code += ['auto result = sqrt(d_eta*d_eta + d_phi*d_phi);']
#     r.result = 'result'
#     r.result_rep = lambda scope: cpp_variable(unique_name('delta_r'), scope=scope, cpp_type='double')

#     call_node.func = r
#     return call_node


def DeltaR(eta1, phi1, eta2, phi2):
    'Calculate the DeltaR between two eta,phi specified vectors'
    raise NotImplementedError('DeltaR should never be called in python!')


def get_math_methods() -> Dict[str, Callable[[ast.Call], ast.Call]]:
    return {
        'DeltaR': lambda call_node: cpp_ast.build_CPPCodeValue(DeltaRSpec, call_node)
    }
