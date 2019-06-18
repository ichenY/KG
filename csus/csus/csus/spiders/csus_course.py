# -*- coding: utf-8 -*-
import scrapy
import os
import json
import re

class CsusCourseSpider(scrapy.Spider):
    name = 'csus_course'
    allowed_domains = ['csus.edu']
    start_urls = ['http://catalog.csus.edu/courses-a-z/']

    def parse(self, response):
        linkList=response.xpath("//div[@id='atozindex']")
        for item in linkList:
            url=item.xpath(".//li/a/@href").extract()
            print(len(url))
            for i in url:
                yield scrapy.Request('http://catalog.csus.edu'+i,callback=self.parse_url)
                
    def parse_url(self,response):
        #print(response.body)
        outitem={}

        outitem['subjectOf'],outitem['providerOf'] = {},{}
        outitem['providerOf']['id'] = 'CSUS'
        outitem['providerOf']['university'] = 'California State University, Sacramento'




        area=response.xpath("//div[@id='content']")
        for big in area:
            subject=big.xpath(".//h1/text()").extract()
            for item in subject:
                subject_c=re.sub('\([^(]*\)','',item)

            #print(subject_c)
            
            block=big.xpath(".//div[@class='courseblock']")
            data=[]
            for s in block:
                outitem['subjectOf']['subject'] = subject_c[:-1]
                outitem['providerOf']['hasSubject'] = subject_c[:-1]
                subitem={}
                name=s.xpath(".//span[@class='title']/text()").extract()
                for mov in name:
                    name_p=re.sub('\S*\s\d+\w?\.','',mov)
                    name_p1=re.sub('\S\s\d+-\w?\.','',mov)
                    #print(name_p)
                    name_clean1=name_p1.replace(u'\xa0',u'')
                    name_clean=name_p.replace(u'\xa0',u'')
                    
                    name_id = name_clean1.split('.')[0]
                    #name_course = name_clean.split('.')[1]
                    #print(name_id[0])
                    #name_id = re.sub('',)


                    
                    #print(name_id[0],name_id[1])
                    name_clean=name_clean[:-2]
                    #print("something",name_clean)
                    #print(name_clean.split('.')[3])
                    subitem['id'] = 'CSUS_'+name_id
                    outitem['subjectOf']['id'] = name_id.split(' ')[0]
                    subitem['course name']=name_clean
                    #print(name_course + name_clean.split('.')[2])
                term=s.xpath(".//p[@class='courseblockextra']/text()").extract()
                for ct in term:
                    subitem['term']=ct.replace("\u2013","")
                unit=s.xpath(".//span[@class='credits']/text()").extract()
                for ct in unit:
                    subitem['units']=ct
                description=s.xpath(".//p[@class='courseblockdesc']/text()").extract()
                for ct in description:
                    subitem['description']=ct.encode('utf-8')
                #prerequisite=s.xpath("//*[@id='textcontainer']/div/div[*]/p[2]/a[0]/text()").extract()
                prerequisite=s.xpath(".//a[@class='bubblelink code']/text()").extract()
                #print(prerequisite)
                if prerequisite:
                    subitem['prerequisite'] = [i.replace(u'\u00a0',u' ') for i in prerequisite]

                #for ct in prerequisite:
                    #print(ct)
                #    ct = ct.replace(u"\u00a0",u"")
                    #print(ct)
                    #subitem['prerequisite'] = ct
                #    subitem['prerequisite'] = [ct]
                    
                data.append(subitem)
                #yield {'des':description,'name':name_p,'term':term}
        
        outitem['courses']=data
        

        path1="./result/"
        self.createFolder(path1)
        completeName=os.path.join(path1,"%s.json" % outitem['subjectOf']['subject'])

        with open(completeName,"w") as outfile:
            json.dump(outitem,outfile,indent=2)



    def createFolder(self,directory):
        try:
            os.makedirs(directory)
        except OSError:
            if not os.path.isdir(directory):
                raise      
        return
