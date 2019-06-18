import pycrfsuite
import spacy
import re,sys
import train_ashford
import glob,os

def write_txt(tup_list,pred_list):
    space_rem = ''
    output = []
    #print(tup_list)
    #print(pred_list[5],tup_list[5])
    for i in range(len(pred_list)):
        #print(tup_list) #[[(word,pos),()],[()]]
        output.extend([pred_list[i][0], tup_list[i][0][0]]) #<tag>, first word
        
        for j in range(1, len(pred_list[i])):
            #print(pred_list[i][j])
            prev, cur = pred_list[i][j-1], pred_list[i][j]
            if tup_list[i][j][0].isspace() and cur != prev:
                output.extend(['</' + prev[1:], cur])
            if not tup_list[i][j][0].isspace():
                if prev == cur: #tag upchanged, append word
                    output.append(tup_list[i][j][0])
                else:#</prev><cur>word
                    output.extend(['</' + prev[1:], cur, tup_list[i][j][0]])
        output.append('</' + cur[1:] + '\n')
    
    space_rem = ' '.join(output)
    space_rem = space_rem.replace(' <des','<des').replace(' ,',',').replace(' .','.')
    space_rem = space_rem.replace('. </','.</').replace('<format>.</format>','')
    return space_rem



def pred(data):
    def get_labels(doc):
        return [label for (token, postag, label) in doc]

    def get_token(doc):
        return [token for (token, postag, label) in doc]

        

    # test_data = get_test_data_unlabel(input_file)

    X_test = [[train_ashford.create_feature(d,i) for i in range(len(d))] for d in data]

    tagger = pycrfsuite.Tagger()
    tagger.open(modelM)
    y_pred = [tagger.tag(xseq) for xseq in X_test] #list[list[string]]
    return y_pred
    #print(y_pred)


    # In[43]:





nlp = spacy.load("en")
root = './Original/*.txt'

'''
input format: python extract.py <model> <input_file> <output_file_name>

command to run: python extract.py ucla.model test-ucla.txt output.txt
'''


#file = 'test-calpoly.txt'
#output_file_name = 'test_calpoly_tag.txt'


def createFolder(directory):
    try:
        os.makedirs(directory)
    except OSError:
        if not os.path.isdir(directory):
            raise      
    return

result_p="./tagdata_folder/"
createFolder(result_p)
modelM = 'ashford.model'

file = glob.glob(root)

for name in file:
    print(name)
    data,filename,y_pred = [],'',''
    filename = name.split('.')[1]
    #print(filename[14:])
    with open(name, "r", encoding='utf8') as f:
        for course in f:
            tup_list = []
            nlpx = nlp(course)
            for tup in nlpx:
                tup_list.append((tup.text,tup.tag_))
            data.append(tup_list)
        y_pred = pred(data)

        completeName=os.path.join(result_p,"%s.txt" % filename[10:])
        curpath = os.path.abspath(os.curdir)
        #print(output_file_name)
        print("Current path is: %s" % curpath)

        with open(completeName, "w", encoding='utf8') as outfile:
            outfile.write(write_txt(data,y_pred))       
# print(data)

