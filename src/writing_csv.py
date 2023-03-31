import pandas

def writing(result_mapping, file):
    # print(result_mapping)
    dataframe = pandas.DataFrame(result_mapping, columns=['raw', 'result'])
    dataframe.to_csv(file, index= False)