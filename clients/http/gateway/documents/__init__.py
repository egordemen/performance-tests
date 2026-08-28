"""Пакет HTTP-клиента для работы с документами через http-gateway."""

from clients.http.gateway.documents.client import (
    DocumentsGatewayHTTPClient,
    build_documents_gateway_http_client,
)

__all__ = ["DocumentsGatewayHTTPClient", "build_documents_gateway_http_client"]