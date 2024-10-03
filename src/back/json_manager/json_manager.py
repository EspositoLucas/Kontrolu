import json
from back.macros.macro_bloque import MACROS
from back.json_manager.dtos import DominioDto, MicroBloqueDto, TipoMicroBloqueDto


file = "datos.json"



def crear_json_para_dominios(dominios: list[str] = ["SISTEMAS","ELECTRONICA"]) -> None:
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

def __agregar_dominio(dominio: str,json) -> json:
    """
    Agrega un dominio al json
    """
    json["dominios"].append(dominio)
    json[str(MACROS.CONTROLADOR)][dominio] = {}
    json[str(MACROS.ACTUADOR)][dominio] = {}
    json[str(MACROS.PROCESO)][dominio] = {}
    json[str(MACROS.MEDIDOR)][dominio] = {}
    return json

def agregar_dominios(dominios: list[str] = None, dominio: str = None) -> None:
    """
    Agrega dominios al archivo json
    """
    doms = []
    if dominio:
        doms.append(dominio)
    if dominios:
        doms.extend(dominios)

    with open(file, "r") as json_file:
        json_data = json.load(json_file)
        json_file.close()

    for dominio in doms:
        if dominio not in json_data["dominios"]:
            json_data = __agregar_dominio(dominio,json_data)

    with open(file, "w") as json_file:
        json.dump(json_data, json_file, indent=4)




def borrar_dominios(dominios: list[str] = None, dominio: str = None) -> None:
    """
    Borra dominios del archivo json
    """
    doms = []
    if dominio:
        doms.append(dominio)
    if dominios:
        doms.extend(dominios)

    with open(file, "r") as json_file:
        json_data = json.load(json_file)
        json_file.close()

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
    with open(file, "r") as json_file:
        json_data = json.load(json_file)
        json_file.close()

    return json_data["dominios"]

def __crear_tipo(tipo: str, dominio: str, macro: MACROS, json_data, descripcion: str = "") -> json:
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
    with open(file, "r") as json_file:
        json_data = json.load(json_file)
        json_file.close()

    json_data[str(macro)][dominio][tipo] = {
        "descripcion": descripcion,
        "micro_bloques": {}
    }

    with open(file, "w") as json_file:
        json.dump(json_data, json_file, indent=4)

def agregar_microbloque(microbloque: MicroBloqueDto, tipo: str, dominio: str, macro: MACROS) -> None:
    """
    Agrega un microbloque a un tipo en el archivo json
    """
    with open(file, "r") as json_file:
        json_data = json.load(json_file)
        json_file.close()
    #check if dominio exist, if not create, check if tipo exist, if not create
    if dominio not in json_data["dominios"]:
        json_data = __agregar_dominio(dominio,json_data)
    
    if tipo not in json_data[str(macro)][dominio]:
        json_data = __crear_tipo(tipo, dominio, macro,json_data)
         
    json_data[str(macro)][dominio][tipo]["micro_bloques"][microbloque.nombre] = microbloque.__dict__

    with open(file, "w") as json_file:
        json.dump(json_data, json_file, indent=4)

def obtener_microbloques_de_una_macro(macro: MACROS) -> list[DominioDto]:
    """
    Obtiene los dominios de una macro en el archivo json
    """
    with open(file, "r") as json_file:
        json_data = json.load(json_file)
        json_file.close()

    dominios = []
    for dominio in json_data[str(macro)].keys():
        tipos = []
        for tipo in json_data[str(macro)][dominio].keys():
            microbloques = []
            for microbloque in json_data[str(macro)][dominio][tipo]["micro_bloques"].values():
                microbloques.append(MicroBloqueDto(**microbloque))
            tipos.append(TipoMicroBloqueDto(nombre_tipo=tipo,descripcion_tipo= json_data[str(macro)][dominio][tipo]["descripcion"],micro_bloques=microbloques))
        dominios.append(DominioDto(nombre=dominio, tipos=tipos))
    return dominios

def obtener_microbloques_de_un_dominio(dominio: str, macro: MACROS) -> list[TipoMicroBloqueDto]:
    """
    Obtiene los tipos de un dominio en el archivo json
    """
    with open(file, "r") as json_file:
        json_data = json.load(json_file)
        json_file.close()

    tipos = json_data[str(macro)][dominio]

    tipos_list = []
    for tipo in tipos:
        microbloques = []
        for microbloque in tipos[tipo]["micro_bloques"].values():
            microbloques.append(MicroBloqueDto(**microbloque))
        tipos_list.append(TipoMicroBloqueDto(nombre_tipo=tipo,descripcion_tipo= tipos[tipo]["descripcion"],micro_bloques=microbloques))
    return DominioDto(nombre=dominio, tipos=tipos_list)

def obtener_micorbloques_de_un_tipo(tipo: str, dominio: str, macro: MACROS) -> TipoMicroBloqueDto:
    """
    Obtiene un tipo de un dominio en el archivo json
    """
    with open(file, "r") as json_file:
        json_data = json.load(json_file)
        json_file.close()

    microbloques = []
    for microbloque in json_data[str(macro)][dominio][tipo]["micro_bloques"].values():
        microbloques.append(MicroBloqueDto(**microbloque))

    return TipoMicroBloqueDto(nombre_tipo=tipo,descripcion_tipo= json_data[str(macro)][dominio][tipo]["descripcion"],micro_bloques=microbloques)

def borrar_tipo(tipo: str, dominio: str, macro: MACROS) -> None:
    """
    Borra un tipo de un dominio en el archivo json
    """
    with open(file, "r") as json_file:
        json_data = json.load(json_file)
        json_file.close()

    del json_data[str(macro)][dominio][tipo]

    with open(file, "w") as json_file:
        json.dump(json_data, json_file, indent=4)

def borrar_micro_bloque(tipo: str, dominio: str, macro: MACROS, microbloque: MicroBloqueDto) -> None:
    """
    Borra un microbloque de un tipo en el archivo json
    """
    with open(file, "r") as json_file:
        json_data = json.load(json_file)
        json_file.close()

    del json_data[str(macro)][dominio][tipo]["micro_bloques"][microbloque.nombre]

    with open(file, "w") as json_file:
        json.dump(json_data, json_file, indent=4)
"""

#Populame el json
crear_json_para_dominios()
#creame tipos en distintos dominios en distintas macros
crear_tipo("tipo1", "SISTEMAS", MACROS.CONTROLADOR, "descripcion")
crear_tipo("tipo2", "SISTEMAS", MACROS.CONTROLADOR, "descripcion")
crear_tipo("tipo3", "SISTEMAS", MACROS.CONTROLADOR, "descripcion")

crear_tipo("tipo1", "SISTEMAS", MACROS.ACTUADOR, "descripcion")
crear_tipo("tipo2", "SISTEMAS", MACROS.ACTUADOR, "descripcion")

crear_tipo("tipo1", "SISTEMAS", MACROS.PROCESO, "descripcion")
crear_tipo("tipo2", "SISTEMAS", MACROS.PROCESO, "descripcion")

crear_tipo("tipo1", "SISTEMAS", MACROS.MEDIDOR, "descripcion")
crear_tipo("tipo2", "SISTEMAS", MACROS.MEDIDOR, "descripcion")
#agregame microbloques a los tipos
agregar_microbloque(MicroBloqueDto("one", "descripcion", "fdt", 1.0, 2.0, 3.0, 4.0, 5.0, "tipo", 6.0, 7.0, 1.0, 2.0, 3.0, 4.0, 5.0, "tipo", 6.0, 7.0, "unidad", "unidad"), "tipo2", "SISTEMAS", MACROS.CONTROLADOR)
agregar_microbloque(MicroBloqueDto("two", "descripcion", "fdt", 1.0, 2.0, 3.0, 4.0, 5.0, "tipo", 6.0, 7.0, 1.0, 2.0, 3.0, 4.0, 5.0, "tipo", 6.0, 7.0, "unidad", "unidad"), "tipo1", "SISTEMAS", MACROS.CONTROLADOR)
#mas microbloques
agregar_microbloque(MicroBloqueDto("three", "descripcion", "fdt", 1.0, 2.0, 3.0, 4.0, 5.0, "tipo", 6.0, 7.0, 1.0, 2.0, 3.0, 4.0, 5.0, "tipo", 6.0, 7.0, "unidad", "unidad"), "tipo2", "SISTEMAS", MACROS.MEDIDOR)
agregar_microbloque(MicroBloqueDto("four", "descripcion", "fdt", 1.0, 2.0, 3.0, 4.0, 5.0, "tipo", 6.0, 7.0, 1.0, 2.0, 3.0, 4.0, 5.0, "tipo", 6.0, 7.0, "unidad", "unidad"), "tipo1", "SISTEMAS", MACROS.ACTUADOR)
#mas microbloques
agregar_microbloque(MicroBloqueDto("five", "descripcion", "fdt", 1.0, 2.0, 3.0, 4.0, 5.0, "tipo", 6.0, 7.0, 1.0, 2.0, 3.0, 4.0, 5.0, "tipo", 6.0, 7.0, "unidad", "unidad"), "tipo2", "SISTEMAS", MACROS.PROCESO)
agregar_microbloque(MicroBloqueDto("six", "descripcion", "fdt", 1.0, 2.0, 3.0, 4.0, 5.0, "tipo", 6.0, 7.0, 1.0, 2.0, 3.0, 4.0, 5.0, "tipo", 6.0, 7.0, "unidad", "unidad"), "tipo1", "SISTEMAS", MACROS.PROCESO)
# haceme todo esto para el dominio de electronica
crear_tipo("tipo1", "ELECTRONICA", MACROS.CONTROLADOR, "descripcion")
crear_tipo("tipo2", "ELECTRONICA", MACROS.CONTROLADOR, "descripcion")
crear_tipo("tipo3", "ELECTRONICA", MACROS.CONTROLADOR, "descripcion")

crear_tipo("tipo1", "ELECTRONICA", MACROS.ACTUADOR, "descripcion")
crear_tipo("tipo2", "ELECTRONICA", MACROS.ACTUADOR, "descripcion")

crear_tipo("tipo1", "ELECTRONICA", MACROS.PROCESO, "descripcion")
crear_tipo("tipo2", "ELECTRONICA", MACROS.PROCESO, "descripcion")

crear_tipo("tipo1", "ELECTRONICA", MACROS.MEDIDOR, "descripcion")
crear_tipo("tipo2", "ELECTRONICA", MACROS.MEDIDOR, "descripcion")
#agregame microbloques a los tipos
agregar_microbloque(MicroBloqueDto("one", "descripcion", "fdt", 1.0, 2.0, 3.0, 4.0, 5.0, "tipo", 6.0, 7.0, 1.0, 2.0, 3.0, 4.0, 5.0, "tipo", 6.0, 7.0, "unidad", "unidad"), "tipo2", "ELECTRONICA", MACROS.CONTROLADOR)
agregar_microbloque(MicroBloqueDto("two", "descripcion", "fdt", 1.0, 2.0, 3.0, 4.0, 5.0, "tipo", 6.0, 7.0, 1.0, 2.0, 3.0, 4.0, 5.0, "tipo", 6.0, 7.0, "unidad", "unidad"), "tipo1", "ELECTRONICA", MACROS.CONTROLADOR)
#mas microbloques
agregar_microbloque(MicroBloqueDto("three", "descripcion", "fdt", 1.0, 2.0, 3.0, 4.0, 5.0, "tipo", 6.0, 7.0, 1.0, 2.0, 3.0, 4.0, 5.0, "tipo", 6.0, 7.0, "unidad", "unidad"), "tipo2", "ELECTRONICA", MACROS.MEDIDOR)
#agregar_microbloque(MicroBloqueDto("one", "descripcion", "fdt", 1.0, 2.0, 3.0, 4.0, 5.0, "tipo", 6.0, 7.0, 1.0, 2.0, 3.0, 4.0, 5.0, "tipo", 6.0, 7.0, "unidad", "unidad"), "tipo2", "SISTEMAS", MACROS.CONTROLADOR)
#agregar_microbloque(MicroBloqueDto("two", "descripcion", "fdt", 1.0, 2.0, 3.0, 4.0, 5.0, "tipo", 6.0, 7.0, 1.0, 2.0, 3.0, 4.0, 5.0, "tipo", 6.0, 7.0, "unidad", "unidad"), "tipo1", "SISTEMAS", MACROS.CONTROLADOR)
#print(obtener_micorbloques_de_un_tipo("tipo2", "SISTEMAS", MACROS.CONTROLADOR))
#crear_tipo("tipo2", "SISTEMAS", MACROS.CONTROLADOR, "descripcion")"""