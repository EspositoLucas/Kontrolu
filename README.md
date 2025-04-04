# **Kontrolu | Proyecto Final | UTN FRBA | 2024**
## **Requisitos Previos**
1. **Python 3.8+**: Asegúrate de tener Python instalado. Puedes verificar tu versión con:
   ```bash
   python --version
   ```
2. **Pip**: El administrador de paquetes de Python. La mayoría de las instalaciones de Python incluyen pip de manera predeterminada.
3. **Git**: Sistema de control de versiones necesario para clonar el repositorio y ejecutar comandos git. Puedes verificar tu versión con:
   ```bash
   git --version
   ```
## **Instalación**
### **1. Clonar Repositorio**
Si tienes el archivo `.zip`, extráelo en una carpeta local. Alternativamente, si el repositorio está en un sistema de control de versiones, puedes clonarlo con:
```bash
git clone <URL_del_repositorio>
cd Kontrolu-master
```
### **2. Crear un entorno virtual (opcional, pero recomendado)**
Se recomienda configurar un entorno virtual para evitar conflictos entre paquetes. Esto puedes hacerlo con los siguientes comandos:
```bash
python -m venv venv
source venv/bin/activate   *# En Linux/macOS*
*# o*
venv\Scripts\activate      *# En Windows*
```
### **3. Instalar Dependencias**
Todas las dependencias necesarias están listadas en `requirements.txt`. Ejecuta el siguiente comando para instalarlas:
```bash
pip install -r requirements.txt
```
## **Ejecución del Proyecto**
Una vez instaladas las dependencias y configurado el entorno, puedes ejecutar la aplicación principal. Este repositorio tiene un archivo principal en `src/main.py`, que inicia la aplicación.
Para ejecutar el proyecto, usa:
```bash
python src/main.py
```
Este comando lanza la aplicación y comienza la simulación/visualización de los procesos definidos en el proyecto.
## **Estructura del Proyecto**
- **`src/main.py`**: Archivo principal para iniciar la aplicación.
- **`src/back/`**: Contiene la lógica de backend del sistema.
- **`src/ui/`**: Contiene los elementos de la interfaz de usuario y visualización.
- **`tests/`**: Carpeta de pruebas unitarias.

## **Desactivación del entorno virtual**
Una vez que hayas terminado, puedes salir del entorno virtual con:
```bash
deactivate
```
---
## **Equipo de Proyecto**
| Integrantes  | Correo Institucional      |
| ------------- | ------------- |  
| Lucas Espósito Tejerina  | luespsito@frba.utn.edu.ar  |  
| Joaquín Solari Parravicini | jsolariparravicini@frba.utn.edu.ar |
| Daniela Ingratta | dingratta@frba.utn.edu.ar |
| Pedro Imanol Torales Gomez |  ptoralesgmez@frba.utn.edu.ar|
| Santiago Javier Demattei | sdemattei@fraba.utn.edu.ar|
