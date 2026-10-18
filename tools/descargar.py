"""Descarga y revisa los creativos de una corrida (idempotente: se puede correr las veces que haga falta).

Uso:  python -I tools/descargar.py corridas/<slug>
Lee:  creativos/urls.json  ({"g1": "https://…", "ugc01": "https://…"}). El agente de creativos lo actualiza
      DESPUÉS DE CADA creations_wait, así un corte a mitad de corrida no pierde lo ya generado.
Hace: descarga lo que falte (ugcNN → creativos/ugc/), y arma creativos/revision.jpg con cada imagen
      al lado de su imagen de la referencia (referencia/imgs/<id>.*) para comparar composición y producto.
Imprime: ids descargados, ids que faltan respecto de la lista fija y ids sin referencia.
"""
import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).parent))
from _seguro import bajar, dentro, id_valido  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")
FIJOS = ["g1", "g2", "g3", "g4", "g5", "t1", "t2", "t3", "t4", "b1", "b2", "b3", "b4", "z1", "z2", "z3", "z4", "z5", "w1", "l1"] + \
        [f"ugc{n:02d}" for n in range(1, 13)]


def destino(cre: Path, img_id: str) -> Path:
    return (cre / "ugc" / f"{img_id}.jpg") if img_id.startswith("ugc") else (cre / f"{img_id}.{'png' if img_id == 'p1' else 'jpg'}")


def main(run_dir):
    run = Path(run_dir)
    cre, ref = run / "creativos", run / "referencia" / "imgs"
    (cre / "ugc").mkdir(parents=True, exist_ok=True)
    urls = json.loads((cre / "urls.json").read_text(encoding="utf-8")) if (cre / "urls.json").exists() else {}
    nuevos = []
    for img_id, url in urls.items():
        if not id_valido(img_id):
            print(f"✗ {img_id!r}: id no válido, se ignora"); continue
        d = destino(cre, img_id)
        if not dentro(d, cre):
            print(f"✗ {img_id!r}: ruta fuera de creativos/, se ignora"); continue
        if d.exists() and d.stat().st_size > 0:
            continue
        try:
            d.write_bytes(bajar(url))
            nuevos.append(img_id)
        except Exception as e:  # URL vencida, no permitida o caída: se reporta y se sigue
            print(f"✗ {img_id}: {e}")
    tiles, s = [], 220
    for img_id in [i for i in FIJOS + ["p1"] if destino(cre, i).exists()]:
        ours = Image.open(destino(cre, img_id)).convert("RGB")
        refs = sorted(ref.glob(f"{img_id}.*")) if ref.exists() else []
        theirs = Image.open(refs[0]).convert("RGB") if refs else None
        t = Image.new("RGB", (s * 2, s + 18), "white")
        if theirs:
            theirs.thumbnail((s, s)); t.paste(theirs, (0, 18))
        ours.thumbnail((s, s)); t.paste(ours, (s, 18))
        ImageDraw.Draw(t).text((4, 2), f"{img_id}  referencia | nuestra", fill="black")
        tiles.append(t)
    if tiles:
        cols = 4
        rows = (len(tiles) + cols - 1) // cols
        sheet = Image.new("RGB", (cols * s * 2 + (cols - 1) * 8, rows * (s + 26)), (235, 235, 235))
        for i, t in enumerate(tiles):
            sheet.paste(t, ((i % cols) * (s * 2 + 8), (i // cols) * (s + 26)))
        sheet.save(cre / "revision.jpg", quality=80)
    faltan = [i for i in FIJOS if not destino(cre, i).exists()]
    sin_ref = [i for i in FIJOS if not (ref.exists() and list(ref.glob(f"{i}.*")))]
    print(f"descargados ahora: {nuevos or 'ninguno'}")
    print(f"faltan (lista fija): {faltan or 'ninguno'}")
    print(f"sin imagen de referencia: {sin_ref or 'ninguno'}")
    print(f"revisión: {cre / 'revision.jpg'}")


if __name__ == "__main__":
    main(sys.argv[1])
