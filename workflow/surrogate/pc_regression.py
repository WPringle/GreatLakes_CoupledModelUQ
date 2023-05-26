import numpy as np
import chaospy
import logging
from wrf_fvcom.variables import PerturbedVariable
from wrf_fvcom.perturb import distribution_from_variables
from sklearn.model_selection import LeavePOut
from sklearn.linear_model import LassoCV
from numpoly import polynomial, ndpoly


class DisableLogger:
    def __enter__(self):
        logging.disable(logging.CRITICAL)

    def __exit__(self, exit_type, exit_value, exit_traceback):
        logging.disable(logging.NOTSET)


def make_pc_surrogate_model(
    train_X, train_Y, polynomial_order: int = 1, LPO_p: int = 1,
):

    nens, ndim = train_X.shape
    nens_, neig = train_Y.shape
    assert nens == nens_
    cv = LeavePOut(p=LPO_p)

    variable_transformed = [
        PerturbedVariable.class_from_scheme_name(scheme) for scheme in train_X['scheme']
    ]
    with DisableLogger():
        polynomial_expansion = chaospy.generate_expansion(
            order=polynomial_order,
            dist=distribution_from_variables(variable_transformed, normalize=True),
            rule='three_terms_recurrence',
        )
    reg = LassoCV(fit_intercept=False, cv=cv, selection='random', random_state=666)

    poly_list = [None] * neig
    for mode in range(neig):
        train_yy = train_Y[:, mode]
        with DisableLogger():
            poly_list[mode] = chaospy.fit_regression(
                polynomials=polynomial_expansion,
                abscissas=train_X.T,
                evals=train_yy,
                model=reg,
            )

    surrogate_model = polynomial(poly_list)

    return surrogate_model