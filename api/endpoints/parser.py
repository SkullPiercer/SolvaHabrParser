from typing import Optional

from fastapi import APIRouter, Query

from utils import parse_habr_jobs
from core.enums import GradeLevel

router = APIRouter()

@router.get('/parse')
async def parse_endpoint(
    q: list[str] = Query(
        ...,
        max_length=3,
        description='Поисковый запрос (например: java, spring)'
    ),
    pages: int = Query(1),
    grade: Optional[GradeLevel] = Query(None, description='Уровень опыта'),
    remote: Optional[bool] = Query(False, description='Только удалённая работа')
):
    """
    Эндпоинт принимает следующие Query параметры:
    - **q** — Профильный ЯП (Опционально можно добавить инструменты 'Java + spring')
    - **grade** — грейд (Enum)
    - **remote** — только удалёнка (bool)
    """
    data = await parse_habr_jobs(
        q=q, pages=pages, grade=grade, remote=remote
    )
    return {'count': len(data), 'vacancies': data}