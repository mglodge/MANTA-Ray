'''

        ----   MANTA-Ray (Modified Absorption for Nonspherical Tiny Aggregates in the Rayleigh regime)   ----   

                                                                                 Matt Lodge (20/08/24)

This code estimates the absorption cross-sections of fractal aggregate dust/aerosol particles using the MANTA-Ray model (Lodge et al. 2024)
The inputs are the wavelength, particle size, particle shape and refractive index, and the output is absorption efficiency (and there is
also an option to directly calculate absorption cross-section).

Absorption efficiencies are estimated by using a multi-variate quadratic fit to data obtained by the discrete dipole approximation (DDA) for a range
of shapes from compact (d_f = 2.7) to linear (d_f = 1.2). See paper for more details, as well as average and maximum expected errors for each
shape type.

The model is bi-modal, and this particular version uses linear interpolation to join the two quadratic models in the region of (n,k) space bounded by:

    n+2=k    and    n+3=k

This linear interpolation blends the two regimes together at the boundary smoothly, rather than having a "hard" boundary to move between them (a step 
function between regimes would not represent the expected optical properties well -- see Appendix A of Lodge et al. 2024). The exact position is somewhat
arbitrary and purely a modelling decision, but we have found that the above choice for the region of "overlap" allows a smooth transition between the two modes.

You are welcome to use, adapt or modify this code in any way you wish, but please cite the following paper if it is used:

    "MANTA-Ray: Supercharging Speeds for Calculating the Optical Properties of Fractal Aggregates in the Long-Wavelength Limit" (2024)
    Lodge, M.G., Wakeford H.R., and Leinhardt, Z.M.

Although every care has been taken to benchmark the code and test it under a wide range of conditions (see attached paper for details), 
this code is provided without a warantee of any kind. The author cannot be held liable or accept any resposibility for any claim, loss 
or damages that arise in connection with the use of this code.

'''




# The main function below (Q_abs) calculates absorption efficiency (using Eq. 5 of Lodge et al. 2024) given the following variables:
#
#       wavelength: the wavelength of the electromagnetic radiation (in um).
#
#       radius: the volume-equivalent spherical radius of the particle (in um). This is the radius of a sphere that would have the same volume 
#       as the fractal aggregate. Note that to be in the Rayleigh regime, and for this theory to work, it is assumed that wavelength > 100*radius,
#       and the code will return an error message if this condition is not true.
#
#       d_f: the fractal dimension of the aggregate. The code has been tested for values between 1.2 (linear) and 2.7 (compact).
#
#       n,k: the real (n) and imaginary (k) components of refractive index respectively.
#

def Q_abs(wavelength, radius, d_f, n, k):

    # quick safety check to ensure that we are in the Rayleigh regime (wavelength >= 100*radius)
    if(wavelength>=(100*radius)):

        if (n+3)>=k:
            
            # calculate coefficients for the (n+2.7) >= k regime using Eq. 27
            a0 = -0.916776*d_f + 3.221436
            a1 = 1.151507*d_f + -3.085145
            a2 = 1.128757*d_f + -3.439070
            a3 = -0.286824*d_f + 0.977069
            a4 = -0.353894*d_f + 0.705205
            a5 = -0.335264*d_f + 1.603978

            X1 = a0 + a1*n + a2*k + a3*n*n +a4*n*k + a5*k*k # calculate modification factor X(n,k,d_f) for regime 1 using Eq. 25

        if (n+2)<=k:
            
            # calculate coefficients for the (n+2.7) < k regime using Eq. 28
            a6 = -22.844445*d_f + 60.839633
            a7 = -12.817920*d_f + 44.435606
            a8 = 21.762958*d_f + -63.878747
            a9 = -3.916172*d_f + 17.503977
            a10 = 6.147451*d_f + -26.877763
            a11= -4.183578*d_f + 15.293480

            X2 = a6 + a7*n + a8*k + a9*n*n +a10*n*k + a11*k*k # calculate modification factor X(n,k,d_f) for regime 2 using Eq. 25


        # choose whether we are exclusively in regime 1 or 2, or whether we are in the transition between models (we then blend each model using linear interpolation between 'k=n+2' -> 'k=n+3)
        if (n+2)>k: # we are exclusively in regime 1
            X = X1

        elif (n+3)>k: # we are in the transition betewen regimes; use a "faded blend" of X1 and X2
            blend_factor= k - n - 2 # calculate fraction of distance travelled across boundary from regime 1 to 2. This value varies from 0 (leaving regime 1) to 1 (arriving at regime 2) and slowly alters the mixture of the two values used at all points between
            X = (1-blend_factor)*X1 + blend_factor*X2

        else: # we are exclusively in regime 2
            X = X2



        # BRICKWALL LIMITER - if X<1, set X=1 (this can happen for very low d_f near the intersection of the bi-modal regimes where the inflection oof the curve 
        # is very steep. This ensures physical results in this region.
        if(X<1):
            X=1

        m= complex(n,k) # combine n + ki into a complex number for efficient computation
        m_term = (m*m - 1)/(m*m + 2) # find bracketed refractive index term from Eq 5.

        return X*(25.13274*radius/wavelength)*m_term.imag # calculate absorption efficiency Q_abs,MR using Eq. 5 (with 8*pi hardcoded as 25.13... for speed)

        
    else:
        print(f"WARNING: Wavelength ({wavelength} um) is not at least 100 x larger than the radius ({radius} um); results will not be valid because we are outside the Rayleigh regime!")    






# This uses the function above, but then also converts the absorption efficiency to an absorption cross-section (in um^2) at the end for convenience
def C_abs(wavelength, radius, d_f, n, k):

    Q_abs = Q_abs(wavelength, radius, d_f, n, k) # find Q_abs

    return Q_abs*3.14159*radius*radius # calculate C_abs = Q_abs*pi*R^2 in um^2
