#!/usr/bin/python

# -*- coding: utf-8 -*-

# For better print formatting
from __future__ import print_function

# Imports
from pycompss.api.parallel import parallel
from pycompss.api.constraint import constraint
from pycompss.api.task import task
from pycompss.api.api import compss_barrier
from pycompss.api.api import compss_wait_on

import numpy as np


############################################
# MATRIX GENERATION
############################################

def initialize_variables(n_size):
    h = create_matrix(n_size)
    e = create_matrix(n_size)

    return h, e


def create_matrix(n_size):
    mat = []
    for i in range(n_size):
        mb = create_entry(i, n_size)
        mat.append(mb)
    return mat


@constraint(ComputingUnits="${ComputingUnits}")
@task(returns=1)
def create_entry(index, n_size):
    return np.float(np.float(index) / np.float(n_size))


############################################
# MAIN FUNCTION
############################################

# [COMPSs Autoparallel] Begin Autogenerated code
import math

from pycompss.api.api import compss_barrier, compss_wait_on, compss_open
from pycompss.api.task import task
from pycompss.api.parameter import *


@task(var2=IN, coef1=IN, var3=IN, var4=IN, returns=1)
def S1(var2, coef1, var3, var4):
    return compute_e(var2, coef1, var3, var4)


@task(var2=IN, coef2=IN, var3=IN, var4=IN, returns=1)
def S2(var2, coef2, var3, var4):
    return compute_h(var2, coef2, var3, var4)


def fdtd_1d(e, h, n_size, t_size, coef1, coef2):
    if __debug__:
        e = compss_wait_on(e)
        h = compss_wait_on(h)
        print('Matrix E:')
        print(e)
        print('Matrix H:')
        print(h)
    if __debug__:
        import copy
        e_seq = copy.deepcopy(e)
        h_seq = copy.deepcopy(h)
        h_expected = seq_fdtd_1d(e_seq, h_seq, n_size, t_size, coef1, coef2)
    if n_size >= 2 and t_size >= 1:
        lbp = 1
        ubp = n_size + 2 * t_size - 3
        for t1 in range(1, n_size + 2 * t_size - 3 + 1):
            lbp = max(int(math.ceil(float(t1 + 1) / float(2))), t1 - t_size + 1
                )
            ubp = min(int(math.floor(float(t1 + n_size - 1) / float(2))), t1)
            for t2 in range(lbp, ubp + 1):
                e[-t1 + 2 * t2] = S1(e[-t1 + 2 * t2], coef1, h[-t1 + 2 * t2
                    ], h[-t1 + 2 * t2 - 1])
                h[-t1 + 2 * t2 - 1] = S2(h[-t1 + 2 * t2 - 1], coef2, e[-t1 +
                    2 * t2 - 1 + 1], e[-t1 + 2 * t2 - 1])
    compss_barrier()
    if __debug__:
        h = compss_wait_on(h)
        print('New Matrix H:')
        print(h)
    if __debug__:
        check_result(h, h_expected)

# [COMPSs Autoparallel] End Autogenerated code


############################################
# MATHEMATICAL FUNCTIONS
############################################

def compute_e(e, coef1, h2, h1):
    # import time
    # start = time.time()

    return e - coef1 * (h2 - h1)

    # end = time.time()
    # tm = end - start
    # print "TIME: " + str(tm*1000) + " ms"


def compute_h(h, coef2, e2, e1):
    # import time
    # start = time.time()

    return h - coef2 * (e2 - e1)

    # end = time.time()
    # tm = end - start
    # print "TIME: " + str(tm*1000) + " ms"


############################################
# RESULT CHECK FUNCTIONS
############################################

def seq_fdtd_1d(e, h, n_size, t_size, coef1, coef2):
    for _ in range(t_size):
        for i in range(1, n_size):
            e[i] -= coef1 * (h[i] - h[i - 1])
        for i in range(n_size - 1):
            h[i] -= coef2 * (e[i + 1] - e[i])

    return h


def check_result(result, result_expected):
    is_ok = np.allclose(result, result_expected)
    print("Result check status: " + str(is_ok))

    if not is_ok:
        raise Exception("Result does not match expected result")


############################################
# MAIN
############################################

if __name__ == "__main__":
    # Import libraries
    import time

    # Parse arguments
    import sys

    args = sys.argv[1:]
    NSIZE = int(args[0])
    TSIZE = int(args[1])
    COEF1 = np.float(0.5)
    COEF2 = np.float(0.7)

    # Log arguments if required
    if __debug__:
        print("Running fdtd-1d application with:")
        print(" - NSIZE = " + str(NSIZE))
        print(" - TSIZE = " + str(TSIZE))
        print(" - COEF1 = " + str(COEF1))
        print(" - COEF2 = " + str(COEF2))

    # Initialize matrices
    if __debug__:
        print("Initializing matrices")
    start_time = time.time()
    H, E = initialize_variables(NSIZE)
    compss_barrier()

    # Begin computation
    if __debug__:
        print("Performing computation")
    fdtd_start_time = time.time()
    fdtd_1d(E, H, NSIZE, TSIZE, COEF1, COEF2)
    compss_barrier()
    end_time = time.time()

    # Log results and time
    if __debug__:
        print("Post-process results")
    total_time = end_time - start_time
    init_time = fdtd_start_time - start_time
    fdtd_time = end_time - fdtd_start_time

    print("RESULTS -----------------")
    print("VERSION AUTOPARALLEL")
    print("NSIZE " + str(NSIZE))
    print("TSIZE " + str(TSIZE))
    print("DEBUG " + str(__debug__))
    print("TOTAL_TIME " + str(total_time))
    print("INIT_TIME " + str(init_time))
    print("FDTD_TIME " + str(fdtd_time))
    print("-------------------------")
