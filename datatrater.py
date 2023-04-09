import pandas as pd

def get_airport_iata_code():
    '''
    Returns a list of airport iata codes
    '''

    df = pd.read_csv('airports.csv')
    df = df.dropna(subset=['iata_code'])
    return df['iata_code'].tolist()
