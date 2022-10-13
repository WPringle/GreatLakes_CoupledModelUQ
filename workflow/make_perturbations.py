from pathlib import Path
from wrf_fvcom.variables import (
    WRF_PBL_SFCLAY, WRF_WATER_Z0, WRF_MP, WRF_RA,
    FVCOM_Prandtl, FVCOM_SWRadiationAbsorption,
)
from wrf_fvcom.perturb import (
    perturb_variables, SampleRule,
)

if __name__ == '__main__':
    
    output_directory = Path.cwd() / 'output_files'

    variables = [
        WRF_PBL_SFCLAY, WRF_WATER_Z0, WRF_MP, WRF_RA, 
        FVCOM_Prandtl, FVCOM_SWRadiationAbsorption,
    ]
    
    # calling the perturb_variables functiob
    perturbations = perturb_variables(
        variables=variables,
        number_perturbations=19,
        sample_rule=SampleRule.KOROBOV,
        output_directory=output_directory,
    )
  
    # dependent variables to follow...

    # 1) Shortwave radiation absorption scheme
    # Calculate Z1 and Z2 from R fraction 
    SW_R = perturbations.sel(variable=FVCOM_SWRadiationAbsorption.name)
    Z1 = FVCOM_SWRadiationAbsorption.calc_Z1(SW_R)
    Z2 = FVCOM_SWRadiationAbsorption.calc_Z2(SW_R)
    
    if output_directory is not None:
        Z1.to_netcdf(
            output_directory / f'perturbation_vector_FVCOM_SWRadiationAbsorption_Z1.nc'
        )
        Z2.to_netcdf(
            output_directory / f'perturbation_vector_FVCOM_SWRadiationAbsorption_Z2.nc'
        )
