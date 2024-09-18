import scrapy
from string import digits


class GutenbergSpider(scrapy.Spider):
    name = 'gutenbergspider'
    start_urls = ["https://www.gutenberg.org/ebooks/bookshelf/"]
    textbooks_categories = ["Anthropology", "Anthropology", "Architecture", "Art", "Biographies", "Biology", "Botany", "British Law", 
                            "Chemistry", "Classical Antiquity", "Current History", "Ecology", "Crafts", "Education", "Engineering", 
                            "English Civil War", "Geology", "Manufacturing", "Maps and Cartography", "Mathematics", "Medicine", "Microbiology", 
                            "Microscopy", "Mycology", "Philosophy", "Photography", "Physics", "Physiology", "Poetry", "Politics", "Psychology", 
                            "Science", "Sociology", "Technology", "Zoology"]

    def parse(self, response):
        for subject in response.css('.bookshelf_pages > ul > li > a'):
            subjlink = subject.css('a::attr(href)').get()
            subjname = subject.css('a::text').get()
            if subjlink is not None:
                yield(response.follow(subjlink, self.parsesubject(subjname)))
    
    def parsesubject(self, subjname):
        def callback(response):
            for book in response.css('.booklink > a'):
                booklink = book.css('a::attr(href)').get()
                if booklink is not None:
                    yield(response.follow(booklink, self.parsebook(subjname)))
                
                links = response.css('.links > a')[0:3]
                for link in links:
                    if link.css('a::attr(accesskey)') == '+':
                         yield(response.follow( link.css('a::attr(href)').get() , self.parsesubject(subjname)))
        return callback

    def parsebook(self, subjname):
        def callback(response):
            rows = response.css('.bibrec > tr')
            author = ''
            title = ''
            subjects = [subjname]
            description = ''
            for row in rows:
                header = row.css('th::text').get()
                if header is not None:
                    if header.startswith('Author'):
                        author = row.css("td > a::text").get()
                        author = author.translate(str.maketrans('', '', digits)) 
                    
                    if header.startswith('Title'):
                        title = row.css("td::text").get()

                    if header.startswith('Subject'):
                        subj = row.css("td > a::text").get()
                        if subj.replace("\n", "") in self.textbooks_categories:
                            subjects.append(subj.replace("\n", ""))
                            
            yield{
                'author': author.replace("\n", ""),
                'title':title.replace("\n", ""),
                'subjects':subjects,
                'description': description.replace("\n", ""),
                'url' : response.request.url
            }
        return callback
