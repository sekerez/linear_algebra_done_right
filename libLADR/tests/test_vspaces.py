import pytest

from sympy import Matrix as Vector


##  HELPERS  ###################################################################

def equal_lists(vecs1, vecs2):
    """
    Returns True if the two lists of SymPy vectors are the same, else raises.
    """
    n1 = len(vecs1)
    n2 = len(vecs2)
    assert n1 == n2, "should have same number of elements"
    for i in range(0,n1):
        assert vecs1[i] == vecs2[i], "should have the same elements"
    return True



##  FIXTURES  ##################################################################

@pytest.fixture
def lin_dep_set():
    v1 = Vector([1,2])
    v2 = Vector([2,4])
    vecs1 = [v1, v2]
    return vecs1

@pytest.fixture
def lin_indep_set():
    v3 = Vector([1,2])
    v4 = Vector([2,5])
    vecs2 = [v3, v4]
    return vecs2



################################################################################

# SUT1
from ..vspaces import is_linearly_indepenent


def test_lin_dep_sets(lin_dep_set):
    assert is_linearly_indepenent(lin_dep_set) == False, "should be dependent"


def test_lin_dep_sets_when_includes_zero(lin_indep_set):
    zerovec = Vector([0,0])
    assert is_linearly_indepenent([zerovec]) == False, "zero vec by itself is dependent"
    assert is_linearly_indepenent(lin_indep_set+[zerovec]) == False, "set containing zero vec is dependent"


def test_empty_list_is_lin_indep():
    assert is_linearly_indepenent([]) == True, "by definition"


def test_lin_indep_sets(lin_indep_set):
    assert is_linearly_indepenent(lin_indep_set) == True, "should be independent"




################################################################################

# SUT2
from ..vspaces import reduce_list


def test_reduces_zero_vec():
    zerovec = Vector([0,0])
    reduced_list = reduce_list([zerovec])
    assert len(reduced_list) == 0, "should be empty list"


def test_reduces_dep_set(lin_dep_set):
    assert is_linearly_indepenent(lin_dep_set) == False, "should be dependent"
    reduced_list = reduce_list(lin_dep_set)
    assert len(reduced_list) < len(lin_dep_set), "should have fewer elements"
    assert reduced_list[0] == lin_dep_set[0], "should have the same first elements"


def test_reduces_list_containing_zero(lin_indep_set):
    zerovec = Vector([0,0])
    # Case 0: zero vec first
    zerofirst = [zerovec] + lin_indep_set
    reduced_list = reduce_list(zerofirst)
    assert equal_lists(reduced_list, lin_indep_set), "should reduce to original"
    # Case 1: zero vec in the middle
    zeromiddle = [lin_indep_set[0]] + [zerovec] + lin_indep_set[1:]
    reduced_list = reduce_list(zeromiddle)
    assert equal_lists(reduced_list, lin_indep_set), "should reduce to original"
    # Case m: zero vec at the end
    zerolast = lin_indep_set + [zerovec]
    reduced_list = reduce_list(zerolast)
    assert equal_lists(reduced_list, lin_indep_set), "should reduce to original"


def test_leaves_lin_indep_set_unchanged(lin_indep_set):
    assert is_linearly_indepenent(lin_indep_set) == True, "should be independent"
    reduced_list = reduce_list(lin_indep_set)
    assert equal_lists(reduced_list, lin_indep_set), "should be the same"



################################################################################

# SUT3
from ..vspaces import spanning_set2basis


def test_removes_zero_vec():
    zerovec = Vector([0,0])
    basis = spanning_set2basis([zerovec])
    assert len(basis) == 0, "should be empty list"


def test_on_dep_set(lin_dep_set):
    basis = spanning_set2basis(lin_dep_set)
    assert len(basis) < len(lin_dep_set), "should have fewer elements"
    assert basis[0] == lin_dep_set[0], "should have the same first elements"


def test_removes_zero_vector(lin_indep_set):
    zerovec = Vector([0,0])
    # Case 0: zero vec first
    zerofirst = [zerovec] + lin_indep_set
    basis = spanning_set2basis(zerofirst)
    assert equal_lists(basis, lin_indep_set), "should reduce to original"
    # Case 1: zero vec in the middle
    zeromiddle = [lin_indep_set[0]] + [zerovec] + lin_indep_set[1:]
    basis = spanning_set2basis(zeromiddle)
    assert equal_lists(basis, lin_indep_set), "should reduce to original"
    # Case m: zero vec at the end
    zerolast = lin_indep_set + [zerovec]
    basis = spanning_set2basis(zerolast)
    assert equal_lists(basis, lin_indep_set), "should reduce to original"


def test_lin_indep_set_is_a_basis(lin_indep_set):
    basis = spanning_set2basis(lin_indep_set)
    assert equal_lists(basis, lin_indep_set), "should be the same"

