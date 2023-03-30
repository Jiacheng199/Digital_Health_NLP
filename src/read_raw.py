import re

def read_raw(): 
    example = {}
    with open('ReasonExample.txt', 'r') as ex:
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

# print(read_raw())
def read_return_raw():
    example = []
    with open('ReasonExample.txt', 'r') as ex:
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
            # if not line:
            #     break
            # all_line = re.split('-|,|/| ', line)
            # tmp_line = []
            # for i in range(len(all_line)):
            #     new_line = ""
            #     for each_alp in all_line[i]:
            #         if ('a' <= each_alp <= 'z' or 'A' <= each_alp <= 'Z' or each_alp == ' ' or '0'<each_alp<'9') and each_alp != ' ':
            #             new_line += each_alp.lower()

            #     if new_line:
            #         tmp_line.append([new_line])
            example.append(line)

    return example

# print(read_raw())