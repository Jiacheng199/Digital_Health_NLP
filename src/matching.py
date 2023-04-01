from read_data import read_data
from writing import writing
from collections import Counter
from snomed_ct import snomed
import nltk
import spacy

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
        self.result_dict = {}
        self.target = ""
        self.nlp = spacy.load("en_ner_bionlp13cg_md")
        self.parent = ""
        self.write_file_name = write_file_name
        self.mod_dict = self.reading.read_his()
        self.statement_check = False
        self.check_ct = False
        

    def mapping(self):
        nltk.download('punkt')
        nltk.download('averaged_perceptron_tagger')
        for finding in self.raw_plain.keys():
            left_mapping_text = self.Non_process_text[self.raw_text_counter]
            self.raw_text_counter += 1
            self.spacy_pos(left_mapping_text)             
            statement_check = False
            self.statement_check = False
            pre_data = self.raw_plain[finding]['processed']
            self.result_dict = {}
            result = ""
            basic_length = 2
            tmp_parent = ""
            self.check_ct = False

            string_for_ct = ""
            for ct_i in pre_data:
                string_for_ct += ct_i[0]
                string_for_ct += " "
            string_for_ct[:-1]
            ct = snomed(string_for_ct[:-1])
            ct_result = ct.ct_search()
            # print(self.result_dict)
            for simgle_word in self.parent:
                tmp_parent += simgle_word.lower()

            if ct_result != "Not Find":
                self.ct_search(ct_result)
                if self.result_dict:
                    for rr in self.result_dict.keys():
                        self.result_mapping.append([left_mapping_text, rr])
                        self.check_ct = True
                        break
            
            # modify
            if finding in self.mod_dict.keys():
                self.result_mapping.append([left_mapping_text, self.mod_dict[finding]]) 
            
            elif self.check_ct == False:
                self.parent = tmp_parent
                statement_check, result_dict = self.find_parent(self.parent,statement_check)
                if len(pre_data) >= 2:
                    for i in range(len(pre_data)):
                        if i + basic_length <= len(pre_data):
                            tmp_finding = pre_data[i:i+basic_length]
                            tmp_string = ""
                            for each_in_combine in tmp_finding:
                                tmp_string += str(each_in_combine[0])
                                tmp_string += " "
                            statement_check, result_dict = self.find_comb(tmp_string[:-1],statement_check)
    
                for target in pre_data:
                    
                    self.target = target[0]
                    self.nltk_mapping()
                    # self.syn_match()
                
                    for i in range(len(self.uil_list)):
                        statement_check, result_dict = self.search(i,statement_check)

                if statement_check:
                    if len(Counter(result_dict)) >= 2 and Counter(result_dict).most_common(2)[0][1] == Counter(result_dict).most_common(2)[1][1]:
                        self.result_mapping.append([left_mapping_text, "Non-Match"])
                    else:
                        self.result_mapping.append([left_mapping_text, Counter(result_dict).most_common(1)[0][0]])

                if not statement_check:
                    result = "Non-Match"
                    self.result_mapping.append([left_mapping_text, result])
            
        # self.writing.writing(self.result_mapping, self.write_file_name)
        return self.writing.writing(self.result_mapping, self.write_file_name)
        
        # return self.result_mapping
    
    def ct_search(self,string_name):
        tmp_string = ""
        for ct_i in string_name:
            tmp_string += ct_i.lower()
        for i in range(len(self.uil_list)):
            str1 = ""
            for word1 in self.uil_list[i][0]:
                str1 += word1.lower()

            if tmp_string == str1:
                # print("111111111111111111111111111111111111111111111111")
                result=self.uil_list[i][0]
                if result in self.result_dict.keys():
                    self.result_dict[result] += 1
                    self.statement_check = True
                else:
                    self.result_dict[result] = 1
                    self.statement_check = True
        

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
            result=self.uil_list[i][0]
            if result in self.result_dict.keys():
                self.result_dict[result] += 1
                statement_check = True

        if self.target in str2:
            result=self.uil_list[i][0]
            if result in self.result_dict.keys():
                statement_check = True
                self.result_dict[result] += 1

        if self.target in str3:
            result=self.uil_list[i][0]
            if result in self.result_dict.keys():
                self.result_dict[result] += 1
                statement_check = True

        if self.target in str4:
            result=self.uil_list[i][0]
            if result in self.result_dict.keys():
                self.result_dict[result] += 1
                statement_check = True
        
        return statement_check, self.result_dict

    def find_parent(self, target, statement_check):
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
                # else:
                #     self.result_dict[result] += 1
            if target in str2:
                statement_check = True
                result=self.uil_list[i][0]
                if result not in self.result_dict.keys():
                    self.result_dict[result] = 1
                # else:
                #     self.result_dict[result] += 1

            if target in str3:
                statement_check = True
                result=self.uil_list[i][0]
                if result not in self.result_dict.keys():
                    self.result_dict[result] = 1
                # else:
                #     self.result_dict[result] += 1

            if target in str4:
                # print("find")
                statement_check = True
                result=self.uil_list[i][0]
                if result not in self.result_dict.keys():
                    self.result_dict[result] = 1
                # else:
                #     self.result_dict[result] += 1
            
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
                
                result=self.uil_list[i][0]
                if result in self.result_dict.keys():
                    statement_check = True
                    self.result_dict[result] += 1
            if target in str2:
                
                result=self.uil_list[i][0]
                if result in self.result_dict.keys():
                    statement_check = True
                    self.result_dict[result] += 1

            if target in str3:
                
                result=self.uil_list[i][0]
                if result in self.result_dict.keys():
                    statement_check = True
                    self.result_dict[result] += 1

            if target in str4:
                # print("find")
                
                result=self.uil_list[i][0]
                if result in self.result_dict.keys():
                    statement_check = True
                    self.result_dict[result] += 1
            
        return statement_check, self.result_dict
    
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


