from read_data import read_data
from writing import writing
from collections import Counter
import spacy
import re
from ct_test import snomed_ct_dict
from autoModel import autoModel
import editdistance


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
        self.new_dict_incl_distance = []
        
    def mapping(self):
        ct_result = snomed_ct_dict(self.file)
        # print(ct_result)
        finding_id = 0
        # autoModel(self.mod_dict,self.Non_process_text)
        for finding in self.raw_plain.keys():
            # print(finding)
            self.result_dict = []
            # curr_ct = ct_result[left_mapping_text]
            finding_id += 1
            # print(finding)
            self.statement_check = False
            self.check_ct = False
            pre_data = self.raw_plain[finding]['processed']
            self.result_dict = {}
            self.target = ""
            self.ct_find = False
            self.ct_available_check = False

            left_mapping_text = self.Non_process_text[self.raw_text_counter]
            curr_ct = ct_result[left_mapping_text]
            self.raw_text_counter += 1
            self.spacy_pos(left_mapping_text)             
            result = ""
            basic_length = 2
            tmp_parent = ""
            
            for simgle_word in self.parent:
                tmp_parent += simgle_word.lower()

            # print(curr_ct)
            if curr_ct != "Not Find":
                self.ct_find = True
                self.ct_search(curr_ct)
                if self.result_dict:
                    for rr in self.result_dict.keys():
                        # self.result_mapping.append([left_mapping_text, rr, "SNOMED CT"])
                        self.check_ct = True
                        break
            
            # modify
            if finding in self.mod_dict.keys():
                self.result_mapping.append([left_mapping_text, self.mod_dict[finding], "UIL"]) 
                self.new_dict_incl_distance.append([left_mapping_text, self.mod_dict[finding], 0, candid_result_in_condition, [curr_ct], "UIL"])
            else:
                self.parent = tmp_parent
                if self.ct_find:
                    self.find_parent(curr_ct)
                else:
                    self.find_parent(self.parent)
                # tmp_string_left = ""
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
                    for ct_tmp in re.split(' ', curr_ct):
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
     
                candid_result_in_condition = []
                if self.statement_check:

                    
                    # best, score = autoModel(left_mapping_text, self.result_dict)
                    # print(best)
                    # print(score)
                    # if score >= 0.85:
                    #     self.result_mapping.append([left_mapping_text, best, "UIL"])
                    # else:
                    #     self.result_mapping.append([left_mapping_text, "Non-Match", "UIL"])
                    # highest uil finding
                    # print([curr_ct])
                    
                    if len(self.result_dict) > 0:
                        for find_key_in_condition in self.result_dict.keys():
                            candid_result_in_condition.append(find_key_in_condition)

                    if len(self.result_dict)>= 2 and Counter(self.result_dict).most_common(2)[0][1] != Counter(self.result_dict).most_common(2)[1][1]:
                        na, dist = self.cal_distance(pre_data)
                        # print("here")
                        if self.ct_find:
                           
                            self.new_dict_incl_distance.append([left_mapping_text, na, dist, candid_result_in_condition, [curr_ct], "UIL"])
                            self.result_mapping.append([left_mapping_text,na, "UIL"])
                        else:
                            self.new_dict_incl_distance.append([left_mapping_text, na, dist, candid_result_in_condition, [], "UIL"])
                            self.result_mapping.append([left_mapping_text,na, "UIL"])
                        
                        # print("highest uil finding")

                    # finding lots of in uil also finding in snomed ct
                    elif len(Counter(self.result_dict)) >=4 and self.ct_find:
                        # base_in_condition = self.re_organ(pre_data)
                        # dist = self.quick_edit_distance(base_in_condition, curr_ct)
                        na, dist = self.cal_distance(pre_data)
                        self.new_dict_incl_distance.append([left_mapping_text, na, dist, candid_result_in_condition, [curr_ct], "UIL"])
                        self.result_mapping.append([left_mapping_text,na, "UIL"])
                        # self.result_mapping.append([left_mapping_text, curr_ct, "SNOMED CT"])
                        # print("finding lots of in uil also finding in snomed ct")
                    
                    # lots of matched but not snomed ct
                    elif len(self.result_dict) > 2 and Counter(self.result_dict).most_common(2)[0][1] == Counter(self.result_dict).most_common(2)[1][1] and not self.ct_find:
                       
                        na, dist = self.cal_distance(pre_data)
                        self.new_dict_incl_distance.append([left_mapping_text, "Non-Match", 999, candid_result_in_condition, [], "UIL"])
                        self.result_mapping.append([left_mapping_text, "Non-Match", "UIL"])
                        # print("lots of matched but not snomed ct")

                    # find on uil but not find in snomed ct
                    elif len(self.result_dict) > 0 and self.ct_find == False:
                        # print("here")
                        na, dist = self.cal_distance(pre_data)
                        n, s = autoModel([left_mapping_text, Counter(self.result_dict).most_common(1)[0][0]])
                        # print(s)
                        # print(n)
                        # print(na)
                        # print(dist)
                        if float(s) > 0.5:
                            self.new_dict_incl_distance.append([left_mapping_text, na, dist, candid_result_in_condition, [], "UIL"])
                            self.result_mapping.append([left_mapping_text, na, "UIL"])
                        else:
                        
                            if len(self.result_dict) == 1 and dist <= 15:
                                self.new_dict_incl_distance.append([left_mapping_text, na, dist, candid_result_in_condition, [], "UIL"])
                                self.result_mapping.append([left_mapping_text, na, "UIL"])
                            else:
                                self.new_dict_incl_distance.append([left_mapping_text, "Non-Match", 999, candid_result_in_condition, [], "UIL"])
                                self.result_mapping.append([left_mapping_text,"Non-Match", "UIL"])

                            
                        # print(Counter(self.result_dict).most_common(2)[0][1])
                        # print("find on uil")

                    # find in snomed ct
                    elif len(self.result_dict) > 0 and self.ct_find:
                        na, dist = self.cal_distance(pre_data)
                        if dist <=3:
                            self.new_dict_incl_distance.append([left_mapping_text, na, dist, candid_result_in_condition, [curr_ct], "UIL"])
                            self.result_mapping.append([left_mapping_text, na, "UIL"])
                        else:
                            base_in_condition = self.re_organ(pre_data)
                            dist = self.quick_edit_distance(base_in_condition, curr_ct)
                            self.new_dict_incl_distance.append([left_mapping_text, curr_ct, dist, candid_result_in_condition, [curr_ct], "SNOMED CT"])
                            self.result_mapping.append([left_mapping_text,curr_ct, "SNOMED CT"])
                        # print(na)
                        # print(dist)
                        # print("here")
                    elif self.ct_find:
                        base_in_condition = self.re_organ(pre_data)
                        dist = self.quick_edit_distance(base_in_condition, curr_ct)
                        self.new_dict_incl_distance.append([left_mapping_text, curr_ct, dist, candid_result_in_condition, [curr_ct], "SNOMED CT"])
                        self.result_mapping.append([left_mapping_text, curr_ct, "SNOMED CT"])
                        # print("find in snomed ct")
                    else:
                        # print("Mapping")
                        base_in_condition = self.re_organ(pre_data)
                        # dist = self.quick_edit_distance(base_in_condition, curr_ct)
                        self.new_dict_incl_distance.append([left_mapping_text, "Non-Match", 9999, candid_result_in_condition, [], "UIL"])
                        self.result_mapping.append([left_mapping_text, "Non-Match", "UIL"])
                
                # find in snomed ct but not relationship with uil
                elif self.ct_find and self.ct_available_check:
                    # print(curr_ct)
                    base_in_condition = self.re_organ(pre_data)
                    dist = self.quick_edit_distance(base_in_condition, curr_ct)
                    self.new_dict_incl_distance.append([left_mapping_text, curr_ct, dist, candid_result_in_condition, [curr_ct], "SNOMED CT"])
                    self.result_mapping.append([left_mapping_text, curr_ct, "SNOMED CT"])
                    # print("find in snomed ct but relationship with uil")
                else:
                    
                    na, dist = self.cal_distance(pre_data)
                    result = "Non-Match"
                    self.new_dict_incl_distance.append([left_mapping_text, "Non-Match", 999, candid_result_in_condition, [], "UIL"])
                    self.result_mapping.append([left_mapping_text, result, "UIL"])
                # print(123)
        
        # self.writing.data_list_to_csv(self.new_dict_incl_distance, self.write_file_name)
        # self.writing.writing_to_json(self.new_dict_incl_distance, self.write_file_name)
        # return 0
        return self.writing.writing(self.result_mapping, self.write_file_name)
        
        # return self.result_mapping
    
    def ct_search(self,string_name):
        tmp_string = ""
        for ct_i in string_name:
            tmp_string += ct_i.lower()
        for i in range(len(self.uil_list)):
            if tmp_string == self.uil_list[i][0]:
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
                if self.target in self.uil_list[i][0]:
                    result=self.uil_list[i][0]
                    if self.result_dict:
                        if result in self.result_dict.keys():
                            self.result_dict[result] += 1
                            self.statement_check = True

                if self.target in self.uil_list[i][1]:
                    result=self.uil_list[i][0]
                    if self.result_dict:
                        if result in self.result_dict.keys():
                            self.statement_check = True
                            self.result_dict[result] += 1

                if self.target in self.uil_list[i][2]:
                    result=self.uil_list[i][0]
                    if self.result_dict:
                        if result in self.result_dict.keys():
                            self.result_dict[result] += 1
                            self.statement_check = True

                if self.target in self.uil_list[i][4]:
                    result=self.uil_list[i][0]
                    if self.result_dict:
                        if result in self.result_dict.keys():
                            self.result_dict[result] += 1
                            self.statement_check = True
        else:
            for i in range(len(self.uil_list)):

                if self.target in self.uil_list[i][0]:
                    result=self.uil_list[i][0]
                    self.ct_available_check = True
                    if self.result_dict:
                        if result in self.result_dict.keys():
                            self.result_dict[result] += 1
                            self.statement_check = True

                if self.target in self.uil_list[i][1]:
                    result=self.uil_list[i][0]
                    self.ct_available_check = True
                    if self.result_dict:
                        if result in self.result_dict.keys():
                            self.statement_check = True
                            self.result_dict[result] += 1

                if self.target in self.uil_list[i][2]:
                    result=self.uil_list[i][0]
                    self.ct_available_check = True
                    if self.result_dict:
                        if result in self.result_dict.keys():
                            self.result_dict[result] += 1
                            self.statement_check = True

                if self.target in self.uil_list[i][4]:
                    result=self.uil_list[i][0]
                    self.ct_available_check = True
                    if self.result_dict:
                        if result in self.result_dict.keys():
                            self.result_dict[result] += 1
                            self.statement_check = True



    def find_parent(self, target):
        # print(target)
        tmp = ""
        for i in target:
            tmp += i.lower()
        # print(tmp)
        target = tmp
        for i in range(len(self.uil_list)):

            if target in self.uil_list[i][0]:
               
                result=self.uil_list[i][0]
                if result not in self.result_dict.keys():
                    # print(8)
                    self.statement_check = True
                    self.result_dict[result] = 1

            if target in self.uil_list[i][1]:
                result=self.uil_list[i][0]
                if result not in self.result_dict.keys():
                    # print(9)
                    self.statement_check = True
                    self.result_dict[result] = 1

            if target in self.uil_list[i][2]:
                result=self.uil_list[i][0]
                if result not in self.result_dict.keys():
                    # print(10)
                    self.result_dict[result] = 1
                    self.statement_check = True
                    # print(self.result_dict)

            if target in self.uil_list[i][4]:
                result=self.uil_list[i][0]
                if result not in self.result_dict.keys():
                    # print(11)
                    self.statement_check = True
                    self.result_dict[result] = 1

    
    def find_comb(self, target):
        for i in range(len(self.uil_list)):
            if target in self.uil_list[i][0]:
                
                result=self.uil_list[i][0]
                if self.result_dict:
                    if result in self.result_dict.keys():
                        # print(12)
                        self.statement_check = True
                        self.result_dict[result] += 1
                    else:
                        self.statement_check = True
                        self.result_dict[result] = 1
            if target in self.uil_list[i][1]:
                
                result=self.uil_list[i][0]
                if self.result_dict:
                    if result in self.result_dict.keys():
                        # print(13)
                        self.statement_check = True
                        self.result_dict[result] += 1
                    else:
                        self.statement_check = True
                        self.result_dict[result] = 1

            if target in self.uil_list[i][2]:
                result=self.uil_list[i][0]
                if self.result_dict:
                    if result in self.result_dict.keys():
                        # print(14)
                        self.statement_check = True
                        self.result_dict[result] += 1
                    else:
                        self.statement_check = True
                        self.result_dict[result] = 1

            if target in self.uil_list[i][4]:
                result=self.uil_list[i][0]
                if self.result_dict:
                    if result in self.result_dict.keys():
                        # print(15)
                        self.statement_check = True
                        self.result_dict[result] += 1
                    else:
                        self.statement_check = True
                        self.result_dict[result] = 1
        
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
            # print(self.parent)
            break

    def re_organ(self, pre_data):
        candi_base = ""
        for tmp_base_distance in pre_data:
            candi_base += tmp_base_distance[0]
            candi_base += " "
        candi_base = candi_base[:-1]
        return candi_base

    def cal_distance(self, pre_data):
        candid = []
        candi_base = ""
        for tmp_base_distance in pre_data:
            candi_base += tmp_base_distance[0]
            candi_base += " "
        candi_base = candi_base[:-1]
        for key_can in self.result_dict.keys():
            candid.append(key_can)
        distance_result, distance_number = self.edit_distance(candid, candi_base)
        return distance_result, distance_number

    def edit_distance(self, a, b):
        min_dist = 9999
        min_name = ""
        for i in a:
            r = editdistance.eval(i, b)
            if r < min_dist:
                min_dist = r
                min_name = i

        return min_name, min_dist
    
    def quick_edit_distance(self, a, b):
        return editdistance.eval(a, b)