import pickle

def picklify(df):
    dt_bytes=pickle.dumps(df)
    return dt_bytes