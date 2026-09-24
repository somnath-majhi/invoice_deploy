from pathlib import Path
import joblib
import pandas as pd

MODEL_PATH = Path(__file__).resolve().parent.parent / "models" / "predict_freight_model.pkl"

def load_model(model_path=MODEL_PATH):
    with open(model_path, 'rb') as f:
        model = joblib.load(f)
    return model

def predict_freight_cost(input_data):
    model = load_model()
    input_df = pd.DataFrame(input_data)
    X=input_df[list(model.feature_names_in_)]
    input_df['Predict_Freight'] = model.predict(X).round()
    return input_df

if __name__ == "__main__":
    sample_input = {
        "Dollars": [18500,9000,3000,200]
    }
    predictions = predict_freight_cost(sample_input)
    print(predictions)