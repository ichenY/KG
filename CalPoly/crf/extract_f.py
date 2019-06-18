
# coding: utf-8

# In[40]:


import pycrfsuite
import spacy
import re
import sys
import model

nlp = spacy.load("en")

'''
input format: python extract.py <model> <input_file> <output_file_name>

command to run: python extract.py ucla.model test-ucla.txt output.txt
'''

modelM = 'calpoly.model'
file = 'test-calpoly.txt'
output_file_name = 'test_calpoly_tag.txt'

#def get_test_data_unlabel(file):
data = []
with open(file, "r", encoding='utf8') as f:
    for course in f:
        tup_list = []
        nlpx = nlp(course)
        for tup in nlpx:
            tup_list.append((tup.text,tup.tag_))
        data.append(tup_list)
# print(data)



# In[41]:



def get_labels(doc):
    return [label for (token, postag, label) in doc]

def get_token(doc):
    return [token for (token, postag, label) in doc]

    

# test_data = get_test_data_unlabel(input_file)

X_test = [model.get_features(course_doc) for course_doc in data]

tagger = pycrfsuite.Tagger()
tagger.open(modelM)
y_pred = [tagger.tag(xseq) for xseq in X_test] #list[list[string]]

print(y_pred)


# In[43]:


def write_txt(tup_list,pred_list):
    output = []
    for i in range(len(pred_list)):
        output.extend([pred_list[i][0], tup_list[i][0][0]])
        for j in range(1, len(pred_list[i])):
            prev, cur = pred_list[i][j-1], pred_list[i][j]
            if tup_list[i][j][0] != '>' and not tup_list[i][j][0].isspace():
                if prev == cur: #tag upchanged, append word
                    output.append(tup_list[i][j][0])
                else:#</prev><cur>word
                    output.extend(['</' + prev[1:], cur, tup_list[i][j][0]])
        output.append('</' + cur[1:] + '\n')

    return ' '.join(output)


with open(str(output_file_name), "w", encoding='utf8') as f:
    f.write(write_txt(data,y_pred))

# write_txt(X_test,y_pred,test_data)

