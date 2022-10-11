from pathlib import Path
from wrf_fvcom.variables_perturb import (
    PerturbedVariable, perturb_variables, 
    distribution_from_variables, 
    WRF_PBL_SFCLAY, FVCOM_Prandtl
)


if __name__ == '__main__':
    
    output_directory = Path.cwd() / 'output_files'

    variables = [WRF_PBL_SFCLAY, FVCOM_Prandtl]
    
    # calling the perturb_variables functiob
    perturbations = perturb_variables(
        variables=variables,
        number_perturbations=19,
        sample_rule='korobov',
        output_directory=output_directory,
    )
