import scrapy

class OpenUmnSpider(scrapy.Spider):
    name = 'open_umn'
    start_urls = ['https://open.umn.edu/opentextbooks']

    def parse(self, response):
        for subject in response.css('ul.subject-directory > li'):
            subject_text = subject.css('a::text').get()
            for subsubject in subject.css('ul > li'):
                subsubject_text = subsubject.css('a::text').get()
                subsubject_page_url = subsubject.css('a::attr("href")').get()
                if subsubject_page_url is not None:
                    yield response.follow(
                        subsubject_page_url,
                        self.parse_subsubject(subject_text, subsubject_text),
                    )

    def parse_subsubject(self, subject_text, subsubject_text):
        def parse_subsubject_callback(subsubject_page):
            for textbook in subsubject_page.css('div#textbook-list > div'):
                textbook_page_url = textbook.css('p.buttons > a::attr("href")').get()
                yield subsubject_page.follow(
                    textbook_page_url,
                    self.parse_textbook(subject_text, subsubject_text),
                )
            # go to the next page if more textbooks in subsubject page
            next_subsubject_page_url = subsubject_page.css('div#infinite-scrolling a.next_page::attr("href")').get()
            if next_subsubject_page_url is not None:
                yield subsubject_page.follow(
                    next_subsubject_page_url,
                    self.parse_subsubject(subject_text, subsubject_text),
                )
        return parse_subsubject_callback

    def parse_textbook(self, subject_text, subsubject_text):
        def parse_textbook_callback(textbook_page):
            title = textbook_page.css('#BasicInfo #info > h1::text').get()
            if textbook_page.css('#Contributors').get() is None:
                author = 'N/A'
            else:
                author = textbook_page.css('#BasicInfo #info > p:nth-child(5)::text').get().split(',')[0]
            description = ''.join(textbook_page.css('#AboutBook > span ::text').getall())
            yield {
                'url': textbook_page.url,
                'subjects': [subject_text, subsubject_text],
                'title': title,
                'author': author,
                'description': description,
            }
        return parse_textbook_callback
