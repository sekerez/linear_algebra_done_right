from sympy import Add
from sympy import Matrix as Vector
from sympy import solve
from sympy import symbols




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
    #print(sol)
    if sol == [] or not any(sol.values()):
        return True
    else:
        return False


    
# 2.21 Linear Dependence Lemma
# Suppose vecs = [v_1, v_2, ..., v_m] is a linearly dependent list in V.
# Then there exists j in [1, 2, ..., m] such that the following hold:
# (a) vj in span(v_1, v_2, ..., v_(j-1))
# (b) if the jth term is removed from [v_1, v_2, ..., v_m],
#     the span of the remaining list equals span(v_1, v_2, ..., v_m)

def reduce_list(vecs):
    """
    Remove the first vector that can be written as a linear combination
    of the preceding vectors in a list of linearly dependent vectors.
    """
    m = len(vecs)
    alphas = symbols("\\alpha_" + str(1) + ":" + str(m+1))

    for j in range(0, m):
        vj = vecs[j]
        print("\nChecking if vector j =", j, vj, "is redundant")
        
        if j == 0 and vj.is_zero_matrix:
            return vecs[1:]

        alphas_until_jminus1 = alphas[0:j]
        vecs_until_jminus1 = vecs[0:j]
        alphavecs_until_jminus1 = [
            alpha*vec for alpha, vec
            in zip(alphas_until_jminus1, vecs_until_jminus1)
        ]
        if alphavecs_until_jminus1:
            lin_comb = Add(*alphavecs_until_jminus1)
            expr = vj - lin_comb
        else:
            expr = vj

        sol = solve(expr, alphas_until_jminus1)
        print("  sol =", sol)
        if sol == []:
            print("  no solution, so keeping vj")
            continue
        else:
            print("  found solution, so vj is can be dropped")
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
        vecs = reduce_list(vecs)
    return vecs
