import joblib
from pathlib import Path

from data_preprocessing import load_vendor_invoice_data, prepare_features_target, split_data
from model_evaluation import (
    linear_model,
    random_forest_model,
    decision_tree_model,
    evaluate_model
)

def main():
    db_path="data/inventory.db"
    model_dir = Path("models")
    model_dir.mkdir(exist_ok=True)

    df= load_vendor_invoice_data(db_path)

    X,y = prepare_features_target(df)
    X_train, X_test, y_train, y_test = split_data(X,y)

    lr_model = linear_model(X_train, y_train)
    dt_model = decision_tree_model(X_train, y_train)
    rf_model = random_forest_model(X_train, y_train)

    result = []
    result.append(evaluate_model(lr_model, X_test, y_test, "Linear Regression"))
    result.append(evaluate_model(dt_model, X_test, y_test, "Decision Tree Regression"))
    result.append(evaluate_model(rf_model, X_test, y_test, "Random Forest Regression"))

    # SELECT BEST MODEL (LOWEST MAE)
    best_model_info = min(result, key=lambda x: x["mae"])
    best_model_name = best_model_info["model_name"]

    best_model = {
        "Linear Regression" : lr_model,
        "Decision Tree Regression":dt_model,
        "Random Forest Regression": rf_model
    }[best_model_name]

    # SAVE THE BEST MODEL
    model_path = model_dir / "predict_freight_model.pkl"
    joblib.dump(best_model,model_path)

    print(f"\nBest model saved: {best_model_name}")
    print(f"Model path: {model_path}")

if __name__ == "__main__":
    main()

