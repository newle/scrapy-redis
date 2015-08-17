# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider, Rule
from scrapy.http import Request
from scrapy.linkextractors import LinkExtractor
from scrapy_redis.spiders import RedisMixin
from jyeoo_crawl.items import JyeooCrawlItem, JyeooCrawlLoader

#from Html2Text import html_to_text
import re
import logging



manfen_detail_regex = re.compile("http://www.manfen5.com/stinfo/")
def process_manfen_url(value):
    if manfen_detail_regex.search(value) is None:
        return None
    return value


def getLabel(url):
    localurl = url.lower()
    if localurl.find("cz_yw"):
        return "初中语文".decode("utf8")
    elif localurl.find("cz_sx"):
        return "初中数学".decode("utf8")
    elif localurl.find("cz_yy"):
        return "初中英语".decode("utf8")
    elif localurl.find("cz_wl"):
        return "初中物理".decode("utf8")
    elif localurl.find("cz_hx"):
        return "初中化学".decode("utf8")
    elif localurl.find("cz_sw"):
        return "初中生物".decode("utf8")
    elif localurl.find("cz_ls"):
        return "初中历史".decode("utf8")
    elif localurl.find("cz_zz"):
        return "初中政治".decode("utf8")
    elif localurl.find("cz_dl"):
        return "初中地理".decode("utf8")
    elif localurl.find("gz_yw"):
        return "高中语文".decode("utf8")
    elif localurl.find("gz_sx"):
        return "高中数学".decode("utf8")
    elif localurl.find("gz_yy"):
        return "高中英语".decode("utf8")
    elif localurl.find("gz_wl"):
        return "高中物理".decode("utf8")
    elif localurl.find("gz_hx"):
        return "高中化学".decode("utf8")
    elif localurl.find("gz_sw"):
        return "高中生物".decode("utf8")
    elif localurl.find("gz_ls"):
        return "高中历史".decode("utf8")
    elif localurl.find("gz_zz"):
        return "高中政治".decode("utf8")
    elif localurl.find("gz_dl"):
        return "高中地理".decode("utf8")








class manfenSpider(RedisMixin, CrawlSpider):
    """Spider that reads urls from redis queue (manfen:start_urls)."""
    name = "manfen"
    redis_key = "manfen:start_urls"
    rules =  (
            Rule(LinkExtractor(process_value = process_manfen_url), callback='parse_page', follow=False),
    )

    def __init__(self, *args, **kwargs):
        domain = kwargs.pop('domain', '')
        self.alowed_domains = filter(None, domain.split(','))
        super(manfenSpider, self).__init__(*args, **kwargs)

    def _set_crawler(self, crawler):
        CrawlSpider._set_crawler(self, crawler)
        RedisMixin.setup_redis(self)

    def parse_page(self, response):
        #answerurl="http://www.1010manfen.com/qiuda.php?questionid="+getdetailurl(questionhtml)
        #answerhtml=fetchhtml(answerurl)
        #if(answerhtml != ""):

        el = JyeooCrawlLoader(response = response)
        el.add_value('question_url', response.url)
        el.add_xpath('label_html', '//div[@class="xiti-content"]/div[@class="ndwz"]')
        el.add_xpath('question_html', '(//div[@class="timutext"])[1]')
        el.add_xpath('ans_html', '(//div[@class="answer_inner"])[1]')

        return el.load_item()

    def parse_manfen_detail_page(self, response):
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
#        #el = manfenCrawlLoader(response = response)
#        #el.add_value('question_url', response.url)
#        #el.add_xpath('question_html', '//div[@class="result-content"]')
#        #el.add_xpath('ans_html', '//div[@class="detail-item"]/div[@class="answer"]')
#        #el.add_xpath('parse_html', '//div[@class="detail-item"]/div[@class="analysis"]')
#        #el.add_xpath('comments_html', '//div[@class="detail-item"]/div[@class="tips"]')
#
#        if response.request.body == "":
#            request = FormRequest("http://www.manfen.com/math3/ques/partialques?r=0.1000001000030408&q=bc2d00e7-3e53-4464-9dd2-3a151c4827d4~cb3584cd-69ec-4638-8049-2564f0a45322~22&s=0&t2=9&d=0",
#                    formdata={'f':'0','p':'2'})
#            self.crawler.engine.crawl(request, spider=self)
#        else:
#            print "response.request.body = " + response.request.body
#
##        print "response.request.body = " + response.request.body
#        #return el.load_item()

#    def parse(self, response):
#        pass



