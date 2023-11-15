import scrapy

from yatube_parsing.items import YatubeParsingItem


class YatubeSpider(scrapy.Spider):
    name = "yatube"
    allowed_domains = ["51.250.32.185"]
    start_urls = ["http://51.250.32.185/"]

    def parse(self, response):
        for card in response.css('div.card-body'):
            text = ' '.join(
                t.strip() for t in card.css('p::text').getall()
            ).strip()
            data = {
                'author': card.css('strong::text').get(),
                'text': text,
                'date': card.css('small::text').get(),
            }
            yield YatubeParsingItem(data)

        next_page = response.xpath("//a[contains(., 'Следующая')]/@href").get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
