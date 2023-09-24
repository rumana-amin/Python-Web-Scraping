# Import neccessary libraries
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class BooksCategoriesSpider(CrawlSpider):
    name = "books_categories"
    #allowed_domains = ["https://www.rokomari.com/book?ref=nm"]
    start_urls = ["https://www.rokomari.com/book/category/1/book?page=1"]

    # Rules for scraping 
    rules = (Rule(LinkExtractor(restrict_xpaths='//div[@class="home-details-btn-wrapper"]/a', deny=['^https://www.rokomari.com/product/']),
                   callback ="parse_item", follow = False),
            Rule(LinkExtractor(restrict_xpaths='//a[text() =  "Next"]'), follow = True))
    

    def parse_item(self, response):
        try:
            original_price = int(response.xpath('//strike[@class="original-price"]/text()').get().replace("TK. ",'').replace(',' ,'').strip())
        except:
            original_price = int(response.xpath('//span[@class="sell-price"]/text()').get().replace(' TK. ','').replace(',', '').strip())

        try:
            discount_amount = int(response.xpath('//span[@class="price-off pl-2"]/text()[2]').get().replace(" TK. ", '').replace(',', '').strip())
        except:
            discount_amount = ''
        
        try:
            discount_percent = round(float(discount_amount/original_price),2)
        except: 
            discount_percent = ''


        try:
            stock_availability = response.xpath('//figure[@class="stock-available"]/text()[2]').get().strip()
        except:
            stock_availability = ''

        try:
            no_of_copies = int(response.xpath('//span[@class="text-danger ml-1"]/text()').get().replace('(only ','').replace(' copies ','').replace(' copy','').replace('left)',''))
        except:
            no_of_copies = ''

        try:
            no_of_reviews = response.xpath('//span[@class="ml-2"]/a/text()').get().replace(' Reviews','').replace(' Review','')
        except:
            no_of_reviews = ''

        try:
            ebook = response.xpath('//div[@class="ebook-info"]/p/text()[1]').get().replace('Get eBook Version', 'Yes')
        except:
            ebook = 'No' 

        try:
            ebook_price = int(response.xpath('//p[@class="ebook-price"]/text()').get().replace('TK. ', '').replace(',' , ''))
        except:
            ebook_price = ''

        try:
            edition = response.xpath('//tr/td[contains(text(), "Edition")]/following-sibling::td/text()').get()
        except:
            edition = ''
    
        yield{
                'url': response.url,
                'Title': response.xpath('//tr/td[contains(text(), "Title")]/following-sibling::td/text()').get().strip(),
                'Author':response.xpath('//p[@class="details-book-info__content-author"]/a/text()').getall(),   
                'Category': response.xpath('//a[@ class="ml-2"]/text()').get().strip(),
                'Original Price': original_price,
                'Sale Price': int(response.xpath('//span[@class="sell-price"]/text()').get().replace(' TK. ','').replace(',', '').strip()),
                'Discount Amount':discount_amount,
                'Discount Percentage': discount_percent,
                'Stock Availability': stock_availability,
                'No of copies available': no_of_copies,
                'No of Reviews': no_of_reviews, 
                'E Book Availability': ebook,
                'E Book Price': ebook_price,
                'Publisher': response.xpath('//td[@class="publisher-link"]/a/text()').get(),
                'ISBN': response.xpath('//tr/td[contains(text(), "ISBN")]/following-sibling::td/text()').get(),
                'Edition': edition,
                'Number of Pages': response.xpath('//tr/td[contains(text(), "Number of Pages")]/following-sibling::td/text()').get(),
                'Country': response.xpath('//tr/td[contains(text(), "Country")]/following-sibling::td/text()').get(),
                'Language': response.xpath('//tr/td[contains(text(), "Language")]/following-sibling::td/text()').get(),
                
            }