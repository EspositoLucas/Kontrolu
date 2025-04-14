# **Kontrolu | Proyecto Final | UTN FRBA | 2024**
## **Requisitos Previos**
1. **Python 3.8+**: Asegúrate de tener Python instalado.
   * **Descarga**: Puedes descargarlo desde [python.org](https://www.python.org/downloads/).
   * **Verificación**: Abre tu terminal o línea de comandos y ejecuta:
       ```bash
       python --version
       ```
       Si ese comando no funciona (común en algunas instalaciones de Linux/macOS o si tienes múltiples versiones), prueba con:
       ```bash
       python3 --version
       ```
2. **Pip**: El administrador de paquetes de Python. La mayoría de las instalaciones de Python incluyen pip de manera predeterminada. Si necesitas instalarlo o actualizarlo, consulta la [documentación oficial de pip](https://pip.pypa.io/en/stable/installation/).
3. **Git**: Sistema de control de versiones necesario para clonar el repositorio.
   * **Descarga**: Puedes descargarlo desde [git-scm.com](https://git-scm.com/downloads). El sitio detectará tu sistema operativo y te ofrecerá la descarga adecuada.
   * **Verificación**:
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
Se recomienda configurar un entorno virtual para evitar conflictos entre paquetes. Usa el comando `python` o `python3` según cuál funcione en tu sistema (ver paso 1 de Requisitos Previos):
```bash
# Opción 1:
python -m venv venv
# Opción 2 (si 'python' no funciona):
python3 -m venv venv

# Activar el entorno:
source venv/bin/activate   # En Linux/macOS
# o
venv\Scripts\activate      # En Windows (cmd o PowerShell)
```
### **3. Instalar Dependencias**
Todas las dependencias necesarias están listadas en `requirements.txt`. Con tu entorno virtual activado, ejecuta el siguiente comando (usa `python` o `python3` según corresponda a tu sistema):
```bash
# Opción 1:
python -m pip install -r requirements.txt
# Opción 2 (si 'python' no funciona):
python3 -m pip install -r requirements.txt
```

## **Recomendaciones**
* **Resolución de Pantalla**: Para una mejor visualización y experiencia de uso de la aplicación, se recomienda ajustar la resolución de tu pantalla a un mínimo de **1600x1200 píxeles** o superior.

## **Ejecución del Proyecto**
Una vez instaladas las dependencias y configurado el entorno, puedes ejecutar la aplicación principal. Usa `python` o `python3` según corresponda:
```bash
# Opción 1:
python src/main.py
# Opción 2:
python3 src/main.py
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
