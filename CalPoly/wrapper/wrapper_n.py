import json, os, sys
from bs4 import BeautifulSoup

def createFolder(directory):
        try:
            os.makedirs(directory)
        except OSError:
            if not os.path.exists(directory):
                raise
        return

path = './page/'
dirs = os.listdir(path)

for page in dirs:
    soup = BeautifulSoup(open(path + page, "r",encoding="utf-8"), "html.parser")

    body = soup.select('div.courseblock')
    #courseinventorycontainer
    #courseinventorycontainer
    ans = {}
    ans["subject"] = soup.select('h1')[0].text
    ans_list = []
    course = ""
    #print(range(len(body)))
    for content in range(len(body)):
        course = body[content].select('p.courseblocktitle strong')[0].text
        course = course.split(".")[1]

        ans_dict = {
        "Course number & title": str(course),
        "Number of units": body[content].select('span.courseblockhours')[0].text.replace("\n",""),
        "Term" : body[content].select('p.noindent')[0].text,
        "Course description": body[content].select('div.courseblockdesc p')[0].text.replace("\u00a0","")
        }

        ans_list.append(ans_dict)

    ans['courses'] = ans_list
    #print(ans)

    subject_name = soup.select('h1')[0].text
    createFolder('./results/')
    filename = os.path.join('./results/', subject_name +'.json')
    with open(filename,'w') as outfile:
        json.dump(ans, outfile, indent = 2)
    
