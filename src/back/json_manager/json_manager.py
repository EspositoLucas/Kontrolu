import json
import os
from back.macros.macro_bloque import MACROS
from back.json_manager.dtos import DominioDto, MicroBloqueDto, TipoMicroBloqueDto

file = "datos.json"
backup_datos = "backup_datos.json"

def crear_json_para_dominios(dominios: list[str] = ["SISTEMAS", "ELECTRONICA"]) -> None:
    """
    Crea un archivo json con la estructura necesaria para guardar los dominios
    """
    with open(file, "w") as json_file:
        json_data = {
            "dominios": dominios,
            str(MACROS.CONTROLADOR): {dominio: {} for dominio in dominios},
            str(MACROS.ACTUADOR): {dominio: {} for dominio in dominios},
            str(MACROS.PROCESO): {dominio: {} for dominio in dominios},
            str(MACROS.MEDIDOR): {dominio: {} for dominio in dominios}
        }
        json.dump(json_data, json_file, indent=4)

def __agregar_dominio(dominio: str, json_data) -> dict:
    """
    Agrega un dominio al json
    """
    json_data["dominios"].append(dominio)
    json_data[str(MACROS.CONTROLADOR)][dominio] = {}
    json_data[str(MACROS.ACTUADOR)][dominio] = {}
    json_data[str(MACROS.PROCESO)][dominio] = {}
    json_data[str(MACROS.MEDIDOR)][dominio] = {}
    return json_data

def agregar_dominios(dominios: list[str] = None, dominio: str = None) -> None:
    """
    Agrega dominios al archivo json
    """
    if not os.path.exists(file):
        crear_json_para_dominios()

    doms = []
    if dominio:
        doms.append(dominio)
    if dominios:
        doms.extend(dominios)

    with open(file, "r") as json_file:
        json_data = json.load(json_file)

    for dominio in doms:
        if dominio not in json_data["dominios"]:
            json_data = __agregar_dominio(dominio, json_data)

    with open(file, "w") as json_file:
        json.dump(json_data, json_file, indent=4)

def borrar_dominios(dominios: list[str] = None, dominio: str = None) -> None:
    """
    Borra dominios del archivo json
    """
    if not os.path.exists(file):
        crear_json_para_dominios()

    doms = []
    if dominio:
        doms.append(dominio)
    if dominios:
        doms.extend(dominios)

    with open(file, "r") as json_file:
        json_data = json.load(json_file)

    for dominio in doms:
        if dominio in json_data["dominios"]:
            json_data["dominios"].remove(dominio)
            del json_data[str(MACROS.CONTROLADOR)][dominio]
            del json_data[str(MACROS.ACTUADOR)][dominio]
            del json_data[str(MACROS.PROCESO)][dominio]
            del json_data[str(MACROS.MEDIDOR)][dominio]

    with open(file, "w") as json_file:
        json.dump(json_data, json_file, indent=4)

def obtener_dominios() -> list[str]:
    """
    Obtiene los dominios guardados en el archivo json
    """
    if not os.path.exists(file):
        crear_json_para_dominios()

    with open(file, "r") as json_file:
        json_data = json.load(json_file)

    return json_data["dominios"]

def __crear_tipo(tipo: str, dominio: str, macro: MACROS, json_data, descripcion: str = "") -> dict:
    """
    Crea un tipo en el archivo json
    """
    json_data[str(macro)][dominio][tipo] = {
        "descripcion": descripcion,
        "micro_bloques": {}
    }
    return json_data

def crear_tipo(tipo: str, dominio: str, macro: MACROS, descripcion: str = "") -> None:
    """
    Crea un tipo en el archivo json
    """
    if not os.path.exists(file):
        crear_json_para_dominios()

    with open(file, "r") as json_file:
        json_data = json.load(json_file)

    json_data[str(macro)][dominio][tipo] = {
        "descripcion": descripcion,
        "micro_bloques": {}
    }
    json_data = borrar_microbloques_vacios(json_data)

    with open(file, "w") as json_file:
        json.dump(json_data, json_file, indent=4)

def agregar_microbloque(microbloque: MicroBloqueDto, tipo: str, dominio: str, macro: MACROS) -> None:
    """
    Agrega un microbloque a un tipo en el archivo json
    """
    if not os.path.exists(file):
        crear_json_para_dominios()

    with open(file, "r") as json_file:
        json_data = json.load(json_file)

    if dominio not in json_data["dominios"]:
        json_data = __agregar_dominio(dominio, json_data)

    if tipo not in json_data[str(macro)][dominio]:
        json_data = __crear_tipo(tipo, dominio, macro, json_data)

    json_data[str(macro)][dominio][tipo]["micro_bloques"][microbloque.nombre] = microbloque.__dict__

    json_data = borrar_microbloques_vacios(json_data)

    with open(file, "w") as json_file:
        json.dump(json_data, json_file, indent=4)

def obtener_microbloques_de_una_macro(macro: MACROS) -> list[DominioDto]:
    """
    Obtiene los dominios de una macro en el archivo json
    """
    if not os.path.exists(file):
        crear_json_para_dominios()

    with open(file, "r") as json_file:
        json_data = json.load(json_file)

    json_data = borrar_microbloques_vacios(json_data)

    dominios = []
    for dominio in json_data[str(macro)].keys():
        tipos = []
        for tipo in json_data[str(macro)][dominio].keys():
            microbloques = []
            for microbloque in json_data[str(macro)][dominio][tipo]["micro_bloques"].values():
                microbloques.append(MicroBloqueDto(**microbloque))
            tipos.append(TipoMicroBloqueDto(nombre_tipo=tipo, descripcion_tipo=json_data[str(macro)][dominio][tipo]["descripcion"], micro_bloques=microbloques))
        dominios.append(DominioDto(nombre=dominio, tipos=tipos))
    return dominios

def obtener_microbloques_de_un_dominio(dominio: str, macro: MACROS) -> list[TipoMicroBloqueDto]:
    """
    Obtiene los tipos de un dominio en el archivo json
    """
    if not os.path.exists(file):
        crear_json_para_dominios()

    with open(file, "r") as json_file:
        json_data = json.load(json_file)

    json_data = borrar_microbloques_vacios(json_data)

    tipos = json_data[str(macro)][dominio]

    tipos_list = []
    for tipo in tipos:
        microbloques = []
        for microbloque in tipos[tipo]["micro_bloques"].values():
            microbloques.append(MicroBloqueDto(**microbloque))
        tipos_list.append(TipoMicroBloqueDto(nombre_tipo=tipo, descripcion_tipo=tipos[tipo]["descripcion"], micro_bloques=microbloques))
    return DominioDto(nombre=dominio, tipos=tipos_list)

def obtener_micorbloques_de_un_tipo(tipo: str, dominio: str, macro: MACROS) -> TipoMicroBloqueDto:
    """
    Obtiene un tipo de un dominio en el archivo json
    """
    if not os.path.exists(file):
        crear_json_para_dominios()

    with open(file, "r") as json_file:
        json_data = json.load(json_file)

    json_data = borrar_microbloques_vacios(json_data)

    microbloques = []
    for microbloque in json_data[str(macro)][dominio][tipo]["micro_bloques"].values():
        microbloques.append(MicroBloqueDto(**microbloque))

    return TipoMicroBloqueDto(nombre_tipo=tipo, descripcion_tipo=json_data[str(macro)][dominio][tipo]["descripcion"], micro_bloques=microbloques)

def borrar_tipo(tipo: str, dominio: str, macro: MACROS) -> None:
    """
    Borra un tipo de un dominio en el archivo json
    """
    if not os.path.exists(file):
        crear_json_para_dominios()

    with open(file, "r") as json_file:
        json_data = json.load(json_file)

    del json_data[str(macro)][dominio][tipo]

    json_data = borrar_microbloques_vacios(json_data)

    with open(file, "w") as json_file:
        json.dump(json_data, json_file, indent=4)

def borrar_micro_bloque(tipo: str, dominio: str, macro: MACROS, microbloque: MicroBloqueDto) -> None:
    """
    Borra un microbloque de un tipo en el archivo json
    """
    if not os.path.exists(file):
        crear_json_para_dominios()

    with open(file, "r") as json_file:
        json_data = json.load(json_file)

    del json_data[str(macro)][dominio][tipo]["micro_bloques"][microbloque.nombre]

    json_data = borrar_microbloques_vacios(json_data)

    with open(file, "w") as json_file:
        json.dump(json_data, json_file, indent=4)

def borrar_microbloques_vacios(json_data) -> dict:
    """
    Borra microbloques vacíos del archivo JSON.
    """
    for macro in MACROS:
        for dominio in json_data[str(macro)].keys():
            tipos_a_borrar = []  # Lista para recopilar tipos a eliminar
            for tipo in json_data[str(macro)][dominio].keys():
                if not json_data[str(macro)][dominio][tipo]["micro_bloques"]:
                    tipos_a_borrar.append(tipo)  # Agregar a la lista para eliminar

            for tipo in tipos_a_borrar:
                del json_data[str(macro)][dominio][tipo]

    return json_data

def crear_desde_backup() -> None:
    """
    Crea el archivo json con los datos del backup
    """
    if os.path.exists(backup_datos):
        with open(backup_datos, "r") as json_file:
            json_data = json.load(json_file)

        with open(file, "w") as json_file:
            json.dump(json_data, json_file, indent=4)

def recrear_datos():
    """
    Borra el archivo json y lo vuelve a crear
    """
    if os.path.exists(file):
        os.remove(file)
    try:
        crear_desde_backup()
    except:
        crear_json_para_dominios()