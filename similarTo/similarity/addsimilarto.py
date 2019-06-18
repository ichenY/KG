
# coding: utf-8

# In[13]:


#copy
import json,os
# calpath = '../../CalPoly/crf_all/structure_data'
ashpath = '../../Ashford/Ashford/Ashford/results'
# csuspath = '../../csus/csus/csus/spiders/result'
matchpath = '../cscu_ashford.txt'
secondtxt = '../calpoly_ashford.txt'
first = open(matchpath,'r')
sec = open(secondtxt,'r')
csustxt = first.readlines()
caltxt = sec.readlines()

# print(csustxt)
# with open(matchpath,'r') as f:
#     matchList = f.readlines()

for file in os.listdir(ashpath):
    jsonf = open(os.path.join(ashpath,file), 'r')
    data = json.load(jsonf)
    for idc in data['courses']:
        similist = []
        for i in range(len(csustxt)):
            if idc['id'] in csustxt[i]:
                check = csustxt[i].split(',')
                similist.append(check[0].replace("(","").strip())   
        for j in range(len(caltxt)):
            if idc['id'] in caltxt[j]:
                check = caltxt[j].split(',')
                similist.append(check[0].replace("(","").strip())
        
        if similist: idc['similarTo'] = similist

#     print(data['courses'])
    out = '../addsimJson/ashford'
    compName = os.path.join(out,file)
    with open(compName, 'w') as outf:
        json.dump(data, outf,indent=2) 


# In[16]:


import json,os
calpath = '../../CalPoly/crf_all/structure_data'
# ashpath = '../../Ashford/Ashford/Ashford/test'
# csuspath = '../../csus/csus/csus/spiders/result'
matchpath = '../cscu_calpoly.txt'
secondtxt = '../calpoly_ashford.txt'
first = open(matchpath,'r')
sec = open(secondtxt,'r')
csustxt = first.readlines()
caltxt = sec.readlines()

# print(csustxt)
# with open(matchpath,'r') as f:
#     matchList = f.readlines()

for file in os.listdir(calpath):
    jsonf = open(os.path.join(calpath,file), 'r')
    data = json.load(jsonf)
    for idc in data['courses']:
        similist = []
        for i in range(len(csustxt)):
            if idc['id'] in csustxt[i]:
                check = csustxt[i].split(',')
                similist.append(check[0].replace("(","").strip())   
        for j in range(len(caltxt)):
            if idc['id'] in caltxt[j]:
                check = caltxt[j].split(',')
                similist.append(check[1].replace(")","").strip())
        
        if similist: idc['similarTo'] = similist

#     print(data['courses'])
    out = '../addsimJson/calpoly'
    compName = os.path.join(out,file)
    with open(compName, 'w') as outf:
        json.dump(data, outf,indent=2) 


# In[25]:


import json,os
# calpath = '../../CalPoly/crf_all/structure_data'
# ashpath = '../../Ashford/Ashford/Ashford/test'
csuspath = '../../csus/csus/csus/spiders/result'
matchpath = '../cscu_calpoly.txt'
secondtxt = '../cscu_ashford.txt'
first = open(matchpath,'r')
sec = open(secondtxt,'r')
csustxt = first.readlines()
caltxt = sec.readlines()


# with open(matchpath,'r') as f:
#     matchList = f.readlines()

for file in os.listdir(csuspath):
    jsonf = open(os.path.join(csuspath,file), 'r')
    data = json.load(jsonf)
    for idc in data['courses']:
        similist = []
        for i in range(len(csustxt)):
            if idc['id'] in csustxt[i]:
                check = csustxt[i].split(',')
                similist.append(check[1].replace(")","").strip())   
        for j in range(len(caltxt)):
            if idc['id'] in caltxt[j]:
                print(idc['id'],caltxt[j])
                check = caltxt[j].split(',')
                similist.append(check[1].replace(")","").strip())
        
        if similist: idc['similarTo'] = similist

#     print(data['courses'])
    out = '../addsimJson/csus'
    compName = os.path.join(out,file)
    with open(compName, 'w') as outf:
        json.dump(data, outf,indent=2) 

