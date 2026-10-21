# Prompt de instalación · Tu tienda online en 15 minutos

Copia todo el bloque y pégalo en una conversación nueva de **Claude Code** (app de escritorio o terminal). No tienes que cambiar nada: Claude te va a preguntar lo que necesita.

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

## Para el siguiente producto

En la misma carpeta, pega solo esto (la tienda ya queda preparada):

```
/tienda-express
Producto: <link o "fotos adjuntas">
Referencia: <link de la página que quiero copiar>
Marca: <la del producto | otra>
Oferta: <"demo" | 1 unidad $____ · Pack x2 $____ + regalo ____>
Garantía: <"demo" | la real>
```
