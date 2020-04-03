# -*- coding: utf-8 -*-
import scrapy


class FetchHomepageSpider(scrapy.Spider):
    name = "fetch_homepage"
    allowed_domains = ["coronavirus.health.ok.gov"]
    start_urls = ["https://coronavirus.health.ok.gov/"]

    def parse(self, response):
        filename = "data/html/osdh-homepage-latest.html"
        self.logger.info(f"Saving {response.url} to {filename}")
        with open(filename, "w") as f:
            f.write(response.css("div.two-thirds-left div.inside").get())
