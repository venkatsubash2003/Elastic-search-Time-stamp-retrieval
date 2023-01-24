import requests
import os
import json
import elasticsearch
from elasticsearch import Elasticsearch
from elasticsearch import Elasticsearch
from json.decoder import JSONDecodeError
es=Elasticsearch([{'host':'localhost','port':9200,'scheme':"http"}])


print(es.ping())
directory = '/home/next/Documents/yttt (copy)/yttts-test'


res = requests.get('http://localhost:9200')
i = 1
count = 1

    
for filename in os.listdir(directory):

    full_path  = directory + '/' + filename
    
    
    if filename.endswith(".json"):
        f = open(full_path)
        docket_content = f.read()
        filename = filename[:-5]
        # Send the data into es
        try:
            print(filename)    
            es.index(index='samsubash', ignore=400,
            id=filename, body=json.loads(docket_content))
            i = i + 1


            print(i)
            print("success")
        except JSONDecodeError as J:
            print(count)
            count += 1


    



