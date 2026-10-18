# Tu tienda online en 15 minutos

Le das a Claude **tu producto** (un link o fotos) y **una página que te guste** (la de cualquier tienda), y en unos 15 minutos tienes en tu Shopify una página de producto con la misma estructura y estilo de esa referencia, con **imágenes nuevas de tu producto**, textos de venta en español y **pago contraentrega**.

Funciona con 6 agentes de Claude Code que trabajan al mismo tiempo: uno lee la página de referencia, otro investiga tu producto, otro crea las imágenes, otro escribe los textos, otro arma la tienda y otro la revisa.

---

## Qué necesitas

| Necesitas | Para qué | Costo |
|---|---|---|
| **Claude Code** (app de escritorio o terminal) | Corre los agentes | Plan de Claude |
| **Una tienda Shopify** con el tema **Horizon** instalado (no hace falta publicarlo) | Donde queda tu página | Plan de Shopify (las tiendas de desarrollo sirven para probar) |
| **Shopify CLI** (`npm install -g @shopify/cli`) | Subir el tema | Gratis |
| **Python 3** con Pillow (`pip install pillow`) | Armar el tema e imágenes | Gratis |
| **Conectores en Claude:** Shopify, Firecrawl, Magnific | Tienda · leer páginas · crear imágenes | Magnific: ≈ 2.500 créditos por tienda |
| **Releasit COD Form** (Shopify App Store) | Formulario de pago contraentrega | Instalación gratis |

> Los conectores se agregan en Claude → Configuración → Conectores. Al usar Shopify, elige tu tienda cuando te lo pida.

## Paso 1 · Descarga el kit (una vez)

```bash
git clone https://github.com/Kreoon/tu-tienda-15-minutos.git
```

Abre esa carpeta en Claude Code y empieza una **conversación nueva** ahí.

## Paso 2 · Prepara tu tienda (una vez, ≈ 10 min)

Pega esto en la conversación:

```
/tienda-preparar
Mi tienda es <tu-tienda>.myshopify.com. Vendo en Colombia en pesos (COP).
Mi bodega está en <ciudad>. Ya instalé Releasit: <sí/no>.
Prepárala para hacer tiendas en 15 minutos.
```

Claude conecta tu tienda, habilita envíos y mercado del país, crea páginas y menús en español (preguntas frecuentes, envíos, devoluciones, términos, rastreo), arma un **tema base neutro** a partir de tu Horizon y deja lista la contraentrega. Al final te dice qué hacer a mano (moneda e idioma en Configuración, instalar Releasit si falta).

## Paso 3 · Tu tienda en 15 minutos (cada producto)

Antes de pegar, en el **panel del navegador** de Claude abre tu tienda (si tiene contraseña, escríbela tú) y deja abierta otra pestaña con tu admin de Shopify.

Pega esto con tus datos:

```
/tienda-express
Corrida cronometrada de 15 minutos. Sigue la skill tienda-express al pie de la letra y llama a los agentes tienda-* por olas, en paralelo.

DATOS
- Producto: <link del producto | "fotos adjuntas">
- Página de referencia (la que quiero copiar): <link>
- Nombre corto (slug): <nombre-sin-espacios>
- Marca de la tienda: <la del producto | otra | "nombre de la tienda">
- Oferta: <"demo" | 1 unidad $____ · Pack x2 $____ + regalo ____>
- Garantía: <"demo 7 días" | la real>

REGLAS
- Misma estructura y elementos que la referencia, sin quitar secciones. Datos solo de mi producto: nada de cifras, reseñas ni garantías de la referencia (reseñas de ejemplo marcadas "demo").
- Cambia TODAS las imágenes; mi producto se ve igual en todas, con la etiqueta legible. Muéstrame creativos/revision.jpg antes de armar.
- Si algo cambia después del armado, vuelve a subir (modo re-subida). No digas "listo" mientras tools/estado.py diga DESACTUALIZADO.
- No toques el tema publicado; no publiques el tema ni envíes pedidos sin mi OK.
- Autorizo: crear el producto, publicarlo en la tienda online, cargar/reemplazar su galería, duplicar el tema base y subir el tema nuevo.
- Avísame en una línea al empezar cada ola y dame al final el link de vista previa, el tiempo por ola y lo que falte.
```

### Qué pasa en esos 15 minutos

| Minuto | Qué hace Claude | Qué recibes |
|---|---|---|
| 0–4 | Lee la referencia, investiga tu producto y empieza a crear las imágenes (en paralelo) | Aviso de arranque |
| 4–8 | Escribe todos los textos de la página | Ficha del producto y ángulos para tus anuncios · hoja de revisión de imágenes |
| 8–11 | Crea el producto, un tema nuevo (copia del base) y sube todo | Link de vista previa |
| 11–13 | Revisa enlaces, imágenes, botón de contraentrega y versión celular | OK o lista de arreglos |
| 13–15 | Cierre | Tiempos y pendientes (publicar, reseñas reales) |

Cuando te guste, publícalo tú: Tienda online → Temas → **Publicar** en el tema de esa corrida.

---

## Si algo sale mal

| Ves esto | Pídele a Claude |
|---|---|
| Las imágenes no cambiaron en la página | `corre tools/estado.py y si dice DESACTUALIZADO relanza tienda-ensamblador en modo re-subida` |
| Imágenes genéricas o sin la etiqueta de tu producto | `rehaz con tienda-creativos los IDs <lista> calcando referencia/imgs/<id>.jpg y luego re-subida` |
| Claude se detiene pidiendo permiso | Apruébalo. Para la próxima, permite de antemano los cambios en Shopify con `/permissions` |
| Pantalla de contraseña en la vista previa | Escribe la contraseña de tu tienda en el panel del navegador de Claude |
| Un agente se cortó | `relanza <agente> con "continúa"` (lo ya generado no se pierde) |
| "Falta tienda.json" | Haz el Paso 2 |

## Buenas prácticas y límites

- **La referencia es inspiración de estructura y estilo**, no contenido: Claude no copia textos, cifras, reseñas, fotos ni marcas de esa página.
- **Tus datos, tu responsabilidad:** revisa precios, garantías y afirmaciones antes de publicar. Las reseñas "demo" se cambian por reseñas reales.
- Si vendes un producto de otra marca, eres revendedor: no te presentes como tienda oficial.
- Cada corrida crea su propio tema y producto; nada sobrescribe tu tienda publicada.

## Qué trae el kit

```
.claude/agents/   6 agentes: referencia · producto · creativos · copy · ensamblador · qa
.claude/skills/   tienda-preparar · tienda-express (orquesta) · y las guías de cada paso
kit/              secciones de Shopify (Liquid) de la página de venta
tools/            scripts: nueva, armar, gen_tema, descargar, ref_imagenes, estado, qa.js
tools/ejemplo/    un brief.json completo de ejemplo
corridas/         aquí queda cada tienda que hagas (no se sube a git)
```

Licencia MIT. Hecho con Claude Code.
