---
name: tienda-leer-referencia
description: "Fase 1 de tienda-express — convierte la URL de una página de referencia (la que vamos a \"copiar\") en screenshot completo, tokens de estilo, mapa de secciones en orden con su equivalente para nuestro producto, y la lista de huecos de creativos. Úsalo cuando alguien pase \"esta es la página de referencia\", \"clona esta tienda\" o al arrancar F1."
---

# Leer la página de referencia

Salida en `corridas/<slug>/referencia/`: `pagina.md`, `pagina-limpia.md`, `branding.json`, `screenshot-full.png`, `hero-desktop.jpg`, `cortes/NN.jpg`, **`mapa-secciones.md`** (el entregable).

## Pasos
1. **Scrape** con Firecrawl (`firecrawl_scrape`): `formats: ["markdown","branding","screenshot"]`, `screenshotOptions.fullPage: true`, `onlyMainContent: false`. El resultado suele pasar el límite y se guarda en un `.txt` JSON: extraer con Python (`json.load`) a los archivos de arriba y descargar la URL del screenshot con `curl`.
2. **Limpiar el texto**: quitar `![..](..)` y URLs de links con regex. Si el markdown trae bloques "blocked by an extension", ignorarlos. Leer TODO el texto antes de mapear.
3. **Cortar el screenshot** en tramos de 1600 px de alto, reducidos a la mitad (PIL), y mirarlos todos con Read. Los popups (ruleta, "rasca y gana", newsletter) suelen tapar el hero.
4. **Hero sin popup**: abrir la URL en el navegador integrado, esperar 4 s, `Escape`, screenshot. Guardar como `hero-desktop.jpg`. (Opcional: vista móvil con `resize_window preset: mobile`.)
5. **Tokens**: de `branding.json` sacar colores (primary, secondary, accent, background), fuentes de título/cuerpo y tamaños; completar con lo que se ve (radios, bordes, forma de botones, ritmo de bandas oscuras/claras).
6. **Mapa de secciones** (`mapa-secciones.md`): tabla en orden con columnas `# · Sección · Contenido en la referencia · Equivalente para nuestro producto · Hueco (creativo)`. Incluir barra de anuncio, header, marquees, buybox con todos sus elementos (galería, estrellas, packs, regalos, escasez, fecha de entrega, acordeones), y footer.
7. **Qué NO se copia**: listar cifras, reseñas, contadores, garantías y sellos de la referencia. Nunca pasan a nuestra página salvo que el equipo los demuestre para nuestro producto.

## Gotchas (Windows)
- `python -I` ignora `PYTHONIOENCODING`: usar `sys.stdout.reconfigure(encoding='utf-8')` al imprimir texto con tildes/emojis.
- La moneda y textos pueden salir en otro idioma según geolocalización del scraper; da igual, lo que importa es la estructura.

## Siguiente
La columna "Hueco" alimenta `tienda-pedido-creativos`; la columna "Equivalente" alimenta `tienda-brief-producto`.
