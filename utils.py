import aiohttp
from bs4 import BeautifulSoup

from core.config import get_settings

settings = get_settings()

async def parse_habr_jobs(q: list, pages: int):
    vacancies = []
    url = f'{settings.habr_url}/vacancies?q={'+'.join(q)}'
    print(url)

    async with aiohttp.ClientSession() as session:
        for page in range(1, pages + 1):
            async with session.get(url.format(page)) as response:
                html = await response.text()

            soup = BeautifulSoup(html, 'html.parser')

            for job_div in soup.select('.vacancy-card__inner'):
                title_tag = job_div.select_one('.vacancy-card__title-link')
                company_tag = job_div.select_one('.vacancy-card__company-title')

                if not title_tag or not company_tag:
                    continue

                vacancies.append({
                    'title': title_tag.text.strip(),
                    'company': company_tag.text.strip(),
                    'link': settings.habr_url + title_tag['href']
                })
    return vacancies
