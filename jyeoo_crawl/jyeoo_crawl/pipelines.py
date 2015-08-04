# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from Html2Text import html_to_text
from UploadUrl import replace_pic, upload

from scrapy import log

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
        (question_html, question_pic) = replace_pic(item['question_html'], self.picfile)
        (ans_html, ans_pic) = replace_pic(item['ans_html'], self.picfile)
        (parse_html, parse_pic) = replace_pic(item['parse_html'], self.picfile)
        (comments_html, comments_pic) = replace_pic(item['comments_html'], self.picfile)

        question_txt = html_to_text(question_html)
        ans_txt = html_to_text(ans_html)
        parse_txt = html_to_text(parse_html)

        print "question_html = " + question_html.encode('gb18030')
        print "ans_html = " + ans_html.encode('gb18030')
        print "parse_html = " + parse_html.encode('gb18030')
        print "comments_html = " + comments_html.encode('gb18030')

        #updatecur.execute(addtoraw, (url, question_html, "good"))
        #updateconn.commit()
        self.updatecur.execute(self.addtoclassified, (question_txt, question_html, ans_txt, ans_html, parse_txt, parse_html, comments_html, item['question_url']))
        self.updateconn.commit()
        #print "good\t" + url

        totalpic = question_pic + ans_pic + parse_pic + comments_pic
        picset = set(totalpic)

        singlenum = len(picset)
        if singlenum > 0:
          self.num += singlenum

          for i in picset:
            #upload pic implement 
            #todo ...
            self.MsgQueue.put((i, self.num))




        #add tags and category
        #if item['referer'] in self.m_albumlist:
        #    item['category'] = self.m_albumlist[item['referer']][0]
        #    extra_tags = self.m_albumlist[item['referer']][1]
        #    if extra_tags != "":
        #        item['tag'] = item['tag'] + "," + extra_tags

        ##insert into mysql db
        #try:
        #    print len(item['ori_pic_src'])
        #    for i in range(len(item['ori_pic_src'])):
        #        #test Variaty
        #        if not self.varified(item, i):
        #            print item['ori_pic_src'][i] + " is not varified!"
        #            continue
        #    
        #        if self.m_dbcur.execute(self.m_testQuery, (item['ori_pic_src'][i], )):
        #            print item['ori_pic_src'][i] + " has in db before we insert!"
        #        else:
        #            #2015年6月16日18:17:23 by yuanshaofei set category to 动图 and set category to tag
        #            item['tag'] = item['category']
        #            item['category'] = "动图"
        #            #2015年6月16日18:17:23 by yuanshaofei set category to 动图 and set category to tag

        #            print "update to server" + item['page_url']
        #            self.m_dbcur.execute(self.m_insertQuery, (
        #                item['ori_pic_src'][i],
        #                item['pic_title'][i],
        #                item['img_desc'][i],
        #                item['page_url'],
        #                item['page_title'],
        #                item['publish_time'],
        #                item['tag'],
        #                item['category'],
        #                item['referer']))
        #            self.m_dbconn.commit()
        #            print "update to server " + item['page_url']
        #except Exception, e:
        #    print e

        return item
