# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from Html2Text import html_to_text
from UploadUrl import replace_pic, upload

import logging

import MySQLdb
import time
import Queue
import threading


def UploadUrl(msgQueue, suffix):
  storeurl = open("storeurl/storeurl_" + str(suffix), "w")
  while True:
    if msgQueue.empty():
      time.sleep(0.001)
    else:
      url = msgQueue.get()
      if url == "-1":
        break

      (url, id) = url
      if upload(url) :
        print >> storeurl, "good\t" + str(id) + "\t" + url
      else:
        print >> storeurl, "bad\t" + str(id) + "\t" + url
  storeurl.close()

def getSQL(url):
    s = "(label_txt, label_html, question_txt, question_html, ans_txt, ans_html, parse_txt, parse_html, comments_html, question_url) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
    if url.find("1010jiajiao.com") != -1:
        return "replace into jiajiao_classified_2" + s
    elif url.find("jyeoo.com") != -1 or url.find("zuoyetong.com") != -1:
        return "replace into jyeoo_raw" + s

def rmGarbageText(html):
    garbagetext = [
            "添加到我的练习册",
            ]
    for i in range(len(garbagetext)):
        html = html.encode('utf8').replace(garbagetext[i], "").decode('utf8')
    return html

class JyeooCrawlPipeline(object):
    picfile = open('picurl.txt', 'w')

    updateconn = MySQLdb.connect("mysql02.edu.sjs", "edu","EDU2014","edu", charset='utf8', use_unicode=False)
    updatecur = updateconn.cursor()
    addtoclassified = "replace into jyeoo_raw(question_txt, question_html, ans_txt, ans_html, parse_txt, parse_html, comments_html, question_url) values(%s, %s, %s, %s, %s, %s, %s, %s);"

    MsgQueue = Queue.Queue(2000)
    threadlist = []
    threadnum = 20
    num = 0
    def __init__(self):
        for i in range(self.threadnum):
          self.threadlist.append(threading.Thread(target=UploadUrl, args = (self.MsgQueue, i, )))

        for i in range(self.threadnum):
          self.threadlist[i].start()


    def process_item(self, item, spider):
        if 'question_html' in item and 'ans_html' in item:
            pass
        else:
            logging.debug("crawl question_html failed")
            return

        (question_html, question_pic) = replace_pic(item['question_html'] if 'question_html' in item else "", self.picfile)
        (ans_html, ans_pic) = replace_pic(item['ans_html'] if 'ans_html' in item else "", self.picfile)
        (parse_html, parse_pic) = replace_pic(item['parse_html'] if 'parse_html' in item else "", self.picfile)
        (comments_html, comments_pic) = replace_pic(item['comments_html'] if 'comments_html' in item else "", self.picfile)
        (label_html, label_pic) = replace_pic(item['label_html'] if 'label_html' in item else "", self.picfile)

        ans_html = rmGarbageText(ans_html)

        question_txt = html_to_text(question_html)
        ans_txt = html_to_text(ans_html)
        parse_txt = html_to_text(parse_html)
        label_txt = html_to_text(label_html)

        print "question_html = " + question_html.encode('gb18030')
        print "ans_html = " + ans_html.encode('gb18030')
        print "parse_html = " + parse_html.encode('gb18030')
        print "comments_html = " + comments_html.encode('gb18030')
        print "label_html = " + label_html.encode('gb18030')

        #updatecur.execute(addtoraw, (url, question_html, "good"))
        #updateconn.commit()
        self.updatecur.execute(getSQL(item['question_url']), (label_txt, label_html, question_txt, question_html, ans_txt, ans_html, parse_txt, parse_html, comments_html, item['question_url']))
        self.updateconn.commit()
        #print "good\t" + url

        totalpic = question_pic + ans_pic + parse_pic + comments_pic + label_pic
        picset = set(totalpic)

        singlenum = len(picset)
        if singlenum > 0:
          self.num += singlenum

          for i in picset:
            #upload pic implement 
            #todo ...
            self.MsgQueue.put((i, self.num))
        return item
