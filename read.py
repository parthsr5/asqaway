import json
  
# Opening JSON file
f = open('training11b.json')
  
# returns JSON object as 
# a dictionary
data = json.load(f)
  
# Iterating through the json
# list
for i in data['questions']:
    print(json.dumps(i, indent=4))
    break
    
  
# Closing file
f.close()