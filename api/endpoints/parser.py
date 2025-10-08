from fastapi import APIRouter, Query

from utils import parse_habr_jobs

router = APIRouter()

@router.get('/parse')
async def parse_endpoint(
    q: list[str] = Query(..., max_length=3),
    pages: int = Query(1)
):
    data = await parse_habr_jobs(q=q, pages=pages)
    return {'count': len(data), 'vacancies': data}