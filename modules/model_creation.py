from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import RandomizedSearchCV
import xgboost as xgb
import math
from sklearn.metrics import mean_absolute_error, mean_squared_error, mean_squared_log_error, r2_score
import matplotlib.pyplot as plt

def metrics(model, X_train, X_test, y_train, y_test):
    predict_train = model.predict(X_train)
    predict_test = model.predict(X_test)

    print(f'Mean Absolute Error = {mean_absolute_error(y_train,predict_train)}')
    print(f'Mean Squared Error = {mean_squared_error(y_train,predict_train)}')
    print(f'Root Mean Squared Error = {math.sqrt(mean_squared_error(y_train,predict_train))}')
    print(f'r2 = {r2_score(y_train,predict_train)}')

    print()
    print(f'Mean Absolute Error = {mean_absolute_error(y_test,predict_test)}')
    print(f'Mean Squared Error = {mean_squared_error(y_test,predict_test)}')
    print(f'Root Mean Squared Error = {math.sqrt(mean_squared_error(y_test,predict_test))}')
    print(f'r2 = {r2_score(y_test,predict_test)}')

def feature_importances(model, dataset, X_train):
    print(dataset.columns)
    importances = model.feature_importances_
    plt.figure()
    plt.title("Feature importances")
    ax = plt.barh(range(len(X_train.columns)),importances,align="center")
    plt.xlabel('Average decrease in MSE')

def model_creation(dataset, n, model, n_estimators_list, max_depth_list, learning_rate_list=[0.01, 0.011, 0.012, 0.013]):
    X = dataset.iloc[:, :n]
    y = dataset.iloc[:, n]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25)

    if model=='rf':
        random_grid = {'n_estimators': n_estimators_list,
                    'max_depth': max_depth_list
        }
        goals_rf = RandomizedSearchCV(RandomForestRegressor(), param_distributions=random_grid, cv=5, n_iter=10,n_jobs=-1)
        goals_rf.fit(X_train, y_train)
        print(goals_rf.best_params_)
        goals_rf = RandomForestRegressor(n_estimators=goals_rf.best_params_['n_estimators'], max_depth=goals_rf.best_params_['max_depth'])
        goals_rf.fit(X_train, y_train)

        metrics(goals_rf, X_train, X_test, y_train, y_test)
        feature_importances(goals_rf, dataset, X_train)
        return goals_rf

    if model == 'xgb':
        regressor=xgb.XGBRegressor()
        param_grid = {"max_depth": max_depth_list,
                    "n_estimators": n_estimators_list,
                    "learning_rate": learning_rate_list}
        goals_xgb = RandomizedSearchCV(regressor, param_distributions=param_grid, cv=5, n_iter=10,n_jobs=-1)
        goals_xgb.fit(X_train, y_train)
        print(goals_xgb.best_params_)
        goals_xgb = xgb.XGBRegressor(n_estimators=goals_xgb.best_params_['n_estimators'], max_depth=goals_xgb.best_params_['max_depth'], learning_rate=goals_xgb.best_params_['learning_rate'])
        goals_xgb.fit(X_train.values, y_train)

        metrics(goals_xgb, X_train, X_test, y_train, y_test)
        feature_importances(goals_xgb, dataset, X_train)
        return goals_xgb