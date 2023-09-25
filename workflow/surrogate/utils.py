from numpoly import ndpoly

# from numpy import empty


# for optional transformation of outputs prior to sensitivity sampling
def inverse_kl(eigenmodes, eigenvalues, samples, mean_vector):
    neig = eigenvalues.shape[0]
    y_out = sum(
        stack(
            [
                dot(
                    (samples * sqrt(eigenvalues))[:, mode_index, None],
                    eigenmodes[None, mode_index, :],
                )
                for mode_index in range(neig)
            ],
            axis=0,
        ),
        axis=0,
    )
    y_out += mean_vector
    return y_out


def surrogate_model_predict(surrogate_model, X_values, kl_dict=None):
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

    if kl_dict is not None:
        Y_values = inverse_kl(
            kl_dict['eigenmodes'], kl_dict['eigenvalues'], Y_values, kl_dict['mean_vector'],
        )

    return Y_values
