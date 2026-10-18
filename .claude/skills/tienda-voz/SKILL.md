---
name: tienda-voz
description: Quita la "voz de IA" de textos en español latinoamericano — copy de landings, FAQs, descripciones de producto, mensajes y avisos. Detecta los patrones que delatan texto generado (frases infladas, tríadas, adjetivos vacíos, anglicismos, falsa urgencia, conectores de relleno) y los reescribe con voz de vendedor real. Úsalo después de generar copy con IA, al revisar un PageSpec, o cuando un texto "suena a ChatGPT".
---

# Voz humana (español LATAM)

El comprador latino detecta en dos segundos el texto genérico y deja de confiar. La regla: **escribe como le hablaría al cliente el dueño del negocio por WhatsApp, pero sin errores.**

## Patrones a eliminar
### Palabras y frases delatoras
| Delata IA | Reemplazo |
|---|---|
| Descubre / Explora / Sumérgete en | di directamente qué es o qué gana |
| Eleva tu… / Lleva tu X al siguiente nivel | el resultado concreto ("tu café sigue caliente a las 3 p. m.") |
| Revoluciona / Transforma tu vida | lo que cambia de verdad, medible |
| Experiencia única / inigualable / excepcional | la prueba (cifra, material, garantía) |
| Calidad premium / de alta calidad | el material o la especificación |
| No busques más / Lo que estabas esperando | elimina |
| Diseñado pensando en ti | para quién exactamente y por qué |
| En el mundo acelerado de hoy… | elimina, empieza por el punto |
| Sin duda / Cabe destacar / Es importante mencionar | elimina |
| Además, … Asimismo, … Por otro lado, … (en cada frase) | frases cortas sin conector |
| Game changer, must-have, all-in-one, upgrade | español: "imprescindible", "todo en uno", "mejora" — o mejor, el dato |

### Estructuras delatoras
- **Tríadas automáticas**: "rápido, fácil y seguro" en cada párrafo. Deja una sola, la que el producto puede probar.
- **Paralelismo de plantilla**: tres beneficios que empiezan igual ("Disfruta de…", "Disfruta de…").
- **Adjetivo + sustantivo inflado**: "increíble comodidad", "asombrosa durabilidad". Cambia por el hecho: "aguanta 200 lavadas".
- **Pregunta retórica de apertura** en cada sección ("¿Cansado de…?"). Una vez en la página, máximo.
- **Cierre moralizante**: "Porque tú te mereces lo mejor." Elimina.
- **Hedging**: "podría ayudarte a potencialmente…". O ayuda o no; si es claim de salud, usa lenguaje seguro: "ayuda a", "apoya", nunca "cura" ni promesas de resultado.
- **Signos**: exceso de exclamaciones, guiones largos en cadena, emojis en titulares, MAYÚSCULAS para gritar.

### Falsa urgencia y falsas pruebas
- "¡Solo quedan 3!" sin dato real → quitar o usar fecha/stock reales configurados.
- "Miles de clientes felices" sin número → quitar o poner el número real.
- Testimonios perfectos y genéricos → específicos (ciudad, uso concreto, un detalle imperfecto) y con el disclaimer de ejemplo hasta tener reales.

## Cómo suena bien
- **Tuteo** cercano, neutro LATAM (sin "vosotros", sin modismos de un solo país salvo que el usuario lo pida: "parce", "wey", "che").
- Frases de 6–14 palabras. Una idea por frase.
- Verbo + resultado + dato: "Mantiene tu bebida fría 24 horas, incluso en el carro al sol."
- Objeciones respondidas como las respondería un vendedor: "¿Y si no me llega? Pagas cuando lo recibes."
- Números con formato local: `$89.900`, `24 h`, `500 ml`.

## Proceso
1. Marca cada frase con el patrón que rompe (tabla de arriba).
2. Reescribe solo esas frases; conserva datos, longitud aproximada y estructura del brief.json.
3. Lee en voz alta mentalmente: si no lo diría un vendedor por WhatsApp, vuelve a escribirlo.
4. Verifica que no inventaste datos al "humanizar" (ningún número nuevo sin fuente en la ficha del producto).

## Ejemplo
**Antes:** "Descubre el termo inteligente que revolucionará tu día. Con su diseño premium y su increíble tecnología, disfrutarás de una experiencia única. ¡No busques más!"
**Después:** "Tu café caliente 12 horas y sin quemarte: la tapa te muestra los grados antes del primer sorbo. Acero 304, 500 ml."

## Salida
Para un brief.json: las secciones modificadas como JSON válido + una tabla `campo · antes · después · patrón`. Para texto suelto: el texto limpio y la lista de patrones corregidos.
