"""Crea la carpeta de una corrida tienda-express.

Uso: python -I tools/nueva.py <slug> "<url producto o 'fotos'>" "<url referencia>"
Crea corridas/<slug>/{insumos,referencia,creativos/marca,creativos/ugc,tema} + corrida.json con hora de inicio.
"""
import json
import sys
from datetime import datetime
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[1]

slug, producto, referencia = sys.argv[1], sys.argv[2], sys.argv[3]
run = ROOT / "corridas" / slug
for d in ("insumos", "referencia", "creativos/marca", "creativos/ugc", "tema"):
    (run / d).mkdir(parents=True, exist_ok=True)
cfg_path = ROOT / "tienda.json"
if not cfg_path.exists():
    sys.exit("Falta tienda.json: corre primero la preparación única (skill tienda-preparar).")
cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
meta = {"slug": slug, "producto": producto, "referencia": referencia, "inicio": datetime.now().isoformat(timespec="seconds"),
        "tienda": cfg["tienda"], "tema_base": cfg["tema_base_nombre"], "tema_base_id": cfg["tema_base_id"], "hitos": {}}
(run / "corrida.json").write_text(json.dumps(meta, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"ok · {run.relative_to(ROOT)}")
