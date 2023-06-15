from numpoly import ndpoly
from numpy import empty
from pyapprox.surrogates.polychaos.gpc import PolynomialChaosExpansion

def surrogate_model_predict(surrogate_model, X_values):
    if type(surrogate_model) is ndpoly:
        Y_values = surrogate_model(*X_values.T).T
    elif type(surrogate_model) == list:
        Y_values = empty((X_values.shape[0], len(surrogate_model)))
        for sdx, sm in enumerate(surrogate_model):
            Y_values[:, sdx] = sm.predict(X_values)
    elif type(surrogate_model) is PolynomialChaosExpansion:
        Y_values = surrogate_model.value(X_values.T)
    else:
        Y_values = surrogate_model.predict(X_values)

    return Y_values
