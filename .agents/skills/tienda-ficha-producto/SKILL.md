---
name: tienda-ficha-producto
description: "Fase 0 de tienda-express — arma la ficha de hechos del producto a partir de lo que llegue (URL de Amazon/AliExpress/proveedor, fotos, texto, PDF o audio), contrastada con la página oficial del fabricante, separando datos confirmados de contradicciones y faltantes. Úsalo cuando alguien pase \"este es el producto\" en cualquier formato."
---

# Ficha de hechos del producto

Salida: `corridas/<slug>/insumos/ficha-producto.md`. Es la **única** fuente de datos para el copy; todo lo demás (referencia, competencia) es inspiración.

## Entradas posibles (cualquiera sirve)
| Llega | Cómo se lee |
|---|---|
| URL de marketplace (Amazon, AliExpress, Mercado Libre) | Firecrawl `formats: ["markdown"]`, `onlyMainContent: true`; guardar en `insumos/<fuente>.md`. En Amazon buscar las secciones "Sobre este artículo", "Información del producto", "Descripción del producto", "Contenido de la caja", "Opiniones de clientes". |
| Fotos del producto | Leerlas con Read (visión): forma, colores, texto visible, accesorios. Guardar en `insumos/fotos/`. |
| Texto, PDF o audio del proveedor | Texto → copiar tal cual; PDF → Read con `pages`; audio → transcribir (Hermes o proveedor de IA). |
| Página oficial del fabricante | Firecrawl con `formats: ["query"]`, `queryOptions.mode: "directQuote"` pidiendo las specs exactas. |

## Pasos
1. Guardar cada fuente cruda en `insumos/` con su URL y fecha.
2. **Contrastar** con la página oficial del fabricante cuando exista (las fichas de marketplace traen errores: peso con empaque, versiones de Bluetooth, NFC inexistente, impedancias absurdas).
3. Escribir la ficha en tres bloques:
   - **Confirmados**: dato · valor · fuente(s) [A], [S]…
   - **Por confirmar**: contradicciones entre fuentes y datos dudosos (⚠️) + lo que solo el equipo sabe (❓ precio COP, costo, proveedor, garantía, stock por color, tiempos de entrega).
   - **Marca y legal**: si es producto de marca ajena, vendemos como revendedor (nada de "tienda oficial", ni su logo como marca nuestra). Categorías de riesgo (salud, belleza) → lenguaje seguro.
4. Preguntar al equipo los ❓ en un solo mensaje. Sin precio y oferta no se escribe el buybox.

## Reglas
- Ninguna cifra, reseña, garantía ni "envío gratis" sin fuente.
- La calificación pública del marketplace se puede citar con su fuente ("4,4/5 en Amazon, 490 calificaciones"), nunca como reseñas propias.
- Las imágenes que se generen después deben ser fieles al producto real (forma, colores, contenido de la caja).
