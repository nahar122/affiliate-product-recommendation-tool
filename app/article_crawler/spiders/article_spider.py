from pathlib import Path
from typing import Any, Iterable
import scrapy
from scrapy.http import Request, Response
# from helpers.funcs import get_urls_from_csv
from scrapy.crawler import CrawlerProcess

class ArticleSpider(scrapy.Spider):
    name = "articles"
    urls_to_scrape = []  # Class attribute to store URLs
    def start_requests(self) -> Iterable[Request]:
        # urls = get_urls_from_csv(r"C:\Users\nahar\OneDrive\desktop\upwork\affiliate_product_recommendation_tool\article_urls.csv")
        for url in self.urls_to_scrape:
            yield scrapy.Request(url=url, callback=self.parse)
    
    # def parse(self, response: Response, **kwargs: Any) -> Any:
    #     title = 'insert_title'
    #     paragraph = response.css("div.tdb-block-inner.td-fix-index").xpath("string(//p[1])").get()
    #     data = {"url": response.url, "title": title, "paragraph": paragraph}
    #     if data['title'] == None or data['paragraph'] == None:
    #         yield None
    #     else:
    #         yield data
    
    def parse(self, response):
        # Extract the first <h1> tag for the title
        title = response.xpath('//h1/text()').get()

        # Initialize the first paragraph variable
        first_paragraph = None

        # Check all <p> tags
        for p in response.xpath('//p'):
            # Extract text from <p> tag
            paragraph_text = p.xpath('string()').get()
            # Count words
            word_count = len(paragraph_text.split())
            # If word count is more than 30, set as first paragraph and break loop
            if word_count > 30:
                first_paragraph = paragraph_text
                break

        # If no suitable <p> tag found, get all text after <h1> until the first <br>
        if not first_paragraph:
            first_paragraph = ''.join(response.xpath('//h1/following-sibling::node()[not(self::br)][preceding-sibling::br[1]]/text()').getall())

        # Yield or process the extracted data
        yield {
            'url': response.url,
            'title': title,
            'paragraph': first_paragraph
        }

