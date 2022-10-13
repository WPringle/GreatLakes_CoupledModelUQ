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
    

class FVCOM_SWRadiationAbsorption(PerturbedVariable):
    """
    ``FVCOM_SWRadiationAbsorption`` (``FVCOM Shortwave radiation absorption``)
    Uniform distribution on R = [0.74,0.78], then with alpha = (0.74-R)/0.04 -> [0,-1]:
    Z1 = 1.7 + 0.3*alpha -> [1.7,1.4] [m]
    Z2 = 16 + 9.7*alpha -> [16,6.3] [m]
     
    Upper bound is the values given in FVCOM User Manual which is low water quality type III,
    and lower bound is from Paulson & Simpson (1977). https://doi.org/10.1175/1520-0485(1977)007<0952:IMITUO>2.0.CO;2
    which corresponds to type IA (pretty clear water).   

    Definitions:
    R: HEATING_LONGWAVE_PERCTAGE, The fraction of the total shortwave flux associated with the longer wavelength irradiance
    Z1: HEATING_LONGWAVE_LENGTHSCALE, The attenuation depth for the longer wavelength component of shortwave irradiance
    Z2: HEATING_SHORTWAVE_LENGTHSCALE, The attenuation depth for shorter wavelength component of shortwave irradiance 
    """
    
    name = 'FVCOM shortwave radiation absorption'
    variable_distribution = VariableDistribution.UNIFORM
    lower_bound = 0.74,
    upper_bound = 0.78,
    mean = None,
    standard_deviation = None,

    def __init__(self):
        super().__init__(
            unit=None,
        )
    
    @classmethod
    def calc_Z1(self,R) -> float:
        alpha = (0.74-R)/0.04
        Z1 = 1.7 + 0.3*alpha
        return Z1 #[m]

    @classmethod
    def calc_Z2(self,R) -> float:
        alpha = (0.74-R)/0.04
        Z2 = 16 + 9.7*alpha
        return Z2 #[m]


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
