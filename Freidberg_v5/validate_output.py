import numpy as np


# Constants
lambdasd = 0.055
lambdabr = 0.0031
Et = 0.025e-6
En = 14.1
ELi = 2.5
Ealpha = 3.5
etat = 0.4
n = 1.5e20
sigmav= 3e-22
Bc = 13
mu0 = 1.24552706212e-6

# Design variables
# My result
# R0 = 5.29
# a = 2.10
# b = 0.99
# c = 0.79

# Freidberg result
# R0 = 5.0
# a = 2.0
# b = 1.2
# c = 0.79

# Other result
R0 = 6.837139307833997
a = 1.4626000070734255
b = 0.8837078989314403
c = 0.598244300331013

## Equations in my model
# Blanket
gammafrac = np.exp(-2*np.sqrt(Et/En)*lambdasd/lambdabr*np.exp(0.5*b/lambdasd-1))

# Coils
ksi = c/(c+2*(a+b))
sigma = Bc**2/(4*mu0*ksi)/10**6 # MPa

# First Wall
PW = En*n**2*sigmav*a/8/(6.241509*10**18) #MW/m2

# Plasma
e = 1.602176634e-19 # elementary charge
PE = 0.25*etat*(Ealpha+En+ELi)*n**2*sigmav*(2*np.pi**2*R0*a**2)*e # MW

# Objective
VIPE = 2*np.pi**2*R0*((a+b+c)**2-a**2)/PE

print('VIPE,              ', 'PW               ,','PE            ,','sigma,','gammafrac,     ')
print(VIPE, PW, PE, sigma, gammafrac)

print()
# Direct Freidberg Equations
PW = 4
sigma = 300*10**6
PE = 1000
gammafrac = 0.01

# Compute b
deltaX = 2*lambdasd*np.log(1-0.5*np.sqrt(En/Et)*lambdabr/lambdasd*np.log(gammafrac))
b = deltaX
print('Freidberg DeltaX = ', deltaX)

# Compute c
ksi = Bc**2/4/mu0/sigma

a = (1 + ksi)/(2*np.sqrt(ksi))*b
print('Freidberg a = ',a)

c = 2*ksi/(1-ksi)*(a+b)
print('Freidberg c = ',c)

VIPE = 0.79*((a+b+c)**2 - a**2)/a/PW
print('Freidberg VIPE = ', VIPE)

R0 = 0.04 * PE/a/PW
print('Freidberg R0 = ',R0)