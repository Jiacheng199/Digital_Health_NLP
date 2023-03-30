from matching import map_sys
from writing_csv import writing

map = map_sys('ReasonExample.txt')
result = map.mapping()
writing(result)




