import spacy, pycrfsuite, re

def create_feature(doc, i):
    token = doc[i][0]
    token_tag = doc[i][1]
    features = [
        'token.lower=' + token.lower(),
        'token.length=' + str(len(token)),
        'token.isupper=%s' % token.isupper(),
        'token.istitle=%s' % token.istitle(),
        'token.isdigit=%s' % token.isdigit(),
        'token.isdot=%s' % isdot(token),
        'token_tag=%s' % token_tag,
        'token_tag[:2]=%s' % token_tag[:2]
    ]
    if i > 0:
        last_token = doc[i-1][0]
        last_token_tag = doc[i-1][1]
        features.extend([
            '-1:token.lower=' + last_token.lower(),
            '-1:token.length=' + str(len(last_token)),
            '-1:token.isupper=%s' % last_token.isupper(),
            '-1:token.istitle=%s' % last_token.istitle(),
            '-1:token.isdigit=%s' % last_token.isdigit(),
            '-1:token.isdot=%s' % isdot(last_token),
            '-1:token_tag=%s' % last_token_tag,
            '-1:token_tag[:2]=%s' % last_token_tag[:2], 
            'last|token=%s|%s' %(last_token,token)
        ])    
    else:
        features.append('BOS')        
    if i < len(doc)-1:
        next_token = doc[i+1][0]
        next_token_tag = doc[i+1][1]
        features.extend([
            '+1:token.lower=' + next_token.lower(),
            '+1:token.length=' + str(len(next_token)),
            '+1:token.isupper=%s' % next_token.isupper(),
            '+1:token.istitle=%s' % next_token.istitle(),
            '+1:token.isdigit=%s' % next_token.isdigit(),
            '+1:token.isdot=%s' % isdot(next_token),
            '+1:token_tag=%s' % next_token_tag,
            '+1:token_tag[:2]=%s' % next_token_tag[:2], 
            'token|next=%s|%s' %(token,next_token), 
        ])
    else:
        features.append('EOS')
        
    if i < len(doc)-2:
        next_token = doc[i+2][0]
        next_token_tag = doc[i+2][1]
        features.extend([
            '+2:token.lower=' + next_token.lower(),
            '+2:token.length=' + str(len(next_token)),
            '+2:token.isupper=%s' % next_token.isupper(),
            '+2:token.istitle=%s' % next_token.istitle(),
            '+2:token.isdigit=%s' % next_token.isdigit(),
            '+2:token.isdot=%s' % isdot(next_token),
            '+2:token_tag=%s' % next_token_tag,
            '+2:token_tag[:2]=%s' % next_token_tag[:2]
        ])    
    if i > 1:
        next_token = doc[i-2][0]
        next_token_tag = doc[i-2][1]
        features.extend([
            '-2:token.lower=' + next_token.lower(),
            '-2:token.length=' + str(len(next_token)),
            '-2:token.isupper=%s' % next_token.isupper(),
            '-2:token.istitle=%s' % next_token.istitle(),
            '-2:token.isdigit=%s' % next_token.isdigit(),
            '-2:token.isdot=%s' % isdot(next_token),
            '-2:token_tag=%s' % next_token_tag,
            '-2:token_tag[:2]=%s' % next_token_tag[:2]
        ])
    return features


def isdot(word):
    return True if '.' in word else False


def extract_label(course):
    return [tup[2] for tup in course]
    #return [doc[2]]

if __name__ == '__main__':
    nlp = spacy.load("en")
    #x pos y
    data_train = []
    data_test = []

    with open("train-ashford-tag.txt", "r") as train_f:
        for line in train_f: #line = course description
            course = []
            for sentence in re.split(r'</[^>]+>', line):
                if not sentence.isspace():
                    try:
                        tags = re.findall(r'<[^>]+>', sentence)
                        #print(tags[0])
                        sentence = re.sub(tags[0],'',sentence.strip())
                        #print(sentence)
                        for w in nlp(sentence):
                            course.append((w.text, w.tag_, tags[0]))
                    except:
                        continue
                data_train.append(course)
            

    X_train = [[create_feature(course, i) for i in range(len(course))] for course in data_train]
    Y_train = [extract_label(course) for course in data_train]
    # [extract_label(tuple_list) for tuple_list in data_train]


    trainer = pycrfsuite.Trainer(verbose=False)

    for xseq, yseq in zip(X_train, Y_train):
        trainer.append(xseq, yseq)

    trainer.set_params({
        'c1': 0.1,
        'c2': 0.01,
        'max_iterations': 10
        #'feature.possible_transitions': True
    })

    trainer.train('ashford.model')
