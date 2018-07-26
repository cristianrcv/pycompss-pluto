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
    a = create_matrix(n_size, 2)
    b = create_matrix(n_size, 3)

    return a, b


def create_matrix(n_size, offset):
    mat = []
    for i in range(n_size):
        mat.append([])
        for j in range(n_size):
            mb = create_entry(i, j, n_size, offset)
            mat[i].append(mb)

    return mat


@constraint(ComputingUnits="${ComputingUnits}")
@task(returns=1)
def create_entry(i, j, n_size, offset):
    return np.float64(np.float64(i * (j + offset) + offset) / np.float64(n_size))


############################################
# MAIN FUNCTION
############################################

# @parallel(pluto_extra_flags=["--tile"], taskify_loop_level=3)
# [COMPSs Autoparallel] Begin Autogenerated code
import math

from pycompss.api.api import compss_barrier, compss_wait_on, compss_open
from pycompss.api.task import task
from pycompss.api.parameter import *


@task(coef=IN, var2=IN, var3=IN, var4=IN, var5=IN, var6=IN, returns=1)
def S1(coef, var2, var3, var4, var5, var6):
    return compute(coef, var2, var3, var4, var5, var6)


@task(coef=IN, var2=IN, var3=IN, var4=IN, var5=IN, var6=IN, returns=1)
def S2(coef, var2, var3, var4, var5, var6):
    return compute(coef, var2, var3, var4, var5, var6)


def jacobi_2d(a, b, n_size, t_size, coef):
    if __debug__:
        a = compss_wait_on(a)
        b = compss_wait_on(b)
        print('Matrix A:')
        print(a)
        print('Matrix B:')
        print(b)
    if __debug__:
        import copy
        a_seq = copy.deepcopy(a)
        b_seq = copy.deepcopy(b)
        a_expected, b_expected = seq_jacobi_2d(a_seq, b_seq, n_size, t_size, coef)
    if n_size >= 3 and t_size >= 1:
        lbp = 1
        ubp = n_size - 2
        for t3 in range(1, n_size - 2 + 1):
            b[t3][1] = S1(coef, a[t3][1], a[t3][1 - 1], a[t3][1 + 1], a[1 + t3][1], a[t3 - 1][1])
        lbp = 2
        ubp = min(n_size - 2, 3 * t_size - 2)
        for t1 in range(2, min(n_size - 2, 3 * t_size - 2) + 1):
            if (2 * t1 + 1) % 3 == 0:
                lbp = int(math.ceil(float(2 * t1 + 1) / float(3)))
                ubp = int(math.floor(float(2 * t1 + 3 * n_size - 8) / float(3)))
                for t3 in range(int(math.ceil(float(2 * t1 + 1) / float(3))), int(math.floor(float(2 * t1 + 3 *
                    n_size - 8) / float(3))) + 1):
                    b[(-2 * t1 + 3 * t3 + 2) / 3][1] = S1(coef, a[(-2 * t1 + 3 * t3 + 2) / 3][1], a[(-2 * t1 + 3 *
                        t3 + 2) / 3][1 - 1], a[(-2 * t1 + 3 * t3 + 2) / 3][1 + 1], a[1 + (-2 * t1 + 3 * t3 + 2) / 3]
                        [1], a[(-2 * t1 + 3 * t3 + 2) / 3 - 1][1])
            lbp = int(math.ceil(float(2 * t1 + 2) / float(3)))
            ubp = t1
            for t2 in range(lbp, ubp + 1):
                b[1][-2 * t1 + 3 * t2] = S1(coef, a[1][-2 * t1 + 3 * t2], a[1][-2 * t1 + 3 * t2 - 1], a[1][1 + (-2 *
                    t1 + 3 * t2)], a[1 + 1][-2 * t1 + 3 * t2], a[1 - 1][-2 * t1 + 3 * t2])
                lbp = 2 * t1 - 2 * t2 + 2
                ubp = 2 * t1 - 2 * t2 + n_size - 2
                for t3 in range(2 * t1 - 2 * t2 + 2, 2 * t1 - 2 * t2 + n_size - 2 + 1):
                    b[-2 * t1 + 2 * t2 + t3][-2 * t1 + 3 * t2] = S1(coef, a[-2 * t1 + 2 * t2 + t3][-2 * t1 + 3 * t2],
                        a[-2 * t1 + 2 * t2 + t3][-2 * t1 + 3 * t2 - 1], a[-2 * t1 + 2 * t2 + t3][1 + (-2 * t1 + 3 *
                        t2)], a[1 + (-2 * t1 + 2 * t2 + t3)][-2 * t1 + 3 * t2], a[-2 * t1 + 2 * t2 + t3 - 1][-2 * t1 +
                        3 * t2])
                    a[-2 * t1 + 2 * t2 + t3 - 1][-2 * t1 + 3 * t2 - 1] = S2(coef, b[-2 * t1 + 2 * t2 + t3 - 1][-2 *
                        t1 + 3 * t2 - 1], b[-2 * t1 + 2 * t2 + t3 - 1][-2 * t1 + 3 * t2 - 1 - 1], b[-2 * t1 + 2 * t2 +
                        t3 - 1][1 + (-2 * t1 + 3 * t2 - 1)], b[1 + (-2 * t1 + 2 * t2 + t3 - 1)][-2 * t1 + 3 * t2 - 1
                        ], b[-2 * t1 + 2 * t2 + t3 - 1 - 1][-2 * t1 + 3 * t2 - 1])
                a[n_size - 2][-2 * t1 + 3 * t2 - 1] = S2(coef, b[n_size - 2][-2 * t1 + 3 * t2 - 1], b[n_size - 2][-2 *
                    t1 + 3 * t2 - 1 - 1], b[n_size - 2][1 + (-2 * t1 + 3 * t2 - 1)], b[1 + (n_size - 2)][-2 * t1 + 3 *
                    t2 - 1], b[n_size - 2 - 1][-2 * t1 + 3 * t2 - 1])
        if n_size == 3:
            lbp = 2
            ubp = 3 * t_size - 2
            for t1 in range(2, 3 * t_size - 2 + 1):
                if (2 * t1 + 1) % 3 == 0:
                    b[1][1] = S1(coef, a[1][1], a[1][1 - 1], a[1][1 + 1], a[1 + 1][1], a[1 - 1][1])
                if (2 * t1 + 2) % 3 == 0:
                    a[1][1] = S2(coef, b[1][1], b[1][1 - 1], b[1][1 + 1], b[1 + 1][1], b[1 - 1][1])
        lbp = 3 * t_size - 1
        ubp = n_size - 2
        for t1 in range(3 * t_size - 1, n_size - 2 + 1):
            lbp = t1 - t_size + 1
            ubp = t1
            for t2 in range(lbp, ubp + 1):
                b[1][-2 * t1 + 3 * t2] = S1(coef, a[1][-2 * t1 + 3 * t2], a[1][-2 * t1 + 3 * t2 - 1], a[1][1 + (-2 *
                    t1 + 3 * t2)], a[1 + 1][-2 * t1 + 3 * t2], a[1 - 1][-2 * t1 + 3 * t2])
                lbp = 2 * t1 - 2 * t2 + 2
                ubp = 2 * t1 - 2 * t2 + n_size - 2
                for t3 in range(2 * t1 - 2 * t2 + 2, 2 * t1 - 2 * t2 + n_size - 2 + 1):
                    b[-2 * t1 + 2 * t2 + t3][-2 * t1 + 3 * t2] = S1(coef, a[-2 * t1 + 2 * t2 + t3][-2 * t1 + 3 * t2],
                        a[-2 * t1 + 2 * t2 + t3][-2 * t1 + 3 * t2 - 1], a[-2 * t1 + 2 * t2 + t3][1 + (-2 * t1 + 3 *
                        t2)], a[1 + (-2 * t1 + 2 * t2 + t3)][-2 * t1 + 3 * t2], a[-2 * t1 + 2 * t2 + t3 - 1][-2 * t1 +
                        3 * t2])
                    a[-2 * t1 + 2 * t2 + t3 - 1][-2 * t1 + 3 * t2 - 1] = S2(coef, b[-2 * t1 + 2 * t2 + t3 - 1][-2 *
                        t1 + 3 * t2 - 1], b[-2 * t1 + 2 * t2 + t3 - 1][-2 * t1 + 3 * t2 - 1 - 1], b[-2 * t1 + 2 * t2 +
                        t3 - 1][1 + (-2 * t1 + 3 * t2 - 1)], b[1 + (-2 * t1 + 2 * t2 + t3 - 1)][-2 * t1 + 3 * t2 - 1
                        ], b[-2 * t1 + 2 * t2 + t3 - 1 - 1][-2 * t1 + 3 * t2 - 1])
                a[n_size - 2][-2 * t1 + 3 * t2 - 1] = S2(coef, b[n_size - 2][-2 * t1 + 3 * t2 - 1], b[n_size - 2][-2 *
                    t1 + 3 * t2 - 1 - 1], b[n_size - 2][1 + (-2 * t1 + 3 * t2 - 1)], b[1 + (n_size - 2)][-2 * t1 + 3 *
                    t2 - 1], b[n_size - 2 - 1][-2 * t1 + 3 * t2 - 1])
        if n_size >= 4:
            lbp = n_size - 1
            ubp = 3 * t_size - 2
            for t1 in range(n_size - 1, 3 * t_size - 2 + 1):
                if (2 * t1 + 1) % 3 == 0:
                    lbp = int(math.ceil(float(2 * t1 + 1) / float(3)))
                    ubp = int(math.floor(float(2 * t1 + 3 * n_size - 8) / float(3)))
                    for t3 in range(int(math.ceil(float(2 * t1 + 1) / float(3))), int(math.floor(float(2 * t1 + 3 *
                        n_size - 8) / float(3))) + 1):
                        b[(-2 * t1 + 3 * t3 + 2) / 3][1] = S1(coef, a[(-2 * t1 + 3 * t3 + 2) / 3][1], a[(-2 * t1 + 3 *
                            t3 + 2) / 3][1 - 1], a[(-2 * t1 + 3 * t3 + 2) / 3][1 + 1], a[1 + (-2 * t1 + 3 * t3 + 2) /
                            3][1], a[(-2 * t1 + 3 * t3 + 2) / 3 - 1][1])
                lbp = int(math.ceil(float(2 * t1 + 2) / float(3)))
                ubp = int(math.floor(float(2 * t1 + n_size - 2) / float(3)))
                for t2 in range(lbp, ubp + 1):
                    b[1][-2 * t1 + 3 * t2] = S1(coef, a[1][-2 * t1 + 3 * t2], a[1][-2 * t1 + 3 * t2 - 1], a[1][1 + (
                        -2 * t1 + 3 * t2)], a[1 + 1][-2 * t1 + 3 * t2], a[1 - 1][-2 * t1 + 3 * t2])
                    lbp = 2 * t1 - 2 * t2 + 2
                    ubp = 2 * t1 - 2 * t2 + n_size - 2
                    for t3 in range(2 * t1 - 2 * t2 + 2, 2 * t1 - 2 * t2 + n_size - 2 + 1):
                        b[-2 * t1 + 2 * t2 + t3][-2 * t1 + 3 * t2] = S1(coef, a[-2 * t1 + 2 * t2 + t3][-2 * t1 + 3 *
                            t2], a[-2 * t1 + 2 * t2 + t3][-2 * t1 + 3 * t2 - 1], a[-2 * t1 + 2 * t2 + t3][1 + (-2 *
                            t1 + 3 * t2)], a[1 + (-2 * t1 + 2 * t2 + t3)][-2 * t1 + 3 * t2], a[-2 * t1 + 2 * t2 + t3 -
                            1][-2 * t1 + 3 * t2])
                        a[-2 * t1 + 2 * t2 + t3 - 1][-2 * t1 + 3 * t2 - 1] = S2(coef, b[-2 * t1 + 2 * t2 + t3 - 1][
                            -2 * t1 + 3 * t2 - 1], b[-2 * t1 + 2 * t2 + t3 - 1][-2 * t1 + 3 * t2 - 1 - 1], b[-2 * t1 +
                            2 * t2 + t3 - 1][1 + (-2 * t1 + 3 * t2 - 1)], b[1 + (-2 * t1 + 2 * t2 + t3 - 1)][-2 * t1 +
                            3 * t2 - 1], b[-2 * t1 + 2 * t2 + t3 - 1 - 1][-2 * t1 + 3 * t2 - 1])
                    a[n_size - 2][-2 * t1 + 3 * t2 - 1] = S2(coef, b[n_size - 2][-2 * t1 + 3 * t2 - 1], b[n_size - 2
                        ][-2 * t1 + 3 * t2 - 1 - 1], b[n_size - 2][1 + (-2 * t1 + 3 * t2 - 1)], b[1 + (n_size - 2)][
                        -2 * t1 + 3 * t2 - 1], b[n_size - 2 - 1][-2 * t1 + 3 * t2 - 1])
                if (2 * t1 + n_size + 2) % 3 == 0:
                    lbp = int(math.ceil(float(2 * t1 - 2 * n_size + 8) / float(3)))
                    ubp = int(math.floor(float(2 * t1 + n_size - 1) / float(3)))
                    for t3 in range(int(math.ceil(float(2 * t1 - 2 * n_size + 8) / float(3))), int(math.floor(float(
                        2 * t1 + n_size - 1) / float(3))) + 1):
                        a[(-2 * t1 + 3 * t3 + 2 * n_size - 5) / 3][n_size - 2] = S2(coef, b[(-2 * t1 + 3 * t3 + 2 *
                            n_size - 5) / 3][n_size - 2], b[(-2 * t1 + 3 * t3 + 2 * n_size - 5) / 3][n_size - 2 - 1],
                            b[(-2 * t1 + 3 * t3 + 2 * n_size - 5) / 3][1 + (n_size - 2)], b[1 + (-2 * t1 + 3 * t3 + 
                            2 * n_size - 5) / 3][n_size - 2], b[(-2 * t1 + 3 * t3 + 2 * n_size - 5) / 3 - 1][n_size - 2]
                            )
        lbp = max(n_size - 1, 3 * t_size - 1)
        ubp = n_size + 3 * t_size - 5
        for t1 in range(max(n_size - 1, 3 * t_size - 1), n_size + 3 * t_size - 5 + 1):
            lbp = t1 - t_size + 1
            ubp = int(math.floor(float(2 * t1 + n_size - 2) / float(3)))
            for t2 in range(lbp, ubp + 1):
                b[1][-2 * t1 + 3 * t2] = S1(coef, a[1][-2 * t1 + 3 * t2], a[1][-2 * t1 + 3 * t2 - 1], a[1][1 + (-2 *
                    t1 + 3 * t2)], a[1 + 1][-2 * t1 + 3 * t2], a[1 - 1][-2 * t1 + 3 * t2])
                lbp = 2 * t1 - 2 * t2 + 2
                ubp = 2 * t1 - 2 * t2 + n_size - 2
                for t3 in range(2 * t1 - 2 * t2 + 2, 2 * t1 - 2 * t2 + n_size - 2 + 1):
                    b[-2 * t1 + 2 * t2 + t3][-2 * t1 + 3 * t2] = S1(coef, a[-2 * t1 + 2 * t2 + t3][-2 * t1 + 3 * t2],
                        a[-2 * t1 + 2 * t2 + t3][-2 * t1 + 3 * t2 - 1], a[-2 * t1 + 2 * t2 + t3][1 + (-2 * t1 + 3 *
                        t2)], a[1 + (-2 * t1 + 2 * t2 + t3)][-2 * t1 + 3 * t2], a[-2 * t1 + 2 * t2 + t3 - 1][-2 * t1 +
                        3 * t2])
                    a[-2 * t1 + 2 * t2 + t3 - 1][-2 * t1 + 3 * t2 - 1] = S2(coef, b[-2 * t1 + 2 * t2 + t3 - 1][-2 *
                        t1 + 3 * t2 - 1], b[-2 * t1 + 2 * t2 + t3 - 1][-2 * t1 + 3 * t2 - 1 - 1], b[-2 * t1 + 2 * t2 +
                        t3 - 1][1 + (-2 * t1 + 3 * t2 - 1)], b[1 + (-2 * t1 + 2 * t2 + t3 - 1)][-2 * t1 + 3 * t2 - 1
                        ], b[-2 * t1 + 2 * t2 + t3 - 1 - 1][-2 * t1 + 3 * t2 - 1])
                a[n_size - 2][-2 * t1 + 3 * t2 - 1] = S2(coef, b[n_size - 2][-2 * t1 + 3 * t2 - 1], b[n_size - 2][-2 *
                    t1 + 3 * t2 - 1 - 1], b[n_size - 2][1 + (-2 * t1 + 3 * t2 - 1)], b[1 + (n_size - 2)][-2 * t1 + 3 *
                    t2 - 1], b[n_size - 2 - 1][-2 * t1 + 3 * t2 - 1])
            if (2 * t1 + n_size + 2) % 3 == 0:
                lbp = int(math.ceil(float(2 * t1 - 2 * n_size + 8) / float(3)))
                ubp = int(math.floor(float(2 * t1 + n_size - 1) / float(3)))
                for t3 in range(int(math.ceil(float(2 * t1 - 2 * n_size + 8) / float(3))), int(math.floor(float(2 *
                    t1 + n_size - 1) / float(3))) + 1):
                    a[(-2 * t1 + 3 * t3 + 2 * n_size - 5) / 3][n_size - 2] = S2(coef, b[(-2 * t1 + 3 * t3 + 2 *
                        n_size - 5) / 3][n_size - 2], b[(-2 * t1 + 3 * t3 + 2 * n_size - 5) / 3][n_size - 2 - 1], b[
                        (-2 * t1 + 3 * t3 + 2 * n_size - 5) / 3][1 + (n_size - 2)], b[1 + (-2 * t1 + 3 * t3 + 2 *
                        n_size - 5) / 3][n_size - 2], b[(-2 * t1 + 3 * t3 + 2 * n_size - 5) / 3 - 1][n_size - 2])
        lbp = 2 * t_size
        ubp = n_size + 2 * t_size - 3
        for t3 in range(2 * t_size, n_size + 2 * t_size - 3 + 1):
            a[t3 - 2 * t_size + 1][n_size - 2] = S2(coef, b[t3 - 2 * t_size + 1][n_size - 2], b[t3 - 2 * t_size + 1]
                [n_size - 2 - 1], b[t3 - 2 * t_size + 1][1 + (n_size - 2)], b[1 + (t3 - 2 * t_size + 1)][n_size - 2],
                b[t3 - 2 * t_size + 1 - 1][n_size - 2])
    compss_barrier()
    if __debug__:
        a = compss_wait_on(a)
        b = compss_wait_on(b)
        print('New Matrix A:')
        print(a)
        print('New Matrix B:')
        print(b)
    if __debug__:
        check_result(a, b, a_expected, b_expected)

# [COMPSs Autoparallel] End Autogenerated code


############################################
# MATHEMATICAL FUNCTIONS
############################################

def compute(coef, left, center, right, top, bottom):
    # import time
    # start = time.time()

    return coef * (left + center + right + top + bottom)

    # end = time.time()
    # tm = end - start
    # print "TIME: " + str(tm*1000) + " ms"


############################################
# RESULT CHECK FUNCTIONS
############################################

def seq_jacobi_2d(a, b, n_size, t_size, coef):
    for _ in range(t_size):
        for i in range(1, n_size - 1):
            for j in range(1, n_size - 1):
                b[i][j] = 0.2 * (a[i][j] + a[i][j - 1] + a[i][1 + j] + a[1 + i][j] + a[i - 1][j])
        for i in range(1, n_size - 1):
            for j in range(1, n_size - 1):
                a[i][j] = 0.2 * (b[i][j] + b[i][j - 1] + b[i][1 + j] + b[1 + i][j] + b[i - 1][j])

    return a, b


def check_result(a, b, a_expected, b_expected):
    is_a_ok = np.allclose(a, a_expected)
    is_b_ok = np.allclose(b, b_expected)
    is_ok = is_a_ok and is_b_ok
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
    COEF = np.float64(np.float64(1) / np.float64(5))

    # Log arguments if required
    if __debug__:
        print("Running jacobi-2d application with:")
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
    jacobi_2d(A, B, NSIZE, TSIZE, COEF)
    compss_barrier(True)
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
