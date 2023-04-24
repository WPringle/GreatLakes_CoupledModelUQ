from wrf_fvcom.perturb import (
    parameter_dict_to_perturbation_vector,
    transform_perturbation_matrix,
)
from surrogate.tree_regression import surrogate_model_predict
from sklearn.metrics import r2_score
from skopt import gp_minimize
from skopt.utils import use_named_args
from numpy import isnan


def gamma2_score(obs, model):
    gamma2 = (model - obs).var() / obs.var()
    return gamma2


def run_bayesian_optimization(
    surrogate_model,
    observed_data,
    perturbation_matrix,
    score_type: str = 'r2',
    n_initial_points=50,
):

    input_space = transform_perturbation_matrix(perturbation_matrix, output_type='space')

    @use_named_args(input_space)
    def objective(**params):
        print(params)

        # process the parameter inputs for surrogate model entry
        parameter_vector = parameter_dict_to_perturbation_vector(params)
        # replace the first matrix entry of the dummy matrix
        perturbation_matrix[0, :] = parameter_vector.values
        variable_matrix = transform_perturbation_matrix(perturbation_matrix)
        variable_vector = variable_matrix.isel(run=0).values.reshape(1, -1)

        # predict using our surrogate model
        predicted_data = surrogate_model_predict(surrogate_model, variable_vector).flatten()

        # get score
        if score_type == 'r2':
            gp_score = 1.0 - r2_score(observed_data, predicted_data)  # minimize 1-r^2
        elif score_type == 'gamma2':
            gp_score = +gamma2_score(observed_data, predicted_data)  # minimize gamma^2
        else:
            raise ValueError(f'{score_type} not recognized.')

        if isnan(gp_score):
            raise ValueError('nans in score')
        else:
            return gp_score

    posterior_gp = gp_minimize(
        objective,
        input_space,
        n_calls=n_initial_points + 50,
        random_state=666,
        initial_point_generator='lhs',
        n_initial_points=n_initial_points,
    )

    return posterior_gp
