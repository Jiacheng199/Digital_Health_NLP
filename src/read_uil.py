import pandas as pd
import copy

def read_uil_list():

    df = pd.read_excel('src/uil.xlsx')
    data=df.values
    return data


# print(read_uil_list())