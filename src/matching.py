from read_data import read_data
from writing import writing
from collections import Counter
from snomed_ct import snomed
import spacy
import re

class map_sys:
    def __init__(self, file_name, write_file_name):
        self.file = file_name
        self.reading = read_data()
        self.writing = writing()
        self.raw_plain = self.reading.read_raw(file_name)
        self.uil_list = self.reading.read_uil_list()
        self.result_mapping = []
        self.Non_process_text = self.reading.read_return_raw(file_name)
        self.raw_text_counter = 0
        
        self.target = ""
        self.nlp = spacy.load("en_ner_bionlp13cg_md")
        self.parent = ""
        self.write_file_name = write_file_name
        self.mod_dict = self.reading.read_his()
        self.statement_check = False
        self.check_ct = False
        self.ct_find = False
        self.result_dict = {}
        self.ct_available_check = False
        

    def mapping(self):
        for finding in self.raw_plain.keys():
            # print(finding)
            self.statement_check = False
            self.check_ct = False
            pre_data = self.raw_plain[finding]['processed']
            self.result_dict = {}
            self.target = ""
            self.ct_find = False
            self.ct_available_check = False

            left_mapping_text = self.Non_process_text[self.raw_text_counter]
            self.raw_text_counter += 1
            self.spacy_pos(left_mapping_text)             
            result = ""
            basic_length = 2
            tmp_parent = ""
            
            ct = snomed()
            ct_result = ct.ct_string_process(pre_data)
            for simgle_word in self.parent:
                tmp_parent += simgle_word.lower()

            # if ct_result == "Not Find":
            #     print("Not")
            if ct_result != "Not Find":
                self.ct_find = True
                # print(ct_result)
                self.ct_search(ct_result)
                if self.result_dict:
                    # print(self.result_dict)
                    # print("Find by SNOMED CT")
                    for rr in self.result_dict.keys():
                        self.result_mapping.append([left_mapping_text, rr])
                        self.check_ct = True
                        break
            
            # modify
            if finding in self.mod_dict.keys():
                self.result_mapping.append([left_mapping_text, self.mod_dict[finding]]) 
            
            elif self.check_ct == False:
                self.parent = tmp_parent
                if self.ct_find:
                    self.find_parent(ct_result)
                else:
                    self.find_parent(self.parent)
                if len(pre_data) >= 2:
                    for i in range(len(pre_data)):
                        if i + basic_length <= len(pre_data):
                            tmp_finding = pre_data[i:i+basic_length]
                            tmp_string = ""
                            for each_in_combine in tmp_finding:
                                tmp_string += str(each_in_combine[0])
                                tmp_string += " "
                            self.find_comb(tmp_string[:-1])
                if self.ct_find:
                    for ct_tmp in re.split(' ', ct_result):
                        tmp_low = ""
                        for i_low in ct_tmp:
                            tmp_low += i_low.lower()
                        self.target=tmp_low
                        # print(self.target)
                        self.search(2)
                else:
                    for target in pre_data:
                        # print(target)
                        self.target = target[0]
                        self.search(1)
                # print(Counter(self.result_dict))
                # print(self.ct_find)
                if self.statement_check:
                    # highest uil finding
                    if 2<=len(Counter(self.result_dict)) <=4  and Counter(self.result_dict).most_common(2)[0][1] != Counter(self.result_dict).most_common(2)[1][1]:
                        self.result_mapping.append([left_mapping_text, Counter(self.result_dict).most_common(1)[0][0]])
                        print("highest uil finding")

                    # finding lots of in uil also finding in snomed ct
                    elif len(Counter(self.result_dict)) >=4 and self.ct_find:
                        self.result_mapping.append([left_mapping_text, ct_result])
                        print("finding lots of in uil also finding in snomed ct")
                    
                    # lots of matched but not snomed ct
                    elif len(self.result_dict) > 2 and Counter(self.result_dict).most_common(2)[0][1] == Counter(self.result_dict).most_common(2)[1][1] and not self.ct_find:
                        self.result_mapping.append([left_mapping_text, "Non-Match"])
                        print("lots of matched but not snomed ct")

                    # find on uil but not find in snomed ct
                    elif len(self.result_dict) > 0 and self.ct_find == False:
                        self.result_mapping.append([left_mapping_text, Counter(self.result_dict).most_common(1)[0][0]])
                        print(Counter(self.result_dict).most_common(2)[0][1])
                        print("find on uil")

                    # find in snomed ct
                    elif self.ct_find:
                        self.result_mapping.append([left_mapping_text, ct_result])
                        print("find in snomed ct")
                    else:
                        self.result_mapping.append([left_mapping_text, "Non-Match"])
                
                # find in snomed ct but not relationship with uil
                elif self.ct_find and self.ct_available_check:
                    print(ct_result)
                    self.result_mapping.append([left_mapping_text, ct_result])
                    print("find in snomed ct but relationship with uil")
                else:
                    result = "Non-Match"
                    self.result_mapping.append([left_mapping_text, result])
            
        self.writing.writing(self.result_mapping, self.write_file_name)
        # return self.writing.writing(self.result_mapping, self.write_file_name)
        
        return self.result_mapping
    
    def ct_search(self,string_name):
        tmp_string = ""
        for ct_i in string_name:
            tmp_string += ct_i.lower()
        for i in range(len(self.uil_list)):
            str1 = ""
            for word1 in self.uil_list[i][0]:
                str1 += word1.lower()

            if tmp_string == str1:
                result=self.uil_list[i][0]
                if result in self.result_dict.keys():
                    self.result_dict[result] += 1
                    self.statement_check = True
                else:
                    self.result_dict[result] = 1
                    self.statement_check = True
        

    def search(self, status):
        if status == 1:
            for i in range(len(self.uil_list)):
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
                    result=self.uil_list[i][0]
                    if self.result_dict:
                        if result in self.result_dict.keys():
                            self.result_dict[result] += 1
                            self.statement_check = True

                if self.target in str2:
                    result=self.uil_list[i][0]
                    if self.result_dict:
                        if result in self.result_dict.keys():
                            self.statement_check = True
                            self.result_dict[result] += 1

                if self.target in str3:
                    result=self.uil_list[i][0]
                    if self.result_dict:
                        if result in self.result_dict.keys():
                            self.result_dict[result] += 1
                            self.statement_check = True

                if self.target in str4:
                    result=self.uil_list[i][0]
                    if self.result_dict:
                        if result in self.result_dict.keys():
                            self.result_dict[result] += 1
                            self.statement_check = True
        else:
            for i in range(len(self.uil_list)):
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
                    result=self.uil_list[i][0]
                    self.ct_available_check = True
                    if self.result_dict:
                        if result in self.result_dict.keys():
                            self.result_dict[result] += 1
                            self.statement_check = True

                if self.target in str2:
                    result=self.uil_list[i][0]
                    self.ct_available_check = True
                    if self.result_dict:
                        if result in self.result_dict.keys():
                            self.statement_check = True
                            self.result_dict[result] += 1

                if self.target in str3:
                    result=self.uil_list[i][0]
                    self.ct_available_check = True
                    if self.result_dict:
                        if result in self.result_dict.keys():
                            self.result_dict[result] += 1
                            self.statement_check = True

                if self.target in str4:
                    result=self.uil_list[i][0]
                    self.ct_available_check = True
                    if self.result_dict:
                        if result in self.result_dict.keys():
                            self.result_dict[result] += 1
                            self.statement_check = True



    def find_parent(self, target):
        for i in range(len(self.uil_list)):
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
               
                result=self.uil_list[i][0]
                if result not in self.result_dict.keys():
                    # print(8)
                    self.statement_check = True
                    self.result_dict[result] = 1

            if target in str2:
                result=self.uil_list[i][0]
                if result not in self.result_dict.keys():
                    # print(9)
                    self.statement_check = True
                    self.result_dict[result] = 1

            if target in str3:
                result=self.uil_list[i][0]
                if result not in self.result_dict.keys():
                    # print(10)
                    self.result_dict[result] = 1
                    self.statement_check = True
                    # print(self.result_dict)

            if target in str4:
                result=self.uil_list[i][0]
                if result not in self.result_dict.keys():
                    # print(11)
                    self.statement_check = True
                    self.result_dict[result] = 1

        # print("In parent")
        # print(self.result_dict)
    
    def find_comb(self, target):
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
                
                result=self.uil_list[i][0]
                if self.result_dict:
                    if result in self.result_dict.keys():
                        # print(12)
                        self.statement_check = True
                        self.result_dict[result] += 1
            if target in str2:
                
                result=self.uil_list[i][0]
                if self.result_dict:
                    if result in self.result_dict.keys():
                        # print(13)
                        self.statement_check = True
                        self.result_dict[result] += 1

            if target in str3:
                result=self.uil_list[i][0]
                if self.result_dict:
                    if result in self.result_dict.keys():
                        # print(14)
                        self.statement_check = True
                        self.result_dict[result] += 1

            if target in str4:
                result=self.uil_list[i][0]
                if self.result_dict:
                    if result in self.result_dict.keys():
                        # print(15)
                        self.statement_check = True
                        self.result_dict[result] += 1

        # print("In Combine")
        # print(self.result_dict)
        
    def nltk_mapping(self):
        pass
        # print(nltk.pos_tag(nltk.word_tokenize(self.target)))

    def syn_match(self):
        pass
        # print(synonyms.nearby(self.target))

    def history_dictionary(self):
        pass

    def spacy_pos(self, strings):
        doc = self.nlp(strings)
        for i in doc:
            self.parent = i.head.text
            break


