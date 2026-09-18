import hmac
import hashlib
from urllib.parse import parse_qsl
from typing import Optional
from fastapi import HTTPException, status


def validate_init_data(init_data: str, bot_token: str) -> dict:
    """
    Проверяет подпись initData от Telegram.
    Возвращает распарсенные данные при успехе, иначе бросает HTTPException.
    """
    if not init_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="initData is empty"
        )

    # Парсим query string
    try:
        parsed = dict(parse_qsl(init_data, strict_parsing=True))
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid initData format"
        )

    # Извлекаем hash
    received_hash = parsed.pop("hash", None)
    if not received_hash:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No hash in initData"
        )

    # Формируем data_check_string: сортируем ключи, соединяем \n
    data_check_string = "\n".join(
        f"{k}={v}" for k, v in sorted(parsed.items())
    )

    # Секретный ключ = HMAC-SHA256("WebAppData", BOT_TOKEN)
    # ВАЖНО: ключ — WebAppData, данные — токен бота (не наоборот!)
    secret_key = hmac.new(
        b"WebAppData",
        bot_token.encode(),
        hashlib.sha256
    ).digest()

    # Вычисляем подпись
    calculated_hash = hmac.new(
        secret_key,
        data_check_string.encode(),
        hashlib.sha256
    ).hexdigest()

    # Сравниваем (constant-time comparison для защиты от timing attacks)
    if not hmac.compare_digest(calculated_hash, received_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid signature"
        )

    return parsed