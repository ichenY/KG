
# coding: utf-8

# In[1]:


import os
import csv
import rltk
import re
import sys
import itertools


# In[2]:


path = '../../matchSim/'

file1 = 'csus.csv'
file2 = 'ashford.csv'


# In[3]:


csus_data = []
ashford_data = []


# In[4]:


with open(path+file1, 'r', encoding="utf-8",errors = 'replace') as csusfile:
    reader = csv.DictReader(csusfile)
    for row in reader:
        #print(row)
        data = row['subject'],row['name'],row['id']
        #print(data)
        #data = row['Subject'],row["Course number & title"].replace('\xa0','')
        #print(data)
        csus_data.append(data)


# In[5]:


print(len(csus_data))


# In[40]:


#import codecs
#csvReader = csv.reader(codecs.open(path+file2, 'rU', 'utf-16'))

with open(path+file2, 'r', encoding='utf-8-sig') as ashfordfile:
    
    reader = csv.DictReader(ashfordfile)
    
    for row in reader:
        data = row['subject'],row["name"],row["id"]
        #print(data)
        ashford_data.append(data)
        #print(data)
        #data = list(data)
        #data[0] = data[0].replace(' Courses','')
        #data[1] = data[1][8:]
        #if data[1].startswith(" "):
        #    data[1] = data[1][1:]
        #    ashford_data.append(data)
        #else:
        #    data[1] = data[1]
        #    ashford_data.append(data)


# In[42]:


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
        #row.append(loc + 1) 
        
        new_data.append(tuple(row))
    return list(set(new_data))


# In[47]:


new_csus = createFeature(csus_data)
new_ashford= createFeature(ashford_data)


# In[50]:


print(len(new_csus))
print(len(new_ashford))


# In[186]:


import nltk 
nltk.download('stopwords')


# In[51]:


from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize  

stop_words = set(stopwords.words('english')) 

def hashingFunc(course_name: str) -> str:
    global stop_words
    global translate_table
    return ''.join(sorted([w[0] for w in word_tokenize(course_name) if not w in stop_words]))[:2]
#3hashingFunc(new_cscu)


# In[52]:


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


# In[53]:


csus = blockFunc(new_csus)
ashford = blockFunc(new_ashford)


# In[190]:



print(sum([len(cscu[k]) for k in cscu.keys()]))
print(sum([len(ashford[k]) for k in ashford.keys()]))
print(len(bucket_keys))

c = 0
for k in bucket_keys:
    if k in cscu and k in ashford:
        c+=1
        #print(len(cscu[k]), len(calpoly[k]))
print(c)


# In[57]:


count = 0

bucket_keys = set(list(csus.keys()) + list(ashford.keys()))
result = []
for k in bucket_keys:
    if k in csus and k in ashford:
        for cs, ash in itertools.product(csus[k], ashford[k]):
            sub = rltk.levenshtein_similarity(cs[0],ash[0])
            name = rltk.levenshtein_similarity(cs[1],ash[1])

            score = 0.4 * sub + 0.6 * name

            if score > 0.7:
                count += 1
                #if score < 0.9:
                ans = (cs[2],ash[2])
                print(ans)
                result.append(ans)
                print(cs,ash,score,'count:' + str(count))


# In[26]:


###CSCU -> ASHFORD
print(result)

