import pandas

class writing:
    def __init__(self):
        pass

    def writing(self, result_mapping, file):
        dataframe = pandas.DataFrame(result_mapping, columns=['raw', 'result', 'Flag'])
        dataframe.to_csv(file, index= False)
        processed_csv = dataframe.to_csv(index=False)
        return processed_csv