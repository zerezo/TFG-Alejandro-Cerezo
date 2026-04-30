# TFG-Alejandro-Cerezo
Repositorio que alberga el código ejecutable del trabajo fin de grado del GITST
# Simulador de Operaciones Multidominio (MDO) - V4.0 Final

![Versión](https://img.shields.io/badge/Versi%C3%B3n-4.0_Final-blue)
![Python](https://img.shields.io/badge/Python-3.10+-green)
![Ontología](https://img.shields.io/badge/OWL-Prot%C3%A9g%C3%A9-orange)
![Framework](https://img.shields.io/badge/Marco-NIST_SP_800--30-red)

## 1. Descripción del Proyecto

[cite_start]Este proyecto consiste en un **Simulador de Operaciones Multidominio (MDO)** desarrollado como Trabajo Fin de Grado en Ingeniería de Telecomunicaciones[cite: 1]. [cite_start]Su objetivo principal es evaluar la viabilidad y resiliencia de misiones militares complejas que involucran los dominios de **Tierra, Mar, Aire, Espacio y Ciberespacio**[cite: 50, 51, 53].

[cite_start]La gran innovación de la **Versión 4.0** es la transición de una lógica de cálculo imperativa (basada en bloques If/Else) a un **Sistema Experto con Inferencia Semántica**[cite: 11]. [cite_start]El sistema utiliza una ontología en OWL para actuar como la "Única Fuente de Verdad", donde el razonador lógico **HermiT** es quien decide el estado de la misión tras analizar el grafo de activos, amenazas y umbrales de riesgo definidos por el estándar **NIST SP 800-30**[cite: 4, 14, 15].

---

## 2. Instalación y Requisitos (Windows)

Para ejecutar el simulador en un entorno Windows, sigue estos pasos:

### Tecnologías Necesarias
* **Python 3.10 o superior:** Motor de ejecución del script principal.
* [cite_start]**Java Runtime Environment (JRE):** Indispensable para que el razonador HermiT pueda procesar la lógica descriptiva de la ontología[cite: 118].
* [cite_start]**Protégé (Opcional):** Para la visualización y edición manual del archivo `Ontologia_31012026.rdf`[cite: 1, 20].

### Pasos de Instalación
1.  **Clonar el repositorio:**
    ```bash
    git clone [https://github.com/tu-usuario/MDO-Simulator-V4.git](https://github.com/tu-usuario/MDO-Simulator-V4.git)
    cd MDO-Simulator-V4
    ```

2.  **Instalar dependencias de Python:**
    Abre la terminal y ejecuta:
    ```bash
    pip install owlready2 fpdf
    ```

3.  **Verificar archivos base:**
    Asegúrate de que los siguientes archivos estén en el mismo directorio raíz:
    * `script_4.0.py` (Lógica de integración)[cite: 21].
    * `Ontologia_31012026.rdf` (Grafo de conocimiento)[cite: 20].
    * `mision.json` (Configuración del escenario táctico)[cite: 20].

---

## 3. Ciclo de Vida y Tecnologías Utilizadas

El sistema opera bajo un flujo de trabajo cíclico que garantiza que cada decisión esté respaldada por lógica formal:

### A. Modelado del Conocimiento (Protégé & OWL)
[cite_start]Se define la taxonomía base (Activos, Amenazas, Dominios) y las relaciones estáticas[cite: 2].
* [cite_start]**Uso:** Se establecen reglas de **Lógica de Descripción (DL)** y clases disjuntas para evitar paradojas y asegurar que el razonador resuelva el escenario en milisegundos[cite: 17, 19].

### B. Ingesta Dinámica de Escenarios (JSON)
[cite_start]El usuario define la "Orden de Batalla" y los niveles de criticidad (C1 a C5) en un archivo JSON[cite: 20].
* [cite_start]**Uso:** Python lee esta configuración y mapea los activos a sus clases correspondientes en la ontología de forma automática[cite: 12].

### C. El Núcleo de Cálculo (NIST SP 800-30)
Se aplica la **Fórmula de Resiliencia Dinámica** para determinar la capacidad de aguante de cada dominio:
* [cite_start]**Fórmula:** $Umbral\_Tolerancia (\%) = (6 - Nivel\_Criticidad) \times Factor\_Tolerancia\_Base$[cite: 7].
* [cite_start]**Uso:** Python inyecta estos valores en las "Data Properties" (`tieneAfectacionReal`, `tieneUmbral`) de la ontología[cite: 12, 18].

### D. Delegación de Inteligencia (Owlready2 + HermiT)
[cite_start]Esta es la fase crítica donde Python cede el control al razonador semántico[cite: 10, 13].
* [cite_start]**Uso:** **HermiT** analiza el grafo: si un dominio estratégico (C5) tiene daños superiores a su umbral, el razonador infiere automáticamente que la clase `Mision_Fracasada` es verdadera[cite: 14].

### E. Generación de Informes (FPDF)
[cite_start]El sistema genera un informe técnico en PDF que lee exclusivamente los datos inferidos en la ontología[cite: 15, 22].
* [cite_start]**Uso:** Proporciona un veredicto visual del estado de los dominios (Operativo, Degradado o Comprometido) y la resolución final de la misión[cite: 8, 9].

---

## Autor
[cite_start]**Alejandro Cerezo** - Proyecto de Fin de Grado en Ingeniería de Telecomunicaciones (2026)[cite: 61, 65, 66].
