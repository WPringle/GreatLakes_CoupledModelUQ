from pathlib import Path
from wrf_fvcom.variables import (
    WRF_PBL_SFCLAY, WRF_WaterZ0, WRF_MP, WRF_RA, WRF_LM,
    FVCOM_Prandtl, FVCOM_SWRadiationAbsorption,
    FVCOM_VerticalMixing, FVCOM_WindStress,
)
from wrf_fvcom.perturb import (
    perturb_variables, SampleRule,
)

if __name__ == '__main__':
    
    output_directory = Path.cwd() / 'output_files'

    variables = [
        WRF_PBL_SFCLAY, WRF_WaterZ0, WRF_MP, WRF_RA,
        FVCOM_VerticalMixing, FVCOM_WindStress, 
        FVCOM_Prandtl, FVCOM_SWRadiationAbsorption, WRF_LM,
    ]
    
    # calling the perturb_variables function (output is written inside the function)
    perturbations = perturb_variables(
        variables=variables,
        number_perturbations=19,
        sample_rule=SampleRule.KOROBOV,
        output_directory=output_directory,
    )
  
    # Dependent variables to follow...

    # Shortwave radiation absorption scheme
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
    
    # plotting the table of experiments
    
