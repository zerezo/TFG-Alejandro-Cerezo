import json
import os
import sys
import datetime 
import uuid 

# --- CONFIGURACIÓN DE CONSOLA PARA WINDOWS (EVITA ERRORES DE CODIFICACIÓN) ---
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

self_path = os.path.dirname(os.path.abspath(__file__))
from contextlib import contextmanager
from owlready2 import *
from fpdf import FPDF

# ==========================================
# CONFIGURACIÓN ESTÉTICA Y RUTAS (IDÉNTICO A V3)
# ==========================================
NOMBRE_ARCHIVO_OWL = "Ontologia_31012026.rdf"
NOMBRE_ARCHIVO_JSON = "mision.json"
VERSION_SISTEMA = "4.0 Final (V3 PDF + V4 OWL Core)"

COLOR_NAVY = (44, 62, 80)
COLOR_WHITE = (255, 255, 255)
COLOR_ACCENT = (52, 152, 219)
COLOR_TEXT_BASE = (44, 62, 80)
COLOR_TEXT_SUBTLE = (100, 100, 100)
COLOR_CRIT_5 = (192, 57, 43)   # Rojo
COLOR_WARNING = (243, 156, 18) # Ámbar
COLOR_SUCCESS = (39, 174, 96)  # Verde

# ==========================================
# UTILIDADES DE TEXTO Y LOGS (IDÉNTICO A V3)
# ==========================================
@contextmanager
def silenciar_output_librerias():
    with open(os.devnull, "w") as devnull:
        old_out, old_err = sys.stdout, sys.stderr
        sys.stdout, sys.stderr = devnull, devnull
        try: yield
        finally: sys.stdout, sys.stderr = old_out, old_err

def clean_text(text):
    return str(text).encode('latin-1', 'replace').decode('latin-1')

def sanitize_filename(text):
    return "".join([c for c in text.replace(" ", "_") if c.isalnum() or c in ('_', '-')])

def get_color_by_level(level):
    if level >= 5: return COLOR_CRIT_5
    if level == 4: return (211, 84, 0)
    if level == 3: return COLOR_WARNING
    if level == 2: return COLOR_SUCCESS
    return (22, 160, 133)

# =================================================================
# CLASE PDF: MOTOR DE GENERACIÓN V3.0 FINAL (EXTRAÍDA LITERALMENTE)
# =================================================================
class MissionReportPDF(FPDF):
    def __init__(self, data_mision, resultados, system_info):
        super().__init__()
        self.data_mision = data_mision
        self.res = resultados
        self.config = data_mision.get('configuracion_mision', {})
        self.system_info = system_info
        self.set_margins(20, 20, 20)
        self.set_auto_page_break(auto=True, margin=25)
        self.toc_entries = []

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(150, 150, 150)
        info = f"Pagina {self.page_no()} | {self.config.get('titulo')} | Ref: {self.system_info['report_id'][:8]} | Datos Inferidos por OWL"
        self.cell(0, 10, clean_text(info), 0, 0, 'C')

    def add_toc_entry(self, title):
        self.toc_entries.append((title, self.page_no()))

    def crear_portada(self):
        self.add_page()
        self.set_fill_color(*COLOR_NAVY)
        self.rect(0, 0, 210, 115, 'F') 
        self.set_y(45)
        self.set_font('Arial', 'B', 28)
        self.set_text_color(*COLOR_WHITE)
        self.multi_cell(0, 12, clean_text("SIMULADOR DE OPERACIONES\nMULTIDOMINIO (MDO)"), 0, 'C')
        self.set_fill_color(*COLOR_ACCENT)
        self.rect(75, 85, 60, 1.5, 'F')
        self.set_y(95)
        self.set_font('Arial', '', 11)
        subt = f"Version Final {self.system_info['version']} | Marco de Riesgos NIST\nMotor de Razonamiento Semantico"
        self.multi_cell(0, 7, clean_text(subt), 0, 'C')
        self.set_y(220)
        self.set_text_color(*COLOR_NAVY)
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, "INFORME TECNICO DE EVALUACION ESTRATEGICA", 0, 1, 'C')
        self.ln(10)
        self.set_font('Arial', '', 10)
        self.set_text_color(*COLOR_TEXT_SUBTLE)
        x_start = 65
        self.set_x(x_start)
        self.cell(40, 6, "INVESTIGADOR:", 0, 0)
        self.set_font('Arial', 'B', 10)
        self.cell(0, 6, clean_text(self.system_info['autor']), 0, 1)
        self.set_x(x_start)
        self.set_font('Arial', '', 10)
        self.cell(40, 6, "PROYECTO:", 0, 0)
        self.cell(0, 6, "Trabajo Fin de Grado (Ing. Telecomunicaciones)", 0, 1)
        self.set_x(x_start)
        self.cell(40, 6, "MISION:", 0, 0)
        self.cell(0, 6, clean_text(self.config.get('titulo')), 0, 1)
        self.set_x(x_start)
        self.cell(40, 6, "FECHA:", 0, 0)
        self.cell(0, 6, self.system_info['fecha'], 0, 1)

    def crear_indice(self, toc_data):
        self.add_page()
        self.set_y(30)
        self.set_font('Arial', 'B', 18)
        self.set_text_color(*COLOR_NAVY)
        self.cell(0, 10, clean_text("INDICE DINAMICO DE CONTENIDOS"), 0, 1, 'L')
        self.ln(15)
        for texto, pag in toc_data:
            y = self.get_y()
            self.set_fill_color(*COLOR_ACCENT)
            self.rect(20, y+1.5, 3, 5, 'F')
            self.set_x(30)
            self.set_font('Arial', '', 12)
            self.set_text_color(*COLOR_TEXT_BASE)
            self.cell(140, 8, clean_text(texto), 0, 0)
            self.set_font('Arial', 'B', 12)
            self.cell(0, 8, str(pag), 0, 1, 'R')
            self.ln(4)

    def crear_presentacion_mision(self, is_dummy=False):
        self.add_page()
        if is_dummy: self.add_toc_entry("1. Contexto Estrategico y Matriz de Criticidad")
        self.set_font('Arial', 'B', 14)
        self.set_text_color(*COLOR_NAVY)
        self.cell(0, 10, clean_text("1. CONTEXTO ESTRATEGICO"), "B", 1, 'L')
        self.ln(5)
        self.set_font('Arial', '', 10)
        self.set_text_color(60, 60, 60)
        self.set_fill_color(248, 249, 251)
        self.multi_cell(0, 6, clean_text(self.config.get('descripcion', '')), 0, 'J', fill=True)
        self.ln(15)
        self.set_font('Arial', 'B', 14)
        self.set_text_color(*COLOR_NAVY)
        self.cell(0, 10, clean_text("1.1 MATRIZ DE PRIORIDADES POR DOMINIO"), 0, 1, 'L')
        self.ln(8)
        crit_data = self.config.get('niveles_criticidad', {})
        for dom, nivel in crit_data.items():
            self.set_x(25)
            self.set_font('Arial', 'B', 10)
            self.set_text_color(*COLOR_TEXT_BASE)
            self.cell(45, 8, clean_text(dom.upper()), 0, 0)
            x, y = self.get_x(), self.get_y() + 2
            self.set_fill_color(235, 237, 240)
            self.rect(x, y, 80, 4, 'F')
            self.set_fill_color(*get_color_by_level(nivel))
            self.rect(x, y, (nivel / 5) * 80, 4, 'F')
            self.set_xy(x + 85, y - 2)
            self.set_font('Arial', 'I', 9)
            self.set_text_color(*COLOR_TEXT_SUBTLE)
            self.cell(20, 8, f"Prioridad {nivel}/5", 0, 1)
            self.ln(3)

    def crear_inventario(self, is_dummy=False):
        self.add_page()
        if is_dummy: self.add_toc_entry("2. Orden de Batalla (Inventario Tactico)")
        self.set_font('Arial', 'B', 14)
        self.set_text_color(*COLOR_NAVY)
        self.cell(0, 10, clean_text("2. ORDEN DE BATALLA (INVENTARIO MDO)"), "B", 1, 'L')
        self.ln(5)
        activos_por_dominio = {}
        for act in self.data_mision.get('activos', []):
            dom = act.get('dominio', 'Desconocido')
            if dom not in activos_por_dominio: activos_por_dominio[dom] = []
            activos_por_dominio[dom].append(act)
        for dom, lista in activos_por_dominio.items():
            self.set_fill_color(*COLOR_NAVY)
            self.set_text_color(*COLOR_WHITE)
            self.set_font('Arial', 'B', 10)
            self.cell(0, 8, clean_text(f"   DOMINIO: {dom.upper()}"), 1, 1, 'L', True)
            self.set_fill_color(248, 249, 251) 
            for idx, act in enumerate(lista):
                borde = 'LBR' if idx == len(lista) - 1 else 'LR'
                self.set_text_color(50, 50, 50)
                self.set_font('Arial', 'B', 9)
                self.cell(100, 7, clean_text(f"   {act['id']}"), borde[0:2], 0, 'L', True)
                self.set_text_color(120, 120, 120)
                self.set_font('Arial', '', 9)
                self.cell(0, 7, clean_text(f"Tipo: {act['tipo']}   "), borde[2:] if len(borde)>2 else borde[1:], 1, 'R', True)
            self.ln(5) 
        self.ln(5)
        amenazas = self.data_mision.get('amenazas', [])
        if amenazas:
            self.set_font('Arial', 'B', 12); self.set_text_color(*COLOR_CRIT_5)
            self.cell(0, 8, clean_text("2.1 VECTORES DE AMENAZA IDENTIFICADOS"), 0, 1, 'L'); self.ln(2)
            self.set_fill_color(*COLOR_CRIT_5); self.set_text_color(*COLOR_WHITE)
            self.set_font('Arial', 'B', 10); self.cell(0, 8, clean_text("   INTELIGENCIA HOSTIL ACTIVA"), 1, 1, 'L', True)
            self.set_fill_color(253, 240, 240) 
            for idx, am in enumerate(amenazas):
                borde = 'LBR' if idx == len(amenazas) - 1 else 'LR'
                self.set_text_color(192, 57, 43); self.set_font('Arial', 'B', 9)
                self.cell(90, 7, clean_text(f"   {am['id']}"), borde[0:2], 0, 'L', True)
                self.set_text_color(150, 100, 100); self.set_font('Arial', '', 9)
                self.cell(0, 7, clean_text(f"Vector: {am['tipo']}   "), borde[2:] if len(borde)>2 else borde[1:], 1, 'R', True)

    def crear_analisis_veredicto(self, is_dummy=False):
        self.add_page()
        if is_dummy: self.add_toc_entry("3. Analisis de Inteligencia y Evaluacion NIST")
        self.set_font('Arial', 'B', 14); self.set_text_color(*COLOR_NAVY)
        self.cell(0, 10, clean_text("3. ANALISIS DE INTELIGENCIA SEMANTICA"), "B", 1, 'L'); self.ln(5)
        ataques = self.res.get('ataques', [])
        if ataques:
            for atq in ataques:
                texto = f"[INFERENCIA] {atq['amenaza']} ➔ Impacta en: {atq['victima']}"
                self.set_font('Arial', 'B', 10); self.set_text_color(*COLOR_CRIT_5)
                self.multi_cell(0, 7, clean_text(texto), 0, 'L'); self.ln(1)
        self.ln(10)
        self.set_font('Arial', 'B', 14); self.set_text_color(*COLOR_NAVY)
        self.cell(0, 10, clean_text("4. EVALUACION DE IMPACTO NIST (ZONAS DE CONTROL)"), "B", 1, 'L'); self.ln(5)
        for dom, stats in self.res['dominios'].items():
            if stats['total'] == 0: continue
            self.set_font('Arial', 'B', 11); self.set_text_color(*COLOR_TEXT_BASE)
            self.cell(50, 8, clean_text(dom.upper()), 0, 0)
            color_est = COLOR_SUCCESS
            if stats['estado'] == "DEGRADADO": color_est = COLOR_WARNING
            if stats['estado'] == "COMPROMETIDO": color_est = COLOR_CRIT_5
            self.set_text_color(*color_est); self.set_font('Arial', 'B', 9)
            self.cell(0, 8, clean_text(f"ESTADO: {stats['estado']} ({stats['afectacion']:.1f}%)"), 0, 1, 'R')
            x, y = self.get_x(), self.get_y()
            self.set_fill_color(240, 240, 240); self.rect(x, y, 170, 6, 'F')
            self.set_fill_color(*color_est); self.rect(x, y, (stats['afectacion'] / 100) * 170, 6, 'F')
            u_max_x = x + (stats['u_max'] / 100) * 170
            u_deg_x = x + ((stats['u_max'] / 2) / 100) * 170
            self.set_fill_color(*COLOR_NAVY)
            if stats['u_max'] < 100: self.rect(u_max_x, y-1, 1, 8, 'F')
            self.set_fill_color(150, 150, 150); self.rect(u_deg_x, y, 0.5, 6, 'F'); self.ln(12)
        if is_dummy: self.add_toc_entry("4. Resolucion y Veredicto Final")
        self.ln(5); self.set_font('Arial', 'B', 14); self.set_text_color(*COLOR_NAVY)
        self.cell(0, 10, clean_text("5. RESOLUCION DE LA MISION"), "B", 1, 'L'); self.ln(5)
        veredicto = self.res['veredicto_mision']
        bg_v, msg = COLOR_SUCCESS, "Mision Exitosa. Impacto asimilado bajo el umbral NIST."
        if veredicto == "FRACASO": bg_v, msg = COLOR_CRIT_5, "Fallo critico en dominios de prioridad maxima."
        if veredicto == "DEGRADADA": bg_v, msg = COLOR_WARNING, "Mision degradada. Capacidades conjuntas comprometidas."
        x_v, y_v = self.get_x(), self.get_y(); self.set_fill_color(*bg_v); self.rect(x_v, y_v, 170, 35, 'F')
        self.set_y(y_v + 8); self.set_text_color(*COLOR_WHITE); self.set_font('Arial', 'B', 20)
        self.cell(0, 10, clean_text(f"ESTADO: MISION {veredicto}"), 0, 1, 'C')
        self.set_font('Arial', '', 11); self.multi_cell(0, 8, clean_text(msg), 0, 'C')

    def crear_pagina_metadatos(self, is_dummy=False):
        self.add_page()
        if is_dummy: self.add_toc_entry("5. Metadatos del Sistema y Telemetria")
        self.set_font('Arial', 'B', 14); self.set_text_color(*COLOR_NAVY)
        self.cell(0, 10, clean_text("5. METADATOS Y TELEMETRIA DE SISTEMA"), "B", 1, 'L'); self.ln(10)
        self.set_fill_color(245, 247, 250); self.rect(20, self.get_y(), 170, 75, 'F')
        self.set_y(self.get_y() + 5); self.set_font('Arial', 'B', 10); self.set_text_color(*COLOR_TEXT_BASE)
        meta = [("ID REPORTE:", self.system_info['report_id']), ("VERSION:", self.system_info['version']), ("MOTOR:", "Owlready2 + HermiT"), ("MARCO:", "NIST SP 800-30")]
        for k, v in meta:
            self.set_x(25); self.cell(50, 8, k, 0, 0); self.set_font('Arial', '', 10); self.cell(0, 8, clean_text(v), 0, 1); self.set_font('Arial', 'B', 10)

    def generar_pasada(self, is_dummy=False, toc_data=None):
        self.crear_portada()
        if not is_dummy and toc_data: self.crear_indice(toc_data)
        elif is_dummy: self.add_page()
        self.crear_presentacion_mision(is_dummy); self.crear_inventario(is_dummy)
        self.crear_analisis_veredicto(is_dummy); self.crear_pagina_metadatos(is_dummy)


# ==========================================
# MOTOR PRINCIPAL (THE SEMANTIC LOOP V4.0)
# ==========================================
print(f"\n[+] INICIANDO SISTEMA MDO V{VERSION_SISTEMA}")

print(f"[*] Fase 1: Cargando escenario '{NOMBRE_ARCHIVO_JSON}'...", end=" ", flush=True)
with open(NOMBRE_ARCHIVO_JSON, 'r', encoding='utf-8') as f:
    data_mision = json.load(f)
onto_path.append(self_path)
with silenciar_output_librerias():
    onto = get_ontology(NOMBRE_ARCHIVO_OWL).load()
print("Hecho.")

dict_activos = {}
totales_dominios = {}
atqs = []

with onto:
    print(f"[*] Fase 2: Instanciando el Grafo (Mision, Activos y Amenazas)...", end=" ", flush=True)
    instancia_mision = onto.Mision("Mision_Operativa_" + str(uuid.uuid4().hex[:6]))
    dominios_map = {"Tierra": onto.Tierra, "Mar": onto.Mar, "Aire": onto.Aire, "Espacio": onto.Espacio, "Ciberespacio": onto.Ciberespacio}
    instancia_mision.involucraDominio = list(dominios_map.values())

    for act in data_mision['activos']:
        c, d = onto[act['tipo']], dominios_map.get(act['dominio'])
        if c and d:
            obj = c(act['id']); obj.opera_en.append(d)
            dict_activos[act['id']] = obj
            
    for am in data_mision['amenazas']:
        ca = onto[am['tipo']]
        if ca:
            amenaza = ca(am['id']); raw = ca.objetivo_primario
            if raw:
                for t in [x.strip() for x in raw[0].split(',')]:
                    if hasattr(onto, t):
                        clase_objetivo = getattr(onto, t)
                        for o in dict_activos.values():
                            if clase_objetivo in o.is_a: amenaza.afecta_a.append(o)
    print("Hecho.")

    print("[*] Fase 3: Ejecutando Razonador HermiT (Vulnerabilidades)...", end=" ", flush=True)
    with silenciar_output_librerias(): sync_reasoner(infer_property_values=True)
    activos_riesgo = list(onto.ActivoEnRiesgo.instances())
    
    # Extraemos ataques para el PDF de la V3
    for am in data_mision['amenazas']:
        ao = getattr(onto, am['id'], None)
        if ao:
            for v in getattr(ao, 'afecta_a', []): 
                atqs.append({"amenaza": ao.name, "victima": v.name})
    print("Hecho.")

    # Sustituye la Fase 4 de tu script por esta versión corregida

    print("[*] Fase 4: Inyectando metricas NIST en OWL...", end=" ", flush=True)
    f_base = data_mision['configuracion_mision'].get('factor_tolerancia_base', 20)
    
    for dom_name, dom_inst in dominios_map.items():
        crit_val = data_mision['configuracion_mision']['niveles_criticidad'].get(dom_name, 1)
        u_max = (6 - crit_val) * f_base
        act_dom = [a for a in dict_activos.values() if a.opera_en and a.opera_en[0].name == dom_name]
        bajas = [a for a in act_dom if a in activos_riesgo]
        afectacion = (len(bajas)/len(act_dom)*100) if act_dom else 0.0
        
        totales_dominios[dom_name] = len(act_dom)

        # 1. Inyección de propiedades de datos (Para el reporte)
        if hasattr(onto, "tieneAfectacionReal"): dom_inst.tieneAfectacionReal = [float(afectacion)]
        if hasattr(onto, "tieneUmbralTolerancia"): dom_inst.tieneUmbralTolerancia = [float(u_max)]
        if hasattr(onto, "tieneCriticidadNivel"): dom_inst.tieneCriticidadNivel = [int(crit_val)]

        # 2. CORRECCIÓN DE NOMENCLATURA: Asignar tieneCriticidad al individuo C1...C5
        if hasattr(onto, "tieneCriticidad"):
            # Buscamos 'C1', 'C2', etc., que es como están en tu RDF
            nombre_individuo_crit = f"C{crit_val}" 
            ind_crit = getattr(onto, nombre_individuo_crit, None)
            if ind_crit: 
                dom_inst.tieneCriticidad = [ind_crit]

        # 3. CORRECCIÓN DE LÓGICA: Asignación de clases inclusiva
        if act_dom:
            if afectacion > u_max:
                # Si está comprometido, también está degradado para la lógica de la misión
                if hasattr(onto, "Dominio_Comprometido"): dom_inst.is_a.append(onto.Dominio_Comprometido)
                if hasattr(onto, "Dominio_Degradado"): dom_inst.is_a.append(onto.Dominio_Degradado)
            elif afectacion >= (u_max/2):
                if hasattr(onto, "Dominio_Degradado"): dom_inst.is_a.append(onto.Dominio_Degradado)
    print("Hecho.")

    print("[*] Fase 5: HermiT aplicando Lógica Descriptiva (Clasificando Misión)...", end=" ", flush=True)
    with silenciar_output_librerias(): sync_reasoner()
    print("Hecho.")

print("[*] Fase 6: Extrayendo la 'Verdad Semántica' para el informe...", end=" ", flush=True)

# CREAMOS EL DICCIONARIO EXACTO QUE TU PDF V3 ESPERA LEER
res_final = {"veredicto_mision": "EXITO", "dominios": {}, "ataques": atqs}

if hasattr(onto, "Mision_Fracasada") and instancia_mision in onto.Mision_Fracasada.instances():
    res_final['veredicto_mision'] = "FRACASO"
elif hasattr(onto, "Mision_Degradada") and instancia_mision in onto.Mision_Degradada.instances():
    res_final['veredicto_mision'] = "DEGRADADA"

for nombre, inst in dominios_map.items():
    afect_extract = inst.tieneAfectacionReal[0] if getattr(inst, "tieneAfectacionReal", None) else 0.0
    umb_extract = inst.tieneUmbralTolerancia[0] if getattr(inst, "tieneUmbralTolerancia", None) else 100.0
    crit_extract = inst.tieneCriticidadNivel[0] if getattr(inst, "tieneCriticidadNivel", None) else 1
    
    est_extract = "OPERATIVO"
    if hasattr(onto, "Dominio_Comprometido") and inst in onto.Dominio_Comprometido.instances(): est_extract = "COMPROMETIDO"
    elif hasattr(onto, "Dominio_Degradado") and inst in onto.Dominio_Degradado.instances(): est_extract = "DEGRADADO"

    res_final['dominios'][nombre] = {
        "total": totales_dominios.get(nombre, 0),
        "afectacion": afect_extract,
        "u_max": umb_extract, # El PDF V3 espera 'u_max', no 'umbral'
        "criticidad": crit_extract,
        "estado": est_extract
    }
print(f"[{res_final['veredicto_mision']}]")

print("[*] Fase 7: Generando Informe PDF (Paginacion Dinamica)...", flush=True)
sys_info = {"autor": "Alejandro Cerezo", "version": VERSION_SISTEMA, "fecha": datetime.datetime.now().strftime("%Y-%m-%d"), "report_id": str(uuid.uuid4()).upper()}

# USAMOS LA LÓGICA DE DOS PASADAS DE TU V3
dummy = MissionReportPDF(data_mision, res_final, sys_info)
dummy.generar_pasada(is_dummy=True)
final = MissionReportPDF(data_mision, res_final, sys_info)
final.generar_pasada(is_dummy=False, toc_data=dummy.toc_entries)

out_name = f"Report_{sanitize_filename(data_mision['configuracion_mision']['titulo'])}_V4_Definitivo.pdf"
final.output(out_name)
print(f"\n[+] PROCESO FINALIZADO EXITOSAMENTE.")
print(f"[+] Informe guardado en: {os.path.abspath(out_name)}\n")