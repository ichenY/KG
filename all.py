
# coding: utf-8

# In[1]:


#university
import json,os
allpath = './all_new_file'
outer = []
csus,ash,cal = [],[],[]
for file in os.listdir(allpath):
    fi = open(os.path.join(allpath,file), 'r')
    uni = {}
    data = json.load(fi)
    idc = data['providerOf']['id']
    university = data['providerOf']['university']
#     hasSubject = data['providerOf']['hasSubject']
    subjectid = data['subjectOf']['id']
    if idc == 'CSUS':
        csus.append(idc+'_'+subjectid)
    if idc == 'AshFord':
        ash.append(idc+'_'+subjectid)
    if idc == 'CalPoly':
        cal.append(idc+'_'+subjectid)
    uni['id'] = idc
    uni['university'] = university
#     uni['hasSubject'] = 
#     if 'hasSubject' in uni
#     uni['hasSubject'] = hasSubject
    if uni not in outer:
        outer.append(uni)
outer[0]['hasSubject'] = csus
outer[1]['hasSubject'] = ash
outer[2]['hasSubject'] = cal

print(outer) 
#     uni['']
outfolder = './entity'
compName = os.path.join(outfolder,'university.json')
with open(compName, 'w') as outf:
    json.dump(outer, outf)   #indent = 2         


# In[2]:


# course
courselist = []
for file in os.listdir(allpath):
    fi = open(os.path.join(allpath,file), 'r')
    data = json.load(fi)
    subjectof = data['subjectOf']['id']
    prefix = data['providerOf']['id']
    for detail in data['courses']:
        cou = {}
        cou['id'] = detail['id']
        cou['units'] = detail['units']
        cou['subjectOf'] = prefix+'_'+subjectof
        cou['courseName'] = detail['course name']
        if 'term' in detail: cou['term'] = detail['term']
        if 'description' in detail: cou['description'] = detail['description'] 
        if 'prerequisite' in detail: cou['prerequisite'] = [prefix+'_'+ x for x in detail['prerequisite'] ]
        if 'similarTo' in detail: cou['similarTo'] = detail['similarTo']
        if 'format' in detail: cou['format'] = detail['format']
        if 'grading' in detail: cou['grading'] = detail['grading']
        if 'other' in detail: cou['other'] = detail['other']
        
        courselist.append(cou)
outfolder = './entity'
compName = os.path.join(outfolder,'courses.json')
with open(compName, 'w') as outf:
    json.dump(courselist, outf)   #indent = 2  


# In[3]:


#subject
sublist = []
for file in os.listdir(allpath):
    fi = open(os.path.join(allpath,file), 'r')
    data = json.load(fi)
    sub = {}
    idc = data['subjectOf']['id']
    subject = data['subjectOf']['subject']
    provider = data['providerOf']['id']
    courselist = []
    for course in data['courses']:
        courselist.append(course['id'])
#     print(courselist)
    sub['id'] = provider+'_'+idc
    sub['subject'] = subject
    sub['hasCourse'] = courselist
    sublist.append(sub)
    
# print(sublist)
outfolder = './entity'
compName = os.path.join(outfolder,'subject.json')
with open(compName, 'w') as outf:
    json.dump(sublist, outf)   #indent = 2  

