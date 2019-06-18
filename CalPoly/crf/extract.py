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
#print(data)



def get_labels(doc):
    return [label for (token, postag, label) in doc]

def get_token(doc):
    return [token for (token, postag) in doc]

    

# test_data = get_test_data_unlabel(input_file)

X_test = [model.get_features(course_doc) for course_doc in data]

tagger = pycrfsuite.Tagger()
tagger.open(modelM)
y_pred = [tagger.tag(xseq) for xseq in X_test] #list[list[string]]

#print(y_pred)


def write_txt(X_test,y_pred,test_data):
#     y_pred_copy = y_pred[:]
    output,wordList = [],[]
    pos = 0
    wordList = [get_token(course_doc) for course_doc in test_data]
    flat_list = [item for sublist in wordList for item in sublist]
#     print(flat_list)
    for i in range(len(y_pred)):
        output.append(y_pred[i][0])
        y_pred[i].append('<>')
        for j in range(1,len(y_pred[i])):
            prev,cur = y_pred[i][j-1],y_pred[i][j] #course i
            if prev != cur:
                output.append(flat_list[pos])
                pos += 1
                prev = prev.replace('<','</')
                cur = cur.replace('<>',' ')
#                 if cur == ' ':
#                     output.append(prev)
#                 else:
                output += prev,cur
            else:
                output.append(flat_list[pos])
                pos += 1
                
        output.append('\n')
    output_result = ' '.join([w for w in output])
#     print(output_result)

    with open(str(output_file_name), "w", encoding='utf8') as f:
        f.write(output_result)

write_txt(X_test,y_pred,data)
