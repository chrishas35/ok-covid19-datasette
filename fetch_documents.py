import scrapy
from scrapy.http import Request


class FetchDocumentsSpider(scrapy.Spider):
    name = "fetch_documents"
    allowed_domains = ["coronavirus.health.ok.gov"]

    start_urls = [
        "https://coronavirus.health.ok.gov/executive-order-reports",
    ]

    def parse(self, response):
        do_history = False
        if getattr(self, "history", None):
            do_history = True

        if do_history:
            links = response.css("h3.field-content a::attr(href)").extract()
        else:
            links = [response.css("h3.field-content a::attr(href)").extract_first()]

        for href in links:
            self.logger.info(f"Found article page {href}")
            yield Request(url=response.urljoin(href), callback=self.parse_article_page)

        if not do_history:
            return

        next_page_link = None
        for page_link in response.css("ul.pagination li.arrow a"):
            if page_link.xpath("@title").extract()[0] == "Go to next page":
                next_page_link = page_link.xpath("@href").extract()[0]
                self.logger.info(f"Found pagination for {next_page_link}")
                yield Request(url=response.urljoin(next_page_link), callback=self.parse)

        if not next_page_link:
            self.logger.info("No next page link found.")

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
