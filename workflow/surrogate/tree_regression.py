import numpy as np
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from xgboost import XGBRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import make_scorer
from sklearn.model_selection import cross_val_score, LeaveOneOut, LeavePOut, GridSearchCV


def kl_scorer(eigenratio, metric=False):
    def weighted_rmse(y_true, y_pred):
        if len(y_true.shape) == 1 and len(y_pred.shape) == 2:
            y_true = y_true.reshape(y_pred.shape)
        if len(y_true.shape) == 2:
            naxis = 1
        else:
            naxis = 0
        wmse = ((y_true - y_pred) ** 2 * eigenratio).sum(axis=naxis)
        return np.mean(np.sqrt(wmse))

    if metric:
        return weighted_rmse
    else:
        return make_scorer(weighted_rmse, greater_is_better=False)


def make_tree_surrogate_model(
    train_X,
    train_Y,
    eigenratio=1.0,
    regressor: str = 'RF',
    criterion: str = 'squared_error',
    loss: str = 'squared_error',
    combined_model: bool = True,
    n_iter_no_change: int = None,
    validation_fraction=0.20,
    LPO_p: int = 1,
):

    nens, ndim = train_X.shape
    nens_, neig = train_Y.shape
    assert nens == nens_
    param_grid = {
        'n_estimators': [ndim, ndim * 2, ndim * 4],
        #        'max_features': [0.1, 0.3, 0.6, 1.0],
    }
    cv = LeavePOut(p=LPO_p)

    if regressor == 'RF':
        reg = RandomForestRegressor(random_state=666, criterion=criterion)
    elif regressor == 'DT':
        param_grid = {
            #'ccp_alpha': [0, 0.025, 0.05, 0.1, 0.25, 0.5],
            'max_features': [0.1, 0.3, 0.6, 1.0]
        }
        reg = DecisionTreeRegressor(random_state=666, criterion=criterion)
    elif regressor == 'GB':
        reg = GradientBoostingRegressor(
            random_state=666,
            criterion=criterion,
            loss=loss,
            n_iter_no_change=n_iter_no_change,
            validation_fraction=validation_fraction,
        )
        combined_model = False  # must be false for GB
    elif regressor == 'XG':
        if combined_model:
            metric = kl_scorer(eigenratio, metric=True)
        else:
            metric = kl_scorer(1.0, metric=True)

        surrogate_model = XGBRegressor(
            n_estimators=ndim,
            tree_method='exact',
            random_state=666,
            early_stopping_rounds=n_iter_no_change,
            eval_metric=metric,
        )

        surrogate_model.fit(train_X, train_Y, eval_set=validation_fraction)
        best_params = []
        cv_score = []
        return surrogate_model, best_params, cv_score
    else:
        raise ValueError(f'{regressor} not recognized')

    if combined_model:
        scorer = kl_scorer(eigenratio)

        grid_reg = GridSearchCV(reg, param_grid, cv=cv, scoring=scorer)
        grid_reg.fit(train_X, train_Y)
        best_params = grid_reg.best_params_

        surrogate_model = grid_reg.best_estimator_
        surrogate_model.fit(train_X, train_Y)

        cv_score = cross_val_score(surrogate_model, train_X, train_Y, cv=cv, scoring=scorer)

    else:
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

    return surrogate_model, best_params, cv_score
