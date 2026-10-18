---
name: tienda-brief-producto
description: "Fase 2 de tienda-express — escribe el brief y el copy de cada sección siguiendo 1:1 el mapa de la referencia, usando solo datos de la ficha del producto y las decisiones comerciales del equipo (precio, oferta, garantía, marca). Úsalo después de tienda-leer-referencia y tienda-ficha-producto, o cuando pidan \"escribe el copy de la página\"."
---

# Brief y copy por sección

Entradas: `referencia/mapa-secciones.md`, `insumos/ficha-producto.md` (solo ✅), `decisiones.md`.
Salida: `corridas/<slug>/brief.md`.

## Antes de escribir
1. Si faltan decisiones comerciales (precio, oferta/packs, colores, garantía, nombre de tienda), preguntarlas **en un solo mensaje**. En una tienda demo se aceptan valores mockup: anotarlos en `decisiones.md` con estado "Demo".
2. Si no hay nombre de marca, inventar uno corto (evento/hackathon) y crear el logo (ver "Marca rápida").

## Estructura de brief.md
- Encabezado: fuentes, voz (español de Colombia, tú, frases cortas), público, **promesa central** (1 frase), ángulo de venta.
- Una sección `## N · Nombre` por fila del mapa, **mismo número y orden**, con el texto final listo para pegar: eyebrow, H1/H2 (marcar la palabra en color con `**…**`), subtítulos, bullets, CTAs, acordeones completos, tablas de comparativa.
- Bloque de compra: prueba social con fuente, beneficios con icono, colores, precio + tachado + ahorro, ofertas, entrega, botón COD, microcopy de confianza ("No pagas nada por adelantado", garantía), acordeones (Descripción, Por qué, Especificaciones, Qué incluye, Envío y pago contraentrega, Garantía).
- Footer con aviso de marca si el producto es de otra marca ("X es marca de Y. Tienda revendedora independiente").

## Reglas de copy
- Cada cifra sale de la ficha (✅) o de `decisiones.md`. Nada de "+10.000 clientes", "4.9" o testimonios inventados: si no hay reseñas propias, mostrar la calificación pública con su fuente y un llamado a reseñar.
- Secciones de la referencia que dependen de datos que no tenemos (resultados por semana, estudios clínicos) se **reinterpretan** con hechos del producto (ej. "Un día con tus audífonos" en vez de "Semana 1 / Mes 1").
- CTA COD en mayúsculas y explícito: "PEDIR AHORA · PAGO CONTRAENTREGA".
- Apoyarse en `tienda-cro` (orden de objeciones) y `tienda-voz` (que no suene a IA).

## Marca rápida (si hace falta)
Logo wordmark + isotipo simple con PIL (Segoe UI Bold en Windows), en color primario y en blanco, PNG recortado a 1180 px de ancho → `creativos/marca/logo-<nombre>.png` y `-blanco.png`. Colores = tokens de la referencia.
