import json, os, sys,re
from bs4 import BeautifulSoup

def createFolder(directory):
        try:
            os.makedirs(directory)
        except OSError:
            if not os.path.exists(directory):
                raise
        return

path = '../Ashford/page/'
dirs = os.listdir(path)

for page in dirs:
    soup = BeautifulSoup(open(path + page, "r", encoding="ascii", errors="ignore"), "html.parser")

    body = soup.select('article')

    #courseinventorycontainer
    #courseinventorycontainer
    ans = {}
    ans["subjectOf"],ans['providerOf'] = {},{}
    ans["subjectOf"]["subject"] = soup.select('h1')[0].text.replace(" at Ashford University", "")
    ans["providerOf"]["id"] = 'AshFord'
    ans["providerOf"]["university"] = 'Ashford University'
    ans["providerOf"]['hasSubject'] = soup.select('h1')[0].text.replace(" at Ashford University", "")
    #ans["providerOf"]["university"] = 'Ashford University'
    ans_list = []
    #print(range(len(body)))
    for content in range(len(body)):

        subitem = {}

        course_name_id = body[content].select('span')[0].text
        #course_clean = course_name.split(' ')
        #course_id = course_clean[0] + ' ' + course_clean[1]
        
        ###ID
        course_id = course_name_id.split(' ')[0] + ' ' + course_name_id.split(' ')[1].replace("Introduction",'')
        subitem['id'] = 'AshFord_'+course_id
        ans['subjectOf']['id'] = course_id[:3]
        ###Name
        course_name = re.sub('\s\d+\W?','',course_name_id)[3:]
        subitem['course name'] = course_name


        ###unit
        unit = body[content].select('div.node__credits')[0].text.replace("\n","")
        subitem['units'] = unit

        ###Descritpion
        description_pre = body[content].select('div.node__description')[0].text.replace("\n","")

        description = description_pre.split('Prerequisite')[0]
        subitem['description'] = description

        #print(subitem)
        ###Prerequisite
        prerequisite = description_pre.split('Prerequisite')
        if len(prerequisite) == 2:

        
                
            if pre_new == ' ':
                continue
            elif pre_new =='':
                continue
            else:
                p = re.split('and',pre_new)
                subitem['prerequisite'] = p
        #print(subitem)
        ans_list.append(subitem)
    #print(ans_list)
            

    
        #print(ans_dict)
        #ans_list.append(ans_dict)

        
    ans['courses'] = ans_list
    #print(ans)


    subject_name = soup.select('h1')[0].text.replace(" at Ashford University", "")
    file_path = '../results/'
    createFolder(file_path)
    filename = os.path.join(file_path, subject_name +'.json')
    with open(filename,'w') as outfile:
        json.dump(ans, outfile, indent = 2)
    
