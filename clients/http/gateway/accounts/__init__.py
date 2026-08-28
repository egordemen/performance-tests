"""Пакет HTTP-клиента для работы со счетами через http-gateway."""

from clients.http.gateway.accounts.client import (
    AccountsGatewayHTTPClient,
    build_accounts_gateway_http_client,
)

__all__ = ["AccountsGatewayHTTPClient", "build_accounts_gateway_http_client"]