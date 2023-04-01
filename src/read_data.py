import re
import pandas as pd
import copy

class read_data:
    def __init__(self):
        pass
    def read_raw(self, file): 
        example = {}
        with open(file, 'r') as ex:
            while True:
                current_line = ex.readline().strip()
                # print(current_line)
                count_bit = 0
                for i in current_line:
                    count_bit+=1
                    if i == '\t':
                        break
                
                line = current_line[count_bit:]
                # print(line)
                if not line:
                    break
                all_line = re.split('-|,|/| ', line)
                tmp_line = []
                for i in range(len(all_line)):
                    new_line = ""
                    for each_alp in all_line[i]:
                        if ('a' <= each_alp <= 'z' or 'A' <= each_alp <= 'Z' or each_alp == ' ' or '0'<each_alp<'9') and each_alp != ' ':
                            new_line += each_alp.lower()

                    if new_line:
                        tmp_line.append([new_line])
                example[line] = {'processed': tmp_line}
        return example

    def read_return_raw(self, file):
        example = []
        with open(file, 'r') as ex:
            while True:
                current_line = ex.readline().strip()
                if not current_line:
                    break
                count_bit = 0
                for i in current_line:
                    count_bit+=1
                    if i == '\t':
                        break
                
                line = current_line[count_bit:]
                example.append(line)

        return example
    
    def read_uil_list(self):
        df = pd.read_excel('uil.xlsx')
        data=df.values
        return data
    
    def read_comp(self):
        df = pd.read_excel('human_match.xlsx', header=None)
        data=df.values
        # print(data[0][3])
        return data