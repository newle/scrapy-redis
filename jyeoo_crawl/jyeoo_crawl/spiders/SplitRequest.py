# -*-coding:utf-8-*-  
  
#from scrapy import log  
import logging
  
"""将需要post的请求分散开 
 
 使用注意：需在settings.py中进行相应的设置。 
 """  
  
import random  
from scrapy.http import FormRequest 
#from scrapy.contrib.downloadermiddleware.useragent import UserAgentMiddleware  

#p=2&f=0
def getPageNum(postdata):
    values = postdata.split("&")
    for v in values:
        kv = v.split("=")
        if kv[0] == "p" :
            return int(kv[1])

class SplitRequestMiddleware(object):  

    def __init__(self, pagesnum, crawler):
        self.pagesnum = pagesnum 
        self.crawler = crawler

    @classmethod
    def from_crawler(cls, crawler):
        o = cls(100, crawler)
        return o

    def process_request(self, request, spider):
        #http://www.jyeoo.com/math3/ques/partialques?r=0.1000001000020462&q=bc2d00e7-3e53-4464-9dd2-3a151c4827d4~5ad53fe4-7322-4808-a390-a3828f42fffd~49&s=0&t2=9&d=0
        if request.url.find("ques/partialques") != -1:
            logging.debug("We Will request 100 pages for this list page : " + request.url)
            if request.body == "":
                for i in range(1, 101):
                    nextrequest = FormRequest(request.url, formdata={'f':'0','p':str(i)}, dont_filter=True)
                    self.crawler.engine.schedule(nextrequest, spider=self.crawler.spider)

#            if request.body == "":
#                nextrequest = FormRequest(request.url, formdata={'f':'0','p':'1'}, dont_filter=True)
#                self.crawler.engine.schedule(nextrequest, spider=self.crawler.spider)
#            else:
#                currentPage = getPageNum(request.body)
#                logging.debug('Current PageNum: '+str(currentPage))  
#                if(currentPage < 100):
#                    nextPage = currentPage + 1
#                    nextrequest = FormRequest(request.url, formdata={'f':'0','p':str(nextPage)}, dont_filter=True)
#                    self.crawler.engine.schedule(nextrequest, spider=self.crawler.spider)
#                else:
#                    logging.debug("has process " + str(currentPage) + " pages in this list")
        return None
