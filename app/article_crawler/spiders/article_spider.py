from pathlib import Path
from typing import Any, Iterable
import scrapy
from scrapy.http import Request, Response
from helpers.funcs import get_urls_from_csv

class ArticleSpider(scrapy.Spider):
    name = "articles"

    def start_requests(self) -> Iterable[Request]:
        urls = get_urls_from_csv(r"C:\Users\nahar\OneDrive\desktop\upwork\affiliate_product_recommendation_tool\article_urls.csv")
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
    
    def parse(self, response: Response, **kwargs: Any) -> Any:
        title = response.css(".tdb-title-text::text").get()
        paragraph = response.css("div.tdb-block-inner.td-fix-index").xpath("string(//p[1])").get()
        data = {"url": response.url, "title": title, "first_paragraph": paragraph}
        if data['title'] == None or data['first_paragraph'] == None:
            yield None
        else:
            yield data