
# coding: utf-8

# In[4]:


import csv,json,os
#stort in C:\Users\user\Desktop\558project\matchSim
# import sys,io
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="UTF-8")

calpath = '../CalPoly/crf_all/structure_data'
# ashpath = '../Ashford/Ashford/Ashford/results'
# csuspath = '../csus/csus/csus/spiders/result'

f_csv = csv.writer(open("calpoly.csv", "w", newline=''))
f_csv.writerow(["id","subject", "name","units","term", "description"])
for file in os.listdir(calpath):
    jsonf = open(os.path.join(calpath,file), 'r')
    print(jsonf)
    struct = json.load(jsonf)
    try:
        subj = struct['subjectOf']['subject']
    except:
        break
    for x in struct['courses']:
        
        if 'id' in x: 
            idc = x['id']
        else: 
            idc = ''
        if 'course name' in x: 
            name = x['course name']
        else:
            name = ''
        if 'units' in x: 
            units = x['units']
        else:
            units = ''
        if 'term' in x: 
            term = x['term']
        else:
            term = ''
        if 'description' in x:
            des = x['description']
        
    
        f_csv.writerow([idc,subj,name,units,term,des])

