import scrapy


class GroupSpider(scrapy.Spider):
    name = "group"
    allowed_domains = ["51.250.32.185"]
    start_urls = ["http://51.250.32.185/"]

    def parse(self, response):
        group_links = response.css('a.group_link::attr(href)')

        for group_link in group_links:
            yield response.follow(group_link, callback=self.parse_group)

        next_page = response.xpath("//a[contains(., 'Следующая')]/@href").get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    def parse_group(self, response):
        yield {
            'group_name': response.css('div.card-body h2::text').get(),
            'description': response.css('p.group_descr::text').get(),
            'posts_count': response.css(
                'div.h6::text').get().strip().replace('Записей: ', '')
        }
