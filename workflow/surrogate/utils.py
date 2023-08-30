from numpoly import ndpoly

# from numpy import empty


def surrogate_model_predict(surrogate_model, X_values):
    if type(surrogate_model) is ndpoly:
        Y_values = surrogate_model(*X_values.T).T
    elif type(surrogate_model) == list:
        # Y_values = empty((X_values.shape[0], len(surrogate_model)))
        n_folds = len(surrogate_model)
        for sdx, sm in enumerate(surrogate_model):
            if sdx == 0:
                Y_values = sm.predict(X_values)
            else:
                Y_values += sm.predict(X_values)
            # Y_values[:, sdx] = sm.predict(X_values)
        Y_values /= n_folds
    else:
        Y_values = surrogate_model.predict(X_values)

    return Y_values
