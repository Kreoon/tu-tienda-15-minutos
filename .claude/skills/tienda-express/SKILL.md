---
name: tienda-express
description: "Orquesta una corrida tienda-express en ~15 minutos: producto + página de referencia → página de producto clonada en un tema nuevo de Shopify, con creativos nuevos, copy, contraentrega (Releasit) y QA, usando 6 agentes en paralelo. Úsalo cuando alguien diga \"montemos la tienda de <producto>\", \"clonemos esta página para <producto>\" o \"corrida de 15 minutos\"."
---

# Tienda express · corrida de 15 minutos

Guía para personas: [`README.md`](../../../README.md). Contrato del brief: [`tools/brief.schema.md`](../../../tools/brief.schema.md).

## 0. Antes de que corra el reloj
Si no existe `tienda.json` en la raíz → corre primero la skill **`tienda-preparar`** (una sola vez por tienda) y vuelve aquí. Si existe, léelo (tienda, tema_base_id) y verifica rápido:
- [ ] El conector de Shopify apunta a la tienda de `tienda.json` (`get-shop-info`).
- [ ] Releasit instalado y configurado en español; App embed en el tema base (`tienda-shopify-setup` §8).
- [ ] Páginas y menús en español sin enlaces rotos (§6). Inicio con `hk-redirect`.
- [ ] Tema base **"Base tienda express (no tocar)"** (`tienda.json → tema_base_id`) con el kit `hk-*` y locale en español, **neutro**: sin logo, sin anuncio, footer genérico, colores neutros. No se edita durante la corrida: se duplica. La marca (logo, colores, textos) la pone cada corrida.
- [ ] Panel del navegador con la tienda desbloqueada (contraseña escrita por el usuario) y sesión de admin; Shopify CLI con sesión (`shopify theme list --store <tienda>.myshopify.com`).
- [ ] Créditos de Magnific ≥ 2.500 (`account_balance`). Si el modo de permisos bloquea a los agentes al usar Magnific, pide al usuario que apruebe esas herramientas y relanza (no las llames tú para saltarte el bloqueo).
- [ ] Existe `.tienda/base/` (lo necesita `gen_tema.py`). Si falta (otra computadora, carpeta nueva), regénéralo: `shopify theme pull --store <tienda> --theme <tema_base_id> --path .tienda/horizon --only sections/header-group.json --only sections/footer-group.json --only locales/en.default.json --only locales/es.json` y `python -I tools/preparar_base.py`.

## 1. Arranque (minuto 0)
Pide en un solo mensaje lo que falte: URL o fotos del producto, URL de referencia, precio/oferta (si no, demo). Luego:
```
python -I tools/nueva.py <slug> "<url producto>" "<url referencia>"
```

## 2. Olas (lanzar cada ola en UN mensaje con varias llamadas `Agent`)
| Min | Ola | Agentes en paralelo | Sale |
|---|---|---|---|
| 0–4 | 1 | `tienda-referencia` · `tienda-producto` · `tienda-creativos` (arranca con la URL; espera `producto.json` si lo necesita) | mapa + estilo · ficha + producto.json · imágenes |
| 4–8 | 2 | `tienda-copy` (creativos sigue corriendo) | brief.json |
| 8–11 | 3 | `tienda-ensamblador` (cuando copy y creativos terminaron) | tema nuevo + producto + preview |
| 11–13 | 4 | `tienda-qa` | qa.js ok + capturas |
| 13–15 | — | Orquestador: resumen al equipo, link de preview, pendientes humanos | |

Prompt de cada agente: `Corrida corridas/<slug>. Lee corrida.json y sigue tu definición. Presupuesto N min.` (nada más: el agente sabe qué hacer).
Mientras corre la ola 2, entrega al usuario la ficha + los ángulos del brief (para empezar anuncios) y `creativos/revision.jpg` (para aprobar creativos).

**Compuertas (aprendidas en pruebas reales):**
- El insumo del producto puede ser fotos u hoja de branding: tienda-producto recorta cada vista a `insumos/ref_*.jpg` (frontal obligatoria). Sin vistas del producto no hay creativos fieles.
- tienda-referencia deja `referencia/imgs/<id>.jpg` (imagen objetivo por ID) **antes** que el mapa; sin eso los creativos salen genéricos.
- No lanzar tienda-ensamblador hasta que creativos termine (o corra el reloj y se ensamble con placeholders, marcando re-subida pendiente).
- **Cualquier cambio después del armado (creativos rehechos, brief editado) ⇒ relanzar `tienda-ensamblador` en modo re-subida** en el mismo turno. La corrida no se cierra mientras `python -I tools/estado.py corridas/<slug>` diga DESACTUALIZADO.
- No terminar el turno con agentes corriendo sin avisar: si el usuario pide un cambio, relanza, espera la notificación y re-sube antes de reportar "listo".

## 3. Si algo se atrasa
- Creativos tarde → ensamblar igual: las imágenes que falten salen como placeholder rayado con su ID; cuando lleguen, ensamblador en modo re-subida.
- Un agente se cortó a mitad → relánzalo con "continúa": `descargar.py` recupera lo ya generado desde `urls.json`.
- Referencia con sección SIN KIT → usar la clave más cercana y anotarlo para crear la sección después (no frenar la corrida).
- Agente sin acceso al navegador → el orquestador corre `tools/qa.js` él mismo.

## 4. Cierre
- Publicar el tema solo con OK explícito del usuario: el conector no publica temas, pero Shopify CLI sí (`CI=1 shopify theme publish --store <tienda> --theme <theme_id> --force`), o el usuario en admin → Temas → Publicar. Si la tienda tiene contraseña, la página no es pública hasta que el usuario la quite (Tienda online → Preferencias).
- Cambios después de publicar: duplica el tema publicado (`themeDuplicate`), apunta `corrida.json → theme_id` a la copia, re-subida ahí, preview, y publica la copia con OK. Nunca edites el tema en vivo.
- Pedido de prueba por Releasit y cancelación (`tienda-shopify-setup` §8), solo si el equipo lo pide.
- Reporta el tiempo por ola desde `corrida.json → hitos`.

## Reglas
- La referencia aporta estructura y estilo; los datos salen del producto. Cifras, reseñas y garantías solo con fuente o decisión del equipo (reseñas demo marcadas).
- Misma estructura que la referencia, sin quitar secciones ni elementos.
- **Imágenes: se cambian todas** y el producto se ve igual en todas (mismo empaque, etiqueta legible). Galería = vistas del producto que mandó el usuario; secciones = composición calcada de la imagen equivalente de la referencia, con nuestro producto y paleta.
- Si se rehacen creativos después de ensamblar: re-subir `assets/` (`--only assets/*`) **y reemplazar** la galería del producto (borrar media vieja, `productCreateMedia` con la nueva), no sumar.
- **Navegación sin callejones**: todo enlace del menú apunta a una página creada o se quita.
- Cada corrida en un **tema nuevo** y con su propia plantilla `product.<sufijo>`; nunca editar el tema publicado ni el base.
- Nunca toques productos o temas que no creó la corrida.
