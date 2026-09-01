"""Базовый HTTP-клиент для взаимодействия с сервисами.

Модуль содержит класс :class:`HTTPClient`, который служит
обёрткой над :class:`httpx.Client` для работы с сервисами
через http-gateway.
"""

from __future__ import annotations
import httpx


class HTTPClient:
    """Базовый класс HTTP-клиента.

    Хранит долгоживущий экземпляр :class:`httpx.Client`, переданный
    извне, и предоставляет метод :meth:`post` для выполнения
    POST-запросов.

    Атрибуты:
        client: Долгоживущий экземпляр :class:`httpx.Client`.
        base_url: Базовый URL сервиса, к которому выполняются запросы.
    """

    def __init__(self, client: httpx.Client, base_url: str) -> None:
        """Инициализирует HTTP-клиент.

        Аргументы:
            client: Готовый экземпляр :class:`httpx.Client`,
                настроенный вызывающим кодом.
            base_url: Базовый URL сервиса (например, ``http://localhost:8003``).
        """
        self.client = client
        self.base_url = base_url.rstrip("/")

    def post(self, url: str, **kwargs) -> httpx.Response:
        """Выполняет POST-запрос.

        Аргументы:
            url: URL запроса.
            **kwargs: Дополнительные аргументы для :meth:`httpx.Client.post`.

        Возвращает:
            httpx.Response: Ответ сервера.
        """
        return self.client.post(url, **kwargs)
