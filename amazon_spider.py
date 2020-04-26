import scrapy

import re

class Amazonspider(scrapy.Spider):
    name = "amazon_spider"
    global domain_name 
    domain_name="https://www.amazon.in"
    allowed_domain=["amazon.in"]   #scrapping only from amazon is allowed
    start_urls=(
        # airpods ==> 1 product 
        #    "https://www.amazon.in/Apple-AirPods-with-Charging-Case/dp/B07Q6153FQ/ref=sr_1_1_sspa?crid=3QV7601VZWVBM&keywords=apple+airpod&qid=1577116618&s=electronics&sprefix=apple+ai%2Celectronics%2C285&sr=1-1-spons&psc=1&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUEyUDBaRkJVMlg5VUMwJmVuY3J5cHRlZElkPUEwMjM3MjQ5MkxUN0JaN1pMTFhHOCZlbmNyeXB0ZWRBZElkPUEwODUxNzkyMzRRWlBITE5XTTM5NyZ3aWRnZXROYW1lPXNwX2F0ZiZhY3Rpb249Y2xpY2tSZWRpcmVjdCZkb05vdExvZ0NsaWNrPXRydWU=",
        # List of all products: page 1 url
            # "https://www.amazon.in/s?k=airpods&i=electronics&ref=nb_sb_noss",
        # All the url
             "https://www.amazon.in/s?k=airpods&i=electronics&qid=1577170626&ref=sr_pg_1",
           )

          

    def parse(self,response):
        print("=========================================")
        all_page_urls = response.xpath("//ul[@class='a-pagination']").extract_first()
        starting_index = all_page_urls.find("href=")
        res_url = all_page_urls[starting_index+5:]
        print(res_url)
        # res_url = res_url[starting_index:res_url.find("=")]
        print(res_url[1:res_url.find("=")])
        res = res_url[1:res_url.find("=")]
        # print(res)
        for i in range(10):
            res_temp = "https://www.amazon.in"+res+"=airpods&amp;rh=n%3A976419031&amp;page="+str(i)
            print(res_temp)
            yield scrapy.Request(res_temp,callback=self.one_page)
        

    def one_page(self,response):
        print("=============== ALL LINKS ================")
        urls = response.xpath("//a[@class='a-link-normal a-text-normal']/@href").extract()
        print("Total no. of urls:",len(urls))
        for every_urls in urls:
            every_urls = "https://www.amazon.in"+every_urls
            yield scrapy.Request(every_urls, callback=self.parse_page)
            

    def parse_page(self,response):
        # print(response.text)
        # Extracting title
        print("========================PROJECT INFO======================")
        produc_name=response.xpath("//span[@id='productTitle']/text()").extract()
        print("========================product name======================")
        produc_name = produc_name[0]
        produc_name = re.sub(' +',' ',produc_name)
        produc_name = produc_name.replace("\n", '')
        produc_name = produc_name.strip()
        print(produc_name)
        print("==========================================================")
        
        print("========================Overall Rating======================")
        all_rating = response.xpath("//span[@class='a-icon-alt']/text()").extract_first()
        print(all_rating)
        print("==========================================================")

        print("========================Meta Description======================")
        description = response.xpath("//meta[@name='description']/@content").extract_first()
        print(description)
        print("==========================================================")

        print("========================Reviews======================")
        revs = response.xpath("//div[@class='a-expander-content reviewText review-text-content a-expander-partial-collapse-content']/text()").extract()
        print(revs)
        print("==========================================================")

        print("==========================================================")
