"""Prepara la base del tema a partir del Horizon de TU tienda (una sola vez, lo usa la skill tienda-preparar).

No redistribuimos archivos de Shopify: se bajan de tu propia tienda y se ajustan aquí.

Uso:
  1. shopify theme pull --store <tienda>.myshopify.com --theme <id del tema base> --path .tienda/horizon \
       --only sections/header-group.json --only sections/footer-group.json --only locales/en.default.json --only locales/es.json
  2. python -I tools/preparar_base.py
Crea .tienda/base/:
  header-group.json  → con la sección hk_ann (barra de anuncio) arriba del header, apagada hasta que una corrida la llene
  footer-group.json  → secciones del footer de Horizon apagadas + footer hk_foot neutro
  en.default.json    → textos del tema en español (es.json fusionado sobre el idioma por defecto)
  index.json         → inicio que lleva al producto (hk-redirect)
"""
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[1]
SRC, OUT = ROOT / ".tienda" / "horizon", ROOT / ".tienda" / "base"


def load_jsonc(p: Path) -> dict:
    t = p.read_text(encoding="utf-8-sig")
    t = re.sub(r"^\s*/\*.*?\*/", "", t, count=1, flags=re.S)            # comentario de cabecera de Shopify
    t = "\n".join(l for l in t.splitlines() if not l.strip().startswith("//"))  # comentarios de línea
    t = re.sub(r",(\s*[}\]])", r"\1", t)                                  # comas colgantes
    return json.loads(t)


def merge(a: dict, b: dict) -> dict:
    for k, v in b.items():
        if isinstance(v, dict) and isinstance(a.get(k), dict):
            merge(a[k], v)
        else:
            a[k] = v
    return a


def save(name: str, data: dict) -> None:
    (OUT / name).write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")


def main():
    need = ["sections/header-group.json", "sections/footer-group.json", "locales/en.default.json", "locales/es.json"]
    missing = [n for n in need if not (SRC / n).exists()]
    if missing:
        sys.exit(f"Faltan archivos en .tienda/horizon: {missing} (haz el theme pull del paso 1)")
    OUT.mkdir(parents=True, exist_ok=True)

    h = load_jsonc(SRC / "sections/header-group.json")
    h["sections"]["hk_ann"] = {"type": "hk-announcement", "settings": {"title": "", "text": "", "countdown_hours": 0}, "disabled": True}
    for k, v in h["sections"].items():  # el anuncio propio de Horizon se apaga: usamos hk_ann
        if v.get("type") == "header-announcements":
            v["disabled"] = True
    h["order"] = ["hk_ann"] + [k for k in h["order"] if k != "hk_ann"]
    save("header-group.json", h)

    f = load_jsonc(SRC / "sections/footer-group.json")
    for v in f["sections"].values():
        v["disabled"] = True
    f["sections"]["hk_foot"] = {"type": "hk-footer", "settings": {"menu": "footer", "news_title": "Únete a nuestra lista",
                                                                  "news_text": "Recibe novedades y ofertas exclusivas.", "legal": ""}}
    f["order"] = [k for k in f["order"] if k != "hk_foot"] + ["hk_foot"]
    save("footer-group.json", f)

    save("en.default.json", merge(load_jsonc(SRC / "locales/en.default.json"), load_jsonc(SRC / "locales/es.json")))
    save("index.json", {"sections": {"redir": {"type": "hk-redirect", "settings": {"text": "Ir a la tienda"}}}, "order": ["redir"]})
    print(f"ok · base lista en {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
