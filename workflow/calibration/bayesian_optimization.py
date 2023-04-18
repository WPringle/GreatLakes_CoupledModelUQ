from wrf_fvcom.peturb import (
    parameter_dict_to_perturbation_vector,
    transform_perturbation_matrix,
)
from sklearn.metrics import r2_score
from skopt import gp_minimize
from skopt.utils import use_named_args


def gamma2_score(obs, model):
    gamma2 = (model - obs).var() / obs.var()
    return gamma2


def run_bayesian_optimization(surrogate_model, observed_data, input_space, score_type):
    @use_named_args(input_space)
    def objective(**params):
        print(params)

        # process the parameter inputs for surrogate model entry
        parameter_vector = parameter_dict_to_perturbation_vector(params)
        variable_vector = transform_perturbation_matrix(perturbation_vector)

        # predict using our surrogate model
        predicted_data = surrogate_model(*variable_vector.T).flatten()

        # get score
        if score_type == 'r2':
            gp_score = 1.0 - r2_score(observed_data, predicted_data)  # minimize 1-r^2
        elif score_type == 'gamma2':
            gp_score = +gamma2_score(observed_data, predicted_data)  # minimize gamma^2
        else:
            raise ValueError(f'{score_type} not recognized.')

        if np.isnan(gp_score):
            return 1000
        else:
            return gp_score

    posterior_gp = gp_minimize(
        objective,
        input_space,
        n_calls=n_points + 50,
        random_state=666,
        initial_point_generator='lhs',
        n_initial_points=n_points,
    )
