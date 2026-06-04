import joblib 
from pathlib import Path


clf = None
preproc = None

def load_model():
    global clf
    
    #loading the model
    path = ("ml_model/stud_performance_classifier.joblib")
    with open(path, "rb") as f:
        clf = joblib.load(f)
    



def load_preprocessor():
    global preproc

    #loading the preprocessor for SHAP analysis
    path = ("ml_model/stud_performance_preprocessor.joblib")
    with open(path, "rb") as g:
        preproc = joblib.load(g)

def get_model():
    return clf

def get_preprocessor():
    return preproc