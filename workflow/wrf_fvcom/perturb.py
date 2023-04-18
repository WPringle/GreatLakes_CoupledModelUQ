import chaospy
import xarray as xr
import numpy as np
from enum import Enum
from os import PathLike
from typing import List
from wrf_fvcom.variables import PerturbedVariable, VariableDistribution
from sklearn.preprocessing import OneHotEncoder


class SampleRule(Enum):
    KOROBOV = 'korobov'
    RANDOM = 'random'
    SOBOL = 'sobol'
    LATINHYPERCUBE = 'latin_hypercube'


class TransformRule(Enum):
    ONEHOT = OneHotEncoder()


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


def transform_perturbation_matrix(
    perturbation_matrix: xr.DataArray,
    rule: TransformRule = TransformRule.ONEHOT,
    scale: bool = True,
) -> xr.DataArray:
    """
    :param perturbation_matrix: DataArray of the perturbation where categorical parameterizations are given in ordinal integers
    :param rule: rule for the transformation, see TransformRule class and sklearn preprocessing class. Only ONEHOT = OneHotEncoder() has been implemented.
    :param scale: scale non-categorical values to [0,1]?
    :return: DataArray of the transformed perturbation_matrix
    """

    variable_names = perturbation_matrix['variable'].values
    runs = perturbation_matrix['run'].values
    # make the matrix for the categorical values
    categorical_matrix = []
    for run in runs:
        pvalues = perturbation_matrix.sel(run=run)
        variable_vector = []
        num_notcat_vars = 0
        for variable_name in variable_names:
            variable = PerturbedVariable.class_from_name(variable_name)
            if variable.variable_distribution == VariableDistribution.DISCRETEUNIFORM:
                scheme_name = variable.return_scheme_name(pvalues.sel(variable=variable_name))
                variable_vector.append(scheme_name)
            else:
                num_notcat_vars += 1
        categorical_matrix.append(variable_vector)

    # transform the categorical values
    enc = rule.value
    variable_matrix_cat = enc.fit_transform(categorical_matrix).toarray()

    scheme_names = np.empty(0)
    for schemes in enc.categories_:
        scheme_names = np.append(scheme_names, schemes)

    # now format into the output with non-categorical added on if present
    variable_matrix = np.empty(
        (variable_matrix_cat.shape[0], variable_matrix_cat.shape[1] + num_notcat_vars)
    )
    vdxc = 0
    css = 0
    cee = 0
    vss = 0
    vee = 0
    for variable_name in variable_names:
        variable = PerturbedVariable.class_from_name(variable_name)
        if variable.variable_distribution == VariableDistribution.DISCRETEUNIFORM:
            lc = len(enc.categories_[vdxc])
            cee = css + lc
            vee = vss + lc
            variable_matrix[:, vss:vee] = variable_matrix_cat[:, css:cee]
            css = cee
            vss = vee
            vdxc += 1
        else:
            pvalues = perturbation_matrix.sel(variable=variable_name)
            if scale:
                pvalues = (pvalues - variable.lower_bound) / (
                    variable.upper_bound - variable.lower_bound
                )
            variable_matrix[:, vss] = pvalues
            scheme_names = np.append(scheme_names, variable_name)
            vss += 1

    return xr.DataArray(
        data=variable_matrix,
        coords={'run': runs, 'variable': scheme_names},
        dims=('run', 'variable'),
        name='transformed_perturbation_matrix',
    )
