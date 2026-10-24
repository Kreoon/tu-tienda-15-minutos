---
name: tienda-pedido-creativos
description: "Convierte la lista de huecos de la referencia en un pedido de creativos (imágenes y videos nuevos, fieles al producto) con formato, prompt y prioridad, y los genera con Magnific cuando hay créditos. Úsalo al terminar tienda-leer-referencia, al pasar trabajo al equipo de creativos o cuando pidan \"genera las imágenes de la tienda\"."
---

# Pedido de creativos

Salida: `corridas/<slug>/creativos/pedido-creativos.md` + archivos `creativos/<id>.jpg`.

## Pedido
Tabla `# · Sección · Pieza · Formato · Prompt base · Prioridad` (P0 = sin esto no se publica: galería del hero y recorte del producto; P1 = misma jornada; P2 = si sobra tiempo, si no placeholder).
Cabecera con reglas: piezas **nuevas**, fieles al producto real (forma, colores, contenido de la caja), sin texto incrustado, sin logos falsos, sin accesorios que no trae; personas y contextos del país de venta.

## Reglas de las imágenes (aprendidas en pruebas reales)
- **Se cambian todas**: cada ID del brief recibe imagen nueva con nuestro producto. Nada de la referencia ni genérico.
- **Consistencia**: el mismo empaque real en todas las piezas (forma, color, etiqueta legible). Empaque sin etiqueta o distinto = rehacer.
- **Galería (g1–g5)** = vistas del producto que mandó el usuario (hoja de branding → recortar cada panel: hero, frontal, lateral, posterior con información, detalle).
- **Secciones** = calco de la composición de la imagen equivalente en la referencia (`referencia/cortes/`), con producto, contexto y paleta propios. Columna `Corte ref.` en la tabla del pedido.
- Error que pasó: la primera pasada generó escenas de estilo de vida genéricas sin mirar la referencia y UGC con potes sin etiqueta → hubo que rehacer las 33.

## Generar con Magnific (MCP)
1. `account_balance` primero. Si `unlimitedAppliesHere` es false, **avisar al usuario el costo antes** de generar (`simulate_cost`). Referencia 2026-10-17: Seedream 5 Pro con referencia = 100 créditos/imagen; Nano Banana 2 Lite = 60.
2. Subir la foto oficial del producto con `creations_upload_image` (URL pública, p. ej. `og:image` de la página del fabricante) y pasarla como `references: [{type: "image"}]` en cada generación para mantener fidelidad.
3. Modelo: `seedream-5-pro` para finales con producto; `imagen-nano-banana-2-lite` para borradores. Variantes de un mismo prompt = una llamada con `count`.
4. `creations_wait` → descargar → revisar con Read (producto deformado, texto inventado, manos raras → descartar) → optimizar (≤ 400 KB, lado largo 2048 px) → `creativos/<id>.jpg`.
5. Recorte sin fondo: `images_remove_background` sobre la mejor foto de producto.

## Lo que funcionó (2026-10-17)
- **Nano Banana 2 Lite** (`imagen-nano-banana-2-lite`, 60 créditos) + foto oficial como referencia `image` = producto consistente en todas las escenas; en el prompt decir "these exact headphones from the reference" y el color deseado.
- Pedir `count: 6` con un prompt de "UGC selfie" a veces devuelve **collages** (2×2, 2×3, 1×3): no se descartan, se cortan con PIL en cuadros y salen 20+ caras para videos, franjas y avatares.
- Revisar con una hoja de contacto (PIL, miniaturas en grilla) antes de subir; recortar artefactos (bloques blancos, manos raras).
- Recorte sin fondo: `images_remove_background` (3 créditos) sobre una foto de producto con fondo liso.
- Costo total de la jornada demo: ~1.500 créditos (≈26 imágenes + recorte).

## Si no hay créditos
Opciones a ofrecer (no elegir solas): recargar/activar ilimitado en Magnific; OpenRouter (llave del proyecto, ADR-010); pasar el pedido al equipo de creativos o a Hermes (`anuncios`/estudio-casa). Mientras tanto se construye la página con placeholders de color del tamaño correcto.
