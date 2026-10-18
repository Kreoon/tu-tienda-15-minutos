# brief.json · contrato de una corrida tienda-express

Un solo archivo por producto: `corridas/<slug>/brief.json`. Lo escribe el agente **tienda-copy**; lo consume `tools/gen_tema.py` (vía `armar.py`).
Ejemplo completo y probado: [`tools/ejemplo/brief.json`](../../tools/ejemplo/brief.json).
Textos en español de Colombia. En los títulos, `<em>…</em>` marca la palabra en color (como la referencia).
Una clave ausente = la sección no se genera. **Ninguna cifra, reseña o garantía sin fuente** (ficha o decisiones del equipo); reseñas de ejemplo con `"demo": true`.

## IDs de imagen fijos (copy y creativos trabajan en paralelo con estos nombres)

| ID | Pieza | Formato | Usada en |
|---|---|---|---|
| `g1` | Producto héroe, fondo liso cálido | 1:1 | galería 1, regalo envío |
| `g2` | Pack / oferta (2 unidades + regalo) | 1:1 | galería 2, regalo bloqueado |
| `g3` | Persona usando el producto (contexto 1) | 1:1 | galería 3, popup |
| `g4` | Persona usando el producto (contexto 2) | 1:1 | galería 4 |
| `g5` | Producto en sus variantes / colores | 1:1 | galería 5, oferta repetida |
| `t1`–`t4` | Macros / detalles técnicos | 1:1 | tecnologías, fondo de cifras (`t1`) |
| `b1`–`b4` | Casos de uso (estilo de vida) | 4:3 | beneficios en filas |
| `z1`–`z5` | Una por razón | 16:9 | 5 razones |
| `w1` | Persona sonriendo con el producto | 4:5 | garantía, regalo garantía |
| `l1` | Escena de marca amplia | 16:9 | línea de tiempo |
| `p1` | Producto sin fondo (PNG) | 1:1 | beneficios con producto al centro |
| `ugc01`…`ugc12` | Selfies UGC verticales (cortados de collages) | 9:16 | videos, avatares, franja de reseñas |
| `logo`, `logo_blanco` | Marca de la tienda (`creativos/marca/logo.png`, `logo_blanco.png`) | — | popup, footer |

Archivos: `creativos/<id>.jpg|png` (+ `creativos/ugc/ugcNN.jpg`). URLs públicas de Magnific en `creativos/urls.json` (`{"g1": "https://…"}`) para la galería del producto.

## Claves

```jsonc
{
  "tema": {"sufijo": "<slugsinguiones>", "nombre": "<Marca> · <producto>"},   // sufijo = plantilla product.<sufijo>.json (único por corrida)
  "marca": {"nombre": "<marca del producto o de la tienda; nunca la de otra corrida>", "logo": "logo", "logo_blanco": "logo_blanco"},
  "orden": ["pop","mq","main","stats","tech","rev1","bc","rows","mq2","tl","why","cmp","gu","vids2","buy2","rev2"], // opcional: orden de la referencia
  "producto": {
    "handle": "…", "titulo": "…", "marca": "…", "tipo": "…", "sku": "BASE", "tags": ["tienda-express"],
    "opcion_color": "Color", "colores": ["Negro","Blanco"],            // [] si no hay colores
    "descripcion_html": "<p>…</p>", "seo": {"title": "…", "description": "…"},
    "galeria": ["g1","g2","g3","g4","g5"],
    "ofertas": [{"valor": "1 unidad", "titulo": "Lleva 1", "detalle": "…", "precio": 99900, "antes": 139900, "sku_sufijo": "X1",
                 "etiqueta": "Más elegido", "regalo": "…"}]                // "valor" = valor exacto de la opción Oferta
  },
  "tokens": {"primario": "#…", "secundario": "#…", "acento": "#…", "fondo_alterno": "#…", "texto": "#…", "texto_suave": "#…",
             "borde": "#…", "alerta": "#…", "oscuro_2": "#…", "oscuro_3": "#…", "comparativa": "#…",
             "fuente_titulos": "'Clash Grotesk', sans-serif", "fuente_texto": "'Satoshi', sans-serif"},
  "anuncio": {"titulo": "…", "texto": "…", "horas": 2},              // va al header-group (encima del header)
  "popup": {"segundos": 5, "etiqueta": "…", "titulo": "…", "texto": "…", "premio": "…", "img": "g3"},
  "cinta": ["beneficio 1", "…"],                                       // marquee (se repite como mq2)
  "compra": {"prueba_social": "…", "eyebrow": "…", "titulo": "…", "subtitulo": "…", "beneficios": ["…"],
             "escasez": 87, "escasez_texto": "…", "entrega_dias": 3, "entrega_texto": "Pide hoy y recíbelo el", "origen": "…",
             "boton": "PEDIR AHORA · PAGO CONTRAENTREGA", "confianza": "a | b",
             "regalos": [{"img": "g1", "titulo": "…", "valor": "$…", "bloqueado": false, "se_desbloquea_con": "<valor oferta>"}],
             "avatares": ["ugc01","ugc02","ugc03","ugc04"],
             "acordeones": [{"titulo": "…", "html": "<p>…</p>"}],
             "videos_titulo": "Lo que dicen nuestros clientes:", "videos": [{"img": "ugc05", "texto": "…"}]},
  "cifras": {"img": "t1", "titulo": "…", "texto": "…", "boton": "…", "items": [{"cifra": "…", "texto": "…"}]},
  "tecnologias": {"titulo": "…", "items": [{"img": "t1", "titulo": "…", "texto": "…"}]},
  "resenas_destacadas": {"titulo": "…", "texto": "…", "fotos": ["ugc01", "…"],
                         "resenas": [{"nota": "5.0", "titulo": "…", "texto": "…", "autor": "…", "avatar": "ugc04", "etiquetas": ["…"], "demo": true}]},
  "beneficios_producto": {"titulo": "…", "texto": "…", "img": "p1", "items": [{"icono": "35h", "texto": "…"}]},
  "beneficios_filas": {"titulo": "…", "texto": "…", "items": [{"img": "b1", "titulo": "…", "subtitulo": "…", "texto": "…"}]},
  "linea_tiempo": {"img": "l1", "titulo": "…", "texto": "…", "boton": "…", "pasos": [{"titulo": "…", "puntos": ["…"]}]},
  "razones": {"badge": "5 razones", "titulo": "…", "boton": "…", "prefijo": "Razón", "items": [{"img": "z1", "titulo": "…", "texto": "…"}]},
  "comparativa": {"nosotros": "…", "otros": "…", "titulo": "…", "puntos": ["<strong>…</strong> — …"], "boton": "…", "filas": [["nosotros","otros"]]},
  "garantia": {"numero": "7", "unidad": "DÍAS", "antetitulo": "…", "titulo": "…", "texto": "…", "img": "w1"},
  "videos": {"titulo": "…", "texto": "…", "boton": "…", "items": [{"img": "ugc06", "texto": "…"}]},
  "oferta_repetida": {"img": "g5", "titulo": "…", "texto": "…"},
  "resenas_lista": {"calificacion": "…", "titulo": "…", "resenas": [{"nota": "5.0", "titulo": "…", "texto": "…", "etiquetas": ["…"], "demo": true}]},
  "footer": {"newsletter_titulo": "…", "newsletter_texto": "…", "legal_html": "<p>…</p>"}
}
```

Validación rápida: `python -I tools/gen_tema.py corridas/<slug>` debe terminar con `ok · N secciones`.
