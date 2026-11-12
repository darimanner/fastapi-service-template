from fastapi import APIRouter
from sqlalchemy import text

from src.core.db.sessions import DbSession

router = APIRouter(prefix="/health", include_in_schema=False)


@router.get("/live")
async def live() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/ready")
async def ready(db: DbSession) -> dict[str, str]:
    await db.execute(text("SELECT 1"))
    return {"status": "ok"}
