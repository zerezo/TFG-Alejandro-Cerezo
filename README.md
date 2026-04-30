# TFG-Alejandro-Cerezo
Repositorio que alberga el código ejecutable del trabajo fin de grado del GITST
# Simulador de Operaciones Multidominio (MDO) - Versión 4.0

## 1. Descripción del Proyecto
[cite_start]Este sistema es un simulador avanzado diseñado para el **Trabajo Fin de Grado (TFG) de Ingeniería de Telecomunicaciones**. [cite_start]Su objetivo es evaluar la resiliencia y el estado de misiones militares en entornos multidominio (Tierra, Mar, Aire, Espacio y Ciberespacio) utilizando un motor de cálculo basado en el estándar **NIST SP 800-30**[cite: 4, 119].

[cite_start]La **Versión 4.0** introduce un salto tecnológico fundamental: la **Integración NIST-Semántica Definitiva**. [cite_start]A diferencia de versiones anteriores basadas en lógica imperativa, esta versión actúa como un **Sistema Experto**[cite: 10]. [cite_start]El sistema delega la "inteligencia" a una ontología OWL, donde el razonador lógico **HermiT** analiza el grafo de activos y amenazas para inferir automáticamente si una misión es un éxito o un fracaso[cite: 11, 13, 118].

## 2. Instalación y Requisitos (Windows)

Para ejecutar este simulador en un PC con Windows, siga estos pasos y asegúrese de contar con las siguientes tecnologías:

### Requisitos de Software
* [cite_start]**Python 3.x**: Lenguaje principal para la ejecución del script y gestión de datos[cite: 5, 21].
* [cite_start]**Java Runtime Environment (JRE)**: Necesario para que el razonador **HermiT** pueda realizar la inferencia semántica[cite: 13, 118].
* [cite_start]**Protégé**: Recomendado para visualizar o editar la taxonomía base y las reglas de la ontología (`.rdf`)[cite: 2, 16].

### Pasos de Instalación
1.  **Instalar librerías de Python**: Abra una terminal y ejecute:
    ```bash
    pip install owlready2 fpdf
    ```
    * `owlready2`: Permite la interacción entre Python y la ontología OWL[cite: 118].
    * `fpdf`: Motor para la generación de los informes técnicos en PDF[cite: 21].

2.  **Preparar archivos**: Asegúrese de tener en el mismo directorio:
    * [cite_start]`script_4.0.py`: El código motor[cite: 21].
    * [cite_start]`Ontologia_31012026.rdf`: La base de conocimiento semántica[cite: 20].
    * [cite_start]`mision.json`: Archivo de configuración del escenario táctico[cite: 19].

3.  **Ejecución**:
    ```bash
    python script_4.0.py
    ```

## 3. Tecnologías y Ciclo de Vida del Sistema

El simulador utiliza un ecosistema tecnológico integrado para transformar datos brutos en decisiones estratégicas:

### A. Modelado Semántico (OWL & Protégé)
[cite_start]La estructura del conocimiento se define en una ontología que identifica Clases (Activos, Amenazas, Dominios) y sus relaciones[cite: 2, 16]. 
* [cite_start]**Uso**: Se definen reglas de Lógica de Descripción (DL) para clasificar misiones degradadas o fracasadas basadas en la criticidad de los dominios afectados[cite: 18].

### B. Ingesta y Cálculo (Python & JSON)
[cite_start]El escenario se carga dinámicamente mediante un archivo JSON que define los activos y su criticidad (Nivel 1 a 5)[cite: 3, 19].
* **Marco Matemático NIST**: Python calcula la resiliencia dinámica. [cite_start]Por ejemplo, un dominio vital (C5) tiene un umbral de fallo del 20% de daños, mientras que uno de nivel C1 tolera hasta el 100%[cite: 7].
* [cite_start]**Inyección de Datos**: Los porcentajes calculados se inyectan en las "Data Properties" de la ontología (`tieneAfectacionReal`, `tieneUmbral`)[cite: 11].

### C. Inferencia Lógica (HermiT Reasoner)
[cite_start]El sistema utiliza el razonador **HermiT** para realizar un análisis de segundo orden[cite: 11, 118].
* [cite_start]**Uso**: El razonador evalúa el grafo: "Si el Dominio A está comprometido Y su nivel es C5, entonces la Misión es un FRACASO"[cite: 13]. [cite_start]Esto elimina la necesidad de bloques complejos de `if/else` en el código principal[cite: 5, 12].

### D. Generación de Informes (PDF)
[cite_start]El resultado final es un informe técnico basado exclusivamente en la ontología, considerada la "Única Fuente de Verdad"[cite: 14, 15].
* [cite_start]**Uso**: Se genera un PDF detallado con la matriz de criticidad, el inventario táctico y el veredicto final inferido por el razonador[cite: 21, 108].

---
**Autor**: Alejandro Cerezo  
**Proyecto**: Trabajo Fin de Grado - Ingeniería de Telecomunicaciones  
[cite_start]**Versión**: 4.0 (Integración NIST-Semántica Definitiva)
