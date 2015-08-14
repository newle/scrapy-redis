# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider, Rule
from scrapy.http import Request
from scrapy.linkextractors import LinkExtractor
from scrapy_redis.spiders import RedisMixin
from jyeoo_crawl.items import JyeooCrawlItem, JyeooCrawlLoader

#from Html2Text import html_to_text
import re
import logging




def getdetailurl(html_doc):
    html_doc = html_doc.encode("utf8")
    start = html_doc.find("jindun('")
    if start != -1:
        end = html_doc.find("');", start)
        if end != -1:
            return html_doc[start+8: end]

def fetchhtml(url):
    try:
        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
        return response.read().decode('gb18030')
    except:
        return ""




jiajiao_detail_regex = re.compile("http://www.1010jiajiao.com/\w+/shiti_id_")
def process_jiajiao_url(value):
    if jiajiao_detail_regex.search(value) is None:
        return None
    return value


#p=2&f=0
def getPageNum(postdata):
    values = postdata.split("&")
    for v in values:
        kv = v.split("=")
        if kv[0] == "p" :
            print int(kv[1])


class JiaJiaoSpider(RedisMixin, CrawlSpider):
    """Spider that reads urls from redis queue (jiajiao:start_urls)."""
    name = "jiajiao"
    redis_key = "jiajiao:start_urls"
    rules =  (
            Rule(LinkExtractor(process_value = process_jiajiao_url), callback='parse_page', follow=False),
    )

    def __init__(self, *args, **kwargs):
        domain = kwargs.pop('domain', '')
        self.alowed_domains = filter(None, domain.split(','))
        super(JiaJiaoSpider, self).__init__(*args, **kwargs)

    def _set_crawler(self, crawler):
        CrawlSpider._set_crawler(self, crawler)
        RedisMixin.setup_redis(self)

    def parse_page(self, response):
        #answerurl="http://www.1010jiajiao.com/qiuda.php?questionid="+getdetailurl(questionhtml)
        #answerhtml=fetchhtml(answerurl)
        #if(answerhtml != ""):

        el = JyeooCrawlLoader(response = response)
        el.add_value('question_url', response.url)
        el.add_xpath('label_html', '//div[@class="xiti-content"]/div[@class="ndwz"]')
        el.add_xpath('question_html', '(//div[@class="timutext"])[1]')
        el.add_xpath('ans_html', '(//div[@class="answer_inner"])[1]')

        return el.load_item()

    def parse_jiajiao_detail_page(self, response):
        el = JyeooCrawlLoader(response = response)

        #el.add_value('question_url', response.url)   
        #el.add_xpath('question_html', '//div[@class="pt1"]')
        #el.add_xpath('question_html', '//div[@class="pt2"]')
  #     # el.add_xpath('examination_point', '//div[@class="pt3"]')
#       # el.add_xpath('', '//div[@class="pt4"]')
        #el.add_xpath('parse_html', '//div[@class="pt5"]')
        #el.add_xpath('ans_html', '//div[@class="pt6"]')
        #el.add_xpath('comments_html', '//div[@class="pt7"]')
        #return el.load_item()


#    def parse_start_url(self, response):
#        #el = jiajiaoCrawlLoader(response = response)
#        #el.add_value('question_url', response.url)
#        #el.add_xpath('question_html', '//div[@class="result-content"]')
#        #el.add_xpath('ans_html', '//div[@class="detail-item"]/div[@class="answer"]')
#        #el.add_xpath('parse_html', '//div[@class="detail-item"]/div[@class="analysis"]')
#        #el.add_xpath('comments_html', '//div[@class="detail-item"]/div[@class="tips"]')
#
#        if response.request.body == "":
#            request = FormRequest("http://www.jiajiao.com/math3/ques/partialques?r=0.1000001000030408&q=bc2d00e7-3e53-4464-9dd2-3a151c4827d4~cb3584cd-69ec-4638-8049-2564f0a45322~22&s=0&t2=9&d=0",
#                    formdata={'f':'0','p':'2'})
#            self.crawler.engine.crawl(request, spider=self)
#        else:
#            print "response.request.body = " + response.request.body
#
##        print "response.request.body = " + response.request.body
#        #return el.load_item()

#    def parse(self, response):
#        pass



