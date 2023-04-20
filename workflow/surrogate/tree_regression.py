import numpy as np
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import make_scorer
from sklearn.model_selection import cross_val_score, LeaveOneOut, ShuffleSplit, GridSearchCV


def kl_scorer(eigenratio):
    def weighted_rmse(y_true, y_pred):
        wmse = ((y_true - y_pred) ** 2 * eigenratio).sum(axis=1)
        return np.mean(np.sqrt(wmse))

    return make_scorer(weighted_rmse, greater_is_better=False)


def make_surrogate_model(
    train_X, train_Y, eigenratio=1.0, regressor: str = 'RF', criterion: str = 'squared_error',
):

    if regressor == 'RF':
        reg = RandomForestRegressor(random_state=666, criterion=criterion)
    elif regressor == 'GB':
        reg = GradientBoostingRegressor(random_state=666)
        # GB_KL_model = []
        # for iout in range(neig):
        #    reg = GradientBoostingRegressor(n_estimators=n_estimators,max_features=0.3,random_state=666)
        #    reg.fit(variable_matrix[1::], kl_xi[1::,iout])
        #    GB_KL_model.append(reg)
    else:
        raise ValueError(f'{regressor} not recognized')

    nens, ndim = train_X.shape
    param_grid = {
        'n_estimators': [ndim, ndim * 2, ndim * 4],
        'max_features': [0.3, 0.6, 0.8, 1.0],
    }
    cv = LeaveOneOut()
    scorer = kl_scorer(eigenratio)
    grid_reg = GridSearchCV(reg, param_grid, cv=cv, scoring=scorer)
    grid_reg.fit(train_X, train_Y)

    surrogate_model = grid_reg.best_estimator_
    surrogate_model.fit(train_X, train_Y)

    cv_score = cross_val_score(surrogate_model, train_X, train_Y, cv=cv, scoring=scorer)

    return surrogate_model, grid_reg.best_params_, cv_score
