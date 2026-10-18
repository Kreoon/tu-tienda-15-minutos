"""Genera todo lo del tema para una corrida de tienda-express a partir de brief.json.

Uso:  python -I tools/gen_tema.py corridas/<slug>
Lee:  corridas/<slug>/brief.json   (esquema: tools/brief.schema.md, ejemplo: tools/ejemplo/brief.json)
Crea: corridas/<slug>/tema/templates/product.<sufijo>.json
      corridas/<slug>/tema/sections/header-group.json, footer-group.json   (anuncio y footer globales)
      corridas/<slug>/tema/assets/hk-tokens.css
      corridas/<slug>/tema/product-set.json      (variables para productSet del MCP de Shopify)

Imágenes: cada valor de imagen del brief es un id ("g1", "ugc04", "logo") → asset del tema "hk-<id>.<ext>".
El archivo real lo deja `assets.py` en .build-tema/assets/. Si el id no existe, la sección muestra un placeholder.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KIT = ROOT / "kit"
BASE = ROOT / ".tienda" / "base"  # generado por tools/preparar_base.py desde el Horizon de TU tienda


def asset(img_id, assets):
    """id de imagen → nombre del asset en el tema ('' si no hay)."""
    if not img_id:
        return ""
    return assets.get(img_id, f"hk-{img_id}.jpg")


class T:
    def __init__(self, assets):
        self.order, self.sections, self.assets = [], {}, assets

    def a(self, img_id):
        return asset(img_id, self.assets)

    def sec(self, key, type_, settings, blocks=()):
        blocks = [b for b in blocks if b]
        ids = [f"{key}_{i}" for i in range(len(blocks))]
        self.sections[key] = {"type": type_, "settings": {k: v for k, v in settings.items() if v is not None},
                              "blocks": dict(zip(ids, blocks)), "block_order": ids}
        self.order.append(key)


def b(type_, **s):
    return {"type": type_, "settings": {k: v for k, v in s.items() if v is not None}}


def buybox(t, br, compact=False):
    c, p = br["compra"], br["producto"]
    blocks = [b("offer", option_value=o["valor"], title=o["titulo"], meta=o.get("detalle"), tag=o.get("etiqueta"), gift=o.get("regalo"))
              for o in p["ofertas"]]
    blocks += [b("gift", image_asset=t.a(g.get("img")), title=g["titulo"], value=g.get("valor", ""), locked=g.get("bloqueado", False),
                 unlock_offer=g.get("se_desbloquea_con")) for g in c.get("regalos", [])]
    if not compact:
        blocks += [b("avatar", image_asset=t.a(x)) for x in c.get("avatares", [])]
        blocks += [b("accordion", title=x["titulo"], body=x["html"]) for x in c.get("acordeones", [])]
        blocks += [b("video", image_asset=t.a(v["img"]), caption=v.get("texto", "")) for v in c.get("videos", [])]
    s = {
        "layout": "compact" if compact else "full",
        "features": "\n".join(c.get("beneficios", [])), "color_option": p.get("opcion_color", "Color"),
        "scarcity": c.get("escasez", 0), "scarcity_label": c.get("escasez_texto", "vendido"),
        "eta_days": c.get("entrega_dias", 3), "shipping": c.get("entrega_texto", "Pide hoy y recíbelo el"),
        "origin": c.get("origen"), "button": c.get("boton", "PEDIR AHORA · PAGO CONTRAENTREGA"),
        "gifts_label": c.get("regalos_titulo", "REGALOS DESBLOQUEADOS"), "trust": c.get("confianza"),
        "videos_heading": c.get("videos_titulo", "Lo que dicen nuestros clientes:"),
    }
    if compact:
        o = br["oferta_repetida"]
        s.update(header_image_asset=t.a(o.get("img")), heading=o["titulo"], subheading=o.get("texto"))
    else:
        s.update(proof=c.get("prueba_social"), eyebrow=c.get("eyebrow"), heading=c["titulo"], subheading=c.get("subtitulo"))
    return s, blocks


def build(br, assets):
    t = T(assets)
    if br.get("popup"):
        x = br["popup"]
        t.sec("pop", "hk-popup", {"enabled": True, "delay": x.get("segundos", 5), "logo_asset": t.a(br["marca"].get("logo")),
              "pill": x.get("etiqueta"), "heading": x["titulo"], "text": x.get("texto"), "prize": x["premio"], "image_asset": t.a(x.get("img"))})
    mq = br.get("cinta", [])
    if mq:
        t.sec("mq", "hk-marquee", {}, [b("item", text=s) for s in mq])
    s, bl = buybox(t, br)
    t.sec("main", "hk-buybox", s, bl)
    if br.get("cifras"):
        x = br["cifras"]
        t.sec("stats", "hk-stats", {"bg_asset": t.a(x.get("img")), "heading": x["titulo"], "text": x.get("texto"), "button": x.get("boton")},
              [b("stat", number=i["cifra"], label=i["texto"]) for i in x["items"]])
    for key, wide in (("tecnologias", False), ("razones", True)):
        x = br.get(key)
        if x:
            t.sec("tech" if key == "tecnologias" else "why", "hk-cards",
                  {"badge": x.get("badge"), "heading": x["titulo"], "text": x.get("texto"), "columns": "3" if wide else "4",
                   "style": "wide" if wide else "square", "alt": True, "button": x.get("boton")},
                  [b("card", image_asset=t.a(i.get("img")), ph=i.get("img", ""), kicker=(f"{x.get('prefijo', 'Razón')} {n}" if wide else None),
                     title=i["titulo"], text=i["texto"]) for n, i in enumerate(x["items"], 1)])
            if key == "tecnologias":
                _after_tech(t, br)
    return t


def _after_tech(t, br):
    x = br.get("resenas_destacadas")
    if x:
        t.sec("rev1", "hk-reviews", {"score": x.get("calificacion", ""), "heading": x["titulo"], "text": x.get("texto"), "alt": True, "layout": "grid"},
              [b("thumb", image_asset=t.a(i)) for i in x.get("fotos", [])] +
              [b("review", rating=r.get("nota", "5.0"), title=r["titulo"], text=r["texto"], author=r.get("autor"), avatar_asset=t.a(r.get("avatar")),
                 tags=" | ".join(r.get("etiquetas", [])), demo=r.get("demo", True)) for r in x.get("resenas", [])])
    x = br.get("beneficios_producto")
    if x:
        t.sec("bc", "hk-benefits-center", {"heading": x["titulo"], "text": x.get("texto"), "image_asset": t.a(x.get("img"))},
              [b("item", icon=i["icono"], title=i["texto"]) for i in x["items"]])
    x = br.get("beneficios_filas")
    if x:
        t.sec("rows", "hk-rows", {"heading": x["titulo"], "text": x.get("texto")},
              [b("row", image_asset=t.a(i.get("img")), ph=i.get("img", ""), title=i["titulo"], subtitle=i.get("subtitulo"), text=i.get("texto")) for i in x["items"]])
    if br.get("cinta"):
        t.sec("mq2", "hk-marquee", {}, [b("item", text=s) for s in br["cinta"]])
    x = br.get("linea_tiempo")
    if x:
        t.sec("tl", "hk-timeline", {"image_asset": t.a(x.get("img")), "heading": x["titulo"], "text": x.get("texto"), "button": x.get("boton")},
              [b("step", title=i["titulo"], items="\n".join(i["puntos"])) for i in x["pasos"]])


def build_rest(t, br):
    x = br.get("comparativa")
    if x:
        t.sec("cmp", "hk-compare", {"us": x["nosotros"], "them": x["otros"], "heading": x["titulo"], "points": "\n".join(x.get("puntos", [])), "button": x.get("boton")},
              [b("row", us=r[0], them=r[1]) for r in x["filas"]])
    x = br.get("garantia")
    if x:
        t.sec("gu", "hk-guarantee", {"number": x["numero"], "unit": x.get("unidad", "DÍAS"), "kicker": x.get("antetitulo"), "heading": x["titulo"],
              "text": x["texto"], "image_asset": t.a(x.get("img"))})
    x = br.get("videos")
    if x:
        t.sec("vids2", "hk-videos", {"heading": x["titulo"], "text": x.get("texto"), "button": x.get("boton")},
              [b("video", image_asset=t.a(v["img"]), caption=v.get("texto", "")) for v in x["items"]])
    if br.get("oferta_repetida"):
        s, bl = buybox(t, br, compact=True)
        t.sec("buy2", "hk-buybox", s, bl)
    x = br.get("resenas_lista")
    if x:
        t.sec("rev2", "hk-reviews", {"score": x.get("calificacion"), "heading": x["titulo"], "alt": False, "layout": "list"},
              [b("review", rating=r.get("nota", "5.0"), title=r["titulo"], text=r["texto"], tags=" | ".join(r.get("etiquetas", [])), demo=r.get("demo", True))
               for r in x["resenas"]])


def groups(br, assets):
    h = json.loads((BASE / "header-group.json").read_text(encoding="utf-8"))
    an = br.get("anuncio") or {}
    h["sections"]["hk_ann"] = {"type": "hk-announcement", "settings": {"title": an.get("titulo", ""), "text": an.get("texto", ""),
                               "countdown_hours": an.get("horas", 0)}, "disabled": not an}
    f = json.loads((BASE / "footer-group.json").read_text(encoding="utf-8"))
    fo, m = br.get("footer", {}), br["marca"]
    f["sections"]["hk_foot"] = {"type": "hk-footer", "settings": {"logo_asset": asset(m.get("logo_blanco"), assets), "menu": "footer",
                                "news_title": fo.get("newsletter_titulo", "Únete a la lista"), "news_text": fo.get("newsletter_texto", ""),
                                "legal": fo.get("legal_html", "")}}
    return h, f


def tokens_css(tk):
    names = {"primario": "primary", "secundario": "secondary", "acento": "accent", "fondo_alterno": "bg-alt", "texto": "text",
             "texto_suave": "text-soft", "borde": "border", "alerta": "alert", "oscuro_2": "dark-2", "oscuro_3": "dark-3", "comparativa": "cmp-us"}
    lines = [f"  --hk-{names[k]}: {v};" for k, v in tk.items() if k in names]
    head = tk.get("fuente_titulos", "'Clash Grotesk', 'Satoshi', system-ui, sans-serif")
    body = tk.get("fuente_texto", "'Satoshi', system-ui, -apple-system, sans-serif")
    lines += [f"  --hk-font-head: {head};", f"  --hk-font-body: {body};"]
    base = (KIT / "assets" / "hk-tokens.base.css").read_text(encoding="utf-8")
    return base + "\n.hk {\n" + "\n".join(lines) + "\n}\n"


def product_set(br):
    p = br["producto"]
    colors = p.get("colores") or []
    variants = []
    for c in (colors or [None]):
        for o in p["ofertas"]:
            ov = [{"optionName": "Oferta", "name": o["valor"]}]
            if c:
                ov.insert(0, {"optionName": p.get("opcion_color", "Color"), "name": c})
            variants.append({"optionValues": ov, "price": str(o["precio"]), "compareAtPrice": str(o.get("antes") or o["precio"]),
                             "inventoryPolicy": "CONTINUE", "inventoryItem": {"tracked": False},
                             "sku": "-".join(x for x in [p["sku"], (c or "")[:3].upper(), o.get("sku_sufijo", "")] if x)})
    opts = ([{"name": p.get("opcion_color", "Color"), "values": [{"name": c} for c in colors]}] if colors else []) + \
           [{"name": "Oferta", "values": [{"name": o["valor"]} for o in p["ofertas"]]}]
    return {"input": {"title": p["titulo"], "handle": p["handle"], "descriptionHtml": p["descripcion_html"], "vendor": p.get("marca", ""),
                      "productType": p.get("tipo", ""), "status": "ACTIVE", "tags": p.get("tags", ["tienda-express"]),
                      "templateSuffix": br["tema"]["sufijo"], "seo": p.get("seo"), "productOptions": opts, "variants": variants}}


sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")


def main(run_dir):
    run = Path(run_dir)
    br = json.loads((run / "brief.json").read_text(encoding="utf-8"))
    am = run / "tema" / "assets-map.json"
    assets = json.loads(am.read_text(encoding="utf-8")) if am.exists() else {}
    t = build(br, assets)
    build_rest(t, br)
    if br.get("orden"):  # orden de la referencia (claves: pop, mq, main, stats, tech, rev1, bc, rows, mq2, tl, why, cmp, gu, vids2, buy2, rev2)
        t.order = [k for k in br["orden"] if k in t.sections]
    out = run / "tema"
    (out / "templates").mkdir(parents=True, exist_ok=True)
    (out / "sections").mkdir(parents=True, exist_ok=True)
    (out / "assets").mkdir(parents=True, exist_ok=True)
    suf = br["tema"]["sufijo"]
    (out / "templates" / f"product.{suf}.json").write_text(json.dumps({"sections": t.sections, "order": t.order}, ensure_ascii=False, indent=1), encoding="utf-8")
    h, f = groups(br, assets)
    (out / "sections" / "header-group.json").write_text(json.dumps(h, ensure_ascii=False, indent=1), encoding="utf-8")
    (out / "sections" / "footer-group.json").write_text(json.dumps(f, ensure_ascii=False, indent=1), encoding="utf-8")
    (out / "assets" / "hk-tokens.css").write_text(tokens_css(br.get("tokens", {})), encoding="utf-8")
    (out / "product-set.json").write_text(json.dumps(product_set(br), ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"ok · {len(t.order)} secciones · product.{suf}.json · header/footer · tokens · product-set.json")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else ".")
