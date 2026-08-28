"""Пакет HTTP-клиента для работы с пользователями через http-gateway."""

from clients.http.gateway.users.client import (
    UsersGatewayHTTPClient,
    build_users_gateway_http_client,
)

__all__ = ["UsersGatewayHTTPClient", "build_users_gateway_http_client"]