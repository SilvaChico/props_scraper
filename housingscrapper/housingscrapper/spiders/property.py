import scrapy
from pathlib import Path
from scrapy.shell import inspect_response

class PropertySpider(scrapy.Spider):
    name = "property"
    allowed_domains = ["idealista.pt"]
    start_urls = [
        "https://www.idealista.pt/comprar-casas/lisboa/pagina-1"
        # "https://www.idealista.pt/comprar-casas/lisboa/pagina-2"
    ]
    user_agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'

    def parse(self, response):
        inspect_response(response, self)
        page = response.url.split("pagina-")[-1]
        filename = f"quotes-{page}.html"
        Path(filename).write_bytes(response.body)
