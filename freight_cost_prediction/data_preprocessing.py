import sqlite3
import pandas as pd
from sklearn.model_selection import train_test_split

# LOAD VENDOR INVOICIE DATA FROM SQLite DATABASE
def load_vendor_invoice_data(db_path: str):
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query("SELECT * FROM vendor_invoice",conn)
    conn.close()
    return df

#SELECT FEATURES AND TARGET VARIABLE
def prepare_features_target(db:pd.DataFrame):
    X=db[["Dollars"]]
    y = db['Freight']
    return X,y
    
#SPLIT DATASET INTO TRAIN AND TEST SETS
def split_data(X,y, test_size=0.2, random_state=42):
    return train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )
