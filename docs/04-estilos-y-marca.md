# 04 · Estilos, marca, recursos y formatos

## Cómo se decide el look de un reel
```
Marca/Marca.md               (común a todo: colores, fuentes, logo, tono, sonido)
   +  Estilos/<Tipo>/estilo.md  (lo propio del tipo: subtítulos, gráficos, recursos, música, CTA)
   =  estilo del reel        (si chocan, gana el del tipo)
```

## Cambiar la marca (vale para todos los reels)
Editá `Reels con Claude/Marca/Marca.md` o pedile a Claude:
> *Cambiá el acento claro de la marca a #D6DEE8 y agregá que los números van siempre con separador de miles.*

- Logos: `Marca/logos/` (SVG o PNG sin fondo). Hoy: `logo-AB.svg` (fondos claros) y `logo-AB-claro.svg` (sobre video).
- Fuentes: `Marca/tipografias/` (.ttf / .otf).
- Música propia: `Marca/musica/`.

## Cambiar o crear el estilo de un tipo
Cada `estilo.md` tiene: objetivo · tono y estructura · subtítulos · gráficos · **recursos permitidos y prohibidos** · sonido · CTA. Todo con valores medibles (HEX, px, segundos, dB).

**Desde referencias** (la mejor forma):
1. Guardá 3–5 reels o capturas que te gusten en `Estilos/<Tipo>/referencias/`.
2. Pedí: *«Mirá las referencias de captación y proponé cambios al estilo. Mostrame antes de guardar.»*

**Desde notas de un reel**: *«Guardá en el estilo de propiedades que las etiquetas de zona duren 3 segundos.»*

**Aprobar un borrador**: *«Marcá el estilo de marca personal como aprobado con el reel del 2026-12-01 como referencia.»*

## Íconos y recursos por tipo
- Cada tipo tiene `Estilos/<Tipo>/recursos/iconos/`. Lo que está ahí **solo se usa en ese tipo**.
- Formato: SVG de un color (blanco o #172844), trazo de 2 px, sin fondo.
- Pedí: *«Diseñá íconos de dormitorio, baño, m², pileta y ubicación para propiedades, con el estilo de la marca.»*
- La lista **Permitidos / Prohibidos** al final de cada `estilo.md` es la que manda: Claude no usa un recurso prohibido aunque lo pidas de pasada (te va a avisar).

## Formatos (cómo se arma un video)
| Formato | Usado por | Dónde |
|---|---|---|
| `propiedad-planos` | Propiedades | `Formatos/propiedad-planos/` (LEEME + plantilla de scripts) |
| `propiedad-recorrido` | Propiedades | `Formatos/propiedad-recorrido/` |
| `cabeza-parlante` | Captación, Marca personal | `Formatos/cabeza-parlante/` (usa las pasadas de la skill) |

**Crear un formato nuevo** (por ejemplo «antes y después», «carrusel animado de fotos», «testimonio de cliente»):
1. Hacé el primer video con Claude a mano hasta que te guste.
2. Pedí: *«Convertí este reel en un formato nuevo de la fábrica llamado <nombre>.»*
3. Claude crea `Formatos/<nombre>/` con su LEEME (qué grabar, pasos) y `plantilla/`, con los datos variables marcados como `EDITAR` o leídos de `propiedad.json`.

## Crear un tipo nuevo (por ejemplo «Alquileres» o «Emprendimientos»)
> *Agregá un tipo nuevo de reel «Emprendimientos», basado en propiedades pero con avance de obra y planos.*

Se crea `Estilos/Emprendimientos/` (estilo.md + recursos + referencias), la carpeta de trabajo y la entrada en la skill.
