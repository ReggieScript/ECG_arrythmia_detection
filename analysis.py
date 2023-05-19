import pandas as pd
import joblib
 

def evaluation(data2predict):
    filename = "modelo_logreg.joblib"
    loaded_model = joblib.load(filename)
    result = loaded_model.predict(data2predict).tolist()
    return result

