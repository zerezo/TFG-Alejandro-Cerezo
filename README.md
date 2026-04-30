# TFG-Alejandro-Cerezo
Repositorio que alberga el código ejecutable del trabajo fin de grado del GITST
# Simulador de Operaciones Multidominio (MDO) - V4.0 Final

![Versión](https://img.shields.io/badge/Versi%C3%B3n-4.0_Final-blue)
![Ingeniería](https://img.shields.io/badge/TFG-Ingenier%C3%ADa_Telecomunicaciones-orange)
![Framework](https://img.shields.io/badge/Marco-NIST_SP_800--30-red)

## 1. Descripción del Proyecto
Este proyecto constituye la versión final del **Simulador de Operaciones Multidominio (MDO)** desarrollado para el Trabajo Fin de Grado[cite: 1]. El sistema permite modelar escenarios militares complejos donde interactúan activos y amenazas en los dominios de Tierra, Aire, Mar, Espacio y Ciberespacio[cite: 1, 2].

La gran innovación de esta **Versión 4.0** es el salto de una lógica imperativa (basada en cálculos manuales en Python) a un **Sistema Experto basado en Inferencia Semántica**[cite: 1]. El sistema utiliza el razonador lógico **HermiT** para determinar el éxito o fracaso de una misión mediante el análisis de un grafo de conocimiento, eliminando la necesidad de lógica condicional rígida en el código fuente[cite: 1, 9].

## 2. Instalación y Configuración (Windows)

Para desplegar el simulador en un entorno local Windows, siga estos pasos:

### Tecnologías Necesarias
*   **Python 3.10+**: Motor de ejecución para la integración y generación de reportes[cite: 9].
*   **Java Runtime Environment (JRE)**: Requisito indispensable para que el razonador semántico (`HermiT`) funcione correctamente[cite: 1, 9].
*   **Archivos Base**: Asegúrese de tener en el mismo directorio:
    *   `script_4.0_2.py`: Script principal de ejecución[cite: 9].
    *   `Ontologia_31012026_2.rdf`: Ontología en formato OWL[cite: 3].
    *   `mision_2.json`: Configuración del escenario táctico[cite: 2].

### Pasos de Instalación
1.  **Instalar dependencias**: Ejecute el siguiente comando en su terminal:
    ```bash
    pip install owlready2 fpdf
    ```
2.  **Verificación**: Asegúrese de que el archivo `mision_2.json` esté configurado con los activos y niveles de criticidad deseados[cite: 2].
3.  **Ejecución**: Lance el simulador mediante:
    ```bash
    python script_4.0_2.py
    ```

## 3. Tecnologías y Ciclo de Vida del Desarrollo

El sistema se basa en una arquitectura de "Delegación de Inteligencia" dividida en las siguientes fases técnicas:

### A. Modelado del Conocimiento (OWL & Protégé)
Se utiliza una ontología formal en OWL (`Ontologia_31012026_2.rdf`) para definir la taxonomía de la misión[cite: 3].
*   **Lógica de Descripción (DL)**: Se han definido clases disjuntas y reglas de inferencia para determinar estados de misión (Fracasada, Degradada, Exitosa) basándose en la afectación de dominios estratégicos.

### B. Análisis de Riesgos Cuantitativo (NIST SP 800-30)
El sistema implementa el rigor matemático del framework NIST para evaluar el impacto de las amenazas[cite: 1].
*   **Resiliencia Dinámica**: Se calcula el umbral de tolerancia de cada dominio mediante la fórmula:  
    $Umbral = (6 - Nivel\_Criticidad) \times Factor\_Tolerancia\_Base$[cite: 1].
*   **Inyección de Datos**: Python calcula los porcentajes de daño real y los inyecta en las propiedades de datos de la ontología (`tieneAfectacionReal`)[cite: 1, 9].

### C. Inferencia Semántica (HermiT)
El núcleo de la Versión 4.0 es la delegación de la decisión final al razonador lógico[cite: 1].
*   **Inferencia de Segundo Orden**: El razonador analiza si el daño inyectado supera el umbral calculado y clasifica automáticamente el dominio como `Comprometido` o `Degradado`[cite: 1, 9].

### D. Generación de Informes Técnicos (FPDF)
La salida oficial del sistema son reportes PDF detallados (ej. `Report_Operación_Muro_Azul_Defensa_Costera_V4_Definitivo_2.pdf`)[cite: 8, 9].
*   **Single Source of Truth**: El informe se genera leyendo exclusivamente las inferencias realizadas por la ontología, garantizando que el veredicto tenga respaldo lógico formal[cite: 1].

---
**Autor:** Alejandro Cerezo  
**Proyecto:** Trabajo Fin de Grado - Ingeniería de Telecomunicaciones (2026)[cite: 1].
