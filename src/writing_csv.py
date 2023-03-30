import pandas

def writing(result_mapping):
    dataframe = pandas.DataFrame(result_mapping, columns=['raw', 'result'])
    dataframe.to_csv('example.csv', index= False)