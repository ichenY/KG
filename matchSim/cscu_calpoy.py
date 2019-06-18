
# coding: utf-8

# In[1]:


import os
import csv
import rltk
import re
import sys
import itertools


# In[2]:


file1 = './cscu.csv'
file2 = './calpoly.csv'


# In[3]:


cscu_data = []
calpoly_data = []


# In[4]:


with open(file1, 'r', encoding="utf-8", errors = 'replace') as cscufile:
    reader = csv.DictReader(cscufile)
    for row in reader:
        #print(row)
        data = row['Subject'],row['course name']
        #print(data)
        #data = row['Subject'],row["Course number & title"].replace('\xa0','')
        #print(data)
        cscu_data.append(data)


# In[5]:


with open(file2, 'r', encoding='utf-8-sig') as calpolyfile:
    reader = csv.DictReader(calpolyfile)
    
    for row in reader:
        data = row['Subject'],row["Course number & title"].replace('\xa0','')
        #print(data)
        calpoly_data.append(data)


# In[6]:


import string

def createFeature(data):
    '''
    input: list[tuple[subject, title]]
    output: list[tuple[subject,title,location]]
    '''
    new_data = []
    translate_table = dict((ord(char), ' ') for char in string.punctuation)  

    for loc, row in enumerate(data):
        row = list(row)
        
        ###Subject
        row[0] = row[0].strip()
        
        ###course_name
        row[1] = row[1].translate(translate_table).strip() #replace all punctuations to blank space
        
        ###ID
        row.append(loc + 1) 
        
        new_data.append(tuple(row))
    return list(set(new_data))


# In[7]:


new_cscu = createFeature(cscu_data)
new_calpoly= createFeature(calpoly_data)


# In[8]:


import nltk 
# nltk.download('stopwords')


# In[9]:


from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize  

stop_words = set(stopwords.words('english')) 

def hashingFunc(course_name: str) -> str:
    global stop_words
    global translate_table
    return ''.join(sorted([w[0] for w in word_tokenize(course_name) if not w in stop_words]))[:2]
#3hashingFunc(new_cscu)


# In[10]:


from collections import defaultdict
def blockFunc(feature_list):
    """
    Like the idea of hashing data into buckets
    list[tuple[full_subject_name, course_name, word_1st_subject, id]]
    """
    result = defaultdict(list)
    for feature in feature_list:
        if feature[1]:
            k = hashingFunc(feature[1])
            result[k].append(feature)
    #print(result)
    return result


# In[12]:


# nltk.download('punkt')


# In[15]:


cscu = blockFunc(new_cscu)
calpoly = blockFunc(new_calpoly)


# In[18]:


print(sum([len(cscu[k]) for k in cscu.keys()]))
print(sum([len(calpoly[k]) for k in calpoly.keys()]))
# print(len(bucket_keys))

# c = 0
# for k in bucket_keys:
#     if k in cscu and k in calpoly:
#         c+=1
#         #print(len(cscu[k]), len(calpoly[k]))
# print(c)


# In[32]:


count = 0

bucket_keys = set(list(cscu.keys()) + list(calpoly.keys()))
result,allr = [],[]
for k in bucket_keys:
    if k in cscu and k in calpoly:
        for cs, ca in itertools.product(cscu[k], calpoly[k]):
            sub = rltk.levenshtein_similarity(cs[0],ca[0])
            title = rltk.levenshtein_similarity(cs[1],ca[1])

            score = 0.6 * sub + 0.4 * title
            mat = []
            if score > 0.867:
                count += 1
                #if score < 0.9:
                mat.append((cs))
                mat.append((ca))
#                 print(ans)
                result.append(mat)
print(result)
#                 print(cs,ca,score,'count:' + str(count))


# In[82]:


#add id to json for CSCU
###CSCU -> CALPOLY
# print(result)
import json
x = 0
newfile = '../match/web'
cscupath = '../match/result_old'
for file in os.listdir(cscupath): 
    fi = open(os.path.join(cscupath,file), 'r')
    
    fi_new = open(os.path.join(newfile,file), 'r')
    subject = content['subject']
    try:
        content_new = json.load(fi_new)
        content = json.load(fi)
        subject = content['subject']
    #     print(content_new['url'])
        content['url'] = content_new['url']
        content['provider'] = content_new['provider']    
        for line in content['course']:
            x += 1
            line['id'] = x
        outfilepath = '../jsonid/jsonid_cscu'
        compName = os.path.join(outfilepath,"%s.json" % subject.strip())
        with open(compName, 'w') as outfile:
            json.dump(content, outfile,indent=2)
    except:
        continue

#     print(content)


# In[87]:


calpath = '../CalPoly/crf_all/structure_data'
y = 0
for file in os.listdir(calpath): 
    fil = open(os.path.join(calpath,file), 'r')
    content = json.load(fil)
    content['provider'] = 'California Polytechnic State University'
    subject = content['subject']
    pos = subject.index('(')
    content['url'] = 'http://catalog.calpoly.edu/coursesaz/'+ subject[pos+1:].replace(')','').lower()
    print(content['url'])
    for line in content['courses']:
        y += 1
        line['id'] = y
    print(content)

