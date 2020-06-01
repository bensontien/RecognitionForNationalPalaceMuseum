import os, json

#Init
base_path = os.path.dirname(__file__)
config = json.load(open(os.path.join(base_path, 'config.json')))
fn1 = config['Append']['Append1']
fn2 = config['Append']['Append2']

with open(fn1, 'a', newline='',encoding = 'utf-8-sig') as output:
     with open(fn2,'r', encoding='utf-8-sig') as sentences:
         for sentence in sentences:
             output.write(sentence)