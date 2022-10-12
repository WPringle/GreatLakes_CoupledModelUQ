from pathlib import Path
from wrf_fvcom.variables import (
    WRF_PBL_SFCLAY, FVCOM_Prandtl
)
from wrf_fvcom.perturb import (
    perturb_variables, SampleRule
)

if __name__ == '__main__':
    
    output_directory = Path.cwd() / 'output_files'

    variables = [WRF_PBL_SFCLAY, FVCOM_Prandtl]
    
    # calling the perturb_variables functiob
    perturbations = perturb_variables(
        variables=variables,
        number_perturbations=19,
        sample_rule=SampleRule.KOROBOV,
        output_directory=output_directory,
    )
