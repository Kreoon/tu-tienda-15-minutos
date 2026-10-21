# Tu tienda online en 15 minutos · kit para Claude Code

Producto + página de referencia → página de producto en Shopify (tema nuevo) con imágenes nuevas, copy en español y contraentrega, en ~15 min con 6 agentes en paralelo.

- Primera vez en una tienda: skill `tienda-preparar` (crea `tienda.json`). Cada producto: skill `tienda-express`.
- Agentes: `.claude/agents/tienda-*.md`. Contrato de textos: `tools/brief.schema.md` (ejemplo en `tools/ejemplo/`).
- Scripts (siempre `python -I`): `tools/nueva.py`, `armar.py`, `gen_tema.py`, `descargar.py`, `ref_imagenes.py`, `estado.py`, `preparar_base.py`, `tarjetas.py` (imagen ↔ texto de su tarjeta); QA en el navegador: `tools/qa.js`.
- Cada corrida vive en `corridas/<slug>/` y en un tema nuevo duplicado de "Base tienda express (no tocar)". Nunca tocar el tema publicado ni el base.
- Reglas: datos solo del producto (nada de cifras/reseñas/garantías de la referencia); misma estructura que la referencia; todas las imágenes nuevas con el producto consistente; menú sin enlaces rotos; no publicar temas ni enviar pedidos sin OK del usuario.
- Español en textos y comunicación; código e identificadores en inglés.
