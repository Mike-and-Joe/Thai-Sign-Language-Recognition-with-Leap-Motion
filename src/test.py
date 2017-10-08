import json

data = {'people':[{'name': 'Scott', 'website': 'stackabuse.com', 'from': 'Nebraska'}]}

with open('./data.txt', 'w') as outfile:
    json.dump(data, outfile)

dict = {'Python' : '.py', 'C++' : '.cpp', 'Java' : '.java'}

json = json.dumps(dict)
f = open("dict.json","w")
f.write(json)
f.close()
