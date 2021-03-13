import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class FatosSpider(CrawlSpider):
    name = 'fatos'
    allowed_domains = ['aosfatos.org']
    start_urls = ['http://aosfatos.org/']

    rules = (
        Rule(LinkExtractor(restrict_xpaths=('//nav//ul//li//ul/li/a[re:test(@href, "checamos")]'))
        ),
        Rule(
            LinkExtractor(
                restrict_css=('.pagination a')
            )
        ),
        Rule(
            LinkExtractor(restrict_css=('.entry-card')
            ),
            callback='parse_new'
            )
        )

    def parse_new(self, response):
        title = response.css('article h1::text').get()
        data = ' '.join(response.css('p.publish_date::text').get().split())

        quotes = response.css('article blockquote p')
        for quote in quotes:
            quote_text = quote.css('::text').get()
            status = quote.xpath('./parent::blockquote/preceding-sibling::figure//figcaption//text()').get()

            if quote_text == '\r\n':
                continue
            if status == '\r\n':
                status = 'INDEFINIDO'

            yield {
                'url': response.url,
                'title': title,
                'date': data,
                'quotes': quote_text,
                'status': status
            }


