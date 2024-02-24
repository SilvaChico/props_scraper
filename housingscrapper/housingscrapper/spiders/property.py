import scrapy
import random
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


    user_agent_list = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 14_4_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1',
        'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 Edg/87.0.664.75',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18363',
    ]

    def start_requests(self):
        for url in self.start_urls:
            return Request(url=url, callback=self.parse,
                        headers={"User-Agent": user_agent_list[random.randint(0, len(user_agent_list)-1)]})

