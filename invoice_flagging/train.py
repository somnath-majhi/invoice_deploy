from modeling_evaluation import train_random_forest, evaluate_classifier
from data_preprocessing import load_invoice_data, apply_labels, split_data, scale_features
import joblib

FEATURES = ['invoice_quantity',
    'invoice_dollars',
    'Freight',
    'total_item_quantity',
    'total_item_dollars'
]

TARGET = 'flag_invoice'

def main():
    db_path="data/inventory.db"

    #load data
    df= load_invoice_data(db_path)
    df= apply_labels(df)

    #Prepare Data
    X_train, X_test, y_train, y_test = split_data(df, FEATURES, TARGET)
    X_train_scaled, X_test_scaled = scale_features(X_train, X_test, 'models/scaler.pkl')

    #Train and Evaluate models
    grid_search = train_random_forest(X_train_scaled, y_train)

    evaluate_classifier(
        grid_search, 
        X_test_scaled, 
        y_test, 
        "Random Forest Classifier"
    )
    #save the model
    joblib.dump(grid_search.best_estimator_, 'models/random_forest_model.pkl')

if __name__ == "__main__":
    main()