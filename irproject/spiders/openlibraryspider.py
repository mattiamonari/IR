import scrapy
import re

class OpenLibrarySpider(scrapy.Spider):
    name = 'openlibrary'
    start_urls = ['https://openlibrary.org/search?subject=Textbooks']

    def parse(self, response):
        for book in response.css(".searchResultItem > .details > .resultTitle > .booktitle > a"):
            yield response.follow(book.css("a::attr(href)").get(), self.scrape_book())
        for page in response.css(".ChoosePage"):
            if page.css('a::text').get().startswith("Next") :
                yield response.follow(page.css("a::attr(href)").get(), self.parse)
                


    
    def scrape_book(self):
        def callback(response):
            title = response.css('.work-title::text').get().replace("\n","").replace("\t","").replace("\r","")
            author = response.css('.edition-byline > a::text').get().replace("\n","").replace("\t","").replace("\r","")
            description = response.css('.book-description > .book-description-content > p::text').get().replace("\n","").replace("\t","").replace("\r","")
            description = re.sub("\s+", " ", description)
            subjname = response.css(".link-box > span > a::text").getall()
            yield{
                'subjects': subjname,
                'title': title,
                'author': author,
                'description': description,
                'url' : response.request.url
            }
        return callback