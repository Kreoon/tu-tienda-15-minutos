---
name: tienda-clonar-pagina
description: "Fase 4 de tienda-express — construye en Shopify la página de producto que replica la referencia, usando el kit de secciones `kit/` (hk-*), una plantilla `product.<marca>.json` generada desde el brief y un tema duplicado sin publicar; sube con Shopify CLI y asigna la plantilla al producto. Úsalo cuando el brief esté listo o pidan \"monta la página igual a la referencia\"."
---

# Clonar la página en Shopify

> **Desde 2026-10-17 (corrida de 15 min):** no se escribe un generador por jornada. El copy va en `brief.json` (`tools/brief.schema.md`) y todo se arma con `python -I tools/armar.py corridas/<slug>` (optimiza imágenes a `assets/hk-<id>`, genera plantilla, grupos de header/footer, tokens, `product-set.json` y `media.json`). Las imágenes se referencian como **assets del tema** (`*_asset`), así que ya no hace falta `fileCreate`. QA: `tools/qa.js`. Lo de abajo queda como referencia del método manual.

## Piezas
| Pieza | Dónde | Qué cambia por jornada |
|---|---|---|
| Kit de secciones `hk-*` + `hk.css` + snippets | `kit/` (reutilizable) | Nada; solo se amplía si la referencia trae una sección nueva |
| Tokens (colores, fuentes) | `corridas/<slug>/tema/assets/hk-tokens.css` | Sí, desde `referencia/branding.json` |
| Plantilla del producto | `corridas/<slug>/tema/gen_template.py` → `templates/product.<marca>.json` | Sí, todo el copy del brief |

Secciones del kit (mapa → sección): anuncio+contador `hk-announcement` · cinta `hk-marquee` · bloque de compra COD `hk-buybox` (galería, prueba social, beneficios, colores, ofertas por variante, regalo, entrega, botón, acordeones) · cifras `hk-stats` · tarjetas foto `hk-cards` (tecnologías / 5 razones, estilo `square` o `wide`) · reseñas `hk-reviews` (solo reales) · beneficios con producto `hk-benefits-center` · filas `hk-rows` · línea de tiempo `hk-timeline` · comparativa `hk-compare` · garantía `hk-guarantee` · oferta repetida `hk-offer-cta`.
Imágenes vacías muestran un placeholder rayado con la etiqueta del pedido de creativos (G1, T1, B1…), así la página se revisa antes de tener creativos.

## Regla de oro
**Misma estructura y elementos que la referencia, sin quitar nada**: cada sección, banner, cinta, popup, carrusel, contador, barra de escasez, bloque de regalos, fecha de entrega, reseñas y footer de la referencia existe en nuestra página, en el mismo orden y con espacios equivalentes. Solo cambian creativos e información del producto. Si un elemento depende de datos que no tenemos (reseñas, cifras), se monta igual con contenido demo marcado (`demo: true` en reseñas) y queda en `decisiones.md` para reemplazar antes de lanzar.

Secciones adicionales del kit: `hk-popup` (rasca y gana), `hk-videos` (carrusel UGC 9:16, video o imagen), `hk-reviews` (franja de fotos + 3 tarjetas con avatar/verificado/etiquetas, o lista), `hk-footer` (newsletter + políticas + avisos), y `hk-buybox` con `layout: compact` para la oferta repetida (barra de escasez, regalos desbloqueables por oferta, fecha de entrega automática en días hábiles, avatares en la prueba social).

## Imágenes en la plantilla (image_picker)
1. Optimizar a `.build-tema/assets/hk-<id>.jpg` (≤1600 px, q82) y subir con `shopify theme push`.
2. URL pública del asset: `https://<tienda>.myshopify.com/cdn/shop/t/<n>/assets/hk-<id>.jpg` (probar `t/1`, `t/2`… con `curl -w %{http_code}`; el tema duplicado suele ser `t/2`).
3. `fileCreate(files: [{originalSource: <url>, filename: "hk-<id>.jpg", contentType: IMAGE, alt}])` en lotes de ~20.
4. En la plantilla: `"image": "shopify://shop_images/hk-<id>.jpg"`.
Galería del producto: `productCreateMedia` con la URL de Magnific (o staged upload para archivos editados localmente).
Header/footer de Horizon: bajar `config/settings_data.json`, `sections/header-group.json` y `footer-group.json` con `shopify theme pull --only …`, poner el logo (`current.logo`), centrarlo, desactivar los anuncios y el footer de Horizon (`"disabled": true`) y subir.

## Pasos
1. `themeDuplicate` del tema publicado → "<MARCA> Landing" (UNPUBLISHED). Nunca tocar el tema MAIN.
2. Copiar `hk-tokens.css` a la jornada y ajustar colores/fuentes.
3. Copiar `gen_template.py` de una jornada anterior, reemplazar el copy por el del brief y correrlo (`python -I tema/gen_template.py`). Los `option_value` de las ofertas deben ser **idénticos** a los valores de la opción "Oferta" de las variantes.
4. Armar `.build-tema/` (en `.gitignore`): `kit/*` + `tema/assets` + `tema/templates`.
5. Subir: `CI=1 shopify theme push --store <tienda>.myshopify.com --theme <id> --path .build-tema --nodelete`. La CLI reutiliza la sesión si ya hay una; si no, abre login en el navegador.
6. `productUpdate(product: {id, templateSuffix: "<marca>"})`.
7. Preview: `https://<tienda>.myshopify.com/products/<handle>?preview_theme_id=<id>`. Tiendas de desarrollo tienen contraseña: la escribe el usuario en el navegador (no el agente).

## Revisión visual (QA)
- Contraseña de tienda de desarrollo: la escribe el usuario en el **panel del navegador de la app** (verificar que la URL ya no sea `/password` antes de seguir; la cookie es httpOnly).
- Desktop: `resize_window` 1280×1400 + `computer zoom` por regiones. Mobile: tamaño normal del panel; desplazarse con `scrollTo({top, behavior:'instant'})` (Horizon usa scroll suave y los screenshots salen corridos). Cerrar el popup y forzar `img.loading='eager'` antes de capturar.
- Comparar contra `referencia/cortes/`: anuncio ENCIMA del header (va en `header-group.json`), videos UGC bajo la galería (bloques `video` del buybox), menús en español (`menuUpdate`).
- Políticas (devoluciones, envíos, términos): `shopPolicyUpdate` requiere `write_legal_policies`, que el conector no tiene → se crean a mano en Configuración → Políticas.

## Errores conocidos
- `name` del schema de sección: **máximo 25 caracteres** (también en presets).
- En `{% render %}` no se pueden usar filtros en los argumentos: `assign` antes.
- Si una sección falla, la plantilla que la usa también falla ("no hace referencia a una sección existente"): arreglar la sección y volver a subir ambas.
- Liquid `money_without_trailing_zeros` depende de la moneda de la tienda: hasta cambiar a COP mostrará "$349,900".

## COD
El botón envía el formulario de producto con `return_to=/checkout`. Al instalar Releasit (o la app COD propia) se activa su *App embed* y toma el botón; revisar en el editor que el embed esté encendido en el tema "<MARCA> Landing".
