import scrapy
from scrapy.http import Request


class FetchDocumentsSpider(scrapy.Spider):
    name = "fetch_documents"
    allowed_domains = ["coronavirus.health.ok.gov"]

    # TODO: Improve pagination handling
    # https://stackoverflow.com/questions/12847965/scrapy-parsing-items-that-are-paginated
    start_urls = [
        "https://coronavirus.health.ok.gov/executive-order-reports?page=%s" % page
        for page in range(-1, 2)
    ]

    def parse(self, response):
        for href in response.css("h3.field-content a::attr(href)").extract():
            yield Request(url=response.urljoin(href), callback=self.parse_article_page)

    def parse_article_page(self, response):
        for href in response.css("span.file a::attr(href)").extract():
            if not href.endswith(".pdf"):
                self.logger.info(f"Found non-PDF file {href}")
                continue
            yield Request(url=response.urljoin(href), callback=self.save_pdf)

    def save_pdf(self, response):
        filename = response.url.split("/")[-1]
        self.logger.info("Saving PDF %s", filename)
        with open(f"data/pdfs/{filename}", "wb") as f:
            f.write(response.body)
