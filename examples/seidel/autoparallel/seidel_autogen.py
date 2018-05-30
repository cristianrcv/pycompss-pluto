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
    a = create_matrix(n_size)

    return a


def create_matrix(n_size):
    mat = []
    for i in range(n_size):
        mat.append([])
        for j in range(n_size):
            mb = create_entry(i, j, n_size)
            mat[i].append(mb)

    return mat


@constraint(ComputingUnits="${ComputingUnits}")
@task(returns=1)
def create_entry(i, j, n_size):
    return np.float64(np.float64(i * (j + 2) + 2) / np.float64(n_size))


############################################
# MAIN FUNCTION
############################################

# [COMPSs Autoparallel] Begin Autogenerated code
import math

from pycompss.api.api import compss_barrier, compss_wait_on, compss_open
from pycompss.api.task import task
from pycompss.api.parameter import *
from pycompss.util.translators.arg_utils.arg_utils import ArgUtils


@task(t1=IN, n_size=IN, returns="LT2_args_size")
def LT2(t1, n_size, *args):
    global LT2_args_size
    var2, var3, var4, var5, var6, var7, var8, var9, var1 = ArgUtils.rebuild_args(args)
    for t3 in range(0, t1 + n_size - 2 + 1 - (t1 + 1)):
        var1[t3] = S1_no_task(var2[t3], var3[t3], var4[t3], var5[t3], var1[t3], var6[t3], var7[t3], var8[t3], var9[t3])
    return ArgUtils.flatten_args(var2, var3, var4, var5, var6, var7, var8, var9, var1)


@task(var2=IN, var3=IN, var4=IN, var5=IN, var6=IN, var7=IN, var8=IN, var9=IN, var10=IN, returns=1)
def S1(var2, var3, var4, var5, var6, var7, var8, var9, var10):
    return compute_distance(var2, var3, var4, var5, var6, var7, var8, var9, var10)


def S1_no_task(var2, var3, var4, var5, var6, var7, var8, var9, var10):
    return compute_distance(var2, var3, var4, var5, var6, var7, var8, var9, var10)


def seidel(a, n_size, t_size):
    if __debug__:
        a = compss_wait_on(a)
        print('Matrix A:')
        print(a)
    if __debug__:
        import copy
        a_seq = copy.deepcopy(a)
        a_expected = seq_seidel(a_seq, n_size, t_size)
    if n_size >= 3 and t_size >= 1:
        lbp = 1
        ubp = n_size + 2 * t_size - 4
        for t1 in range(1, n_size + 2 * t_size - 4 + 1):
            lbp = max(int(math.ceil(float(t1 + 1) / float(2))), t1 - t_size + 1)
            ubp = min(int(math.floor(float(t1 + n_size - 2) / float(2))), t1)
            for t2 in range(lbp, ubp + 1):
                lbp = t1 + 1
                ubp = t1 + n_size - 2
                LT2_aux_0 = [a[-t1 + 2 * t2 - 1][-t1 + t3 - 1] for t3 in range(t1 + 1, t1 + n_size - 2 + 1)]
                LT2_aux_1 = [a[-t1 + 2 * t2 - 1][-t1 + t3] for t3 in range(t1 + 1, t1 + n_size - 2 + 1)]
                LT2_aux_2 = [a[-t1 + 2 * t2 - 1][-t1 + t3 + 1] for t3 in range(t1 + 1, t1 + n_size - 2 + 1)]
                LT2_aux_3 = [a[-t1 + 2 * t2][-t1 + t3 - 1] for t3 in range(t1 + 1, t1 + n_size - 2 + 1)]
                LT2_aux_4 = [a[-t1 + 2 * t2][-t1 + t3 + 1] for t3 in range(t1 + 1, t1 + n_size - 2 + 1)]
                LT2_aux_5 = [a[-t1 + 2 * t2 + 1][-t1 + t3 - 1] for t3 in range(t1 + 1, t1 + n_size - 2 + 1)]
                LT2_aux_6 = [a[-t1 + 2 * t2 + 1][-t1 + t3] for t3 in range(t1 + 1, t1 + n_size - 2 + 1)]
                LT2_aux_7 = [a[-t1 + 2 * t2 + 1][-t1 + t3 + 1] for t3 in range(t1 + 1, t1 + n_size - 2 + 1)]
                LT2_aux_8 = [a[-t1 + 2 * t2][-t1 + t3] for t3 in range(t1 + 1, t1 + n_size - 2 + 1)]
                LT2_argutils = ArgUtils()
                LT2_flat_args = LT2_argutils.flatten(LT2_aux_0, LT2_aux_1, LT2_aux_2, LT2_aux_3, LT2_aux_4,
                    LT2_aux_5, LT2_aux_6, LT2_aux_7, LT2_aux_8)
                global LT2_args_size
                LT2_args_size = len(LT2_flat_args)
                LT2_new_args = LT2(t1, n_size, *LT2_flat_args)
                (LT2_aux_0, LT2_aux_1, LT2_aux_2, LT2_aux_3, LT2_aux_4, LT2_aux_5, LT2_aux_6, LT2_aux_7, LT2_aux_8
                    ) = LT2_argutils.rebuild(LT2_new_args)
                LT2_index = 0
                for t3 in range(t1 + 1, t1 + n_size - 2 + 1):
                    a[-t1 + 2 * t2 - 1][-t1 + t3 - 1] = LT2_aux_0[LT2_index]
                    a[-t1 + 2 * t2 - 1][-t1 + t3] = LT2_aux_1[LT2_index]
                    a[-t1 + 2 * t2 - 1][-t1 + t3 + 1] = LT2_aux_2[LT2_index]
                    a[-t1 + 2 * t2][-t1 + t3 - 1] = LT2_aux_3[LT2_index]
                    a[-t1 + 2 * t2][-t1 + t3 + 1] = LT2_aux_4[LT2_index]
                    a[-t1 + 2 * t2 + 1][-t1 + t3 - 1] = LT2_aux_5[LT2_index]
                    a[-t1 + 2 * t2 + 1][-t1 + t3] = LT2_aux_6[LT2_index]
                    a[-t1 + 2 * t2 + 1][-t1 + t3 + 1] = LT2_aux_7[LT2_index]
                    a[-t1 + 2 * t2][-t1 + t3] = LT2_aux_8[LT2_index]
                    LT2_index = LT2_index + 1
    compss_barrier()
    if __debug__:
        a = compss_wait_on(a)
        print('New Matrix A:')
        print(a)
    if __debug__:
        check_result(a, a_expected)

# [COMPSs Autoparallel] End Autogenerated code


############################################
# MATHEMATICAL FUNCTIONS
############################################

def compute_distance(a_tl, a_tc, a_tr, a_cl, a_cc, a_cr, a_bl, a_bc, a_br):
    # import time
    # start = time.time()

    return np.float64((np.float64(a_tl + a_tc + a_tr + a_cl + a_cc + a_cr + a_bl + a_bc + a_br)) / np.float64(9))

    # end = time.time()
    # tm = end - start
    # print "TIME: " + str(tm*1000) + " ms"


############################################
# RESULT CHECK FUNCTIONS
############################################

def seq_seidel(a, n_size, t_size):
    for _ in range(t_size):
        for i in range(1, n_size - 1):
            for j in range(1, n_size - 1):
                a[i][j] = np.float64(np.float64(
                    a[i - 1][j - 1] + a[i - 1][j] + a[i - 1][j + 1] + a[i][j - 1] + a[i][j] + a[i][j + 1] + a[i + 1][
                        j - 1] + a[i + 1][j] + a[i + 1][j + 1]) / np.float64(9))

    return a


def check_result(a, a_expected):
    is_ok = np.allclose(a, a_expected)
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

    # Log arguments if required
    if __debug__:
        print("Running seidel application with:")
        print(" - NSIZE = " + str(NSIZE))
        print(" - TSIZE = " + str(TSIZE))

    # Initialize matrices
    if __debug__:
        print("Initializing matrices")
    start_time = time.time()
    A = initialize_variables(NSIZE)
    compss_barrier()

    # Begin computation
    if __debug__:
        print("Performing computation")
    seidel_start_time = time.time()
    seidel(A, NSIZE, TSIZE)
    compss_barrier(True)
    end_time = time.time()

    # Log results and time
    if __debug__:
        print("Post-process results")
    total_time = end_time - start_time
    init_time = seidel_start_time - start_time
    seidel_time = end_time - seidel_start_time

    print("RESULTS -----------------")
    print("VERSION AUTOPARALLEL")
    print("NSIZE " + str(NSIZE))
    print("TSIZE " + str(TSIZE))
    print("DEBUG " + str(__debug__))
    print("TOTAL_TIME " + str(total_time))
    print("INIT_TIME " + str(init_time))
    print("SEIDEL_TIME " + str(seidel_time))
    print("-------------------------")
