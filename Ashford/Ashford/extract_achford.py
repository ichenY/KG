import pycrfsuite
import re
import sys
import train_ashford, spacy
nlp = spacy.load("en")


def write_txt(tup_list,pred_list):
    # y_pred_copy = y_pred[:]
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


#model = 'ashford.model'
#file_input = 'train-ashford.txt'
#file_output = 'result.txt'
model = sys.argv[1]
file_input = sys.argv[2]
file_output = sys.argv[3]
data_test = []

with open(file_input, "r") as test_f:
    for course in test_f:
        tup_list = []
        for w in nlp(course):
            tup_list.append((w.text, w.tag_))

        data_test.append(tup_list)

#        for w in nlp(course):
#            tup_list.append((w.text, w.tag_))
#        data_test.append(tup_list)
"""
with open('train-ashford-tag.txt', "r") as test_f:
    for line in test_f: #line = course description
        course = []
        for sentence in re.split(r'</[^>]+>', line):
            if not sentence.isspace() and sentence:  
                match = re.match(r'<[^>]+>', sentence.strip())
                tag = match.group()
                sentence = sentence[:match.start()] + sentence[match.end():]
                for w in nlp(sentence):
                    course.append((w.text, w.tag_, tag))
        data_test.append(course)

"""
X_test = [[train_ashford.create_feature(course, i) for i in range(len(course))] for course in data_test]

tagger = pycrfsuite.Tagger()
tagger.open(model)


predict = [tagger.tag(course)  for course in X_test]

predict = [] #list(list(string)) course-word predicts
for test in X_test:
    predict.append(tagger.tag(test))

"""
Y_test = [train_ashford.extract_label(course) for course in data_test]
tp = 0 
tn = 0 
fp = 0 
fn = 0 
for j in range(len(Y_test)):
    for i in range(1,len(Y_test[j])):
        if Y_test[j][i] == Y_test[j][i-1]: 
            test_result = 'N' 
        else:
            test_result = 'P'
        if predict[j][i] != predict[j][i-1] : #P
            if test_result == 'P':
                tp += 1
            else:
                fp += 1  
        else:
            if test_result == 'N':
                if data_test[j][i-1][0] == '.':
                    tp += 1
                else:
                    tn += 1
            else:
                fn += 1 
print(tp, fp+fn)


precision = float(tp)/(tp+fp)
recall = float(tp)/(tp+fn)
f = 2*precision*recall / (precision + recall)
print('Precision = %f\nRecall = %f\nF1 score = %f' %(precision, recall, f))
"""
with open(file_output, "w") as f:
    f.write(write_txt(data_test, predict))



