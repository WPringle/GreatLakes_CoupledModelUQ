import chaospy
import pint
import xarray as xr
from os import PathLike
from abc import ABC
from enum import Enum
from typing import List, Union
from pint import Quantity
units = pint.UnitRegistry()


class PerturbationType(Enum):
    GAUSSIAN = 'gaussian'
    UNIFORM = 'uniform'
    DISCRETEUNIFORM = 'discreteuniform'


class Variable(ABC):
    name: str

    def __init__(
        self, unit: pint.Unit = None,
    ):
        self.unit = unit

    @property
    def unit(self) -> pint.Unit:
        return self._unit

    @unit.setter
    def unit(self, unit: Union[str, pint.Unit]):
        if not isinstance(unit, pint.Unit):
            if unit is None:
                unit = ''
            unit = units.Unit(unit)
        self.__unit = unit


class PerturbedVariable(Variable, ABC):
    perturbation_type: PerturbationType
    lower_bound: Quantity
    upper_bound: Quantity
    mean: Quantity
    standard_deviaton: Quantity

    def __init__(
        self,
        unit: pint.Unit = None,
    ):
        super().__init__(unit=unit)

    @classmethod
    def chaospy_distribution(self) -> chaospy.Distribution:

        if self.perturbation_type == PerturbationType.GAUSSIAN:
            distribution = chaospy.Normal(mu=self.mean, sigma=self.standard_deviation)
        elif self.perturbation_type == PerturbationType.UNIFORM:
            distribution = chaospy.Uniform(lower=self.lower_bound, upper=self.upper_bound)
        elif self.perturbation_type == PerturbationType.DISCRETEUNIFORM:
            distribution = chaospy.DiscreteUniform(lower=self.lower_bound, upper=self.upper_bound)
        else:
            raise ValueError(f'perturbation type {self.perturbation_type} not recognized')

        return distribution


class WRF_PBL_SFCLAY(PerturbedVariable):
    """
    ``WRF_PBL_SFCLAY`` (``WRF Planetary Bounday Layer and Surface Layer Scheme``)
    Discrete uniform distribution on [0,2].
        0: YSU PBL and revised MM5 SFCLAY
        1: MYJ PBL and MOJ SFCLAY
        2: MYNN2.5 PBL and MYNN SFCLAY
    """

    name = 'WRF PBL_SFCLAY'
    perturbation_type = PerturbationType.DISCRETEUNIFORM
    lower_bound=0,
    upper_bound=2,
    mean=None,
    standard_deviation=None,
    
    def __init__(self):
        super().__init__(
            unit=None,
        )
    


class FVCOM_Prandtl(PerturbedVariable):
    """
    ``FVCOM_Prandtl`` (``FVCOM Prandlt Number``)
    Uniform distribution on [1,10] of the horizontal=vertical Prandtl number.
    """
    
    name = 'FVCOM Prandtl'
    perturbation_type = PerturbationType.UNIFORM
    lower_bound = 1.0,
    upper_bound = 10.0,
    mean = None,
    standard_deviation = None,

    def __init__(self):
        super().__init__(
            unit=None,
        )
    

def distribution_from_variables(variables: List[PerturbedVariable]) -> chaospy.Distribution:
    """
    :param variables: names of random variables we are perturbing
    :return: chaospy joint distribution encompassing variables
    """
    
    return chaospy.J(*(variable.chaospy_distribution() for variable in variables))


def perturb_variables(
    variables: List[PerturbedVariable],
    number_perturbations: int = 1,
    sample_rule: str = 'korobov',
    output_directory: PathLike = None,
) -> xr.DataArray:
    """
    :param variables: names of random variables we are perturbing
    :param number_perturbations: number of perturbations for the ensemble
    :param sample_rule: rule for sampling the joint distribution (e.g., korobov), see chaospy docs
    :param output_directory: directory where to write the DataArray netcdf file, not written if None
    :return: DataArray of the perturbation_matrix
    """

    distribution = distribution_from_variables(variables)

    # get random samples from joint distribution
    random_sample = distribution.sample(number_perturbations, rule=sample_rule)
    if len(variables) == 1:
        random_sample = random_sample.reshape(-1, 1)
    else:
        random_sample = random_sample.T
        
    run_names = [
        f'{len(variables)}_variable_{sample_rule}_{index + 1}'
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
            output_directory / f'perturbation_matrix_{len(variables)}_variable_{sample_rule}.nc'
        )

    return perturbations
