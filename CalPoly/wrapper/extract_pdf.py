#!/usr/bin/env python
# coding: utf-8

# In[1]:


import json, os, sys, tika
from tika import parser
from tika import unpack
from bs4 import BeautifulSoup


# In[2]:


path = "/Users/iankan/Desktop/111/art.html"


# In[3]:


soup = BeautifulSoup(open(path, "r",encoding = 'utf-8'),"html.parser")


# In[4]:


#body = soup.select("div.course-table")
body = soup.select("div.course-info")


# In[5]:


subject = soup.select('h2.dept-title')[0].text
subject_id = subject.split('(')[1].replace(")","").strip()


# In[12]:


#subject_id = subject.split('(')[1].replace(")","").strip()
print(subject_id)
print(subject)


# In[7]:


print(range(len(body)))


# In[14]:


import re
from PyPDF2 import PdfFileReader
tika.initVM()

contents = []
#pdf_urls = []
course_id = []
for content in range(len(body)):
    #print(content,body[0])
    courses = {}
    pdf_urls = []
    course = body[content].select("div.course-id")[0].text
    #courseID = re.match(r"\w+ \d+",course)
    courseID = course.split(':')[0].replace("Crosslist ","")
    #print(course)
    #print(courseID)
    course_id.append(courseID)
    units = course.split('(')[1].replace(")","")
    #courseID1 = re.match(r'(\w*)',courseID)
    courseDescription = body[content].select("div.catalogue")[0].text
    #teacher = body[content].select("td.instructor")[0].text
    pdf = body[content].select("td.syllabus")[0].find('a')#.find('href')
    #print(pdf)
    if pdf:
        pdf = pdf.get('href')
        courses['id'] = 'USC_' + courseID
        courses['units'] = units
        courses['subjectOf'] = 'USC_' + subject_id
        courses['courseName'] = course.split(':')[1].split('(')[0].strip()
        courses['description'] = courseDescription
        teachers = []
        if pdf.endswith('.pdf'):
            parsed = parser.from_file(pdf)
            content = parsed['content']
            teacher_email = re.split(r"Professor|Prof.",content)[1].split(")")[0].replace("(","").replace("\n","").replace("Departments","").strip()
            name = teacher_email.split(" ")
            email = re.findall('\S+@\S+',teacher_email)
            teacher_name = name[0] + ' ' + name[1] + ' ' + name [2]
            course_d = re.split(r"Course Description|Office phone:",content)[1].split("Learning Objectives")[0]
            courses['instructor'] = teacher_name
            courses['instructor_email'] = email
            courses['description'] = course_d.replace(" \n","").replace("\n"," ").strip()

        contents.append(courses)   
    else:
        courses['id'] = 'USC_' + courseID
        courses['units'] = units
        courses['subjectOf'] = 'USC_' + subject_id
        courses['courseName'] = course.split(':')[1].split('(')[0].strip()
        courses['description'] = courseDescription
        contents.append(courses)


# In[ ]:





# In[11]:


print(contents)


# In[ ]:





# In[ ]:




