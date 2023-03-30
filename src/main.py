from read_raw import read_raw, read_return_raw
from read_uil import read_uil_list
from collections import Counter
import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
raw_plain = read_raw()
uil_list = read_uil_list()
result_mapping = []
Non_process_text = read_return_raw()

def search(i, statement_check):
    str1 = ""
    str2 = ""
    str3 = ""
    str4 = ""
    for word1 in uil_list[i][0]:
        str1 += word1.lower()

    for word1 in uil_list[i][1]:
        str2 += word1.lower()

    for word1 in uil_list[i][2]:
        str3 += word1.lower()

    for word1 in uil_list[i][4]:
        str4 += word1.lower()

    if target in str1:
        # print("find")
        statement_check = True
        result=uil_list[i][0]
        if result not in result_dict.keys():
            result_dict[result] = 1
        else:
            result_dict[result] += 1

    if target in str2:
        # print("find")
        statement_check = True
        result=uil_list[i][0]
        if result not in result_dict.keys():
            result_dict[result] = 1
        else:
            result_dict[result] += 1

    if target in str3:
        # print("find")
        statement_check = True
        result=uil_list[i][0]
        if result not in result_dict.keys():
            result_dict[result] = 1
        else:
            result_dict[result] += 1

    if target in str4:
        # print("find")
        statement_check = True
        result=uil_list[i][0]
        if result not in result_dict.keys():
            result_dict[result] = 1
        else:
            result_dict[result] += 1
    
    return statement_check, result_dict

def find_comb(target, statement_check):
    for i in range(len(uil_list)):
        # print(123)
        str1 = ""
        str2 = ""
        str3 = ""
        str4 = ""
        for word1 in uil_list[i][0]:
            str1 += word1.lower()

        for word1 in uil_list[i][1]:
            str2 += word1.lower()

        for word1 in uil_list[i][2]:
            str3 += word1.lower()

        for word1 in uil_list[i][4]:
            str4 += word1.lower()

        if target in str1:
            statement_check = True
            result=uil_list[i][0]
            if result not in result_dict.keys():
                result_dict[result] = 1
            else:
                result_dict[result] += 1
        if target in str2:
            statement_check = True
            result=uil_list[i][0]
            if result not in result_dict.keys():
                result_dict[result] = 1
            else:
                result_dict[result] += 1

        if target in str3:
            statement_check = True
            result=uil_list[i][0]
            if result not in result_dict.keys():
                result_dict[result] = 1
            else:
                result_dict[result] += 1

        if target in str4:
            # print("find")
            statement_check = True
            result=uil_list[i][0]
            if result not in result_dict.keys():
                result_dict[result] = 1
            else:
                result_dict[result] += 1
        
    return statement_check, result_dict


raw_text_counter = 0
for finding in raw_plain.keys():
    # nltk.word_tokenize()
    left_mapping_text = Non_process_text[raw_text_counter]
    raw_text_counter += 1
    statement_check = False
    pre_data = raw_plain[finding]['processed']
    result_dict = {}
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
                statement_check, result_dict = find_comb(tmp_string[:-1],statement_check)
    # print(Counter(result_dict))
    for target in pre_data:
        # print(nltk.pos_tag(nltk.word_tokenize(target[0])))
        target = target[0]
       
        for i in range(len(uil_list)):
            statement_check, result_dict = search(i,statement_check)

    if statement_check:
        if len(Counter(result_dict)) >= 7 and Counter(result_dict).most_common(1)[0][1] == 1:
            result_mapping.append([left_mapping_text, "Non-Match"])
        else:
            result_mapping.append([left_mapping_text, Counter(result_dict).most_common(1)[0][0]])

    if not statement_check:
        result = "Non-Match"
        result_mapping.append([left_mapping_text, result])
    
    

# print(123)
import pandas
dataframe = pandas.DataFrame(result_mapping, columns=['raw', 'result'])
dataframe.to_csv('example.csv', index= False)
