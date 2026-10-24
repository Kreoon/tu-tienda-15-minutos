---
name: tienda-preparar
description: "Preparación única (≈10 min, una sola vez por tienda) para poder correr tienda-express: conecta la tienda, la habilita para vender en el país, crea páginas y menús en español, arma el tema base neutro desde el Horizon de la tienda y deja Releasit (contraentrega) listo. Úsalo cuando alguien diga \"prepara mi tienda\", la primera vez que se usa el paquete, o si falta tienda.json."
---

# Preparar la tienda (una sola vez)

Resultado: `tienda.json` en la raíz + tema **"Base tienda express (no tocar)"** en la tienda. Después de esto, cada corrida (`/tienda-express`) tarda ~15 min.
Pide al usuario solo lo que falte, en UN mensaje: dominio `xxxx.myshopify.com`, país de venta (por defecto Colombia/COP), dirección de la bodega (ciudad), y si ya instaló Releasit.

## 0. Requisitos (verificar, no asumir)
- Conector **Shopify** de Codex conectado a ESA tienda: `get-shop-info` y confirmar el dominio con el usuario.
- **Shopify CLI** con sesión: `shopify version` y `shopify theme list --store <tienda>.myshopify.com` (si pide login, el usuario lo aprueba en el navegador).
- Python 3 + Pillow: `python -I -c "import PIL"` (si falta: `pip install pillow`).
- Conectores de **Firecrawl** y **Magnific** disponibles (`ToolSearch "firecrawl"`, `ToolSearch "magnific images_generate"` o `account_balance`).
- El tema publicado de la tienda es **Horizon** (el kit está probado ahí). Si no, avisa: hay que instalar Horizon gratis desde la Theme Store (sin publicarlo es suficiente).

## 1. Vender en el país (Admin GraphQL vía conector)
- `deliveryProfileUpdate` del perfil por defecto: zona del país (`code: CO`, `includeAllProvinces: true`) con tarifa `0` en la moneda local ("Envío gratis · Pago contraentrega") o la tarifa que diga el usuario.
- `marketCreate`: mercado del país (`regionsCondition.regions: [{countryCode: CO}]`, `status: ACTIVE`) si no existe.
- `locationEdit`: bodega con la dirección del usuario.
- **A mano en el admin (díselo al usuario):** moneda de la tienda (COP) e idioma principal (español) en Configuración.

## 2. Páginas y menús en español (sin enlaces rotos)
- `pageCreate` (publicadas) si no existen: `preguntas-frecuentes`, `rastrear-pedido`, `envios-y-entregas`, `politica-de-devoluciones`, `terminos-y-condiciones`. Textos **genéricos** (sin marca ni producto): pago contraentrega, 2–5 días hábiles, devolución hasta 7 días (dañado/defecto: reembolso o cambio; si no le gustó: devuelve y paga el envío), términos con enlaces a envíos y devoluciones.
- `pageUpdate`: `contact` → "Contacto"; `data-sharing-opt-out` → "Tus opciones de privacidad".
- `menuUpdate`: `main-menu` = Preguntas frecuentes · Rastrear mi pedido · Contacto; `footer` = esas + Envíos y entregas · Política de devoluciones · Términos y condiciones · Tus opciones de privacidad (`type: PAGE` + `resourceId`). Cada corrida agrega su producto arriba.

## 3. Tema base neutro
1. `themeDuplicate` del tema Horizon → nombre **"Base tienda express (no tocar)"** → guarda su id.
2. `shopify theme pull --store <tienda> --theme <id base> --path .tienda/horizon --only sections/header-group.json --only sections/footer-group.json --only locales/en.default.json --only locales/es.json`
3. `python -I tools/preparar_base.py` → `.tienda/base/`.
4. Arma `.build-base/` con `kit/sections`, `kit/snippets`, `kit/assets/hk.css`, `kit/assets/hk-tokens.neutro.css` como `assets/hk-tokens.css`, `.tienda/base/header-group.json` y `footer-group.json` en `sections/`, `en.default.json` en `locales/`, `index.json` en `templates/`. Sube: `CI=1 shopify theme push --store <tienda> --theme <id base> --path .build-base --nodelete` y borra `.build-base/`.
5. Verifica el preview de la base (`https://<tienda>/pages/preguntas-frecuentes?preview_theme_id=<id>`): header con el nombre de la tienda, footer neutro, sin errores.

## 4. Contraentrega con Releasit
- El usuario instala **Releasit COD Form** desde la Shopify App Store (acepta permisos él mismo).
- App embed en la base: baja `config/settings_data.json` del tema publicado y del base; copia a `current.blocks` del base el bloque cuyo `type` empieza por `shopify://apps/releasit-cod-form/blocks/app-embed/` (con `disabled: false`) y súbelo.
- Configuración del formulario (con el usuario en el admin, o tú en el panel del navegador si te da sesión): ver `tienda-shopify-setup` §8 (plantilla, textos en español, código postal opcional, país). Los colores se ajustan por corrida si hace falta.
- Respaldo: método manual "Contra reembolso" en Configuración → Pagos.

## 5. tienda.json
```json
{"tienda": "<tienda>.myshopify.com", "pais": "CO", "moneda": "COP",
 "tema_base_id": 0, "tema_base_nombre": "Base tienda express (no tocar)",
 "releasit": true, "preparada": "<fecha ISO>"}
```
Cierra con una lista de lo que quedó hecho y lo que el usuario debe hacer a mano (moneda, idioma, instalar Releasit, contraseña de la tienda si es de desarrollo).
