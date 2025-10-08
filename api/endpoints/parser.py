from typing import Optional

from fastapi import APIRouter, Query

from core.config import get_settings
from core.enums import GradeLevel


settings = get_settings()

router = APIRouter()


@router.get('/vacancies')
async def get_vacancies(
    q: list[str] = Query(..., description='Поисковый запрос (например: java, spring)'),
    grade: Optional[GradeLevel] = Query(None, description='Уровень опыта'),
    remote: Optional[bool] = Query(None, description='Только удалённая работа')
):
    """
    Эндпоинт принимает следующие Query параметры:
    - **q** — Профильный ЯП (Опционально можно добавить инструменты 'Java + spring')
    - **grade** — грейд (Enum)
    - **remote** — только удалёнка (bool)
    """
    params = []

    if q:
        params.append(f'q={'+'.join(q)}')

    if grade:
        params.append(f'qid={grade.value.split()[0]}')

    if remote:
        params.append(f'remote={remote}')

    result_url = f'{settings.habr_url}?{'&'.join(params)}'

    return {'parsed_url': result_url}
