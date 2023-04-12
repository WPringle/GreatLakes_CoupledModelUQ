import chaospy
import xarray as xr
from enum import Enum
from os import PathLike
from typing import List
from wrf_fvcom.variables import PerturbedVariable


class SampleRule(Enum):
    KOROBOV = 'korobov'
    RANDOM = 'random'
    SOBOL = 'sobol'
    LATINHYPERCUBE = 'latin_hypercube'


def distribution_from_variables(variables: List[PerturbedVariable]) -> chaospy.Distribution:
    """
    :param variables: names of random variables we are perturbing
    :return: chaospy joint distribution encompassing variables
    """

    return chaospy.J(*(variable.chaospy_distribution() for variable in variables))


def perturb_variables(
    variables: List[PerturbedVariable],
    number_perturbations: int = 1,
    sample_rule: SampleRule = SampleRule.RANDOM,
    output_directory: PathLike = None,
) -> xr.DataArray:
    """
    :param variables: names of random variables we are perturbing
    :param number_perturbations: number of perturbations for the ensemble
    :param sample_rule: rule for sampling the joint distribution (e.g., KOROBOV) see SampleRule class and chaospy docs
    :param output_directory: directory where to write the DataArray netcdf file, not written if None
    :return: DataArray of the perturbation_matrix
    """

    distribution = distribution_from_variables(variables)

    # get random samples from joint distribution
    random_sample = distribution.sample(number_perturbations, rule=sample_rule.value)
    if len(variables) == 1:
        random_sample = random_sample.reshape(-1, 1)
    else:
        random_sample = random_sample.T

    run_names = [
        f'{len(variables)}_variable_{sample_rule.value}_{index + 1}'
        for index in range(0, number_perturbations)
    ]
    variable_names = [f'{variable.name}' for variable in variables]

    perturbations = xr.DataArray(
        data=random_sample,
        coords={'run': run_names, 'variable': variable_names},
        dims=('run', 'variable'),
        name='perturbation_matrix',
    )

    if output_directory is not None:
        perturbations.to_netcdf(
            output_directory
            / f'perturbation_matrix_{len(variables)}variables_{sample_rule.value}{number_perturbations}.nc'
        )

    return perturbations
