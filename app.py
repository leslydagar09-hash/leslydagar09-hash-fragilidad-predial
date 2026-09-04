{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# 📊 Informe de Diagnóstico Hidromorfológico y Evaluación de Amenazas\n",
    "\n",
    "Este cuaderno recopila el análisis comparativo del comportamiento hidráulico, morfología del lecho y evaluación de amenaza por avenida torrencial e inundación para la **Quebrada la María** y el **Río Alvarado**."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "--- \n",
    "## 1. 🏞️ Quebrada la María (Abscisas $0+364.75$ a $0+380.00$)\n",
    "\n",
    "### Análisis Geomorfológico e Hidráulico\n",
    "El análisis geomorfológico e hidráulico de la Quebrada la María revela un lecho de montaña altamente encajonado con una sección transversal característica en forma de **\"V\"**, la cual experimenta un leve ensanchamiento en su base al avanzar desde la progresiva $0+364.75$ hacia la $0+380.00$. Presenta una fuerte pendiente longitudinal (superior al 5%), lo que permite clasificar la morfología de su cauce bajo la tipología de tipo ***Cascade*** o ***Step-Pool*** (peldaño-posa), compuesta por bloques y material rocoso, y caracterizada por la ausencia total de llanuras de inundación laterales.\n",
    "\n",
    "Desde la perspectiva del comportamiento hidráulico, la elevada pendiente favorece el desarrollo de un régimen de flujo predominantemente **supercrítico** ($Fr > 1$), con una alta energía cinética, tiempos de respuesta hidrológica muy cortos ante eventos de lluvia extremos y una elevada capacidad para el transporte y arrastre de sedimentos de fondo. Debido a la falta de espacio para disipar energía horizontalmente, cualquier incremento en el caudal genera un aumento drástico en el tirante de agua, concentrando los máximos esfuerzos cortantes en la base del cauce y al pie de los taludes laterales.\n",
    "\n",
    "### Evaluación de Amenaza\n",
    "Por lo anterior, la amenaza por avenida torrencial en este tramo se clasifica como **🚨 ALTA**. La combinación de fuertes pendientes, alto confinamiento y laderas inestables incrementa el riesgo de desprendimientos o deslizamientos que puedan generar represamientos temporales del cauce. La eventual ruptura de estos taponamientos desencadenaría **flujos de detritos (*debris flows*)** con un alto poder destructivo, caracterizados por una intensa socavación lateral e impacto de macro-bloques sobre cualquier obra de infraestructura o drenaje ubicada aguas abajo."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "--- \n",
    "## 2. 🌊 Río Alvarado (Abscisas $0+641.87$ a $0+660.00$)\n",
    "\n",
    "### Análisis Geomorfológico e Hidráulico\n",
    "El análisis geomorfológico e hidráulico del tramo de 600 metros del Río Alvarado evidencia un comportamiento de cauce semi-confinado a no confinado con una pendiente longitudinal moderada a suave, pasando de la cota $947.57\\text{ m s. n. m.}$ en la progresiva $0+642$ a más de $968\\text{ m s. n. m.}$ aguas arriba. A diferencia de tramos de alta montaña encajonados, las secciones transversales ($0+641.87$ y $0+660.00$) muestran un cauce más abierto y asimétrico, con presencia de terrazas laterales en la margen izquierda y un confinamiento moderado únicamente hacia la ladera derecha. Morfológicamente, la tipología se clasifica como un lecho de **Plano-Grava (*Plane-Bed*)** o **Río de Grava con Bancas/Terrazas**, compuesto principalmente por cantos rodados, gravas y arenas, donde la energía cinética se distribuye a lo largo de un cauce más ancho.\n",
    "\n",
    "En términos del comportamiento hidráulico, el régimen de flujo es predominantemente **subcrítico a crítico** ($Fr \\le 1$) durante condiciones normales, pudiendo alcanzar condiciones supercríticas locales durante avenidas pico. La geometría abierta de las secciones permite que ante un incremento en el caudal el flujo se expanda hacia las terrazas planas de la margen izquierda, aumentando el área hidráulica y disipando energía de manera horizontal. La capacidad de transporte de sedimentos es moderada, con tendencia a la sedimentación o depósito de material de arrastre en las zonas donde el canal se ensancha y disminuye la velocidad del agua.\n",
    "\n",
    "### Evaluación de Amenaza\n",
    "En consecuencia, la evaluación de amenaza por avenida torrencial en este tramo se clasifica como **⚠️ MEDIA A MODERADA**. Aunque existe un riesgo latente de inundación y desbordamiento sobre la margen izquierda debido a la escasa contención lateral y la suave pendiente, la probabilidad de flujos de detritos (*debris flows*) hiperconcentrados e intempestivos es menor que en tramos encajonados en \"V\". El principal mecanismo de afectación en este punto corresponde a la **inundación por desbordamiento**, la migración lateral del cauce y la **socavación en el pie de la ladera derecha**, la cual podría desestabilizar el talud contiguo en eventos de crecida prolongada."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "--- \n",
    "## 3. 📋 Cuadro Comparativo\n",
    "\n",
    "| Criterio / Parámetro | 🏞️ Quebrada la María | 🌊 Río Alvarado |\n",
    "| :--- | :--- | :--- |\n",
    "| **Geometría Transversal** | Sección encajonada en **\"V\"** estrecha y profunda | Sección abierta en forma de **plato/depósito amplio** |\n",
    "| **Pendiente Longitudinal ($S$)** | **Fuerte / Alta** ($S > 5\\% - 10\\%$) | **Moderada a Suave** |\n",
    "| **Clasificación Morfológica** | **Cascada (*Cascade*) / Peldaño-Posa (*Step-Pool*)** | **Plano-Grava (*Plane-Bed*)** con bancas/terrazas |\n",
    "| **Confinamiento Lateral** | **Alto confinamiento** (laderas empinadas a ambos lados) | **Semi-confinado** (terraza izquierda, talud derecho) |\n",
    "| **Llanura de Inundación** | **Ausente** | **Presente / Funcional** en la margen izquierda |\n",
    "| **Régimen Hidráulico** | **Supercrítico** ($Fr > 1$) | **Subcrítico a Crítico** ($Fr \\le 1$) |\n",
    "| **Respuesta Hidrológica** | **Muy rápida** (crecidas pico agudas) | **Gradual** (mayor capacidad de regulación) |\n",
    "| **Transporte de Sedimentos** | **Muy alto** (bloques, cantos y detritos) | **Moderado** (gravas/arenas con zonas de depósito) |\n",
    "| **Nivel de Amenaza** | 🚨 **ALTA** (Avenida Torrencial) | ⚠️ **MEDIA / MODERADA** (Inundación / Socavación) |\n",
    "| **Mecanismo Principales** | Represamiento, flujos de detritos y socavación | Inundación por desbordamiento y socavación de talud |"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Código sugerido para exportar resumen en formato DataFrame si deseas procesarlo con Pandas\n",
    "import pandas as pd\n",
    "\n",
    "data = {\n",
    "    \"Parámetro\": [\n",
    "        \"Geometría Transversal\", \"Pendiente Longitudinal\", \"Tipología Morfológica\", \n",
    "        \"Confinamiento Lateral\", \"Régimen Hidráulico\", \"Nivel de Amenaza\"\n",
    "    ],\n",
    "    \"Quebrada la María\": [\n",
    "        \"Encajonada en V\", \"Fuerte (>5%)\", \"Cascade / Step-Pool\", \n",
    "        \"Alto\", \"Supercrítico (Fr > 1)\", \"ALTA\"\n",
    "    ],\n",
    "    \"Río Alvarado\": [\n",
    "        \"Abierta / Forma de Plato\", \"Moderada a Suave\", \"Plane-Bed / Grava\", \n",
    "        \"Semi-confinado\", \"Subcrítico / Crítico (Fr <= 1)\", \"MEDIA / MODERADA\"\n",
    "    ]\n",
    "}\n",
    "\n",
    "df = pd.DataFrame(data)\n",
    "df.set_index(\"Parámetro\", inplace=True)\n",
    "df"
   ]
  }
 ],
 "metadata": {
  "language_info": {
   "name": "python"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}