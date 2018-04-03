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


############################################
# MATRIX GENERATION
############################################

def initialize_variables(n_size):
    a = create_matrix(n_size, False)
    b = create_matrix(n_size, True)

    return a, b


def create_matrix(n_size, is_zero):
    mat = []
    for i in range(n_size):
        mb = create_entry(i, n_size, is_zero)
        mat.append(mb)

    return mat


@constraint(ComputingUnits="${ComputingUnits}")
@task(returns=1)
def create_entry(index, n_size, is_zero):
    if is_zero:
        return float(0)
    else:
        return float(index) / float(n_size)


############################################
# MAIN FUNCTION
############################################

# [COMPSs Autoparallel] Begin Autogenerated code
import math

from pycompss.api.api import compss_barrier, compss_wait_on, compss_open
from pycompss.api.task import task
from pycompss.api.parameter import *


@task(coef=IN, var2=IN, var3=IN, var4=IN, returns=1)
def S1(coef, var2, var3, var4):
    return compute_b(coef, var2, var3, var4)


@task(var2=IN, returns=1)
def S2(var2):
    return copy(var2)


def jacobi_1d(a, b, n_size, t_size, coef):
    if __debug__:
        print('Matrix A:')
        print(a)
        print('Matrix B:')
        print(b)
    if n_size >= 4 and t_size >= 1:
        lbp = 2
        ubp = n_size + 2 * t_size - 4
        for t1 in range(2, n_size + 2 * t_size - 4 + 1):
            lbp = max(int(math.ceil(float(t1 + 2) / float(2))), t1 - t_size + 1
                )
            ubp = min(int(math.floor(float(t1 + n_size - 2) / float(2))), t1)
            for t2 in range(lbp, ubp + 1):
                b[-t1 + 2 * t2] = S1(coef, a[-t1 + 2 * t2 - 1], a[-t1 + 2 *
                    t2], a[-t1 + 2 * t2 + 1])
                a[-t1 + 2 * t2] = S2(b[-t1 + 2 * t2])
    compss_barrier()
    if __debug__:
        print('New Matrix A:')
        a = compss_wait_on(a)
        print(a)
        print('New Matrix B:')
        b = compss_wait_on(b)
        print(b)

# [COMPSs Autoparallel] End Autogenerated code


############################################
# MATHEMATICAL FUNCTIONS
############################################

def compute_b(coef, a_left, a_center, a_right):
    # import time
    # start = time.time()

    return coef * (a_left + a_center + a_right)

    # end = time.time()
    # tm = end - start
    # print "TIME: " + str(tm*1000) + " ms"


def copy(b):
    return b


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
    COEF = float(1) / float(3)

    # Log arguments if required
    if __debug__:
        print("Running jacobi-1d application with:")
        print(" - NSIZE = " + str(NSIZE))
        print(" - TSIZE = " + str(TSIZE))

    # Initialize matrices
    if __debug__:
        print("Initializing matrices")
    start_time = time.time()
    A, B = initialize_variables(NSIZE)
    compss_barrier()

    # Begin computation
    if __debug__:
        print("Performing computation")
    jacobi_start_time = time.time()
    jacobi_1d(A, B, NSIZE, TSIZE, COEF)
    compss_barrier()
    end_time = time.time()

    # Log results and time
    if __debug__:
        print("Post-process results")
    total_time = end_time - start_time
    init_time = jacobi_start_time - start_time
    jacobi_time = end_time - jacobi_start_time

    print("RESULTS -----------------")
    print("VERSION AUTOPARALLEL")
    print("NSIZE " + str(NSIZE))
    print("TSIZE " + str(TSIZE))
    print("DEBUG " + str(__debug__))
    print("TOTAL_TIME " + str(total_time))
    print("INIT_TIME " + str(init_time))
    print("JACOBI_TIME " + str(jacobi_time))
    print("-------------------------")
