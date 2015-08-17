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




zuoyebao_detail_regex = re.compile("http://www.1010zuoyebao.com/\w+/shiti_id_")
def process_zuoyebao_url(value):
    if zuoyebao_detail_regex.search(value) is None:
        return None
    return value


#p=2&f=0
def getnewid(url):
    values = url.split("/")
    return int(values[4]) + 1

class zuoyebaoSpider(RedisMixin, CrawlSpider):
    """Spider that reads urls from redis queue (zuoyebao:start_urls)."""
    name = "zuoyebao"
    #start_urls = [
    #        "http://www.zuoyebao.com/q/1943100",
    #        ]
    redis_key = "zuoyebao:start_urls"

    def __init__(self, *args, **kwargs):
        domain = kwargs.pop('domain', '')
        self.alowed_domains = filter(None, domain.split(','))
        super(zuoyebaoSpider, self).__init__(*args, **kwargs)

    def _set_crawler(self, crawler):
        CrawlSpider._set_crawler(self, crawler)
        RedisMixin.setup_redis(self)

    def parse(self, response):
        #answerurl="http://www.1010zuoyebao.com/qiuda.php?questionid="+getdetailurl(questionhtml)
        #answerhtml=fetchhtml(answerurl)
        #if(answerhtml != ""):

        el = JyeooCrawlLoader(response = response)
        el.add_value('question_url', response.url)
        el.add_xpath('label_html', '//div[@class="xiti-content"]/div[@class="ndwz"]')
        el.add_xpath('question_html', '//div[@id="qBodySec"]')
        el.add_xpath('type_html', '//div[@id="qBodySec"]/div[@class="hd"]')
        el.add_xpath('ans_html', '//div[@class="q-view-sec q-view-lt" and ./div[@class="hd" and contains(.,"' + "答案".decode('utf8') + '")]]')
        el.add_xpath('parse_html', '//div[@class="q-view-sec q-view-lt" and ./div[@class="hd" and contains(.,"' + "解析".decode('utf8') + '")]]')

#        logging.debug("parse_html is yes" if el.get_output_value('parse_html') is not None else "no")
    #    if el.get_output_value('ans_html') is not None :
    #        nextrequest = Request("http://www.zuoyebao.com/q/" + str(getnewid(response.url)))
    #        self.crawler.engine.schedule(nextrequest, spider=self.crawler.spider)

        return el.load_item()
