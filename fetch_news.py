import scrapy
from scrapy.http import Request


class FetchNewsSpider(scrapy.Spider):
    name = "fetch_news"
    allowed_domains = ["coronavirus.health.ok.gov"]
    start_urls = ["https://coronavirus.health.ok.gov/news"]

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
            yield Request(url=response.urljoin(href), callback=self.save_article)

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

    def save_article(self, response):
        filename = "data/html/news/%s.html" % response.url.split("/")[-1]
        self.logger.info(f"Saving {response.url} to {filename}")
        with open(filename, "w") as f:
            f.write(response.css("div.main").extract_first())
