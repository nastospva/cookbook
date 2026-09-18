from fastapi import Header, HTTPException, status
from app.config import settings
from app.core.security import validate_init_data


async def get_current_user(authorization: str = Header(...)) -> dict:
    """
    Dependency для защиты эндпоинтов.
    Ожидает заголовок: Authorization: Tg <initData>
    """
    if not authorization.startswith("Tg "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid auth header format. Expected: 'Tg <initData>'"
        )

    init_data = authorization[3:]  # отрезаем "Tg "
    user_data = validate_init_data(init_data, settings.BOT_TOKEN)
    return user_data