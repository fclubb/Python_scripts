cd #======================================================================#
# fluvial_relief.py
# This script calculates the K value needed to get a specific relief
# using detachment limited stream power.
# Based on Whipple and Tucker, 1999, JGR
# FJC 04/08/17
#======================================================================#
import numpy as np

def get_K_from_relief(U, m, n, h, R_f, L, x_c, H):
    """
    This function calculates the K value needed to get a specific
    relief using detachment-limited stream power.

    Args:
        U: the uplift rate
        m: m exponent
        n: n exponent
        h: Hack's exponent
        R_f: desired relief
        L: total length of all bedrock channels
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

    if ((hm)/n) == 1:
        K = U_0 * (K_a)**(-m) * L**(n-hm) * H**(-n) * (-((R_f * (U/U_0)**(-1/n))/(log(x_c))))**(-n)
    else:
        K = U_0 * (K_a)**(-m) * L**(n-hm) * H**(-n) * (U/U_0) * ((1 - x_c**(1-hm/n)/(R_f*(1-hm/n))))

    print "The K value for this relief is: " + str(K) + ", m/n = " + str(m/n)

if __name__ == '__main__':
    U =
    m = 0.5
    n = 1
    h =
    R_f =
    L =
    x_c =
    H =

    get_K_from_relief(U, m, n, h, R_f, L, x_c, H)
