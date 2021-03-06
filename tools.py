import numpy as np
from math import factorial, fabs
from itertools import combinations

_CONST_EPSILON = 0.00001
EPSILON = _CONST_EPSILON


def set_epsilon(new_epsilon):
    if 0 <= new_epsilon <= 0.1:
        global EPSILON
        EPSILON = new_epsilon
    # End if
# End set_epsilon()


def reset_epsilon():
    global EPSILON
    EPSILON = _CONST_EPSILON
# reset_epsilon()


def get_index(arr, elem):
    """ Return index of elem in arr """
    index = -1
    for a in arr:
        index += 1
        if a == elem:
            return index
        # End if
    # End for
    return index
# get_index()


def init_x():
    """ Read file 'x.txt' and generate reference vector x """
    x = np.genfromtxt("resources/x.txt", delimiter=' ', dtype=np.float)
    if is_not_valid(x):
        print("Reference vector x is not valid")
        return None
    # End if
    return x
# init_x()


def is_not_valid(vector):
    """
    Checking: vector >= 0
    Return negative indexes
    """
    return list(filter(lambda i: vector[i] < -EPSILON, range(len(vector))))
# is_not_valid()


def is_positive(vector):
    """ Checking: vector > 0 """
    return any(vector > EPSILON)
# is_positive()


def get_indexes(x):
    """ Return indexes N_+ and N_0 """
    N_plus = list(filter(lambda i: x[i] > EPSILON, range(len(x))))
    N_zero = list(set(range(len(x))) - set(N_plus))

    assert (len(N_plus) + len(N_zero) == len(x))
    return N_plus, N_zero
# get_indexes()


def get_bases_matrix(A, N_plus, N_zero):
    """ Return matrix of bases A and indexes N_k, L_k, added_indexes """
    bases_matrix = None
    added_indexes = None
    N_k = None
    L_k = None

    num_free_indexes = len(A) - len(N_plus)
    index_comb = combinations(N_zero, num_free_indexes)
    # order = 0
    for indexes in index_comb:
        # order += 1
        indexes = list(indexes)
        N_k = list(N_plus + indexes)

        if fabs(np.linalg.det(A[:, N_k])) > EPSILON:
            bases_matrix = np.array(A[:, N_k])
            L_k = list(set(N_zero) - set(indexes))
            added_indexes = indexes
            break
        # End if
    # End for

    return bases_matrix, N_k, L_k, added_indexes  # index_comb, order
# get_bases_matrix()


def get_tetha(u, x, N_k):
    """ Return tetha for simplex method and its index """
    u_positive_indexes = list(filter(lambda k: u[k] > EPSILON, N_k))
    tethas = list(map(lambda k: x[k] / u[k], u_positive_indexes))
    tetha = min(tethas)
    index = tethas.index(tetha)

    return tetha, u_positive_indexes[index]
# get_tetha()


def change_bases(bases_matrix, A, N_k, L_k, added_indexes):
    """ Change bases of bases_matrix """
    new_bases_matrix = np.array(bases_matrix)
    new_N_k = list(N_k)
    new_L_k = list(L_k)
    new_added_indexes = list(added_indexes)

    start_pos = len(N_k) - len(added_indexes)
    # print(start_pos)
    # print(N_k, L_k)
    for j in range(len(added_indexes)):
        counter = 0
        for i in L_k:
            new_bases_matrix[:, start_pos + j] = A[:, i]

            if fabs(np.linalg.det(new_bases_matrix)) > EPSILON:
                new_N_k[start_pos + j] = i
                new_L_k[counter] = added_indexes[j]
                new_added_indexes[j] = i

                return new_bases_matrix, new_N_k, new_L_k, new_added_indexes
            # End if
            counter += 1
        # End for

        new_bases_matrix[:, j] = bases_matrix[:, j]
    # End for
    return new_bases_matrix, new_N_k, new_L_k, new_added_indexes
# change_bases()
