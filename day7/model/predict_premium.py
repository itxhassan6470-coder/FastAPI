import pickle
import pandas as pd
#loading model
with open("model/model.pkl","rb") as f:
    model=pickle.load(f)

def predict_premium(input : dict):
    data_frame=pd.DataFrame([input])
    output= model.predict(data_frame)[0]
    return output