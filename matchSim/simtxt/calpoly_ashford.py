#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import csv
import rltk
import re
import sys
import itertools
import nltk 
nltk.download('stopwords')


# In[2]:


path = '/Users/iankan/Desktop/project_stringmatching/data/'

file1 = 'calpoly.csv'
file2 = 'ashford.csv'


# In[3]:


calpoly_data = []
ashford_data = []


# In[4]:


with open(path+file1, 'r', encoding='utf-8-sig') as calpolyfile:
    reader = csv.DictReader(calpolyfile)    
    for row in reader:
        data = row['subject'],row["name"],row['id']
        #print(data)
        calpoly_data.append(data)


# In[5]:


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


# In[6]:


print(len(calpoly_data))
print(len(ashford_data))


# In[7]:


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


# In[8]:


new_calpoly = createFeature(calpoly_data)
new_ashford= createFeature(ashford_data)


# In[9]:


print(len(new_calpoly))
print(len(new_ashford))


# In[10]:


from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize  

stop_words = set(stopwords.words('english')) 

def hashingFunc(course_name: str) -> str:
    global stop_words
    global translate_table
    return ''.join(sorted([w[0] for w in word_tokenize(course_name) if not w in stop_words]))[:2]
#3hashingFunc(new_cscu)


# In[11]:


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


calpoly = blockFunc(new_calpoly)
ashford = blockFunc(new_ashford)


# In[13]:


"""
print(sum([len(calpoly[k]) for k in calpoly.keys()]))
print(sum([len(ashford[k]) for k in ashford.keys()]))
print(len(bucket_keys))

c = 0
for k in bucket_keys:
    if k in calpoly and k in ashford:
        c+=1
        #print(len(cscu[k]), len(calpoly[k]))
print(c)
"""


# In[34]:


count = 0

bucket_keys = set(list(calpoly.keys()) + list(ashford.keys()))
frequent_words = set(['Introduction', 'Advanced', 'Intermediate', 'I', 'II', 'III','Principles'])
result = []
for k in bucket_keys:
    if k in calpoly and k in ashford:
        for ca, ash in itertools.product(calpoly[k], ashford[k]):
            sub = rltk.levenshtein_similarity(ca[0],ash[0][:-8])
            #name
            ca_name = set(ca[1].split()) - stop_words - frequent_words
            ash_name = set(ash[1].split()) - stop_words - frequent_words
            name = rltk.monge_elkan_similarity(list(ca_name), list(ash_name), function = rltk.levenshtein_similarity)

            score = 0.5 * sub + 0.5 * name

            if score > 0.77:
                count += 1
                ans = (ca[2], ash[2])
                #print(ans)
                result.append(ans)
                print(ca,ash,score,'count:',str(count))
                print()
                


# In[33]:


print(count)


# In[59]:


###CALPOLY -> ASHFORD
print(result)


# In[35]:


file_out = open("calpoly_ashford.txt", "w")

for row in result:
    line = ', '.join(str(x) for x in row)
    file_out.write('(' + line + ')' + '\n')
file_out.close()


# In[ ]:





# In[ ]:




