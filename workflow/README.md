# Scripts and Instructions for Recreating Experiment

## Details on generating input configuration matrix (Step 2)
Running `make_perturbations.py` will generate the perturbation matrix for all variables (there are 9) using a Korobov sequence with 18 samples which samples 89.5% of the range of each variable. Values for each perturbation are output into a netCDF file. This is the same idea as in Pringle et al. (2023)

One may view each variable and available options inside `wrf_fvcom/variables`. 

There are 5 different perturbations for WRF, each of these are treated as discrete uniform variables corresponding to the integer option in WRF namelist for the chosen parameterization scheme:
- WRF planetary bounday layer and surface layer scheme [discrete]
- WRF surface roughness (z0) scheme over water [discrete]
- WRF microphysics scheme [discrete]
- WRF radiation scheme [discrete]
- WRF land surface model [discrete]

There are 4 different perturbations for FVCOM, two of these are treated as discrete uniform variables corresponding to the compiler option for the chosen parameterization scheme and the other two are continous uniform variables corresponding to the float value used in the FVCOM namelist:
- FVCOM vertical mixing scheme [discrete]
- FVCOM bulk wind stress formulation [discrete]
- FVCOM shortwave radiation absorption: R [continuous]
- FVCOM Prandlt Number [continuous]

## References
1. Pringle, W. J., Burnett, Z., Sargsyan, K., Moghimi, S., & Myers, E. (2023). Efficient Probabilistic Prediction and Uncertainty Quantification of Tropical Cyclone-driven Storm Tides and Inundation. Artificial Intelligence for the Earth Systems, 2(2), e220040. https://doi.org/10.1175/AIES-D-22-0040.1
