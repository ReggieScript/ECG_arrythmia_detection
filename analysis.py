import pandas as pd
import joblib
 

def evaluation(data2predict):
    filename = "modelo_logreg.joblib"
    loaded_model = joblib.load(filename)
    result = loaded_model.predict(data2predict).tolist()
    probability = loaded_model.predict_proba(data2predict)[:,1]

    #probability filter

    probab_df = pd.DataFrame()
    probab_df['probab'] = probability
    probab_df['result'] = result

    probab_df[(probab_df["probab"] < 0.7) & (probab_df["result"] == 1)] = 0

    result = probab_df["result"].to_list()

    return result
