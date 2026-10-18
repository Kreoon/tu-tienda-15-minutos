"""Arma la carpeta del tema de una corrida tienda-express (sin red; la subida la hace el agente con Shopify CLI).

Uso:  python -I tools/armar.py corridas/<slug>
Pasos:
  1. Optimiza corridas/<slug>/creativos/**/<id>.(jpg|jpeg|png|webp) → .build-tema/<slug>/assets/hk-<id>.(jpg|png)
     (≤1600 px, JPG q82; PNG con transparencia se queda PNG). Logos: creativos/marca/logo*.png → "logo" / "logo_blanco".
     Se ignoran revision-*, collages U1..Un ya cortados y archivos que empiezan con "_".
  2. Escribe corridas/<slug>/tema/assets-map.json (id → archivo del tema) y corre gen_tema.py.
  3. Copia kit (secciones, snippets, hk.css), base (locales, index) y la salida de gen_tema a .build-tema/<slug>/.
  4. Escribe corridas/<slug>/tema/media.json: galería del producto (URLs públicas de creativos/urls.json en el orden de brief.producto.galeria).
"""
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
KIT = ROOT / "kit"
BASE = ROOT / ".tienda" / "base"  # generado por tools/preparar_base.py desde el Horizon de TU tienda
SKIP = re.compile(r"^(revision|_)|^u\d+$", re.I)


def optimize(src: Path, dst_dir: Path, img_id: str) -> str:
    im = Image.open(src)
    has_alpha = im.mode in ("RGBA", "LA") or (im.mode == "P" and "transparency" in im.info)
    im.thumbnail((1600, 1600))
    if has_alpha:
        name = f"hk-{img_id}.png"
        im.save(dst_dir / name, optimize=True)
    else:
        name = f"hk-{img_id}.jpg"
        im.convert("RGB").save(dst_dir / name, quality=82, optimize=True, progressive=True)
    return name


sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")


def main(run_dir: str):
    run = (ROOT / run_dir).resolve() if not Path(run_dir).is_absolute() else Path(run_dir)
    slug = run.name
    if not (BASE / "header-group.json").exists():
        print("Falta .tienda/base: corre primero la preparación única (skill tienda-preparar)."); sys.exit(1)
    out = ROOT / ".build-tema" / slug
    if out.exists():
        shutil.rmtree(out)
    (out / "assets").mkdir(parents=True)

    amap = {}
    cre = run / "creativos"
    cre.mkdir(parents=True, exist_ok=True)
    # Solo creativos/<id>, creativos/ugc/<id> y creativos/marca/logo*: cualquier otra subcarpeta (v1/, viejos/…) es respaldo
    # y NO entra (bug de una prueba real: v1/ugc/ugc08.jpg pisaba a ugc/ugc08.jpg por orden alfabético).
    fuentes = [p for p in cre.iterdir() if p.is_file()] + \
              [p for sub in ("ugc", "marca") if (cre / sub).is_dir() for p in (cre / sub).iterdir() if p.is_file()]
    for f in sorted(fuentes):
        if f.suffix.lower() not in (".jpg", ".jpeg", ".png", ".webp") or SKIP.search(f.stem):
            continue
        if f.parent.name == "marca":
            if not f.stem.lower().startswith("logo"):
                continue
            img_id = "logo_blanco" if "blanco" in f.stem.lower() or "white" in f.stem.lower() else "logo"
        else:
            img_id = f.stem.lower()
        amap[img_id] = optimize(f, out / "assets", img_id)
    (run / "tema").mkdir(exist_ok=True)
    (run / "tema" / "assets-map.json").write_text(json.dumps(amap, indent=1), encoding="utf-8")
    print(f"assets: {len(amap)}")

    subprocess.run([sys.executable, "-I", str(ROOT / "tools/gen_tema.py"), str(run)], check=True)

    for sub in ("sections", "snippets"):
        shutil.copytree(KIT / sub, out / sub, dirs_exist_ok=True)
    shutil.copy(KIT / "assets/hk.css", out / "assets/hk.css")
    (out / "locales").mkdir(exist_ok=True)
    shutil.copy(BASE / "en.default.json", out / "locales/en.default.json")
    (out / "templates").mkdir(exist_ok=True)
    shutil.copy(BASE / "index.json", out / "templates/index.json")
    t = run / "tema"
    for rel in ("assets/hk-tokens.css", "sections/header-group.json", "sections/footer-group.json"):
        shutil.copy(t / rel, out / rel)
    for tpl in (t / "templates").glob("product.*.json"):
        shutil.copy(tpl, out / "templates" / tpl.name)

    br = json.loads((run / "brief.json").read_text(encoding="utf-8"))
    urls = run / "creativos" / "urls.json"
    urls = json.loads(urls.read_text(encoding="utf-8")) if urls.exists() else {}
    gal = br["producto"].get("galeria", [])
    media = [{"mediaContentType": "IMAGE", "originalSource": urls[g], "alt": br["producto"]["titulo"]} for g in gal if g in urls]
    (t / "media.json").write_text(json.dumps(media, ensure_ascii=False, indent=1), encoding="utf-8")
    missing = [g for g in gal if g not in urls]
    print(f"galería: {len(media)} con URL" + (f" · sin URL: {missing}" if missing else ""))

    refs = set(re.findall(r'"(hk-[\w-]+\.(?:jpg|png))"', (out / "templates" / f"product.{br['tema']['sufijo']}.json").read_text(encoding="utf-8")))
    absent = sorted(r for r in refs if not (out / "assets" / r).exists())
    print(f"build: {out.relative_to(ROOT)} · imágenes referenciadas sin archivo (saldrán como placeholder): {absent or 'ninguna'}")


if __name__ == "__main__":
    main(sys.argv[1])
