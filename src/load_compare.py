import pandas as pd
import copy

def read_comp():

    df = pd.read_excel('src/human_match.xlsx', header=None)
    data=df.values
    print(data[0][3])
    return data



# read_comp()