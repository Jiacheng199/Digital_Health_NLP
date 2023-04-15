import pandas

class writing:
    def __init__(self):
        pass

    def writing(self, result_mapping, file, pending_check):
        dataframe = pandas.DataFrame(result_mapping, columns=['raw', 'result', 'Flag'])
        dataframe.to_csv(file, index= False)
        processed_csv = dataframe.to_csv(index=False)
        pending_check = True
        return processed_csv, pending_check
        # return processed_csv