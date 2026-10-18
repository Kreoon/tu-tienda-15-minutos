"""Utilidades de seguridad para los scripts de tools/tienda (descargas de URLs y rutas desde JSON).

- `bajar(url)`: solo http/https, host público (rechaza loopback, privadas, link-local, reservadas), sin redirecciones
  hacia hosts no permitidos, tope de 20 MB. Lanza ValueError si algo no cumple.
- `id_valido(img_id)`: ids de imagen = [a-z0-9_]{1,16}; evita escribir fuera de la carpeta de la corrida.
- `dentro(ruta, base)`: confirma que la ruta resuelta queda dentro de base.
"""
import ipaddress
import re
import socket
import urllib.request
from pathlib import Path
from urllib.parse import urlparse

from PIL import Image

MAX_BYTES = 20 * 1024 * 1024
Image.MAX_IMAGE_PIXELS = 60_000_000  # ~ 7.700 × 7.700: tope para no agotar memoria al decodificar
_ID = re.compile(r"[a-z0-9_]{1,16}")


def id_valido(img_id: str) -> bool:
    return bool(_ID.fullmatch(img_id or ""))


def dentro(ruta: Path, base: Path) -> bool:
    return ruta.resolve().is_relative_to(base.resolve())


def _host_publico(host: str) -> bool:
    try:
        infos = socket.getaddrinfo(host, None)
    except socket.gaierror:
        return False
    for info in infos:
        ip = ipaddress.ip_address(info[4][0])
        if ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved or ip.is_multicast or ip.is_unspecified:
            return False
    return True


def _validar(url: str) -> None:
    p = urlparse(url)
    if p.scheme not in ("http", "https") or not p.hostname:
        raise ValueError(f"URL no permitida: {url[:80]}")
    if not _host_publico(p.hostname):
        raise ValueError(f"host no público: {p.hostname}")


class _SinRedirecciónInsegura(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        _validar(newurl)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


_opener = urllib.request.build_opener(_SinRedirecciónInsegura)


def bajar(url: str, timeout: int = 20) -> bytes:
    _validar(url)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with _opener.open(req, timeout=timeout) as r:
        data = r.read(MAX_BYTES + 1)
    if len(data) > MAX_BYTES:
        raise ValueError("archivo de más de 20 MB")
    return data
