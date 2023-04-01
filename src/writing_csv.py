import pandas

def writing(result_mapping, file):
    # print(result_mapping)
    dataframe = pandas.DataFrame(result_mapping, columns=['raw', 'result'])
    dataframe.to_csv(file, index= False)
    processed_csv = dataframe.to_csv(index=False)
    return processed_csv