from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from parcer.spiders.HabrSpider import HabrSpider


if __name__ == '__main__':
    process = CrawlerProcess(get_project_settings())
    process.crawl(HabrSpider, q='go')
    process.start()
