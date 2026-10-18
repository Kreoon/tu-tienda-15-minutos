"""¿Lo que está en Shopify es lo último que se generó? Lo corre tienda-qa y el orquestador antes de dar una corrida por cerrada.

Uso: python -I tools/estado.py corridas/<slug>
Compara la fecha de la imagen más nueva de creativos/ y de brief.json contra el último armado (.build-tema/<slug>/).
Sale con código 1 y "DESACTUALIZADO" si hay que volver a armar y subir (ensamblador en modo re-subida).
"""
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[1]
run = (ROOT / sys.argv[1]).resolve()
build = ROOT / ".build-tema" / run.name
fuentes = [p for p in (run / "creativos").rglob("*") if p.suffix.lower() in (".jpg", ".jpeg", ".png", ".webp") and "v1" not in p.parts and not p.name.startswith("revision")]
fuentes.append(run / "brief.json")
nuevo = max(fuentes, key=lambda p: p.stat().st_mtime)
armado = [p for p in build.rglob("*") if p.is_file()] if build.exists() else []
if not armado:
    print("DESACTUALIZADO · nunca se armó: correr tools/armar.py y subir"); sys.exit(1)
ultimo = max(p.stat().st_mtime for p in armado)
if nuevo.stat().st_mtime > ultimo:
    print(f"DESACTUALIZADO · {nuevo.relative_to(run)} es más nuevo que el último armado: armar.py + push --only assets/* templates/* + reemplazar galería")
    sys.exit(1)
print("AL DÍA · lo subido corresponde a los últimos creativos y brief")
