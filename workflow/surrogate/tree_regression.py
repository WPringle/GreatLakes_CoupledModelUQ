import numpy as np
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import make_scorer
from sklearn.model_selection import cross_val_score, LeaveOneOut, ShuffleSplit, GridSearchCV


def kl_scorer(eigenratio):
    def weighted_rmse(y_true, y_pred):
        if len(y_true.shape) == 2:
            naxis = 1
        else:
            naxis = 0
        wmse = ((y_true - y_pred) ** 2 * eigenratio).sum(axis=naxis)
        return np.mean(np.sqrt(wmse))

    return make_scorer(weighted_rmse, greater_is_better=False)


def make_surrogate_model(
    train_X,
    train_Y,
    eigenratio=1.0,
    regressor: str = 'RF',
    criterion: str = 'squared_error',
    loss: str = 'squared_error',
    n_iter_no_change: int = None,
    validation_fraction: float = 0.20,
):

    nens, ndim = train_X.shape
    nens_, neig = train_Y.shape
    assert nens == nens_
    param_grid = {
        'n_estimators': [ndim, ndim * 2, ndim * 4],
        'max_features': [0.3, 0.6, 0.8, 1.0],
    }
    cv = LeaveOneOut()

    if regressor == 'RF':
        reg = RandomForestRegressor(random_state=666, criterion=criterion)
        scorer = kl_scorer(eigenratio)

        grid_reg = GridSearchCV(reg, param_grid, cv=cv, scoring=scorer)
        grid_reg.fit(train_X, train_Y)
        best_params = grid_reg.best_params_

        surrogate_model = grid_reg.best_estimator_
        surrogate_model.fit(train_X, train_Y)

        cv_score = cross_val_score(surrogate_model, train_X, train_Y, cv=cv, scoring=scorer)

    elif regressor == 'GB':
        reg = GradientBoostingRegressor(
            random_state=666,
            criterion=criterion,
            loss=loss,
            n_iter_no_change=n_iter_no_change,
            validation_fraction=validation_fraction,
        )
        scorer = kl_scorer(1.0)

        surrogate_model = []
        best_params = []
        cv_score = []
        for iout in range(neig):
            train_yy = train_Y[:, iout]
            grid_reg = GridSearchCV(reg, param_grid, cv=cv, scoring=scorer)
            grid_reg.fit(train_X, train_yy)
            best_params.append(grid_reg.best_params_)

            sm = grid_reg.best_estimator_
            sm.fit(train_X, train_yy)

            cv_score.append(cross_val_score(sm, train_X, train_yy, cv=cv, scoring=scorer))

            surrogate_model.append(sm)
    else:
        raise ValueError(f'{regressor} not recognized')

    return surrogate_model, best_params, cv_score


def surrogate_model_predict(surrogate_model, X_values):
    if type(surrogate_model) == list:
        Y_values = np.empty((X_values.shape[0], len(surrogate_model)))
        for sdx, sm in enumerate(surrogate_model):
            Y_values[:, sdx] = sm.predict(X_values)
    else:
        Y_values = surrogate_model.predict(X_values)

    return Y_values
