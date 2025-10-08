from fastapi import FastAPI

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from api.routers import main_router
from core.config import get_settings
from parcer.spiders.HabrSpider import HabrSpider


settings = get_settings()
# if __name__ == '__main__':
#     process = CrawlerProcess(get_project_settings())
#     process.crawl(HabrSpider, q='go')
#     process.start()

app = FastAPI(title=settings.title, description=settings.description)

app.include_router(main_router)