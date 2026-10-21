"""Copia el kit de Claude Code a su versión para Codex (lo corre quien mantiene el repo después de editar agentes o skills).

Uso: python -I tools/sync_codex.py
- .claude/agents/<nombre>.md  → .codex/agents/<nombre>.toml (name, description, developer_instructions)
- .claude/skills/<nombre>/     → .agents/skills/<nombre>/ (mismo contenido; "de Claude" → "de Codex")
"""
import json
import re
import shutil
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[1]
FRONT = re.compile(r"\A---\n(.*?)\n---\n(.*)\Z", re.S)


def campo(front: str, clave: str) -> str:
    m = re.search(rf"^{clave}:\s*(.*)$", front, re.M)
    if not m:
        return ""
    v = m.group(1).strip()
    return json.loads(v) if v.startswith('"') else v


def codex(texto: str) -> str:
    return texto.replace("de Claude", "de Codex")


def agentes() -> int:
    n = 0
    for md in sorted((ROOT / ".claude/agents").glob("tienda-*.md")):
        m = FRONT.match(md.read_text(encoding="utf-8").replace("\r\n", "\n"))
        if not m:
            sys.exit(f"Sin frontmatter: {md}")
        front, cuerpo = m.groups()
        cuerpo = codex(cuerpo.strip()).replace("\\", "\\\\").replace('"""', '\\"\\"\\"')
        toml = (f"name = {json.dumps(campo(front, 'name'), ensure_ascii=False)}\n"
                f"description = {json.dumps(codex(campo(front, 'description')), ensure_ascii=False)}\n"
                f'developer_instructions = """\n{cuerpo}"""\n')
        (ROOT / ".codex/agents" / f"{md.stem}.toml").write_text(toml, encoding="utf-8")
        n += 1
    return n


def skills() -> int:
    n = 0
    for src in sorted((ROOT / ".claude/skills").glob("tienda-*")):
        dst = ROOT / ".agents/skills" / src.name
        if dst.exists():
            shutil.rmtree(dst)
        for f in src.rglob("*"):
            if f.is_file():
                out = dst / f.relative_to(src)
                out.parent.mkdir(parents=True, exist_ok=True)
                if f.suffix == ".md":
                    out.write_text(codex(f.read_text(encoding="utf-8")), encoding="utf-8")
                else:
                    shutil.copy2(f, out)
        n += 1
    return n


if __name__ == "__main__":
    (ROOT / ".codex/agents").mkdir(parents=True, exist_ok=True)
    print(f"ok · {agentes()} agentes → .codex/agents · {skills()} skills → .agents/skills")
