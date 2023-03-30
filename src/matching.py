from read_raw import read_raw, read_return_raw
from read_uil import read_uil_list
from collections import Counter
import nltk

class map_sys:
    def __init__(self, file_name):
        self.file = file_name
        self.raw_plain = read_raw(file_name)
        self.uil_list = read_uil_list()
        self.result_mapping = []
        self.Non_process_text = read_return_raw(file_name)
        self.raw_text_counter = 0
        self.result_dict = {}
        self.target = ""
        

    def mapping(self):
        nltk.download('punkt')
        nltk.download('averaged_perceptron_tagger')

        for finding in self.raw_plain.keys():
            # nltk.word_tokenize()
            left_mapping_text = self.Non_process_text[self.raw_text_counter]
            self.raw_text_counter += 1
            statement_check = False
            pre_data = self.raw_plain[finding]['processed']
            self.result_dict = {}
            result = ""
            basic_length = 2
            if len(pre_data) >= 2:
                for i in range(len(pre_data)):
                    if i + basic_length <= len(pre_data):
                        tmp_finding = pre_data[i:i+basic_length]
                        tmp_string = ""
                        for each_in_combine in tmp_finding:
                            tmp_string += str(each_in_combine[0])
                            tmp_string += " "
                        statement_check, result_dict = self.find_comb(tmp_string[:-1],statement_check)
            # print(Counter(result_dict))
            for target in pre_data:
                # print(nltk.pos_tag(nltk.word_tokenize(target[0])))
                self.target = target[0]
            
                for i in range(len(self.uil_list)):
                    statement_check, result_dict = self.search(i,statement_check)

            if statement_check:
                if len(Counter(result_dict)) >= 7 and Counter(result_dict).most_common(1)[0][1] == 1:
                    self.result_mapping.append([left_mapping_text, "Non-Match"])
                else:
                    self.result_mapping.append([left_mapping_text, Counter(result_dict).most_common(1)[0][0]])

            if not statement_check:
                result = "Non-Match"
                self.result_mapping.append([left_mapping_text, result])
            
            

        # print(123)
        import pandas
        dataframe = pandas.DataFrame(self.result_mapping, columns=['raw', 'result'])
        dataframe.to_csv('example.csv', index= False)

        

    def search(self,i, statement_check):
        str1 = ""
        str2 = ""
        str3 = ""
        str4 = ""
        for word1 in self.uil_list[i][0]:
            str1 += word1.lower()

        for word1 in self.uil_list[i][1]:
            str2 += word1.lower()

        for word1 in self.uil_list[i][2]:
            str3 += word1.lower()

        for word1 in self.uil_list[i][4]:
            str4 += word1.lower()

        if self.target in str1:
            # print("find")
            statement_check = True
            result=self.uil_list[i][0]
            if result not in self.result_dict.keys():
                self.result_dict[result] = 1
            else:
                self.result_dict[result] += 1

        if self.target in str2:
            # print("find")
            statement_check = True
            result=self.uil_list[i][0]
            if result not in self.result_dict.keys():
                self.result_dict[result] = 1
            else:
                self.result_dict[result] += 1

        if self.target in str3:
            # print("find")
            statement_check = True
            result=self.uil_list[i][0]
            if result not in self.result_dict.keys():
                self.result_dict[result] = 1
            else:
                self.result_dict[result] += 1

        if self.target in str4:
            # print("find")
            statement_check = True
            result=self.uil_list[i][0]
            if result not in self.result_dict.keys():
                self.result_dict[result] = 1
            else:
                self.result_dict[result] += 1
        
        return statement_check, self.result_dict

    def find_comb(self, target, statement_check):
        for i in range(len(self.uil_list)):
            # print(123)
            str1 = ""
            str2 = ""
            str3 = ""
            str4 = ""
            for word1 in self.uil_list[i][0]:
                str1 += word1.lower()

            for word1 in self.uil_list[i][1]:
                str2 += word1.lower()

            for word1 in self.uil_list[i][2]:
                str3 += word1.lower()

            for word1 in self.uil_list[i][4]:
                str4 += word1.lower()

            if target in str1:
                statement_check = True
                result=self.uil_list[i][0]
                if result not in self.result_dict.keys():
                    self.result_dict[result] = 1
                else:
                    self.result_dict[result] += 1
            if target in str2:
                statement_check = True
                result=self.uil_list[i][0]
                if result not in self.result_dict.keys():
                    self.result_dict[result] = 1
                else:
                    self.result_dict[result] += 1

            if target in str3:
                statement_check = True
                result=self.uil_list[i][0]
                if result not in self.result_dict.keys():
                    self.result_dict[result] = 1
                else:
                    self.result_dict[result] += 1

            if target in str4:
                # print("find")
                statement_check = True
                result=self.uil_list[i][0]
                if result not in self.result_dict.keys():
                    self.result_dict[result] = 1
                else:
                    self.result_dict[result] += 1
            
        return statement_check, self.result_dict


