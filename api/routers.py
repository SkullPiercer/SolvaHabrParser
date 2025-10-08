from fastapi import APIRouter

from api.endpoints import parser_router

main_router = APIRouter(prefix='/api/v1')

main_router.include_router(parser_router, prefix='/parse')