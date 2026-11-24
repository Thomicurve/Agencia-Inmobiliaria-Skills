#!/usr/bin/env python3
"""Informe de una campaña de Meta Ads de la inmobiliaria.

Lee, de la carpeta de la campaña:
  campana.json           plan (tipo, nombre en Meta, KPIs objetivo, fechas)
  resultados/*.csv       exporte del Administrador de anuncios (usa el más nuevo, o --export)
  leads.csv              seguimiento de contactos (opcional pero recomendado)
y escribe informes/AAAA-MM-DD.md con totales, tabla por anuncio, embudo y alertas.

Uso:
  python analizar.py "<carpeta campaña>" [--export archivo.csv] [--cerrar]

--cerrar  además suma una fila a historico.csv (en la carpeta de Meta Ads) y marca la campaña como cerrada.
Solo usa la biblioteca estándar de Python.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import sys
import unicodedata
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")  # consola de Windows
except Exception:
    pass

# ---------------------------------------------------------------- columnas
# campo lógico -> lista de (palabras que deben estar, palabras que no deben estar)
COLUMNAS = {
    "campana": [(["nombre de la campana"], []), (["campaign name"], [])],
    "conjunto": [(["nombre del conjunto"], []), (["ad set name"], [])],
    "anuncio": [(["nombre del anuncio"], []), (["ad name"], [])],
    "gasto": [(["importe gastado"], []), (["amount spent"], []), (["gasto"], ["costo"])],
    "impresiones": [(["impresiones"], ["costo", "cpm"]), (["impressions"], ["cost", "cpm"])],
    "alcance": [(["alcance"], ["costo"]), (["reach"], ["cost"])],
    "frecuencia": [(["frecuencia"], []), (["frequency"], [])],
    "clics_enlace": [
        (["clics en el enlace"], ["ctr", "cpc", "costo", "unicos", "porcentaje"]),
        (["link clicks"], ["ctr", "cpc", "cost", "unique", "rate"]),
    ],
    "resultados": [
        (["resultados"], ["costo", "indicador", "tipo", "tasa"]),
        (["results"], ["cost", "indicator", "type", "rate"]),
    ],
    "conversaciones": [
        (["conversaciones", "iniciadas"], ["costo"]),
        (["messaging conversations started"], ["cost"]),
    ],
    "leads": [
        (["clientes potenciales"], ["costo", "sitio web", "conversion", "fuera"]),
        (["leads"], ["cost", "website", "conversion", "offline"]),
    ],
    "indicador": [(["indicador de resultado"], []), (["result indicator"], []), (["tipo de resultado"], [])],
    "inicio": [(["inicio del informe"], []), (["reporting starts"], [])],
    "fin": [(["fin del informe"], []), (["reporting ends"], [])],
}

ETAPAS = {
    # (etiqueta, estados que cuentan como haber llegado a esa etapa)
    "captacion": [
        ("Respondieron", {"contactado", "calificado", "descartado", "tasacion", "captado", "perdido"}),
        ("Calificados", {"calificado", "tasacion", "captado", "perdido"}),
        ("Tasaciones", {"tasacion", "captado"}),
        ("Captaciones", {"captado"}),
    ],
    "venta": [
        ("Contactados", {"contactado", "calificado", "descartado", "visita", "oferta", "reserva", "vendido", "perdido"}),
        ("Calificados", {"calificado", "visita", "oferta", "reserva", "vendido", "perdido"}),
        ("Visitas", {"visita", "oferta", "reserva", "vendido"}),
        ("Ofertas/reservas", {"oferta", "reserva", "vendido"}),
    ],
}


def norm(s: str) -> str:
    s = unicodedata.normalize("NFKD", str(s or "")).encode("ascii", "ignore").decode()
    return " ".join(s.lower().replace("_", " ").split())


def mapear_columnas(headers: list[str]) -> dict[str, str]:
    nh = {h: norm(h) for h in headers}
    out: dict[str, str] = {}
    for campo, reglas in COLUMNAS.items():
        for incluir, excluir in reglas:
            cand = [h for h, n in nh.items()
                    if all(w in n for w in incluir) and not any(w in n for w in excluir)]
            if cand:
                out[campo] = min(cand, key=len)  # la más corta = la más «pura»
                break
    return out


def num(v) -> float | None:
    if v is None:
        return None
    s = str(v).strip().replace("US$", "").replace("USD", "").replace("$", "").replace("%", "").replace(" ", "").replace(" ", "")
    if s in ("", "-", "—", "n/a", "N/A"):
        return None
    if "," in s and "." in s:
        if s.rfind(",") > s.rfind("."):
            s = s.replace(".", "").replace(",", ".")
        else:
            s = s.replace(",", "")
    elif "," in s:
        ent, _, dec = s.rpartition(",")
        if len(dec) == 3 and ent not in ("", "0", "-0") and s.count(",") >= 1 and not ent.startswith("0"):
            s = s.replace(",", "")  # separador de miles
        else:
            s = ent.replace(",", "") + "." + dec
    try:
        return float(s)
    except ValueError:
        return None


def leer_csv(path: Path) -> list[dict]:
    raw = path.read_bytes()
    for enc in ("utf-8-sig", "utf-16", "latin-1"):
        try:
            texto = raw.decode(enc)
            break
        except UnicodeDecodeError:
            continue
    muestra = texto[:4000]
    delim = ";" if muestra.count(";") > muestra.count(",") else ","
    return list(csv.DictReader(texto.splitlines(), delimiter=delim))


def div(a, b):
    return a / b if a is not None and b else None


def f(v, dec=2, suf=""):
    if v is None:
        return "—"
    if dec == 0:
        return f"{v:,.0f}".replace(",", ".") + suf
    return f"{v:,.{dec}f}".replace(",", "X").replace(".", ",").replace("X", ".") + suf


def metricas(rows: list[dict], col: dict, tipo: str) -> dict:
    def suma(campo):
        if campo not in col:
            return None
        vals = [num(r.get(col[campo])) for r in rows]
        vals = [v for v in vals if v is not None]
        return sum(vals) if vals else 0.0

    principal = "conversaciones" if tipo == "captacion" else "leads"
    res = suma(principal) if principal in col else suma("resultados")
    m = {
        "gasto": suma("gasto"),
        "impresiones": suma("impresiones"),
        "alcance": suma("alcance"),
        "clics": suma("clics_enlace"),
        "resultados": res,
    }
    m["cpm"] = div(m["gasto"], m["impresiones"]) * 1000 if div(m["gasto"], m["impresiones"]) is not None else None
    m["ctr"] = div(m["clics"], m["impresiones"]) * 100 if div(m["clics"], m["impresiones"]) is not None else None
    m["cpc"] = div(m["gasto"], m["clics"])
    m["cpr"] = div(m["gasto"], m["resultados"])
    if len(rows) == 1 and "frecuencia" in col:
        m["frecuencia"] = num(rows[0].get(col["frecuencia"]))
    else:
        m["frecuencia"] = div(m["impresiones"], m["alcance"])
    return m


def leer_leads(path: Path) -> list[dict]:
    if not path.exists():
        return []
    rows = leer_csv(path)
    return [{norm(k): (v or "").strip() for k, v in r.items() if k} for r in rows if any((v or "").strip() for v in r.values())]


def embudo(leads: list[dict], tipo: str) -> list[tuple[str, int]]:
    out = []
    for etiqueta, estados in ETAPAS[tipo]:
        n = 0
        for l in leads:
            est = norm(l.get("estado", "")).replace("tasacion agendada", "tasacion")
            calif = norm(l.get("calificado", "")) in ("si", "s", "1", "true", "x")
            if est in estados or (etiqueta == "Calificados" and calif):
                n += 1
            elif etiqueta in ("Respondieron", "Contactados") and calif:
                n += 1
        out.append((etiqueta, n))
    return out


def buscar_raiz_ads(carpeta: Path) -> Path | None:
    for p in [carpeta, *carpeta.parents]:
        if (p / "agencia.json").exists() or (p / "historico.csv").exists():
            return p
    return None


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("carpeta")
    ap.add_argument("--export", help="CSV a usar (por defecto, el más nuevo de resultados/)")
    ap.add_argument("--cerrar", action="store_true", help="cerrar campaña y sumar a historico.csv")
    a = ap.parse_args()

    carpeta = Path(a.carpeta).resolve()
    cj = carpeta / "campana.json"
    if not cj.exists():
        sys.exit(f"No encuentro {cj}. ¿Es la carpeta de una campaña?")
    camp = json.loads(cj.read_text(encoding="utf-8"))
    tipo = "venta" if norm(camp.get("tipo", "")).startswith("vent") else "captacion"
    kpi = camp.get("kpis_objetivo", {}) or {}
    nombre_meta = (camp.get("meta", {}) or {}).get("nombre_campana", "")

    if a.export:
        export = Path(a.export)
    else:
        csvs = sorted((carpeta / "resultados").glob("*.csv"), key=lambda p: p.stat().st_mtime)
        if not csvs:
            sys.exit("No hay ningún .csv en resultados/. Exportá la tabla del Administrador de anuncios (pestaña Anuncios, «Desde el inicio», .csv) y guardalo ahí.")
        export = csvs[-1]
    filas = leer_csv(export)
    if not filas:
        sys.exit(f"{export.name} está vacío.")
    col = mapear_columnas(list(filas[0].keys()))

    avisos: list[str] = []
    faltan = [c for c in ("gasto", "impresiones", "clics_enlace") if c not in col]
    principal = "conversaciones" if tipo == "captacion" else "leads"
    if principal not in col and "resultados" not in col:
        faltan.append(principal)
    if faltan:
        avisos.append("Columnas no encontradas en el exporte: " + ", ".join(faltan)
                      + ". Agregalas en el Administrador de anuncios (Columnas → Personalizar) y volvé a exportar.")
    if principal not in col and "resultados" in col:
        avisos.append(f"No hay columna específica de {principal}; uso «Resultados». Verificá que el indicador de resultado sea el correcto.")

    # filas totales / vacías fuera; filtrar por nombre de campaña si coincide
    nombres = [c for c in ("campana", "conjunto", "anuncio") if c in col]
    filas = [r for r in filas if any((r.get(col[c]) or "").strip() for c in nombres)] if nombres else filas
    if "campana" in col and nombre_meta and "<" not in nombre_meta:
        propias = [r for r in filas if norm(r.get(col["campana"])) == norm(nombre_meta)]
        if propias:
            filas = propias
        else:
            avisos.append(f"Ninguna fila tiene el nombre de campaña «{nombre_meta}»: analizo todo el archivo.")

    total = metricas(filas, col, tipo)

    # por anuncio
    clave = col.get("anuncio") or col.get("conjunto") or col.get("campana")
    grupos: dict[str, list[dict]] = {}
    if clave:
        for r in filas:
            grupos.setdefault((r.get(clave) or "(sin nombre)").strip(), []).append(r)
    por_anuncio = {k: metricas(v, col, tipo) for k, v in grupos.items()}

    # fechas
    hoy = dt.date.today()
    inicio = None
    try:
        inicio = dt.date.fromisoformat((camp.get("fechas", {}) or {}).get("inicio", "")[:10])
    except ValueError:
        pass
    if not inicio and "inicio" in col:
        try:
            inicio = min(dt.date.fromisoformat(r[col["inicio"]][:10]) for r in filas if r.get(col["inicio"]))
        except ValueError:
            pass
    dias = (hoy - inicio).days + 1 if inicio else None

    # leads
    leads = leer_leads(carpeta / "leads.csv")
    etapas = embudo(leads, tipo) if leads else []
    calificados = dict(etapas).get("Calificados", 0) if etapas else None
    costo_calif = div(total["gasto"], calificados) if calificados else None

    # ---------------------------------------------------------- alertas
    alertas: list[str] = []
    if dias is not None and dias < 7:
        alertas.append(f"⏳ Lleva {dias} día(s): lectura preliminar. Solo corregir errores de entrega; no optimizar antes del día 7.")
    if (total["resultados"] or 0) < 10:
        alertas.append(f"⏳ Solo {f(total['resultados'], 0)} resultados: muestra chica, las diferencias entre anuncios pueden ser azar.")
    if total["gasto"] is not None and total["gasto"] == 0:
        alertas.append("🔴 No gastó nada: revisar aprobación de anuncios, público demasiado chico o medio de pago.")
    if kpi.get("cpm_max_usd") and total["cpm"] and total["cpm"] > 2 * kpi["cpm_max_usd"]:
        alertas.append(f"🔴 CPM {f(total['cpm'])} USD, más del doble del máximo ({kpi['cpm_max_usd']}): público chico/saturado.")
    elif kpi.get("cpm_max_usd") and total["cpm"] and total["cpm"] > kpi["cpm_max_usd"]:
        alertas.append(f"🟡 CPM {f(total['cpm'])} USD por encima del máximo ({kpi['cpm_max_usd']}).")
    if kpi.get("ctr_enlace_min_pct") and total["ctr"] is not None and total["ctr"] < kpi["ctr_enlace_min_pct"]:
        alertas.append(f"🟡 CTR de enlace {f(total['ctr'])} % bajo el mínimo ({kpi['ctr_enlace_min_pct']} %): revisar gancho/creativo.")
    if kpi.get("costo_por_resultado_usd") and total["cpr"] and total["cpr"] > kpi["costo_por_resultado_usd"]:
        nivel = "🔴" if total["cpr"] > 2 * kpi["costo_por_resultado_usd"] else "🟡"
        alertas.append(f"{nivel} Costo por resultado {f(total['cpr'])} USD vs objetivo {kpi['costo_por_resultado_usd']}.")
    if kpi.get("frecuencia_max"):
        for k, m in por_anuncio.items():
            if m["frecuencia"] and m["frecuencia"] > kpi["frecuencia_max"]:
                alertas.append(f"🟡 «{k}» frecuencia {f(m['frecuencia'])} > {kpi['frecuencia_max']}: posible fatiga, rotar creativo.")
    # anuncio claramente peor
    con_res = {k: m for k, m in por_anuncio.items() if m["cpr"] and m["gasto"]}
    if len(con_res) >= 2:
        mejor_k = min(con_res, key=lambda k: con_res[k]["cpr"])
        mejor = con_res[mejor_k]
        for k, m in con_res.items():
            if k != mejor_k and m["cpr"] > 2 * mejor["cpr"] and m["gasto"] >= 0.3 * mejor["gasto"]:
                alertas.append(f"🟡 «{k}» cuesta {f(m['cpr'])} USD por resultado, más del doble que «{mejor_k}» ({f(mejor['cpr'])}). Candidato a pausar/reemplazar.")
    sin_res = [k for k, m in por_anuncio.items() if (m["gasto"] or 0) > 0 and not m["resultados"]]
    for k in sin_res:
        if (por_anuncio[k]["gasto"] or 0) >= 2 * (total["cpr"] or 1e9):
            alertas.append(f"🟡 «{k}» gastó {f(por_anuncio[k]['gasto'])} USD sin resultados.")
    if not leads:
        alertas.append("📋 leads.csv vacío o inexistente: sin él no se puede medir costo por calificado (el KPI principal).")
    else:
        if total["resultados"] and len(leads) < 0.7 * total["resultados"]:
            alertas.append(f"📋 leads.csv tiene {len(leads)} contactos y Meta reporta {f(total['resultados'], 0)} resultados: ¿faltan cargar contactos?")
        if total["resultados"] and calificados is not None and kpi.get("tasa_calificacion_min_pct"):
            tasa = calificados / total["resultados"] * 100
            if tasa < kpi["tasa_calificacion_min_pct"] and total["resultados"] >= 10:
                alertas.append(f"🟡 Solo {f(tasa, 1)} % de los resultados califica (mín. {kpi['tasa_calificacion_min_pct']} %): el público o el gancho atrae curiosos.")
        if kpi.get("costo_por_calificado_usd") and costo_calif:
            if costo_calif <= kpi["costo_por_calificado_usd"] and calificados >= 3 and (dias or 0) >= 7:
                alertas.append(f"🟢 Costo por calificado {f(costo_calif)} USD ≤ objetivo ({kpi['costo_por_calificado_usd']}) con {calificados} calificados: candidata a escalar 20–30 %.")
            elif costo_calif > 2 * kpi["costo_por_calificado_usd"] and (dias or 0) >= 14:
                alertas.append(f"🔴 Costo por calificado {f(costo_calif)} USD, más del doble del objetivo tras {dias} días: evaluar pausar.")
        if calificados == 0 and len(leads) > 30:
            alertas.append("🔴 Más de 30 contactos y ningún calificado: pausar y revisar zona/gancho.")

    # ---------------------------------------------------------- informe
    L = []
    L.append(f"# Informe · {nombre_meta or camp.get('id', carpeta.name)}")
    L.append("")
    L.append(f"**Fecha:** {hoy.isoformat()} · **Tipo:** {tipo} · **Días activa:** {dias if dias is not None else '—'} · "
             f"**Exporte:** `resultados/{export.name}` · **Presupuesto plan:** {camp.get('presupuesto', {}).get('diario_usd', '—')} USD/día")
    L.append("")
    L.append("## Totales")
    nombre_res = "Conversaciones" if tipo == "captacion" else "Clientes potenciales"
    L.append("| Gasto USD | Impresiones | Alcance* | Frecuencia* | CPM USD | Clics enlace | CTR enlace | " + nombre_res + " | Costo/resultado USD |")
    L.append("|---|---|---|---|---|---|---|---|---|")
    t = total
    L.append(f"| {f(t['gasto'])} | {f(t['impresiones'], 0)} | {f(t['alcance'], 0)} | {f(t['frecuencia'])} | {f(t['cpm'])} | "
             f"{f(t['clics'], 0)} | {f(t['ctr'])} % | {f(t['resultados'], 0)} | {f(t['cpr'])} |")
    L.append("")
    L.append("*Alcance y frecuencia totales son aproximados si se suman varios anuncios (Meta no suma personas únicas).")
    L.append("")
    if len(por_anuncio) > 1:
        L.append("## Por anuncio")
        L.append("| Anuncio | Gasto USD | CPM | CTR enlace | Frecuencia | Resultados | Costo/resultado | Calificados (leads.csv) | Costo/calificado |")
        L.append("|---|---|---|---|---|---|---|---|---|")
        for k, m in sorted(por_anuncio.items(), key=lambda kv: (kv[1]["cpr"] is None, kv[1]["cpr"] or 0)):
            cal_ad = None
            if leads:
                cal_ad = sum(1 for l in leads
                             if norm(l.get("anuncio", "")) and norm(l.get("anuncio", "")) in norm(k)
                             and (norm(l.get("calificado", "")) in ("si", "s", "1", "true", "x")
                                  or norm(l.get("estado", "")) in ETAPAS[tipo][1][1]))
            L.append(f"| {k} | {f(m['gasto'])} | {f(m['cpm'])} | {f(m['ctr'])} % | {f(m['frecuencia'])} | {f(m['resultados'], 0)} | "
                     f"{f(m['cpr'])} | {cal_ad if cal_ad is not None else '—'} | {f(div(m['gasto'], cal_ad)) if cal_ad else '—'} |")
        L.append("")
    L.append("## Embudo (leads.csv)")
    if etapas:
        L.append(f"| Etapa | Cantidad | % sobre resultados de Meta | Costo por etapa USD |")
        L.append("|---|---|---|---|")
        L.append(f"| {nombre_res} (Meta) | {f(t['resultados'], 0)} | 100 % | {f(t['cpr'])} |")
        L.append(f"| Registrados en leads.csv | {len(leads)} | {f(div(len(leads), t['resultados']) * 100 if div(len(leads), t['resultados']) is not None else None, 0)} % | — |")
        for etiqueta, n in etapas:
            pct = div(n, t["resultados"])
            L.append(f"| {etiqueta} | {n} | {f(pct * 100 if pct is not None else None, 0)} % | {f(div(t['gasto'], n)) if n else '—'} |")
    else:
        L.append("Sin datos: completá `leads.csv` (una fila por contacto, columna `estado`).")
    L.append("")
    L.append("## Contra objetivos")
    L.append("| Métrica | Real | Objetivo |")
    L.append("|---|---|---|")
    L.append(f"| Costo por resultado USD | {f(t['cpr'])} | {kpi.get('costo_por_resultado_usd', '—')} |")
    L.append(f"| CTR de enlace % | {f(t['ctr'])} | ≥ {kpi.get('ctr_enlace_min_pct', '—')} |")
    L.append(f"| CPM USD | {f(t['cpm'])} | ≤ {kpi.get('cpm_max_usd', '—')} |")
    L.append(f"| Costo por calificado USD | {f(costo_calif)} | {kpi.get('costo_por_calificado_usd', '—')} |")
    L.append(f"| Calificados | {calificados if calificados is not None else '—'} | {kpi.get('calificados_meta', '—')} |")
    L.append(f"_Fuente de los objetivos: {kpi.get('fuente', '—')}_")
    L.append("")
    L.append("## Alertas automáticas")
    L.extend(f"- {x}" for x in (alertas or ["Sin alertas."]))
    if avisos:
        L.append("")
        L.append("## Avisos sobre los datos")
        L.extend(f"- {x}" for x in avisos)
        L.append(f"- Columnas reconocidas: " + ", ".join(f"{k} → «{v}»" for k, v in col.items()))
    L.append("")
    L.append("## Diagnóstico y recomendación")
    L.append("<!-- Lo completa Claude siguiendo el árbol de diagnóstico de references/analisis.md: UNA recomendación principal y concreta. -->")
    L.append("")

    (carpeta / "informes").mkdir(exist_ok=True)
    salida = carpeta / "informes" / f"{hoy.isoformat()}.md"
    salida.write_text("\n".join(L), encoding="utf-8")
    print("\n".join(L))
    print(f"\n→ Informe guardado en {salida}")

    # ---------------------------------------------------------- cierre
    if a.cerrar:
        raiz = buscar_raiz_ads(carpeta.parent)
        if not raiz:
            print("⚠ No encontré la carpeta de Meta Ads (con agencia.json o historico.csv): no actualizo el histórico.")
        else:
            hist = raiz / "historico.csv"
            campos = ["campana", "tipo", "zona_o_propiedad", "inicio", "fin", "dias", "gasto_usd", "impresiones", "alcance",
                      "cpm_usd", "ctr_enlace_pct", "resultados", "costo_resultado_usd", "leads_registrados", "calificados",
                      "costo_calificado_usd", "avance", "costo_avance_usd", "cierres", "costo_cierre_usd",
                      "publico_advantage", "notas"]
            avance = dict(etapas).get("Tasaciones" if tipo == "captacion" else "Visitas") if etapas else None
            cierres = dict(etapas).get("Captaciones" if tipo == "captacion" else "Ofertas/reservas") if etapas else None
            r2 = lambda v: "" if v is None else round(v, 2)
            fila = {
                "campana": nombre_meta or camp.get("id", carpeta.name), "tipo": tipo,
                "zona_o_propiedad": camp.get("propiedad") or camp.get("zona", ""),
                "inicio": inicio.isoformat() if inicio else "", "fin": hoy.isoformat(), "dias": dias or "",
                "gasto_usd": r2(t["gasto"]), "impresiones": r2(t["impresiones"]), "alcance": r2(t["alcance"]),
                "cpm_usd": r2(t["cpm"]), "ctr_enlace_pct": r2(t["ctr"]), "resultados": r2(t["resultados"]),
                "costo_resultado_usd": r2(t["cpr"]), "leads_registrados": len(leads) if leads else "",
                "calificados": "" if calificados is None else calificados, "costo_calificado_usd": r2(costo_calif),
                "avance": "" if avance is None else avance, "costo_avance_usd": r2(div(t["gasto"], avance)) if avance else "",
                "cierres": "" if cierres is None else cierres, "costo_cierre_usd": r2(div(t["gasto"], cierres)) if cierres else "",
                "publico_advantage": ";".join(str(c.get("publico_advantage")) for c in camp.get("conjuntos", [])),
                "notas": "",
            }
            nuevo = not hist.exists() or hist.stat().st_size == 0
            with hist.open("a", newline="", encoding="utf-8") as fh:
                w = csv.DictWriter(fh, fieldnames=campos)
                if nuevo:
                    w.writeheader()
                w.writerow(fila)
            print(f"→ Fila agregada a {hist}")
        camp["estado"] = "cerrada"
        camp.setdefault("fechas", {})["fin_real"] = hoy.isoformat()
        cj.write_text(json.dumps(camp, ensure_ascii=False, indent=2), encoding="utf-8")
        print("→ campana.json marcado como cerrado. Falta anotar lo aprendido en aprendizajes.md.")


if __name__ == "__main__":
    main()
