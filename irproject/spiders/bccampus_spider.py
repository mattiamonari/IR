import scrapy

class BccampusSpider(scrapy.Spider):
    name = 'bccampus'
    start_urls = ['https://collection.bccampus.ca/search']

    def parse(self, response):
        for subject in response.css('.card'):
            subject_text = subject.css('.bccampus-search-filter-box-label::text').get()
            subsubject_page_url = subject.css('a::attr("href")').get()
            if subsubject_page_url is not None:
                yield response.follow(
                    subsubject_page_url,
                    self.parse_subsubject(subject_text, ''),
                )

    def parse_subsubject(self, subject_text, subsubject_text):
        def parse_subsubject_callback(subsubject_page):
            textbook_div = None
            for div in subsubject_page.css('.bccampus-search-container > div'):
                div_heading_text = div.css('.bccampus-typography-heading::text').get()
                if div_heading_text and div_heading_text.startswith('Textbooks'):
                    textbook_div = div
                    break
            if textbook_div is None:
                return
            # cannot click on show-more button so just get top-listed textbooks
            for textbook in textbook_div.css('.bccampus-textbook-info-card'):
                textbook_page_url = textbook.css('a::attr("href")').get()
                yield subsubject_page.follow(
                    textbook_page_url,
                    self.parse_textbook(subject_text, subsubject_text),
                )
        return parse_subsubject_callback

    def parse_textbook(self, subject_text, subsubject_text):
        def parse_textbook_callback(textbook_page):
            title = textbook_page.css('h1::text').get()
            author = ''
            for row in textbook_page.css('.bccampus-page-section-content .ant-row'):
                row_text = row.css('::text').getall()
                if row_text[0] and row_text[1] and row_text[0].startswith('Author'):
                    author = row_text[1]
                    break
            desc_section = textbook_page.css('.bccampus-cms-content')[0]
            description = ''.join(desc_section.css('::text').getall())
            yield {
                'url': textbook_page.url,
                'subjects': [subject_text],
                'title': title,
                'author': author,
                'description': description,
            }
        return parse_textbook_callback
