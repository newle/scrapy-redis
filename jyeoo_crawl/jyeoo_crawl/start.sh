mkdir -p storeurl

scrapy crawl jiajiao > jiajiao.log 2>&1 &
scrapy crawl mofangge > mofangge.log 2>&1 &
