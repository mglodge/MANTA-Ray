![MANTA Ray logo final](https://github.com/user-attachments/assets/daace825-8432-44ba-a673-0f6d441a3116)

MANTA-Ray (<ins>**M**</ins>odified <ins>**A**</ins>bsorption of <ins>**N**</ins>on-spherical <ins>**T**</ins>iny <ins>**A**</ins>ggregates in the <ins>**Ray**</ins>leigh regime) is a model that calculates the absorption efficiency and absorption cross-section of fractal aggregates. It is a very powerful and fast tool that can be used to estimate the amount of absorption that occurs in dust and haze particles of any shape, provided that the electomagnetic radiation is in the Rayleigh regime (see below for strict definition), often in the context of planetary atmospheres or protoplanetary disks. It obtains values within 10-20% of those calculated by a rigourous benchmark model (the discrete dipole approximation), but is $10^{13}$ times faster. It is provided here as a python function. For full details of the methodology, or if the code is useful in your project, please cite the paper below:

  "MANTA-Ray: Supercharging Speeds for Calculating the Optical Properties of Fractal Aggregates in the Long-Wavelength Limit" (2024), Lodge, M.G., Wakeford H.R., and Leinhardt, Z.M.

# Getting started

The easiest way to run MANTA-Ray is to install it into your python environment using pip (**IMPORTANT:** note the use of an **underscore _** instead of a **hyphon -**, as per the PEP 8 style guide for distributed packages):

	pip install MANTA_Ray

Then import the two functions into your python code:

	from MANTA_Ray import Q_abs_MR, C_abs_MR

The inputs to the functions are:

1) wavelength: the wavelength ($\lambda$) of the electromagnetic radiation (in μm).
2) radius: the particle radius ($R$) (in μm) -- see note below*.
3) d_f: the fractal dimension ($d_f$) of the aggregate. The code has been tested for values between $d_f=$ 1.2 (linear) and 2.7 (compact). See section "The Model" below for more details.
4) n: the real component of refractive index
5) k: the imaginary component of refractive index

*Because the aggregates are non-spherical, they do not have a radius. To represent the physical size of the particle, we use the radius of a <i>sphere that has exactly the same volume</i> as the fractal aggregate (i.e. the radius if the aggregate material was squashed/compacted into a sphere). 

Note that to be in the Rayleigh regime, and for this theory to work, it is assumed that $\lambda \geq 100R$, and the code will return an error message if this condition is not true.

To use each of functions, just provide the above inputs, strictly in that order. For example, to determine the absorption efficiency of an aggregate of fractal dimension 1.8, with a radius of 0.5 μm, at a wavelength of 100 μm, and assuming a refractive index $m=n+k$ i $=3+0.5$ i:

	wavelength = 100   # in um
 	radius = 0.5   # in um
	d_f = 1.8		
 	n = 3
	k = 0.5
	
	Q_abs = Q_abs_MR(wavelength, radius, d_f, n, k)   # calculate Q_abs
	print(Q_abs)
 
If MANTA-Ray installed correcty, you should see:

	Q_abs = 0.021153387751343056  

Two functions are provided:

1) Q_abs_MR: calculates absorption efficiency $Q_{abs,MR}$ (Eq. 5 in Lodge et al. 2024)
2) C_abs_MR: calculates absorption cross-section (where $C_{abs}=Q_{abs} \pi R^2$)

Both functions are called in exactly the same way:

	Q_abs = Q_abs_MR(wavelength, radius, d_f, n, k)
	C_abs = C_abs_MR(wavelength, radius, d_f, n, k)

If a pip install fails (or simply if you prefer), you could copy and paste the functions from MANTA_Ray.py directly into your code and use them in the same way.

# The Model

This section provides a brief overview of the model, but for a full explanation and more details, please read Lodge et al. 2024. 

Transmission Electron Microscope (TEM) images of solid matter in Earth's atmosphere shows that they often form very complex shapes, which we call fractal aggregates. Their exact shape depends on the material and conditions under which they form. Typically, we characterise them by a single number -- their fractal dimension $d_f$:

<p align="center">
  <img src="https://github.com/user-attachments/assets/7060caea-1465-45dd-9f64-74a351b0733b" alt="drawing" width="400" />
</p>

In the image above the two aggregates are both composed of 24 "monomers" (individual spheres), but in different arrangements. These shapes are characterised in many optical models by $d_f$ which is a number between 1 (representing a straight line) and 3 (compact and perfectly spherical).

Modelling the optical properties of complex shapes is difficult, and Mie theory is often used (which assumes that the particles are spherical). However, this can often be a significant underestimate of the amout of absorption (by factors of up to 1,000 -- see Lodge et al. 2024). Calculating the optical properties for the true aggregate shape can be done using a rigourous code such as the discrete dipole approximation (DDA -- Draine and Flatau, 1994), but this is usually incredibly time consuming (and unfeasible for use in forward models that wish to study many wavelengths/particle sizes). In contrast, MANTA-Ray estimates absorption cross-sections with average accuracies of 10-20% compared to DDA, but $10^{13}$ times faster. It works for any wavelength, particle size, and refractive index $m$ within 1+0.01i< $m$ <11+11i. It is strictly only for use in the Rayleigh Regime (where the wavelength $\lambda$ is signficantly larger than the radius $R$ of a sphere of equivalent volume to the aggregate -- here we define this regime as $\lambda \geq 100R$).
