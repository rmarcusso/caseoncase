import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class FatosSpider(CrawlSpider):
    name = 'fatos'
    allowed_domains = ['aosfatos.org']
    start_urls = ['http://aosfatos.org/']

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//nav//ul//li//ul/li/a[re:test(@href, "checamos")]')
             ),
        Rule(
            LinkExtractor(restrict_css='.pagination a')
        ),
        Rule(
            LinkExtractor(restrict_css='.entry-card'),
            callback='parse_new'
        )
    )
    def parse_new(self, response):

        title = response.css('article h1::text').get()
        data = ' '.join(response.css('p.publish_date::text').get().split())
        dia, mes, ano = data.split(' ')[0], data.split(' ')[2], data.split(' ')[4].replace(',', '')

        quotes = response.css('article blockquote p')
        for quote in quotes:
            # quote_text = quote.css('::text').get()
            quote_text = ''.join(quote.css('::text').extract())
            status = quote.xpath('./parent::blockquote/preceding-sibling::figure//figcaption//text()').get()

            numero_mes = {'janeiro': 1, 'fevereiro': 2, 'março': 3, 'abril': 4, 'maio': 5, 'junho': 6, 'julho': 7,
                        'agosto': 8, 'setembro': 9, 'outubro': 10, 'novembro': 11, 'dezembro': 12}

            if quote_text == '\r\n' or not quote_text:
                # continue
                quote_text = 'Texto inexistente'
            if status == '\r\n' or not status:
                # continue
                status = 'OUTLIER'

            yield {
                'url': response.url,
                'title': title,
                'date': data,
                'dia': dia,
                'numero_mes': numero_mes[mes],
                'mes': mes.capitalize(),
                'ano': ano,
                'quotes': quote_text,
                'status': status
            }
