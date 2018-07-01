# -*- coding: utf-8 -*-
import scrapy


class NbuCrawlerSpider(scrapy.Spider):
    name = 'nbu_crawler'
    allowed_domains = ['https://bank.gov.ua/control/uk/curmetal/detail/currency?period=daily']
    start_urls = ['https://bank.gov.ua/control/uk/curmetal/detail/currency?period=daily']

    def parse(self, response):
        currencies_table = response.css('.content div + table + table')
        rows = currencies_table.css('tr')[1:]
        for row in rows:
            (_, symbol, count, name, cost) = row.css('td::text').extract()
            try:
                count = int(count)
                cost = float(cost)
                cost /= count
            except ValueError:
                self.logger.warning(f'Parsing row. ValueError: <{count}> not an integer!')
            except ZeroDivisionError:
                self.logger.warning('Parse row. ZeroDivisionError: Count is Zero!')
            else:
                yield {
                    'symbol': symbol,
                    'name': name,
                    'cost': cost,
                }
