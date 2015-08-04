# -*- coding: utf-8 -*-

from HTMLParser import HTMLParser
import htmlentitydefs

class HTMLTextExtractor(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.result = [ ]

    def handle_data(self, d):
        self.result.append(d)

    def handle_charref(self, number):
        codepoint = int(number[1:], 16) if number[0] in (u'x', u'X') else int(number)
        self.result.append(unichr(codepoint))

    def handle_entityref(self, name):
        if name in htmlentitydefs.name2codepoint:
            codepoint = htmlentitydefs.name2codepoint[name]
            self.result.append(unichr(codepoint))
        else:
            self.result.append(name)

    def get_text(self):
        return u''.join(self.result)

def html_to_text(html): #保留实体符号  
    try:
        s = HTMLTextExtractor()
        s.feed(html)
        return s.get_text()
    except Exception,e:
        print Exception, ": ", e 
        print html.encode('gb18030')
        return html
   


