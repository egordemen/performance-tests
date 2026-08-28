"""Базовый HTTP-клиент для взаимодействия с сервисами.

Модуль содержит абстрактный класс :class:`HTTPClient`, который служит
фундаментом для всех специализированных HTTP-клиентов, работающих
с сервисами через http-gateway.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
import httpx


class HTTPClient(ABC):
    """Абстрактный базовый класс HTTP-клиента.

    Инкапсулирует общую логику работы с HTTP-запросами: хранение базового
    URL сервиса, управление таймаутом и создание синхронного клиента
    :class:`httpx.Client`.

    Атрибуты:
        base_url (str): Базовый URL сервиса, к которому выполняются запросы.
        timeout (float): Таймаут запроса в секундах.
    """

    def __init__(self, base_url: str, timeout: float = 30.0) -> None:
        """Инициализирует HTTP-клиент.

        Аргументы:
            base_url: Базовый URL сервиса (например, ``http://localhost:8003``).
            timeout: Таймаут запроса в секундах. По умолчанию ``30.0``.
        """
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def _client(self) -> httpx.Client:
        """Создаёт и возвращает синхронный HTTP-клиент.

        Возвращает:
            httpx.Client: Настроенный экземпляр клиента с заданным таймаутом.
        """
        return httpx.Client(timeout=self.timeout)

    def _url(self, path: str) -> str:
        """Формирует полный URL на основе базового URL и пути.

        Аргументы:
            path: Путь к эндпоинту (например, ``/api/v1/cards/issue-virtual-card``).

        Возвращает:
            str: Полный URL запроса.
        """
        return f"{self.base_url}{path}"

    @abstractmethod
    def close(self) -> None:
        """Закрывает HTTP-клиент и освобождает ресурсы.

        Должен быть реализован в подклассах.
        """
        raise NotImplementedError