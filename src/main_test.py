from matching import map_sys
from writing_csv import writing
from load_compare import read_comp

map = map_sys('src/ReasonExample.txt', 'src/example.csv')
result = map.mapping()
# writing(result)

true_value = read_comp()


not_match_total = 0
not_match_acc= 0
counter = 0
for i in range(len(result)):
    print(result[i][1] + "    " + true_value[i][3])
    
    if result[i][1] == true_value[i][3]:
        counter+= 1
        if true_value[i][3] != "Non-Match":
            not_match_acc += 1
    
    if true_value[i][3] != "Non-Match" and result[i][1] != "Non-Match":
        not_match_total += 1

print(counter/len(result))

print(not_match_acc/not_match_total)
