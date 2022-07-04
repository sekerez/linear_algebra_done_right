from sympy import Add
from sympy import Matrix as Vector
from sympy import solve
from sympy import symbols



# Helper methods for interpeting the rsults of `solve` for linear combinations.

def no_solution(sol):
    """
    SymPy solve returns [] when there is no solution to given equation.
    """
    if sol == []:
        return True
    else:
        return False


def all_zeros(sol):
    """
    Returns True if the solution is the all zeros solution.
    """
    if no_solution(sol):
        return False
    values = sol.values()
    all_zero_values = not any(values)
    if all_zero_values:
        return True
    else:
        return False



# 2.17 Definition linearly independent
# A list vecs = [v_1, v_2, ..., v_m] of vectors in V is called
# linearly independent if the only solution to the equation
# a_1*v_1 + a_2*v_2 + ... + a_m*v_n = 0 is [0, 0, ..., 0].

def is_linearly_indepenent(vecs):
    """
    Check if the list of vectors `vecs` is linearly indepenent.
    """
    for vec in vecs:
        if vec.is_zero_matrix:
            return False
    n = len(vecs)
    alphas = symbols("\\alpha_" + str(1) + ":" + str(n+1))
    lin_comb = Add(*[alpha*vec for alpha, vec in zip(alphas,vecs)])
    sol = solve(lin_comb, alphas)
    if no_solution(sol) or all_zeros(sol):
        return True
    else:
        return False


def is_in_span(vec, vecs):
    """
    Returns True if vector `vec` is in the span of vectors `vecs`.
    """
    # special handling of case when list of vectors is the empty list []
    if len(vecs) == 0:
        if vec.is_zero_matrix:
            return True
        else:
            return False

    # we want to solve the equation   vec = a1*v1 + a2*v2 + ... + an*vn
    # which is equivalent to the equation vec - a1*v1 - a2*v2 - ... - an*vn = 0.
    n = len(vecs)
    alphas = symbols("\\alpha_" + str(1) + ":" + str(n+1))
    alphavecs = [ alpha*vec for alpha, vec in zip(alphas, vecs) ]
    lin_comb = Add(*alphavecs)
    sol = solve(vec - lin_comb, alphas)
    if no_solution(sol):
        return False  # no solution, so `vec` is not in the span of `vecs`
    elif all_zeros(sol):
        # trivial solution exists, which means `vec` is the zero vector
        return True   # by convention, zero vec is in span of any set of vecs
    else:
        return True   # a solution exists, so vec must be in the span of `vecs`


    
# 2.21 Linear Dependence Lemma
# Suppose vecs = [v_1, v_2, ..., v_m] is a linearly dependent list in V.
# Then there exists j in [1, 2, ..., m] such that the following hold:
# (a) vj in span(v_1, v_2, ..., v_(j-1))
# (b) if the jth term is removed from [v_1, v_2, ..., v_m],
#     the span of the remaining list equals span(v_1, v_2, ..., v_m)

def reduce_list_of_dep_vectors(vecs):
    """
    Remove the first vector that can be written as a linear combination
    of the preceding vectors in a list of linearly dependent vectors.
    """
    m = len(vecs)
    for j in range(0, m):
        vj = vecs[j]
        if is_in_span(vj, vecs[0:j]):
            reduced_vecs = vecs[0:j] + vecs[j+1:]
            return reduced_vecs
    return vecs



# 2.31 Spanning list contains a basis
# Every spanning list in a vector space can be reduced
# to a basis of the vector space.

def spanning_set2basis(vecs):
    """
    Reduce the spanning set of vectors `vecs` to a basis.
    """
    while not is_linearly_indepenent(vecs):
        vecs = reduce_list_of_dep_vectors(vecs)
    return vecs


