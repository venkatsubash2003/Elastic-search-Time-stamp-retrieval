from flask import Flask, request
import subprocess
import json
from requests import post
app = Flask(__name__)
global word

path = "@/home/next/flask_application/template.json"
@app.route('/timestamp',methods=['POST'])
def my_app():
    if request.method == 'POST':
        word = request.json['text']
    data_file = open('/home/next/flask_application/template.json')
    newdata = json.load(data_file)
    newdata["query"]["nested"]["query"]["match"]["key.text"] = word
    inp = '/home/next/flask_application/input/' + word + '.json'
    with open(inp,'w') as convert_file:
        convert_file.write(json.dumps(newdata))

    inp ='@' + inp

    f = open('/home/next/flask_application/output/'+ word + '.json','w')
    subprocess.run(["curl","-X","POST","localhost:9200/samsubash/_search?pretty&size=50","-H","Content-Type: application/json","-d",inp],stdout = f)

    print(word)
    

    f = open("/home/next/flask_application/output/"+ word + ".json")
    docket_content = f.read()
    data = json.loads(docket_content)
    val = data["hits"]["total"]["value"]
    obj = dict()
    for i in range(50):
        try:
            uniq_id = data["hits"]["hits"][i]["_id"]
            start = data["hits"]["hits"][i]["inner_hits"]["key"]["hits"]["hits"][0]["fields"]["key.start"][0]
            check = data["hits"]["hits"][i]["inner_hits"]["key"]["hits"]["total"]["value"]



            if check > 1 and check < 4:
                arr = []
                for j in range(check):
                    arr.append(data["hits"]["hits"][i]["inner_hits"]["key"]["hits"]["hits"][j]["fields"]["key.start"][0])
                obj[uniq_id] = arr

                arr = []
            elif check > 3:
                for j in range(3):
                    arr.append(data["hits"]["hits"][i]["inner_hits"]["key"]["hits"]["hits"][j]["fields"]["key.start"][0])
                obj[uniq_id] = arr
            else:
                obj[uniq_id] = [start]
    
        except IndexError as exc:
            pass
    out = '/home/next/flask_application/result/' + word + '.json'
    print(out)
    print(obj)
    with open(out,'w') as convert_file:
        convert_file.write(json.dumps(obj))
    return obj
