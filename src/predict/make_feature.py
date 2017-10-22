import json
import numpy as np

with open('../record/one/json_1.txt') as json_data:
    d = json.load(json_data)
    d1 = d[0]["hands"]["right"]["fingers"][0]["bones"][3]["next_joint"]
    d1 = np.array(d1)
    d1 = d1.reshape(d1.shape[0],1)
    print(d1)