from matching import map_sys
import uuid
import os
myuuid = uuid.uuid4()
cmd = 'mpiexec -n 12 python snomed_ct.py ' + str(myuuid) + ' ' + str("C:/Users/23906/Desktop/DI-RedBack/data_samples/ReasonExample.txt")
os.system(cmd)
m = map_sys("C:/Users/23906/Desktop/DI-RedBack/data_samples/ReasonExample.txt", "output", str(myuuid))
m.mapping()