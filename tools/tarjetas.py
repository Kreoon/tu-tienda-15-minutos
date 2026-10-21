"""¿Qué texto acompaña a cada imagen? Lo usan tienda-creativos (al revisar) y tienda-qa (coherencia imagen ↔ tarjeta).

Uso: python -I tools/tarjetas.py corridas/<slug>
Lee brief.json y lista cada ID de imagen (g1, t1, b1, z1, ugc01…) con la ruta donde se usa y el texto de su tarjeta.
Una imagen es coherente si muestra lo que dice su tarjeta, en el nicho del producto (no el de la referencia).
"""
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[1]
ID = re.compile(r"(g\d|t\d|b\d|z\d|w1|l1|p1|ugc\d\d)")
TAG = re.compile(r"<[^>]+>")


def textos(d: dict) -> str:
    partes = [TAG.sub("", v).strip() for v in d.values()
              if isinstance(v, str) and not ID.fullmatch(v) and len(v) > 3 and not v.startswith(("#", "http"))]
    return " | ".join(p[:90] for p in partes[:3])


def recorrer(o, ruta: list, ctx: str, filas: list) -> None:
    if isinstance(o, dict):
        ctx = textos(o) or ctx
        for k, v in o.items():
            recorrer(v, ruta + [k], ctx, filas)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            recorrer(v, ruta + [str(i)], ctx, filas)
    elif isinstance(o, str) and ID.fullmatch(o):
        filas.append((o, ".".join(ruta), ctx))


def main():
    brief = ROOT / sys.argv[1] / "brief.json"
    if not brief.exists():
        sys.exit(f"Falta {brief.relative_to(ROOT)} (lo escribe tienda-copy)")
    filas: list = []
    recorrer(json.loads(brief.read_text(encoding="utf-8")), [], "", filas)
    for img_id, ruta, ctx in filas:
        print(f"{img_id:6} {ruta[:42]:42} :: {ctx[:220]}")


if __name__ == "__main__":
    main()
