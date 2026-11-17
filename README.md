# Simulador de Operaciones Multidominio (MDO) - V5.0 (Hardened & Modular)

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Ontology](https://img.shields.io/badge/OWL_2_DL-Protégé-orange.svg)](https://protege.stanford.edu/)
[![Framework](https://img.shields.io/badge/NIST-SP_800--30-success.svg)](https://csrc.nist.gov/publications/detail/sp/800-30/rev-1/final)

## 📌 Descripción del Proyecto

Este repositorio contiene el código fuente, la base de conocimiento y los escenarios de prueba del **Simulador de Riesgos de Ciberseguridad para Operaciones Multidominio (MDO)**, desarrollado como Trabajo Fin de Grado en Ingeniería de Tecnologías y Servicios de Telecomunicación (ETSIT-UPM).

El sistema consiste en un Sistema Basado en Conocimiento (KBS) con una arquitectura de software híbrida. Combina un motor de inferencia semántica (Lógica Descriptiva en OWL) para la clasificación de topologías de red interconectadas, con un orquestador en Python que implementa las métricas deterministas de la matriz de riesgos del estándar norteamericano **NIST SP 800-30**. 

El simulador ingiere un escenario táctico, evalúa los vectores de amenaza y calcula de forma autónoma la resiliencia sistémica de los dominios operativos (Tierra, Mar, Aire, Espacio y Ciberespacio), delegando el veredicto estratégico global al razonador HermiT.

## 🏗️ Arquitectura y Flujo de Ejecución

1. **Ingesta y Validación (JSON):** Carga dinámica de activos tácticos y amenazas, validada en tiempo de ejecución de forma estricta (Fail-Fast) contra el esquema derivado de la TBox.
2. **Razonamiento Topológico (OWL 2 DL):** HermiT escanea intersecciones y clasifica axiomáticamente los individuos expuestos dentro de la clase `ActivoEnRiesgo`.
3. **Puente Cuantitativo (Python + NIST):** Cálculo de la afectación real frente al umbral dinámico de tolerancia de cada entorno (basado en su nivel de criticidad C1-C5.
4. **Subsunción y Veredicto Global:** Inyección de *Data Properties* en la ontología; HermiT asume el control para deducir el colapso funcional (`Mision_Fracasada` o `Mision_Degradada`).
5. **Generación de Inteligencia:** Extracción forense desde el grafo inferido (Única Fuente de Verdad) hacia un informe automatizado (PDF).

## 📂 Estructura del Repositorio

* `script.py`: Orquestador principal del sistema. Integra la lectura del json, el puente aritmético NIST, las llamadas de subsunción a `owlready2` y la invocación de `fpdf`.
* `OntologiaMDO.rdf`: Modelo semántico formal base (TBox). Desarrollado en Protégé, contiene la jerarquía de clases disjuntas, propiedades (Data y Object Properties) y las aserciones de Lógica Descriptiva.
* `mision.json`: Archivo de parametrización modular. Permite inyectar inventarios tácticos, vectores de amenaza y métricas base sin modificar el código lógico.
* `requirements.txt`: Manifiesto estricto de dependencias de la arquitectura.

## 📦 Archivos Generados en Ejecución

Tras la ejecución exitosa del sistema, se instancian los siguientes artefactos en el directorio raíz:
* `Report_<Titulo_Mision>_V5.pdf`: Informe forense automatizado estructurado en 5 bloques analíticos (Contexto, Inventario, Inferencia Semántica, Impacto NIST y Resolución de la Misión).
* `Grafo_Inferido_Mision_Operativa_<UUID>.owl`: Evidencia criptográfica del grafo de conocimiento. Contiene la instanciación topológica y todas las relaciones de estado deducidas (A-Box poblada), sirviendo como rastro de auditoría inmutable.

## ⚙️ Instalación y Ejecución

Es estrictamente recomendable aislar el entorno de despliegue mediante un entorno virtual (`venv`) para no comprometer la pureza de las bibliotecas del sistema, especialmente por la dependencia subyacente de la JVM para el razonador de `owlready2`.

```bash
# 1. Clonar el repositorio
git clone <https://github.com/zerezo/TFG-Alejandro-Cerezo>
cd Simulador-MDO

# 2. Crear y activar el entorno virtual
python -m venv venv
# En Windows:
venv\Scripts\activate
# En Linux/macOS:
source venv/bin/activate

# 3. Instalar las dependencias estrictas
pip install -r requirements.txt

# 4. Ejecutar la simulación
python script.py
