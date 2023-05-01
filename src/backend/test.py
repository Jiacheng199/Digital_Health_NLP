import json
with open('process/08d3a3e4e2af11ed957d0242ac120002/797aefe7-6d7c-4232-9ed4-b7170b349484.json', 'r', encoding='utf-8') as file:
    data = json.load(file)
data[0]["raw_data"]="1"
with open('process/08d3a3e4e2af11ed957d0242ac120002/797aefe7-6d7c-4232-9ed4-b7170b349484.json', 'w') as file:
    json.dump(data, file, indent=0) 
