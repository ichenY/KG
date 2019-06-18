import scrapy
import re
import os
from scrapy.http import Request

class AshfordSpider(scrapy.Spider):
    name = "ash"

    start_urls = ['https://www.ashford.edu/online-degrees/online-courses']

    def parse(self,response):
    	for body in response.css('div.section__content'):
    		for subject_page in body.css('ul.columns--2 a::attr(href)').extract():
    			yield Request("https://www.ashford.edu/" + subject_page + '/',callback =self.parse_content)
                

    def parse_content(self,response):
        #ans = {}
        #ans_list = []
        #ans["subject"] = response.css("h1::text").extract_first().encode('utf-8')
        subject_name = response.css("div h1::text").extract_first().encode("utf-8").replace(" at Ashford University", '')

        #print(subject_name)
        path = self.createFolder('./Ashford/page/')
        filename = os.path.join('./Ashford/page', subject_name + '.html')
        with open(filename, 'wb') as f:
            f.write(response.body)

    def createFolder(self,directory):
        try:
            os.makedirs(directory)
        except OSError:
            if not os.path.exists(directory):
                raise
        return

    