## Scripts and Instructions for Recreating Experiment

# Instructions
Running `make_perturbations.py` will generate the perturbation matrix for all variables (there are 8) using a Korobov sequence with 19 samples which samples the 90% of the range of each variables. Values for each perturbation are output into a netCDF file. This is the same idea as in Pringle et al. (2022)

One may view each variable and available options inside `wrf_fvcom/variables`. 

There are 4 different perturbations for WRF, each of these are treated as discrete uniform variables corresponding to the integer option in WRF namelist for the chosen parameterization scheme:
- WRF planetary bounday layer and surface layer scheme [discrete]
- WRF surface roughness (z0) scheme over water [discrete]
- WRF microphysics scheme [discrete]
- WRF radiation scheme [discrete]

There are 4 different perturbations for FVCOM, two of these are treated as discrete uniform variables corresponding to the compiler option for the chosen parameterization scheme and the other two are continous uniform variables corresponding to the float value used in the FVCOM namelist:
- FVCOM vertical mixing scheme [discrete]
- FVCOM bulk wind stress formulation [discrete]
- FVCOM shortwave radiation absorption: R [continuous]
- FVCOM Prandlt Number [continuous]

# References
1. Pringle, W. J., Burnett, Z., Sargsyan, K., Moghimi, S., & Myers, E. (2022). Efficient Probabilistic Prediction and Uncertainty Quantification of Hurricane Surge and Inundation. Artificial Intelligence for the Earth Systems, revised manuscript submitted. https://doi.org/10.31223/X5VW6D    
