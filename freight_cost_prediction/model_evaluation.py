from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error,root_mean_squared_error,r2_score

def linear_model(X_train, y_train):
    model=LinearRegression()
    model.fit(X_train, y_train)
    return model

def decision_tree_model(X_train, y_train, max_depth=4):
    model=DecisionTreeRegressor(
        max_depth=max_depth, random_state=42
    )
    model.fit(X_train, y_train)
    return model

def random_forest_model(X_train, y_train, max_depth=4):
    model= RandomForestRegressor(
        max_depth=max_depth, random_state=42
    )
    model.fit(X_train, y_train)
    return model

def evaluate_model(model, X_test, y_test, model_name: str) -> dict:
    preds = model.predict(X_test)

    mae=mean_absolute_error(y_test, preds)
    rmse = root_mean_squared_error(y_test, preds)
    r2 = r2_score(y_test, preds)*100

    print(f"\n{model_name} Performance:")
    print(f"MAE : {mae:.2f}")
    print(f"RMSE : {rmse:.2f}")
    print(f"R : {r2:.2f}%")

    return {
        "model_name" : model_name,
        "mae":mae,
        "rmse":rmse,
        "r2":r2
    }