# -*- coding: utf-8 -*-
import hashlib
import urllib2
import random

def getmd5(str):
  m = hashlib.md5()
  m.update(str)
  return m.hexdigest()

def getdetailurllist(html_doc, base="http://www.zuoyetong.com.cn"):
  oriurllist = []
  urllist = []
  if not html_doc:
    return (oriurllist, urllist)

  start = html_doc.find("src=")
  while start != -1: 
    first = start + 4 
    if html_doc[first:first+1] == "\"":
      first += 1
    elif html_doc[first:first+2] == "\\\"":
      first += 2
    else:
      start = html_doc.find("src=", first+1)
      continue

    last = html_doc.find("\"", first)
    oriurl = ""
    if first != -1 and last != -1: 
      if html_doc[last-1: last+1] == "\\\"" :
        last -= 1

      oriurl = html_doc[first: last]
      url = oriurl
      if url[0:1] == "/":
        url = base + oriurl
      oriurllist.append(oriurl)
      urllist.append(url)
    start = html_doc.find("src=", last+1)
  return (oriurllist, urllist)




def replace_pic(html, picfile):        
  (oriurllist, urllist) = getdetailurllist(html, "http://www.zuoyetong.com.cn")
  appid = "200516"
  uploadurllist = []

  for i in range(len(urllist)):
    key = getmd5(urllist[i])
    print >> picfile, urllist[i] + "\t" + key
    #showurl = "http://imgstore.cdn.sogou.com/" + appid + "/" + key
    #example: http://img01.sogoucdn.com/app/a/200516/31f07a90e628d26de07228bf18bc20b9
    showurl = "http://img0" + str(random.randint(1,3)) + ".sogoucdn.com/app/a/" + appid + "/" + key
    uploadurl = "http://innerupload01.picupload.djt.sogou-op.org/http_upload?url1=" + urllist[i] + "&sign_url1=" + key + "&appid=" + appid + "&referer="
    uploadurllist.append(uploadurl)
    html = html.replace(oriurllist[i], showurl)
  
  return (html, uploadurllist)

def isGoodRet(reponse):
  if reponse.find('"status":"0"') != -1:
    return True
  else:
    return False

def upload(url):
  try:
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    if isGoodRet(response.read().decode('gb18030')):
      return True
    else:
      return False
  except:
    return False


