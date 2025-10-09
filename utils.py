import aiohttp
from bs4 import BeautifulSoup

from core.config import get_settings

settings = get_settings()


async def build_vacancy_url(q: list[str], grade: str | None, remote: bool) -> str:
    """Формирует URL для поиска вакансий"""
    url = f'{settings.habr_url}/vacancies?q={'+' .join(q)}'

    if grade:
        url += f'&qid={grade.value.split()[0]}'
    if remote:
        url += '&remote=true'

    return url


async def parse_vacancy_details(session: aiohttp.ClientSession, url: str):
    """Парсит страницу отдельной вакансии"""
    async with session.get(url) as response:
        html = await response.text()

    soup = BeautifulSoup(html, 'html.parser')

    description_tag = soup.select_one('.vacancy-description__text')
    description = description_tag.text.strip() if description_tag else ''

    stack_tags = soup.select('.inline-list a.link-comp')
    stack = [a.get_text(strip=True) for a in stack_tags]

    return {'description': description, 'stack': stack}


async def parse_habr_jobs(
    q: list, pages: int, grade: str = None, remote: bool = False
):
    """Основной парсер вакансий"""
    vacancies = []

    url = await build_vacancy_url(q, grade, remote)

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

                link = settings.habr_url + title_tag["href"]
                details = await parse_vacancy_details(session, link)

                vacancies.append({
                    'title': title_tag.text.strip(),
                    'company': company_tag.text.strip(),
                    'link': link,
                    **details
                })
    return vacancies
