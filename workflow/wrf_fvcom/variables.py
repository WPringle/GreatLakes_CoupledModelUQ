import chaospy
import pint
from abc import ABC
from enum import Enum
from typing import Union
from pint import Quantity
units = pint.UnitRegistry()


class VariableDistribution(Enum):
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
    variable_distribution: VariableDistribution
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

        if self.variable_distribution == VariableDistribution.GAUSSIAN:
            distribution = chaospy.Normal(mu=self.mean, sigma=self.standard_deviation)
        elif self.variable_distribution == VariableDistribution.UNIFORM:
            distribution = chaospy.Uniform(lower=self.lower_bound, upper=self.upper_bound)
        elif self.variable_distribution == VariableDistribution.DISCRETEUNIFORM:
            distribution = chaospy.DiscreteUniform(lower=self.lower_bound, upper=self.upper_bound)
        else:
            raise ValueError(f'perturbation type {self.variable_distribution} not recognized')

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
    variable_distribution = VariableDistribution.DISCRETEUNIFORM
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
    variable_distribution = VariableDistribution.UNIFORM
    lower_bound = 1.0,
    upper_bound = 10.0,
    mean = None,
    standard_deviation = None,

    def __init__(self):
        super().__init__(
            unit=None,
        )
