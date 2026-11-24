# 05 · Meta Ads con los reels

Skill: `meta-ads-inmobiliaria`. Carpeta: `Meta Ads/`. Tres fases: **planear → cargar → analizar**.

| Tipo | Objetivo | Creativo |
|---|---|---|
| **Captación** | Propietarios que quieren vender o tasar, por barrio (mensajes a WhatsApp/Instagram) | Reels de `Captacion/` |
| **Ventas** | Compradores para una propiedad (formulario instantáneo) | Reels de `Propiedades/<prop>/reels/` |

## Pedidos típicos
> *Armá una campaña de ventas para <Localidad> - <Dirección> con el reel de planos. Presupuesto 30.000 por semana.*
> *Dame la ficha de carga paso a paso para el Administrador de anuncios.*
> *Te paso el CSV de resultados: ¿pauso, cambio o escalo?*

- Los datos de la propiedad salen de `propiedad.json` (no se copian a mano).
- Primera vez: Claude crea `Meta Ads/agencia.json` (página, WhatsApp, cuenta publicitaria) y `zonas.md`.
- **Los leads (`leads.csv`) y los exportes de resultados no se suben a GitHub**: tienen datos personales.
