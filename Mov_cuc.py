"""
=============================================================
  SISTEMA INTELIGENTE DE RUTAS - BUSES URBANOS CÚCUTA
 
 #Basado en: Representación del conocimiento con reglas lógicas
 #Búsqueda heurística A*
=============================================================
  Sistema de transporte cubierto:
    - Ruta 1  : Terminal ↔ Aeropuerto  (corredor principal)
    - Ruta 2  : Villa del Rosario ↔ Los Patios
    - Ruta 3  : Atalaya ↔ El Zulia
    - Ruta 4  : Circular Centro
    - Ruta 5  : Corredor Sur (Villa del Rosario ↔ Atalaya)
    - Ruta 6  : Corredor Universidades
    - Ruta 7  : Los Patios ↔ Aeropuerto
    - Ruta 8  : Centro ↔ La Parada (frontera)

    #SE SACAN LAS ZONAS COMUNES DE LA CIUDA DEBIDO A QUE LA CIUDAD CUENTA CON SISTEMA DE TRANSPORTE PUBLICO COMUN.
"""

import heapq
import math


# ================================================================
#  PARTE 1: BASE DE HECHOS
#  Coordenadas reales aproximadas (latitud, longitud)
# ================================================================

ESTACIONES = {

    # ── CENTRO HISTÓRICO ────────────────────────────────────────
    "Parque Santander":         (7.8931,  -72.5059),   # Corazón del centro
    "Parque Los Libertadores":  (7.8945,  -72.5043),
    "Catedral San José":        (7.8939,  -72.5051),
    "Palacio Municipal":        (7.8952,  -72.5038),
    "Calle 10 con Av. 0":       (7.8918,  -72.5067),
    "Mercado San Mateo":        (7.8967,  -72.5023),

    # ── TERMINAL Y ACCESOS ───────────────────────────────────────
    "Terminal de Transporte":   (7.8734,  -72.5189),
    "Entrada Terminal":         (7.8745,  -72.5178),

    # ── AEROPUERTO ───────────────────────────────────────────────
    "Aeropuerto Camilo Daza":   (7.9276,  -72.5115),
    "Acceso Aeropuerto":        (7.9261,  -72.5123),

    # ── ZONA NORTE ───────────────────────────────────────────────
    "Los Patios":               (7.9345,  -72.5234),
    "Centro Los Patios":        (7.9312,  -72.5212),
    "La Garita":                (7.9189,  -72.5156),
    "Nuevo Horizonte":          (7.9123,  -72.5134),
    "Villa Camila":             (7.9056,  -72.5112),
    "El Zulia":                 (7.9512,  -72.5678),
    "Atalaya Norte":            (7.9089,  -72.4978),

    # ── ZONA SUR (Villa del Rosario / Frontera) ──────────────────
    "Villa del Rosario":        (7.8345,  -72.4734),
    "Centro Villa del Rosario": (7.8367,  -72.4756),
    "La Parada":                (7.8289,  -72.4623),   # Frontera Venezuela
    "Puente Internacional":     (7.8256,  -72.4589),
    "San Faustino":             (7.8412,  -72.4812),
    "Puerto Santander":         (7.7989,  -72.4412),

    # ── ZONA OCCIDENTE ───────────────────────────────────────────
    "Atalaya":                  (7.8823,  -72.5345),
    "Barrio Antonia Santos":    (7.8867,  -72.5289),
    "Comuneros":                (7.8912,  -72.5234),
    "La Libertad":              (7.8845,  -72.5312),
    "Quinta Orientales":        (7.8978,  -72.5178),

    # ── ZONA ORIENTE ────────────────────────────────────────────
    "San Luis":                 (7.8989,  -72.4912),
    "Cúcuta Norte":             (7.9034,  -72.4867),
    "La Playa":                 (7.8901,  -72.4989),
    "El Llano":                 (7.8856,  -72.5023),

    # ── CENTROS COMERCIALES / REFERENCIA ────────────────────────
    "Unicentro Cúcuta":         (7.9023,  -72.5089),
    "Ventura Plaza":            (7.8978,  -72.5134),
    "Centro Comercial Alejandría": (7.8856, -72.5167),

    # ── UNIVERSIDADES ────────────────────────────────────────────
    "UFPS (Univ. Francisco de Paula Santander)": (7.9078, -72.5023),
    "Universidad Libre":        (7.8934,  -72.4978),
    "UNAD Cúcuta":              (7.8912,  -72.5056),
    "UCC Cúcuta":               (7.8867,  -72.5089),

    # ── HOSPITALES / SERVICIOS ───────────────────────────────────
    "Hospital Erasmo Meoz":     (7.9001,  -72.5045),
    "Clínica Norte":            (7.9056,  -72.4989),
    "Bomba de Gasolina Av. 0":  (7.8923,  -72.5112),

    # ── BARRIOS RESIDENCIALES IMPORTANTES ───────────────────────
    "San José":                 (7.8812,  -72.5078),
    "Caobos":                   (7.8878,  -72.5156),
    "Chapinero":                (7.8934,  -72.5223),
    "El Progreso":              (7.9012,  -72.5167),
    "Belén":                    (7.8756,  -72.5089),
    "Primero de Mayo":          (7.8801,  -72.5134),
}

# Conexiones: (parada_A, parada_B, minutos, ruta)
CONEXIONES = [

    # ── RUTA 1: Terminal ↔ Centro ↔ Aeropuerto (corredor principal Av. 0) ──
    ("Terminal de Transporte",  "Entrada Terminal",         3,  "Ruta-1"),
    ("Entrada Terminal",        "Belén",                    5,  "Ruta-1"),
    ("Belén",                   "Primero de Mayo",          4,  "Ruta-1"),
    ("Primero de Mayo",         "San José",                 4,  "Ruta-1"),
    ("San José",                "Bomba de Gasolina Av. 0",  3,  "Ruta-1"),
    ("Bomba de Gasolina Av. 0", "Calle 10 con Av. 0",       3,  "Ruta-1"),
    ("Calle 10 con Av. 0",      "Parque Santander",         3,  "Ruta-1"),
    ("Parque Santander",        "Parque Los Libertadores",  2,  "Ruta-1"),
    ("Parque Los Libertadores", "Quinta Orientales",        4,  "Ruta-1"),
    ("Quinta Orientales",       "Ventura Plaza",            3,  "Ruta-1"),
    ("Ventura Plaza",           "Unicentro Cúcuta",         3,  "Ruta-1"),
    ("Unicentro Cúcuta",        "Hospital Erasmo Meoz",     4,  "Ruta-1"),
    ("Hospital Erasmo Meoz",    "El Progreso",              3,  "Ruta-1"),
    ("El Progreso",             "Nuevo Horizonte",          5,  "Ruta-1"),
    ("Nuevo Horizonte",         "Acceso Aeropuerto",        5,  "Ruta-1"),
    ("Acceso Aeropuerto",       "Aeropuerto Camilo Daza",   3,  "Ruta-1"),

    # ── RUTA 2: Villa del Rosario ↔ Centro ↔ Los Patios ───────────────────
    ("Villa del Rosario",       "Centro Villa del Rosario", 3,  "Ruta-2"),
    ("Centro Villa del Rosario","San Faustino",             5,  "Ruta-2"),
    ("San Faustino",            "Terminal de Transporte",   8,  "Ruta-2"),
    ("Terminal de Transporte",  "Caobos",                   5,  "Ruta-2"),
    ("Caobos",                  "Palacio Municipal",        4,  "Ruta-2"),
    ("Palacio Municipal",       "Catedral San José",        2,  "Ruta-2"),
    ("Catedral San José",       "Mercado San Mateo",        3,  "Ruta-2"),
    ("Mercado San Mateo",       "UFPS (Univ. Francisco de Paula Santander)", 5, "Ruta-2"),
    ("UFPS (Univ. Francisco de Paula Santander)", "La Garita", 5, "Ruta-2"),
    ("La Garita",               "Centro Los Patios",        5,  "Ruta-2"),
    ("Centro Los Patios",       "Los Patios",               3,  "Ruta-2"),

    # ── RUTA 3: Atalaya ↔ Centro ↔ El Zulia ───────────────────────────────
    ("Atalaya",                 "La Libertad",              4,  "Ruta-3"),
    ("La Libertad",             "Barrio Antonia Santos",    3,  "Ruta-3"),
    ("Barrio Antonia Santos",   "Comuneros",                3,  "Ruta-3"),
    ("Comuneros",               "Chapinero",                3,  "Ruta-3"),
    ("Chapinero",               "Parque Santander",         4,  "Ruta-3"),
    ("Parque Santander",        "Cúcuta Norte",             6,  "Ruta-3"),
    ("Cúcuta Norte",            "Atalaya Norte",            5,  "Ruta-3"),
    ("Atalaya Norte",           "El Zulia",                10,  "Ruta-3"),

    # ── RUTA 4: Circular Centro ────────────────────────────────────────────
    ("Parque Santander",        "Catedral San José",        3,  "Ruta-4"),
    ("Catedral San José",       "Palacio Municipal",        2,  "Ruta-4"),
    ("Palacio Municipal",       "El Llano",                 4,  "Ruta-4"),
    ("El Llano",                "Centro Comercial Alejandría", 3, "Ruta-4"),
    ("Centro Comercial Alejandría", "UCC Cúcuta",           3,  "Ruta-4"),
    ("UCC Cúcuta",              "UNAD Cúcuta",              3,  "Ruta-4"),
    ("UNAD Cúcuta",             "Parque Los Libertadores",  4,  "Ruta-4"),
    ("Parque Los Libertadores", "Parque Santander",         2,  "Ruta-4"),

    # ── RUTA 5: Corredor Sur (Villa del Rosario ↔ Atalaya) ────────────────
    ("Villa del Rosario",       "La Parada",                5,  "Ruta-5"),
    ("La Parada",               "Puente Internacional",     3,  "Ruta-5"),
    ("Villa del Rosario",       "Belén",                   10,  "Ruta-5"),
    ("Belén",                   "Atalaya",                  6,  "Ruta-5"),
    ("Atalaya",                 "Comuneros",                4,  "Ruta-5"),
    ("Comuneros",               "San José",                 5,  "Ruta-5"),

    # ── RUTA 6: Corredor Universidades ────────────────────────────────────
    ("Terminal de Transporte",  "UCC Cúcuta",               8,  "Ruta-6"),
    ("UCC Cúcuta",              "Universidad Libre",        4,  "Ruta-6"),
    ("Universidad Libre",       "La Playa",                 3,  "Ruta-6"),
    ("La Playa",                "San Luis",                 4,  "Ruta-6"),
    ("San Luis",                "Clínica Norte",            4,  "Ruta-6"),
    ("Clínica Norte",           "UFPS (Univ. Francisco de Paula Santander)", 5, "Ruta-6"),
    ("UFPS (Univ. Francisco de Paula Santander)", "Villa Camila", 5, "Ruta-6"),

    # ── RUTA 7: Los Patios ↔ Aeropuerto ──────────────────────────────────
    ("Los Patios",              "Centro Los Patios",        3,  "Ruta-7"),
    ("Centro Los Patios",       "Aeropuerto Camilo Daza",   8,  "Ruta-7"),
    ("Aeropuerto Camilo Daza",  "Villa Camila",             5,  "Ruta-7"),
    ("Villa Camila",            "Nuevo Horizonte",          5,  "Ruta-7"),

    # ── RUTA 8: Centro ↔ La Parada (frontera Venezuela) ──────────────────
    ("Parque Santander",        "Terminal de Transporte",   8,  "Ruta-8"),
    ("Terminal de Transporte",  "San Faustino",             6,  "Ruta-8"),
    ("San Faustino",            "La Parada",                7,  "Ruta-8"),
    ("La Parada",               "Puerto Santander",        20,  "Ruta-8"),
]

MODO = {
    "Ruta-1": "🚌 Bus Av. 0 (Terminal-Aeropuerto)",
    "Ruta-2": "🚌 Bus Norte-Sur (Villa Rosario-Los Patios)",
    "Ruta-3": "🚌 Bus Atalaya-El Zulia",
    "Ruta-4": "🚌 Bus Circular Centro",
    "Ruta-5": "🚌 Bus Corredor Sur",
    "Ruta-6": "🚌 Bus Universidades",
    "Ruta-7": "🚌 Bus Los Patios-Aeropuerto",
    "Ruta-8": "🚌 Bus Centro-Frontera",
    "Inicio": "📍 Inicio",
}


# ================================================================
#  PARTE 2: BASE DE REGLAS LÓGICAS
# ================================================================

class BaseDeReglas:
    """
    Reglas lógicas del sistema experto de transporte de Cúcuta.

    REGLA 1 – Bidireccionalidad:
        ∀A,B: conexion(A,B,c,r) → puede_ir(A,B,c) ∧ puede_ir(B,A,c)

    REGLA 2 – Accesibilidad transitiva:
        ∀A,B: accesible(A) ∧ puede_ir(A,B) → accesible(B)

    REGLA 3 – Transbordo (cambio de ruta):
        ∀r1,r2: viajando(r1) ∧ siguiente(r2) ∧ r1≠r2 → transbordo()

    REGLA 4 – Zona fronteriza:
        ∀p: parada_en({La Parada, Puente Internacional, Puerto Santander})
            → zona_fronteriza(p) ∧ requiere_documento()

    REGLA 5 – Validación de parada:
        ∀X: existe(X) → válido(X)
        ∀X: ¬existe(X) → error(X)
    """

    ZONAS_FRONTERIZAS = {"La Parada", "Puente Internacional", "Puerto Santander"}

    def __init__(self):
        self.grafo  = {}
        self.hechos = set()
        self._construir_grafo()

    def _construir_grafo(self):
        """Aplica REGLA 1: construye el grafo bidireccional."""
        for est in ESTACIONES:
            self.grafo[est] = []
            self.hechos.add(f"existe_parada({est})")

        for orig, dest, costo, ruta in CONEXIONES:
            self.grafo.setdefault(orig, []).append((dest, costo, ruta))
            self.grafo.setdefault(dest, []).append((orig, costo, ruta))
            self.hechos.add(f"conectado({orig},{dest},costo={costo},ruta={ruta})")
            self.hechos.add(f"conectado({dest},{orig},costo={costo},ruta={ruta})")

    def aplicar_regla_accesibilidad(self, inicio):        # REGLA 2
        visitados, cola = {inicio}, [inicio]
        while cola:
            actual = cola.pop(0)
            for vecino, _, _ in self.grafo.get(actual, []):
                if vecino not in visitados:
                    visitados.add(vecino); cola.append(vecino)
        return visitados

    def aplicar_regla_transbordo(self, ruta_a, ruta_b):   # REGLA 3
        return ruta_a not in ("Inicio", ruta_b)

    def es_zona_fronteriza(self, parada):                  # REGLA 4
        return parada in self.ZONAS_FRONTERIZAS

    def verificar_existencia(self, parada):                # REGLA 5
        return f"existe_parada({parada})" in self.hechos

    def obtener_vecinos(self, parada):
        return self.grafo.get(parada, [])


# ================================================================
#  PARTE 3: MOTOR DE INFERENCIA A*
# ================================================================

class MotorDeInferencia:

    def __init__(self, base_reglas):
        self.reglas = base_reglas

    def heuristica(self, actual, destino):
        """
        h(n) = distancia_euclídea(actual, destino) × 120
        Convierte grados geográficos a minutos estimados de bus.
        Es admisible: nunca sobreestima el tiempo real.
        """
        lat1, lon1 = ESTACIONES[actual]
        lat2, lon2 = ESTACIONES[destino]
        return math.sqrt((lat1 - lat2)**2 + (lon1 - lon2)**2) * 120

    def buscar_ruta_optima(self, inicio, destino):
        encabezado("MOTOR DE INFERENCIA A*", f"{inicio}  →  {destino}")

        # Regla 5: validar paradas
        for p in (inicio, destino):
            if not self.reglas.verificar_existencia(p):
                print(f"  ✗ '{p}' no existe en la base de hechos.")
                return None

        # Regla 2: verificar accesibilidad
        if destino not in self.reglas.aplicar_regla_accesibilidad(inicio):
            print(f"  ✗ No hay ruta entre '{inicio}' y '{destino}'.")
            return None

        if inicio == destino:
            print("  ✓ Ya estás en el destino.")
            return {"camino": [(inicio, "Inicio")], "costo_total": 0,
                    "transbordos": [], "rutas_usadas": []}

        h0   = self.heuristica(inicio, destino)
        cola = [(h0, 0, inicio, [(inicio, "Inicio")])]
        visitados = {}
        iteracion = 0

        print(f"  h({inicio}) estimado = {h0:.1f} min\n")
        print(f"  {'Iter':>4}  {'Parada':<40}  {'g':>5}  {'h':>5}  {'f':>5}")
        print(f"  {'-'*65}")

        while cola:
            f, g, actual, camino = heapq.heappop(cola)
            iteracion += 1
            h = self.heuristica(actual, destino)
            print(f"  {iteracion:>4}  {actual:<40}  {g:>5.1f}  {h:>5.1f}  {f:>5.1f}")

            if actual == destino:
                print(f"\n  ✓ Destino alcanzado en {iteracion} iteraciones.")
                return self._resultado(camino, g)

            if visitados.get(actual, float("inf")) <= g:
                continue
            visitados[actual] = g

            for vecino, costo, ruta in self.reglas.obtener_vecinos(actual):
                g_nuevo = g + costo
                if g_nuevo < visitados.get(vecino, float("inf")):
                    f_nuevo = g_nuevo + self.heuristica(vecino, destino)
                    heapq.heappush(cola, (f_nuevo, g_nuevo, vecino, camino + [(vecino, ruta)]))

        print("  ✗ No se encontró ruta.")
        return None

    def _resultado(self, camino, costo_total):
        transbordos, rutas = [], []
        linea_ant = None
        for i, (est, ruta) in enumerate(camino):
            if i > 0:
                if self.reglas.aplicar_regla_transbordo(linea_ant, ruta):
                    transbordos.append((est, ruta))
                if ruta not in rutas and ruta != "Inicio":
                    rutas.append(ruta)
            linea_ant = ruta
        return {"camino": camino, "costo_total": costo_total,
                "transbordos": transbordos, "rutas_usadas": rutas}


# ================================================================
#  PARTE 4: PRESENTACIÓN DE RESULTADOS
# ================================================================

def encabezado(titulo, subtitulo=""):
    print(f"\n{'═'*65}")
    print(f"  {titulo}")
    if subtitulo:
        print(f"  {subtitulo}")
    print(f"{'═'*65}")

def mostrar_resultado(resultado, inicio, destino, base):
    if not resultado:
        print("\n  No se pudo calcular la ruta.")
        return

    camino      = resultado["camino"]
    costo       = resultado["costo_total"]
    transbordos = resultado["transbordos"]
    rutas       = resultado["rutas_usadas"]

    encabezado("RUTA ÓPTIMA ENCONTRADA")
    print(f"\n  🏁 {inicio}  →  {destino}")
    print(f"  ⏱  Tiempo estimado : {costo} min")
    print(f"  📍 Paradas         : {len(camino) - 1}")
    print(f"  🔄 Transbordos     : {len(transbordos)}")
    if rutas:
        print(f"  🚌 Rutas usadas    : {', '.join(rutas)}")

    # Advertencia zona fronteriza (Regla 4)
    fronterizas = [e for e, _ in camino if base.es_zona_fronteriza(e)]
    if fronterizas:
        print(f"\n  ⚠️  AVISO (Regla 4 – Zona Fronteriza):")
        for f in fronterizas:
            print(f"     La parada '{f}' está en zona fronteriza.")
        print(f"     → Recuerde llevar documento de identidad vigente.")

    print(f"\n  {'─'*62}")
    print(f"  {'':3}  {'Parada':<38}  {'Transporte'}")
    print(f"  {'─'*62}")

    transbordo_ests = {e for e, _ in transbordos}
    for i, (est, ruta) in enumerate(camino):
        icono = MODO.get(ruta, ruta)
        if i == 0:
            marca = "🟢 ORIGEN "
        elif i == len(camino) - 1:
            marca = "🔴 DESTINO"
        elif est in transbordo_ests:
            marca = "🔄 TRANSB. "
        elif base.es_zona_fronteriza(est):
            marca = "⚠️  FRONTER."
        else:
            marca = f"   {i:2d}.    "
        print(f"  {marca}  {est:<38}  {icono}")

    # Instrucciones paso a paso
    print(f"\n  INSTRUCCIONES DE VIAJE:")
    print(f"  {'─'*62}")
    ruta_act, tramo_inicio = None, camino[0][0]
    for i, (est, ruta) in enumerate(camino):
        if ruta == "Inicio":
            continue
        if ruta != ruta_act:
            if ruta_act:
                print(f"  • Aborda {MODO.get(ruta_act, ruta_act)}")
                print(f"    desde '{tramo_inicio}' hasta '{camino[i-1][0]}'")
                print(f"    ↳ Transbordo en '{est}' → {MODO.get(ruta, ruta)}")
            ruta_act = ruta
            tramo_inicio = camino[i-1][0] if i > 0 else est
    if ruta_act:
        print(f"  • Aborda {MODO.get(ruta_act, ruta_act)}")
        print(f"    desde '{tramo_inicio}' hasta '{camino[-1][0]}'")
    print(f"  ✅ ¡Has llegado a '{destino}'!")

    # Hechos derivados
    print(f"\n  HECHOS DERIVADOS (base de conocimiento):")
    print(f"  - ruta_optima({inicio}, {destino}) = {costo} min")
    print(f"  - num_transbordos = {len(transbordos)}")
    for est, r in transbordos:
        print(f"  - transbordo_en({est}, {r}) = verdadero")
    for f in fronterizas:
        print(f"  - zona_fronteriza({f}) = verdadero")

def listar_paradas(base):
    encabezado("PARADAS DISPONIBLES", f"{len(ESTACIONES)} paradas en la base de hechos")
    agrupadas = {}
    for orig, dest, _, ruta in CONEXIONES:
        agrupadas.setdefault(ruta, set()).update([orig, dest])
    for ruta in sorted(agrupadas):
        print(f"\n  {MODO.get(ruta, ruta)}  [{ruta}]")
        for est in sorted(agrupadas[ruta]):
            conn = len(base.obtener_vecinos(est))
            frontera = "  ⚠️ Zona fronteriza" if base.es_zona_fronteriza(est) else ""
            print(f"    • {est:<45} ({conn} conexiones){frontera}")

def mostrar_reglas():
    encabezado("BASE DE REGLAS LÓGICAS")
    print("""
  REGLA 1 – BIDIRECCIONALIDAD:
    SI conexion(A, B, costo, ruta)
    ENTONCES puede_ir(A→B, costo) ∧ puede_ir(B→A, costo)

  REGLA 2 – ACCESIBILIDAD TRANSITIVA:
    SI accesible(A) ∧ puede_ir(A, B)
    ENTONCES accesible(B)

  REGLA 3 – TRANSBORDO (cambio de bus):
    SI viajando_en(R1) ∧ siguiente_ruta(R2) ∧ R1 ≠ R2
    ENTONCES requiere_transbordo(verdadero)

  REGLA 4 – ZONA FRONTERIZA:
    SI parada ∈ {La Parada, Puente Internacional, Puerto Santander}
    ENTONCES zona_fronteriza(parada) ∧ requiere_documento(cédula)

  REGLA 5 – VALIDACIÓN DE PARADA:
    SI existe_parada(X)  → válido(X)
    SI ¬existe_parada(X) → error_parada(X)

  HEURÍSTICA A*:
    h(n) = distancia_euclídea(n, destino) × 120
    g(n) = tiempo acumulado real desde el inicio (minutos)
    f(n) = g(n) + h(n)  ← función de evaluación total
    """)

def menu(base, motor):
    encabezado(
        "SISTEMA INTELIGENTE DE RUTAS  –  CÚCUTA, N. de S.",
        "Buses Urbanos  |  Motor de Inferencia A*  |  Base de Conocimiento"
    )
    while True:
        print("\n  MENÚ:")
        print("  1. Buscar ruta óptima entre dos paradas")
        print("  2. Ver paradas por ruta")
        print("  3. Ver base de reglas lógicas")
        print("  4. Ejecutar ejemplos automáticos")
        print("  5. Salir")
        op = input("\n  Opción (1-5): ").strip()

        if op == "1":
            listar_paradas(base)
            print("\n  Escriba los nombres exactamente como aparecen arriba.")
            org = input("\n  Parada ORIGEN:  ").strip()
            dst = input("  Parada DESTINO: ").strip()
            resultado = motor.buscar_ruta_optima(org, dst)
            mostrar_resultado(resultado, org, dst, base)

        elif op == "2":
            listar_paradas(base)

        elif op == "3":
            mostrar_reglas()

        elif op == "4":
            ejemplos = [
                ("Terminal de Transporte",  "Aeropuerto Camilo Daza",
                 "Terminal → Aeropuerto  (Ruta directa Av. 0)"),
                ("Villa del Rosario",       "Los Patios",
                 "Sur a Norte cruzando el centro"),
                ("Atalaya",                 "UFPS (Univ. Francisco de Paula Santander)",
                 "Barrio occidental → Universidad"),
                ("Terminal de Transporte",  "La Parada",
                 "Terminal → Frontera con Venezuela  (Regla 4 activa)"),
                ("Los Patios",              "UCC Cúcuta",
                 "Norte → Universidad  (múltiples transbordos)"),
            ]
            for org, dst, desc in ejemplos:
                print(f"\n  ══  EJEMPLO: {desc}  ══")
                resultado = motor.buscar_ruta_optima(org, dst)
                mostrar_resultado(resultado, org, dst, base)
                input("\n  [ENTER para continuar...]")

        elif op == "5":
            print("\n  ¡Hasta pronto!  🚌\n")
            break
        else:
            print("  Opción no válida.")


# ================================================================
#  INICIO DEL PROGRAMA
# ================================================================

if __name__ == "__main__":
    print("\n  Iniciando sistema inteligente...")
    base  = BaseDeReglas()
    motor = MotorDeInferencia(base)

    print(f"  ✓ Paradas en base de hechos    : {len(ESTACIONES)}")
    print(f"  ✓ Conexiones (bidireccionales) : {len(CONEXIONES) * 2}")
    print(f"  ✓ Hechos derivados totales     : {len(base.hechos)}")
    print(f"  ✓ Rutas modeladas              : 8")
    print(f"  ✓ Paradas fronterizas (Regla 4): {len(BaseDeReglas.ZONAS_FRONTERIZAS)}")
    print(f"  ✓ Motor de inferencia A*       : listo")

    menu(base, motor)