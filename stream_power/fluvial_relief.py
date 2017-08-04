#======================================================================#
# fluvial_relief.py
# This script calculates the K value needed to get a specific relief
# using detachment limited stream power.
# Based on Whipple and Tucker, 1999, JGR
# FJC 04/08/17
#======================================================================#
from __future__ import division
import numpy as np

def get_K_from_relief(U, U_0, K_a, m, n, h, R_f, L, x_c, H):
    """
    This function calculates the K value needed to get a specific
    relief using detachment-limited stream power.

    Args:
        U: the uplift rate
        U_0: the average uplift rate. Steady state: U = U_0
        K_a: area-length coefficient in Hack's law (suggested value of 6.69)
        m: m exponent
        n: n exponent
        h: Hack's exponent (suggested value of 1.67)
        R_f: desired relief
        L: range half width
        x_c: hillslope length
        H: vertical scale (equal to desired relief)

    Returns:
        K: K value needed to get the correct relief

    Author:
        FJC
    """

    # back-calculate K from the relief.
    # N_E = (U_0/K) * (K_a)^(-m) * L^(n-hm) * H^(-n) (equation 19)
    # R_f = (-N_E)^(1/n) * (U/U_0)^(1/n) * log(x_c) (equation 22) hm/n = 1
    # R_f = (N_E)^(1/n) * (U/U_0)^(1/n) * (1- ((hm)/n))^(-1) * (1 - x_c^(1- ((hm)/n))) (equation 22) hm/n not equal to 1
    x_c_nd = x_c/L
    #print x_c_nd
    R_f_nd = R_f/H
    print R_f_nd

    if ((h*m)/n) == 1:
        K = U_0 * (K_a)**(-m) * L**(n-h*m) * H**(-n) * (-(((R_f) * (U/U_0)**(-1/n))/(log(x_c/L))))**(-n)
    else:
        K = U_0 * (K_a)**(-m) * L**(n-h*m) * H**(-n) * (U/U_0) * ((1 - (x_c/L)**(1-h*m/n)/((R_f)*(1-h*m/n))))

    #print "The K value for this relief is: " + str(K) + ", m/n = " + str(m/n)
    return K

def get_K_from_relief_varying_mn(U, U_0, K_a, h, R_f, L, x_c, H, n, start_m, n_moverns, d_movern):
    """
    This function calculates the K value needed to get a specific
    relief using detachment-limited stream power. Goes through a series
    of m/n values and gets the correct K for each one.

    Args:
        U: the uplift rate
        U_0: the average uplift rate. Steady state: U = U_0
        K_a: area-length coefficient in Hack's law (suggested value of 6.69)
        h: Hack's exponent (suggested value of 1.67)
        R_f: desired relief
        L: range half width
        x_c: hillslope length
        H: vertical scale (equal to desired relief)
        n: the n exponent
        start_m: the starting m value
        n_moverns: the number of m/n values to test
        d_movern: the increment of the m value

    Returns:
        K: K value needed to get the correct relief

    Author:
        FJC
    """
    # get the movern list
    # Get a vector of the m over n values
    end_m = start_m+d_movern*(n_moverns-1)
    m_values = np.linspace(start_m,end_m,n_moverns)
    print "This uplift rate is: " + str(U) +" m/yr"

    for m in m_values:
        this_K = get_K_from_relief(U, U_0, K_a, m, n, h, R_f, L, x_c, H)
        print "m/n: " + str(m/n) + " K: " + str(this_K)

if __name__ == '__main__':
    U = 0.01
    U_0 = 0.01
    K_a = 6.69
    m = 0.5
    n = 1
    h = 1.67
    R_f = 1000
    L = 5000
    x_c = 300
    H = 1000

    get_K_from_relief(U, U_0, K_a, m, n, h, R_f, L, x_c, H)

    start_m = 0.2
    n_moverns = 7
    d_movern = 0.1
    get_K_from_relief_varying_mn(U, U_0, K_a, h, R_f, L, x_c, H, n, start_m, n_moverns, d_movern)
