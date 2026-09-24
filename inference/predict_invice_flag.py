from pathlib import Path
import joblib
import pandas as pd

MODEL_PATH = Path(__file__).resolve().parent.parent / "models" / "random_forest_model.pkl"

def load_model(model_path=MODEL_PATH):
    with open(model_path, 'rb') as f:
        model = joblib.load(f)
    return model

def predict_invoice_flag(input_data):
    model = load_model()
    input_df = pd.DataFrame(input_data)
    input_df['flag_invoice'] = model.predict(input_df)
    return input_df

if __name__ == "__main__":
    sample_input = {
        "invoice_quantity": [10, 5, 20],
        "invoice_dollars": [1000, 500, 2000],
        "Freight": [50, 30, 100],
        "total_item_quantity": [10, 5, 20],
        "total_item_dollars": [1000, 500, 2000]
    }
    predictions = predict_invoice_flag(sample_input)
    print(predictions)