import numpy as np

def log2(df):
    '''x -> log_2 (x)'''
    return df.apply(np.log2, axis=0)

def loge(df):
    '''x -> log_e (x)'''
    return df.apply(np.log, axis=0)

def log2p(df):
    '''x -> log_2 (x+1)'''
    df = df.fillna(0)
    return df.apply(lambda x: np.log2(x+1), axis=0)

def logep(df):
    '''x -> log_e (x+1)'''
    df = df.fillna(0)
    return df.apply(np.log1p, axis=0)

def zscore(df):
    '''x -> (x-mean)/std'''
    return df.apply(lambda x: (x-np.mean(x))/np.std(x), axis=0)
    
def median(df):
    '''x -> x/median'''
    return df.apply(lambda x: x/np.median(x), axis=0)
    
def mean(df):
    '''x -> x/mean'''
    return df.apply(lambda x: x/np.mean(x), axis=0)

def none(df):
    '''Do nothing.'''
    return df
