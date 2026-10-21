# Tu tienda online en 15 minutos

**Le das a Claude tu producto y una página que te guste. En unos 15 minutos tienes en tu Shopify una página de venta lista para anuncios:** misma estructura y estilo de esa referencia, imágenes nuevas de tu producto, textos de venta en español y pago contraentrega.

Gratis y de código abierto. Un solo prompt lo instala todo: lo copias, lo pegas y respondes unas preguntas.

---

## Qué obtienes

- **Página de producto completa en Shopify:** las mismas secciones de la página que elegiste (galería, beneficios, comparativa, reseñas, preguntas frecuentes, oferta…), en un tema nuevo que no toca tu tienda publicada.
- **Más de 30 imágenes nuevas de tu producto** creadas con IA: tu empaque igual en todas, con la etiqueta legible, en escenas del nicho de tu producto.
- **Textos de venta en español** escritos a partir de los datos reales de tu producto, sin copiar cifras, reseñas ni garantías ajenas.
- **Pago contraentrega** con Releasit, envío configurado y páginas legales en español (envíos, devoluciones, términos, rastreo).
- **Ficha del producto y ángulos de venta** para empezar tus anuncios mientras la página se arma.

## Empieza aquí · 1 prompt

1. Abre **Claude Code** (app de escritorio o terminal) y empieza una conversación nueva.
2. Copia y pega este prompt:

```
Quiero montar la página de venta de mi producto en Shopify con el kit "Tu tienda online en 15 minutos":
https://github.com/Kreoon/tu-tienda-15-minutos

Hazlo todo tú, paso a paso, y pregúntame solo lo necesario. Háblame en español y en palabras simples.

1. INSTALA EL KIT
   - Si la carpeta actual no es el kit, clónalo en una carpeta "tu-tienda-15-minutos" (dentro de Documentos si estás en mi carpeta de inicio) y trabaja desde ahí. Si ya existe, actualízalo con git pull.
   - Si puedes cambiar tu carpeta de trabajo a esa carpeta, hazlo. Si no, sigue igual: lee las skills y los agentes desde la carpeta clonada (.claude/skills/*/SKILL.md y .claude/agents/*.md) y síguelos al pie de la letra; cada agente tienda-* lo corres como subagente con el contenido de su archivo como instrucciones.

2. REVISA MI COMPUTADOR (pídeme permiso antes de instalar algo)
   - git, Node.js, Shopify CLI (npm install -g @shopify/cli) y Python 3 con Pillow (pip install pillow).
   - Conectores de Claude: Shopify, Firecrawl y Magnific. Si falta alguno, dime exactamente dónde conectarlo (Configuración → Conectores) y espera a que te avise.

3. PREGÚNTAME EN UN SOLO MENSAJE
   - El dominio de mi tienda (xxxx.myshopify.com).
   - País y moneda (si no digo nada: Colombia, COP) y la ciudad de mi bodega.
   - Si ya instalé la app Releasit COD Form (contraentrega).
   - Mi producto: link o fotos.
   - La página de referencia que quiero copiar (estructura y estilo).
   - Marca de la tienda, oferta (precio de 1 unidad, Pack x2 + regalo, o "demo") y garantía (la real o "demo").

4. PREPARA MI TIENDA (solo la primera vez)
   - Si no existe tienda.json, corre la skill tienda-preparar con mis datos. Si mi tienda es de desarrollo, avísame que nunca podrá vender.
   - Dime en una lista corta lo que debo hacer yo a mano en el admin.

5. MONTA LA PÁGINA
   - Corre la skill tienda-express con mis datos, por olas y con los agentes en paralelo.
   - Misma estructura y elementos que la referencia, sin quitar secciones, pero los datos salen solo de mi producto: nada de cifras, reseñas ni garantías de la referencia (reseñas de ejemplo marcadas "demo").
   - Cambia TODAS las imágenes: mi producto igual en todas, con la etiqueta legible y a escala real, y cada imagen debe mostrar lo que dice su tarjeta en el nicho de mi producto. Muéstrame creativos/revision.jpg antes de armar.
   - Si algo cambia después del armado, vuelve a subir. No digas "listo" mientras tools/estado.py diga DESACTUALIZADO.
   - Autorizo: crear el producto, publicarlo en la tienda online, cargar o reemplazar su galería, duplicar el tema base y subir el tema nuevo.
   - No toques el tema publicado. No publiques el tema ni envíes pedidos sin mi OK.
   - Avísame en una línea al empezar cada ola. Al final dame el link de vista previa, el tiempo por ola y lo que falte.
```

3. Responde las preguntas de Claude (tu tienda, tu producto y la página de referencia). Él instala, prepara tu tienda y monta la página. Al final te da el link de vista previa.

> El mismo prompt está en [`PROMPT.md`](PROMPT.md), junto con el prompt corto para tus siguientes productos.

## Qué necesitas

| Necesitas | Para qué | Costo |
|---|---|---|
| **Claude Code** | Corre los agentes | Tu plan de Claude |
| **Una tienda Shopify con plan de pago** y el tema gratuito **Horizon** instalado (no hace falta publicarlo) | Donde queda tu página | Plan de Shopify. Una tienda de desarrollo sirve para probar, pero nunca podrá vender |
| **Conectores en Claude:** Shopify, Firecrawl y Magnific | Tu tienda · leer la página de referencia · crear las imágenes | Magnific: unos 2.500 créditos por página (los rehechos se cobran aparte) |
| **Releasit COD Form** (Shopify App Store) | Formulario de pago contraentrega | Instalación gratis |
| Shopify CLI y Python 3 | Subir el tema y armar las imágenes | Gratis. Claude los instala si faltan |

> Los conectores se agregan en Claude → Configuración → Conectores. Al conectar Shopify, elige tu tienda.

## Cómo funciona

Seis agentes de Claude trabajan al mismo tiempo, por olas:

| Minuto | Qué pasa | Qué recibes |
|---|---|---|
| 0–4 | Un agente lee la página de referencia, otro investiga tu producto y otro empieza a crear las imágenes | Aviso de arranque |
| 4–8 | Se escriben todos los textos de la página | Ficha del producto, ángulos de venta y hoja de revisión de imágenes |
| 8–11 | Se crea el producto, un tema nuevo y se sube todo | Link de vista previa |
| 11–13 | Se revisan enlaces, imágenes, botón de contraentrega y versión celular | OK o lista de arreglos |
| 13–15 | Cierre | Tiempos y pendientes |

La primera vez se suma la preparación de la tienda (unos 10 minutos): envíos, mercado del país, páginas y menús en español, tema base y contraentrega.

Cuando la página te guste, pídele a Claude que la publique o hazlo tú en Tienda online → Temas → **Publicar**.

## Preguntas frecuentes

**¿Copia la página de otra tienda?**
Copia la **estructura y el estilo**, no el contenido. Textos, cifras, reseñas, fotos y marcas de la referencia no se usan: todo sale de tu producto.

**¿Sirve si la referencia es de otro nicho?**
Sí. Las imágenes toman el encuadre de la referencia, pero muestran el nicho de tu producto y lo que dice cada tarjeta (por ejemplo, un suplemento para perros muestra perros, no personas corriendo).

**¿Toca mi tienda publicada?**
No. Cada página se arma en un tema nuevo. Nada se publica ni se envía un pedido sin tu OK.

**¿Y si una imagen no me gusta?**
Dile a Claude cuál y cómo la quieres. La rehace y vuelve a subir la página (cada imagen rehecha cuesta unos 75 créditos de Magnific).

**¿Puedo hacer varios productos?**
Sí. La tienda se prepara una sola vez; cada producto nuevo es un prompt corto (está en [`PROMPT.md`](PROMPT.md)).

**¿Funciona fuera de Colombia?**
Está probado en Colombia con pesos (COP) y contraentrega. Para otro país, dile a Claude tu país y tu moneda al empezar.

## Si algo sale mal

| Ves esto | Pídele a Claude |
|---|---|
| Las imágenes no cambiaron en la página | `corre tools/estado.py y si dice DESACTUALIZADO vuelve a subir` |
| Una imagen no tiene que ver con su texto | `rehaz la imagen <id> mostrando <escena> y vuelve a subir` |
| Claude se detiene pidiendo permiso | Apruébalo. Es normal la primera vez que usa Shopify o Magnific |
| La vista previa pide contraseña | Escribe la contraseña de tu tienda en el panel del navegador de Claude |
| Un agente se cortó | `relanza <agente> con "continúa"` (lo ya generado no se pierde) |
| "Falta tienda.json" | `prepara mi tienda` |

## Buenas prácticas

- **Revisa antes de publicar:** precios, garantías y afirmaciones son tu responsabilidad. Cambia las reseñas "demo" por reseñas reales.
- Si vendes un producto de otra marca, eres revendedor: no te presentes como tienda oficial.
- Sin promesas médicas ni cifras que no puedas demostrar.

## Qué trae el kit

```
PROMPT.md         el prompt de instalación y el prompt corto por producto
.claude/agents/   6 agentes: referencia · producto · creativos · copy · ensamblador · qa
.claude/skills/   tienda-preparar · tienda-express (orquesta) · y las guías de cada paso
kit/              secciones de Shopify (Liquid) de la página de venta
tools/            scripts: nueva, armar, gen_tema, descargar, estado, tarjetas, qa.js…
tools/ejemplo/    un brief.json completo de ejemplo
.agents/ .codex/  la misma versión para Codex (experimental) · AGENTS.md
corridas/         aquí queda cada página que hagas (no se sube a git)
```

---

Hecho con Claude Code por **El Master IA · Alexander Cast**. Parte de la Bóveda del Master. Licencia MIT: úsalo, modifícalo y compártelo.
