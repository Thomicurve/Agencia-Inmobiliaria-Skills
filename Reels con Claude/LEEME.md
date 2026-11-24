# Fábrica de reels · Inmobiliaria

Abrí Claude en la carpeta del repo (la de arriba de esta) y pedí, por ejemplo:
- «Hacé el reel de planos de **Funes - San Martín 450**»
- «Editá el video de captación que dejé en la Bandeja»
- «Reel de marca personal con la toma de hoy»

Claude reconoce el **tipo** (propiedad / captación / marca personal), aplica la **base de marca** + el **estilo de ese tipo** y usa la **plantilla del formato**.

```
Reels con Claude/
├─ Bandeja/                    ← tirá acá lo que grabaste (desde el celular). Claude lo ordena.
├─ Marca/                      ← base común a todo
│   ├─ Marca.md                paleta, tipografías, logo, tono, sonido, formato
│   ├─ logos/  tipografias/  musica/
├─ Estilos/                    ← lo que cambia según el tipo de video
│   ├─ Propiedades/            estilo.md · recursos/iconos · referencias/
│   ├─ Captacion/              estilo.md · recursos/iconos · referencias/
│   └─ Marca personal/         estilo.md · recursos/iconos · referencias/
├─ Formatos/                   ← cómo se arma cada tipo de video (plantillas probadas)
│   ├─ propiedad-planos/       LEEME.md + plantilla/ (scripts)
│   ├─ propiedad-recorrido/    LEEME.md + plantilla/
│   └─ cabeza-parlante/        LEEME.md (usa la skill)
├─ Propiedades/                ← una carpeta por propiedad (SOLO LOCAL: no se sube a GitHub)
│   └─ <Localidad> - <Dirección>/
│       ├─ propiedad.json      precio, dirección, datos, palabra del CTA (se cambia solo acá)
│       ├─ guiones/
│       ├─ tomas/<recorrida | planos | planos-hablado>/
│       └─ reels/AAAA-MM-DD · <formato>/   proyecto.json · trabajo/ · graficos/ · FINAL · portada
├─ Captacion/                  ← un reel por carpeta
│   └─ AAAA-MM-DD · <tema>/    toma/ · guion.md · proyecto.json · trabajo/ · graficos/ · FINAL
└─ Marca personal/             ← igual que Captacion
```

## Reglas
- Las tomas originales nunca se modifican: Claude trabaja con copias en `trabajo/`.
- Un dato de la propiedad (precio, dirección) se cambia **solo** en `propiedad.json`; los reels lo leen de ahí.
- `trabajo/` ocupa varios GB: se puede borrar cuando el reel está publicado.
- Íconos y recursos que solo valen para un tipo van en `Estilos/<Tipo>/recursos/`. Lo que se permite y lo que no está al final de cada `estilo.md`.
