import json
import sys
import datetime 
import uuid 
import time
import jsonschema
from jsonschema.exceptions import ValidationError
from pathlib import Path

# --- CONFIGURACIÓN DE CONSOLA PARA WINDOWS ---
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

from contextlib import contextmanager
from owlready2 import *
from fpdf import FPDF

# ==========================================
# CONSTANTES Y CONFIGURACIÓN SEGURA
# ==========================================
BASE_DIR = Path(__file__).resolve().parent
OWL_FILE = BASE_DIR / "OntologiaMDO.rdf"
JSON_FILE = BASE_DIR / "mision.json"
VERSION_SISTEMA = "5.0 (Hardened & Modular)"

COLOR_NAVY = (44, 62, 80)
COLOR_WHITE = (255, 255, 255)
COLOR_ACCENT = (52, 152, 219)
COLOR_TEXT_BASE = (44, 62, 80)
COLOR_TEXT_SUBTLE = (100, 100, 100)
COLOR_CRIT_5 = (192, 57, 43)   
COLOR_WARNING = (243, 156, 18) 
COLOR_SUCCESS = (39, 174, 96)  

# ==========================================
# UTILIDADES GLOBALES
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
# CLASE PDF: MOTOR DE GENERACIÓN VISUAL
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
        info = f"Pagina {self.page_no()} | {self.config.get('titulo', 'MDO')} | Ref: {self.system_info['report_id'][:8]} | Datos Inferidos por OWL"
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
        subt = f"Version Final {self.system_info['version']}\nMotor de Razonamiento Semantico Modular"
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
        self.cell(0, 6, clean_text(self.config.get('titulo', 'N/A')), 0, 1)
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
                texto = f"[INFERENCIA DL] {atq['victima']} ➔ Estado: {atq['amenaza']}"
                self.set_font('Arial', 'B', 10); self.set_text_color(*COLOR_CRIT_5)
                self.multi_cell(0, 7, clean_text(texto), 0, 'L'); self.ln(1)
        else:
            self.set_font('Arial', 'I', 10); self.set_text_color(*COLOR_TEXT_SUBTLE)
            self.cell(0, 10, "No se han detectado activos comprometidos mediante razonamiento DL.", 0, 1)

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
            
            x = self.get_x()
            y = self.get_y() + 3
            
            self.set_fill_color(240, 240, 240); self.rect(x, y, 170, 6, 'F')
            self.set_fill_color(*color_est); self.rect(x, y, (stats['afectacion'] / 100) * 170, 6, 'F')
            
            u_max_x = x + (stats['u_max'] / 100) * 170
            u_deg_x = x + ((stats['u_max'] / 2) / 100) * 170
            
            self.set_font('Arial', '', 7)
            
            lbl_deg = f"{stats['u_max']/2:.1f}%"
            w_deg = self.get_string_width(lbl_deg)
            self.set_text_color(120, 120, 120)
            self.text(u_deg_x - w_deg/2, y - 2, lbl_deg)
            self.set_fill_color(150, 150, 150); self.rect(u_deg_x, y, 0.5, 6, 'F')
            
            if stats['u_max'] < 100: 
                lbl_max = f"{stats['u_max']:.1f}%"
                w_max = self.get_string_width(lbl_max)
                self.set_text_color(*COLOR_NAVY)
                self.text(u_max_x - w_max/2, y - 2, lbl_max)
                self.set_fill_color(*COLOR_NAVY)
                self.rect(u_max_x, y-1, 1, 8, 'F')
            
            self.set_y(y + 6)
            self.ln(9)
            
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

def generar_informe_forense(data_mision, resultados, sys_info, base_dir):
    dummy = MissionReportPDF(data_mision, resultados, sys_info)
    dummy.generar_pasada(is_dummy=True)
    
    final = MissionReportPDF(data_mision, resultados, sys_info)
    final.generar_pasada(is_dummy=False, toc_data=dummy.toc_entries)

    titulo_limpio = sanitize_filename(data_mision.get('configuracion_mision', {}).get('titulo', 'Simulacion'))
    out_name = base_dir / f"Report_{titulo_limpio}_V5.pdf"
    final.output(str(out_name))
    
    return out_name

# ==========================================
# MÓDULOS DEL MOTOR LÓGICO (HARDENED)
# ==========================================
def inicializar_ontologia(owl_path):
    onto_path.append(str(BASE_DIR))
    with silenciar_output_librerias():
        return get_ontology(str(owl_path)).load()

def extraer_vocabulario_ontologico(onto):
    """Extracción dinámica de la taxonomía TBox para garantizar SSoT."""
    try:
        activos_validos = [cls.name for cls in onto.Activo.descendants() if cls != onto.Activo]
        amenazas_validas = [cls.name for cls in onto.Amenaza.descendants() if cls != onto.Amenaza]
        dominios_validos = [inst.name for inst in onto.Dominio.instances()]
        return activos_validos, amenazas_validas, dominios_validos
    except Exception as e:
        print(f"[ERROR CRÍTICO] Fallo en la introspección ontológica: {e}")
        sys.exit(1)

def cargar_y_validar_escenario(json_path, onto):
    """Validación estructural estricta frente al vocabulario OWL y los límites NIST."""
    activos_owl, amenazas_owl, dominios_owl = extraer_vocabulario_ontologico(onto)

    esquema_mdo_estricto = {
        "type": "object",
        "required": ["configuracion_mision", "activos", "amenazas"],
        "properties": {
            "configuracion_mision": {
                "type": "object",
                "required": ["titulo", "descripcion", "factor_tolerancia_base", "niveles_criticidad"],
                "properties": {
                    "factor_tolerancia_base": {
                        "type": "number", 
                        "exclusiveMinimum": 0, 
                        "maximum": 100
                    },
                    "niveles_criticidad": {
                        "type": "object",
                        "additionalProperties": False,
                        "patternProperties": {
                            f"^({'|'.join(dominios_owl)})$": {
                                "type": "integer",
                                "minimum": 1,
                                "maximum": 5
                            }
                        }
                    }
                }
            },
            "activos": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": ["id", "tipo", "dominio"],
                    "properties": {
                        "id": {"type": "string", "minLength": 1},
                        "tipo": {"type": "string", "enum": activos_owl},
                        "dominio": {"type": "string", "enum": dominios_owl}
                    }
                }
            },
            "amenazas": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": ["id", "tipo", "dominio_despliegue"],
                    "properties": {
                        "id": {"type": "string", "minLength": 1},
                        "tipo": {"type": "string", "enum": amenazas_owl},
                        "dominio_despliegue": {"type": "string", "enum": dominios_owl}
                    }
                }
            }
        }
    }

    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        jsonschema.validate(instance=data, schema=esquema_mdo_estricto)
        return data

    except ValidationError as e:
        print(f"\n[ERROR DE INTEGRIDAD DE DATOS] Violación del estándar de ingesta.")
        print(f"Ruta del error: {' -> '.join([str(p) for p in e.path])}")
        print(f"Detalle: {e.message}")
        sys.exit(1)
    except FileNotFoundError:
        print(f"\n[ERROR DE I/O] No se localiza el vector de ingesta JSON en {json_path}")
        sys.exit(1)

def procesar_simulacion_mdo(data_mision, onto):
    dict_activos = {}
    totales_dominios = {}
    atqs = []
    
    config = data_mision.get('configuracion_mision', {})
    niveles_crit = config.get('niveles_criticidad', {})
    f_base = config.get('factor_tolerancia_base', 20)
    
    with onto:
        print("\n    └─ Fase 3: Instanciación Topológica...", end=" ", flush=True)
        mision_id = "Mision_Operativa_" + uuid.uuid4().hex[:6]
        instancia_mision = onto.Mision(mision_id)
        
        dominios_map = {dom_name: getattr(onto, dom_name) for dom_name in niveles_crit.keys()}
        instancia_mision.involucraDominio = list(dominios_map.values())

        for act in data_mision.get('activos', []):
            clase_activo = getattr(onto, act['tipo'])
            dominio_obj = dominios_map.get(act['dominio'])
            if clase_activo and dominio_obj:
                obj = clase_activo(act['id'])
                obj.opera_en.append(dominio_obj)
                dict_activos[act['id']] = obj
                
        for am in data_mision.get('amenazas', []):
            clase_amenaza = getattr(onto, am['tipo'])
            dominio_obj = dominios_map.get(am.get('dominio_despliegue'))
            if clase_amenaza and dominio_obj:
                amenaza = clase_amenaza(am['id'])
                amenaza.ataca_en_dominio.append(dominio_obj)
        print("OK")

        print("    └─ Fase 4: Inferencia Semántica DL (Vulnerabilidades)...", end=" ", flush=True)
        with silenciar_output_librerias(): 
            # ¡CORRECCIÓN CRÍTICA APLICADA AQUÍ: CONTEXTO 'onto.world'!
            sync_reasoner(onto.world, infer_property_values=True)
            
        activos_riesgo = list(onto.ActivoEnRiesgo.instances())
        for activo in activos_riesgo:
            clases_riesgo = [c.name for c in activo.is_a if hasattr(c, 'ancestors') and onto.ActivoEnRiesgo in c.ancestors()]
            causa = clases_riesgo[0] if clases_riesgo else "Riesgo Topológico"
            atqs.append({"amenaza": causa, "victima": activo.name})
        print(f"OK ({len(activos_riesgo)} detectados)")

        print("    └─ Fase 5: Cálculo NIST, Data Properties y Subsunción...", end=" ", flush=True)
        for dom_name, dom_inst in dominios_map.items():
            crit_val = niveles_crit.get(dom_name, 1)
            u_max = (6 - crit_val) * f_base
            
            act_dom = [a for a in dict_activos.values() if a.opera_en and a.opera_en[0].name == dom_name]
            bajas = [a for a in act_dom if a in activos_riesgo]
            afectacion = (len(bajas)/len(act_dom)*100) if act_dom else 0.0
            totales_dominios[dom_name] = len(act_dom)

            dom_inst.tieneAfectacionReal = [float(afectacion)]
            dom_inst.tieneUmbralTolerancia = [float(u_max)]
            dom_inst.tieneCriticidadNivel = [int(crit_val)]

            nombre_crit = f"C{crit_val}" 
            ind_crit = getattr(onto, nombre_crit, None)
            if ind_crit: dom_inst.tieneCriticidad = [ind_crit]

            if act_dom:
                if afectacion >= u_max:
                    dom_inst.is_a.append(onto.Dominio_Comprometido)
                elif afectacion >= (u_max/2):
                    dom_inst.is_a.append(onto.Dominio_Degradado)
        print("OK")

        print("    └─ Fase 6: Resolución de Misión (Axiomas Globales)...", end=" ", flush=True)
        with silenciar_output_librerias(): 
            # ¡CORRECCIÓN CRÍTICA APLICADA AQUÍ: CONTEXTO 'onto.world'!
            sync_reasoner(onto.world)
        print("OK")

        # [Insertar en script_5.py / script_6.py después de sync_reasoner]
        print("    └─ Guardando grafo inferido para evidencia forense...")
        onto.save(file=str(BASE_DIR / f"Grafo_Inferido_{mision_id}.owl"), format="rdfxml")

    res_final = {"veredicto_mision": "EXITO", "dominios": {}, "ataques": atqs}

    if instancia_mision in onto.Mision_Fracasada.instances():
        res_final['veredicto_mision'] = "FRACASO"
    elif instancia_mision in onto.Mision_Degradada.instances():
        res_final['veredicto_mision'] = "DEGRADADA"

    for nombre, inst in dominios_map.items():
        afect = inst.tieneAfectacionReal[0] if getattr(inst, "tieneAfectacionReal", None) else 0.0
        umb = inst.tieneUmbralTolerancia[0] if getattr(inst, "tieneUmbralTolerancia", None) else 100.0
        crit = inst.tieneCriticidadNivel[0] if getattr(inst, "tieneCriticidadNivel", None) else 1
        
        est = "OPERATIVO"
        if inst in onto.Dominio_Comprometido.instances(): est = "COMPROMETIDO"
        elif inst in onto.Dominio_Degradado.instances(): est = "DEGRADADO"

        res_final['dominios'][nombre] = {
            "total": totales_dominios.get(nombre, 0), "afectacion": afect,
            "u_max": umb, "criticidad": crit, "estado": est
        }
        
    return res_final

# ==========================================
# ORQUESTADOR PRINCIPAL
# ==========================================
def main():
    print(f"\n[+] INICIANDO SISTEMA MDO V{VERSION_SISTEMA}")
    
    t_inicio_absoluto = time.perf_counter()
    
    print("[*] Fase 1: Cargando base de conocimiento TBox...", end=" ", flush=True)
    t_onto_in = time.perf_counter()
    onto = inicializar_ontologia(OWL_FILE)
    print(f"Hecho ({time.perf_counter() - t_onto_in:.4f} s).")

    print("[*] Fase 2: Ingesta y validación estructural NIST/OWL...", end=" ", flush=True)
    t_json_in = time.perf_counter()
    data_mision = cargar_y_validar_escenario(JSON_FILE, onto)
    print(f"Hecho ({time.perf_counter() - t_json_in:.4f} s).")
    
    print("[*] Ejecutando Motor Semantico...")
    t_motor_inicio = time.perf_counter()
    resultados = procesar_simulacion_mdo(data_mision, onto)
    print(f"[*] Veredicto Semántico: [{resultados['veredicto_mision']}] (Procesado en {time.perf_counter() - t_motor_inicio:.4f} s)")
    
    print("[*] Fase 7: Generando Informe Forense (PDF)...", end=" ", flush=True)
    sys_info = {
        "autor": "Alejandro Cerezo Gilarranz", 
        "version": VERSION_SISTEMA, 
        "fecha": datetime.datetime.now().strftime("%Y-%m-%d"), 
        "report_id": str(uuid.uuid4()).upper()
    }
    
    ruta_pdf = generar_informe_forense(data_mision, resultados, sys_info, BASE_DIR)
    print("Hecho.")
    
    t_fin_absoluto = time.perf_counter()
    print("\n[+] PROCESO FINALIZADO EXITOSAMENTE.")
    print(f"[+] Documento guardado en: {ruta_pdf}")
    print(f"[+] TELEMETRÍA GLOBAL: Tiempo total de ejecución: {t_fin_absoluto - t_inicio_absoluto:.4f} segundos.\n")

if __name__ == "__main__":
    main()