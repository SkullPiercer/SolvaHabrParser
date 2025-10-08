import scrapy


class HabrSpider(scrapy.Spider):
    name = 'habr'
    allowed_domains = ['career.habr.com']
    def __init__(self, q="python", experience=None, remote=False, **kwargs):
        super().__init__(**kwargs)

        base_url = 'https://career.habr.com/vacancies?type=all'
        params = [f'q={q}']

        if experience:
            params.append(f'experience={experience}')
        if remote:
            params.append('remote=true')

        self.start_urls = [f'{base_url}&{'&'.join(params)}']

    def parse(self, response):
        vacancies = response.css('div.vacancy-card')

        for v in vacancies:
            yield {
                'title': v.css('div.vacancy-card__title a::text').get(default='').strip(),
                'link': response.urljoin(v.css('div.vacancy-card__title a::attr(href)').get()),
                'company': v.css('div.vacancy-card__company-title a::text').get(default='').strip(),
                'city': v.css('span.vacancy-card__meta-item::text').get(default='').strip(),
                'salary': v.css('div.vacancy-card__salary::text').get(default='').strip(),
                'date': v.css('time::attr(datetime)').get(default=''),
            }

        next_page = response.css('a.button_compact::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
