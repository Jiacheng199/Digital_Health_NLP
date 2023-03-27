from read_raw import read_raw
from read_uil import read_uil_list
from collections import Counter

raw_plain = read_raw()
uil_list = read_uil_list()
result_mapping = []
for finding in raw_plain.keys():
    statement_check = False
    pre_data = raw_plain[finding]['processed']
    result_dict = {}
    result = ""
    # print(pre_data)
    # full_match = ""
    # for tmp in pre_data:
    #     full_match += tmp[0]
    #     full_match += " "
    
    # print(full_match- " ")
    for target in pre_data:
        target = target[0]
        # print(target)
        if statement_check:
            break

       
        for i in range(len(uil_list)):
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
                # result_mapping.append([finding, result])
                # break
            elif target in str2:
                # print("find")
                statement_check = True
                result=uil_list[i][0]
                if result not in result_dict.keys():
                    result_dict[result] = 1
                else:
                    result_dict[result] += 1
                # result_mapping.append([finding, result])
                # break
            elif target in str3:
                # print("find")
                statement_check = True
                result=uil_list[i][0]
                if result not in result_dict.keys():
                    result_dict[result] = 1
                else:
                    result_dict[result] += 1
                # result_mapping.append([finding, result])
                # break
            elif target in str4:
                # print("find")
                statement_check = True
                result=uil_list[i][0]
                if result not in result_dict.keys():
                    result_dict[result] = 1
                else:
                    result_dict[result] += 1
                # result_mapping.append([finding, result])
                # break
        # print(result_dict)
        # # print(len(Counter(result_dict)))
        # print(Counter(result_dict).most_common(1)[0][1])
    # print(result_dict)
    if statement_check:
        if len(Counter(result_dict)) >= 7 and Counter(result_dict).most_common(1)[0][1] == 1:
            result_mapping.append([finding, "Non-Match"])
        else:
            result_mapping.append([finding, Counter(result_dict).most_common(1)[0][0]])
        # result_mapping.append([])
    if not statement_check:
        result = "Non-Match"
        result_mapping.append([finding, result])
    


import pandas
# print(raw)
# print(result_mapping)
dataframe = pandas.DataFrame(result_mapping, columns=['raw', 'result'])
dataframe.to_csv('example.csv', index=False)


    # print(result)
    # print(finding)
    # print(targets)
    # if statement_check:
    #     print(result)
    

        # file.write(finding)
        # file.write("           ")
        # if statement_check:
        #     file.write(result)
        # else:
        #     file.write("Not Match")
        # file.write("'/n")
