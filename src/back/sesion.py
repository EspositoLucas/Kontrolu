from .macros.macro_actuador import MacroActuador
from .macros.macro_controlador import MacroControlador
from .macros.macro_medidor import MacroMedidor
from .macros.macro_proceso import MacroProceso
from back.topologia.microbloque import MicroBloque
from .topologia.carga import Carga
from sympy import simplify, latex,inverse_laplace_transform,degree
from sympy.abc import s,z,t



class Sesion():
    def __init__(self):
        self.nueva_sesion()
    
    def nueva_sesion(self):
        self.entrada = MicroBloque(nombre="Entrada")
        self.controlador = MacroControlador(sesion=self)
        self.actuador = MacroActuador(sesion=self)
        self.proceso = MacroProceso(sesion=self)
        self.medidor = MacroMedidor(sesion=self)
        self.carga = Carga(entrada=self.entrada)
        self.tiempo_total = 10
        self.salida_inicial = 0
        self.delta_t = 1
        self.velocidad = 1000
        self.nombre = "Sistema de Control"

    def validar_entrada_controlador(self, unidad: str)-> bool:
        return self.medidor.unidad_salida() == unidad
    def validar_salida_controlador(self, unidad: str)-> bool:
        return self.actuador.unidad_entrada() == unidad
    
    def validar_entrada_actuador(self, unidad: str)-> bool:
        return self.controlador.unidad_salida() == unidad
    def validar_salida_actuador(self, unidad: str)-> bool:
        return self.proceso.unidad_entrada() == unidad
    
    def validar_entrada_proceso(self, unidad: str)-> bool:
        return self.actuador.unidad_salida() == unidad
    def validar_salida_proceso(self, unidad: str)-> bool:
        return self.medidor.unidad_entrada() == unidad
    
    def validar_entrada_medidor(self, unidad: str)-> bool:
        return self.proceso.unidad_salida() == unidad
    def validar_salida_medidor(self, unidad: str)-> bool:
        return self.controlador.unidad_entrada() == unidad
    
    def unidad_recibida_controlador(self)-> str:
        return self.medidor.unidad_salida()
    def unidad_recibida_actuador(self)-> str:
        return self.controlador.unidad_salida()
    def unidad_recibida_proceso(self)-> str:
        return self.actuador.unidad_salida()
    def unidad_recibida_medidor(self)-> str:
        return self.proceso.unidad_salida()
    
    def unidad_esperada_controlador(self)-> str:
        return self.actuador.unidad_entrada()
    def unidad_esperada_actuador(self)-> str:
        return self.proceso.unidad_entrada()
    def unidad_esperada_proceso(self)-> str:
        return self.medidor.unidad_entrada()
    def unidad_esperada_medidor(self)-> str:
        return self.controlador.unidad_entrada()
    
    def to_json(self) -> str:
        return {
            "entrada": self.entrada.to_json(),
            "controlador": self.controlador.to_json(),
            "actuador": self.actuador.to_json(),
            "proceso": self.proceso.to_json(),
            "medidor": self.medidor.to_json(),
            "carga": self.carga.to_json(),
            "tiempo_total": self.tiempo_total,
            "salida_inicial": self.salida_inicial,
            "delta_t": self.delta_t,
            "velocidad": self.velocidad,
            "nombre": self.nombre
        }
    
    def from_json(self, datos: dict):
        self.entrada = MicroBloque(from_json = datos["entrada"])
        self.controlador = MacroControlador(from_json = datos["controlador"])
        self.controlador.sesion = self
        self.actuador = MacroActuador(from_json = datos["actuador"])
        self.actuador.sesion = self
        self.proceso = MacroProceso(from_json = datos["proceso"])
        self.proceso.sesion = self
        self.medidor = MacroMedidor(from_json = datos["medidor"])
        self.medidor.sesion = self
        self.carga = Carga(from_json = datos["carga"])
        self.carga.entrada = self.entrada
        self.tiempo_total = float(datos["tiempo_total"])
        self.salida_inicial = float(datos["salida_inicial"])
        self.delta_t = float(datos["delta_t"])
        self.velocidad = float(datos["velocidad"])
        self.nombre = datos["nombre"]

    @staticmethod
    def validar_dict(datos: dict) -> bool:
        required_keys = ["entrada", "controlador", "actuador", "proceso", "medidor", "carga", "nombre", "tiempo_total", "salida_inicial", "delta_t", "velocidad"]
        for key in required_keys:
            if key not in datos:
                raise Exception(f"El diccionario no contiene la clave {key}")
        
        if not isinstance(datos["nombre"], str):
            raise Exception("El nombre de la sesión debe ser un string")
        

        try:
            MicroBloque.validar_dict(datos["entrada"])
        except Exception as e:
            raise Exception(f"Error en la entrada: {e}")
        
        try:
            MacroControlador.validar_dict(datos["controlador"])
        except Exception as e:
            raise Exception(f"Error en el controlador: {e}")
        
        try:
            MacroActuador.validar_dict(datos["actuador"])
        except Exception as e:
            raise Exception(f"Error en el actuador: {e}")
        
        try:
            MacroProceso.validar_dict(datos["proceso"])
        except Exception as e:
            raise Exception(f"Error en el proceso: {e}")
        
        try:
            MacroMedidor.validar_dict(datos["medidor"])
        except Exception as e:
            raise Exception(f"Error en el medidor: {e}")

        try:   
            Carga.validar_dict(datos["carga"])
        except Exception as e:
            raise Exception(f"Error en la carga: {e}")
        
        return True
    
    def operar_fdt(self,input):

        return self.calcular_fdt() * input
    

    def calcular_fdt_lazo_abierto(self):

        return self.controlador.calcular_fdt() * self.actuador.calcular_fdt() * self.proceso.calcular_fdt()
    
    def obtener_fdt_lazo_abierto_simpy(self):

        return simplify(self.calcular_fdt_lazo_abierto())
    
    def obtener_fdt_lazo_abierto_latex(self):

        return latex(self.obtener_fdt_lazo_abierto_simpy())
    
    def obtener_fdt_lazo_abierto_simpy_tiempo(self):

        _,denom = self.obtener_fdt_lazo_abierto_simpy().as_numer_denom()

        degree_denom = degree(denom,s)

        if degree_denom >= 4:
            return None

            
        return inverse_laplace_transform(self.obtener_fdt_lazo_abierto_simpy(),s,t)

    def obtener_fdt_lazo_abierto_latex_tiempo(self):
        return latex(self.obtener_fdt_lazo_abierto_simpy_tiempo())
        
    def calcular_fdt_realimentacion(self):

        return self.medidor.calcular_fdt()
    
    def obtener_fdt_realimentacion_simpy(self):

        return simplify(self.calcular_fdt_realimentacion())
    

    
    def obtener_fdt_realimentacion_latex(self):

        return latex(self.obtener_fdt_realimentacion_simpy())
    
    def calcular_fdt_global(self):

        return self.obtener_fdt_lazo_abierto_simpy() / (1 + self.obtener_fdt_lazo_abierto_simpy() * self.obtener_fdt_realimentacion_simpy())
    
    def calcular_fdt_realimentacion_tiempo(self):

        _,denom = self.obtener_fdt_realimentacion_simpy().as_numer_denom()

        degree_denom = degree(denom,s)

        if degree_denom >= 4:
            return None
            
        return inverse_laplace_transform(self.obtener_fdt_realimentacion_simpy(),s,t)
    
    def obtener_fdt_realimentacion_latex_tiempo(self):

        return latex(self.calcular_fdt_realimentacion_tiempo())
    
    def obtener_fdt_global_simpy(self):

        return self.calcular_fdt_global()
    
    def obtener_fdt_global_latex(self):

        return latex(self.obtener_fdt_global_simpy())
    
    def obtener_fdt_global_tiempo(self):
        
        _,denom = self.obtener_fdt_global_simpy().as_numer_denom()

        degree_denom = degree(denom,s)

        if degree_denom >= 4:
            return None
            
        return inverse_laplace_transform(self.obtener_fdt_global_simpy(),s,t)
    
    def obtener_fdt_global_latex_tiempo(self):

        return latex(self.obtener_fdt_global_tiempo())
    
    def calcular_fdt_con_entrada(self):

        return self.calcular_fdt_global() * self.entrada.calcular_fdt()

    def obtener_fdt_con_entrada_simpy(self):
            
        return self.calcular_fdt_con_entrada()
    
    def obtener_fdt_con_entrada_latex(self):

        return latex(self.obtener_fdt_con_entrada_simpy())
    
    def obtener_fdt_con_entrada_tiempo(self):

        _,denom = self.obtener_fdt_con_entrada_simpy().as_numer_denom()

        degree_denom = degree(denom,s)

        if degree_denom >= 4:
            return None


        return inverse_laplace_transform(self.obtener_fdt_con_entrada_simpy(),s,t)
    
    def obtener_fdt_con_entrada_latex_tiempo(self):

        return latex(self.obtener_fdt_con_entrada_tiempo())
    
    def calcular_abierta_si_unitario(self):

        return self.calcular_fdt_lazo_abierto()/(1+self.calcular_fdt_lazo_abierto()*(self.calcular_fdt_realimentacion()-1))
    
    def obtener_abierta_si_unitario_simpy(self):

        return simplify(self.calcular_abierta_si_unitario())
    
    def obtener_abierta_si_unitario_latex(self):

        return latex(self.obtener_abierta_si_unitario_simpy())
    
    def obtener_abierta_si_unitario_sympy_tiempo(self):

        _,denom = self.obtener_abierta_si_unitario_simpy().as_numer_denom()

        degree_denom = degree(denom,s)

        if degree_denom >= 4:
            return None

            
        return inverse_laplace_transform(self.obtener_abierta_si_unitario_simpy(),s,t)
    
    def obtener_abierta_si_unitario_latex_tiempo(self):

        return latex(self.obtener_abierta_si_unitario_sympy_tiempo())
    
    def calcular_sistema_unitario(self):

        return 1/(1+self.calcular_abierta_si_unitario())
    
    def obtener_sistema_unitario_simpy(self):

        return simplify(self.calcular_sistema_unitario())
    
    def obtener_sistema_unitario_latex(self):

        return latex(self.obtener_sistema_unitario_simpy())
    
    def obtener_sistema_unitario_tiempo(self):

        _,denom = self.obtener_sistema_unitario_simpy().as_numer_denom()

        degree_denom = degree(denom,s)

        if degree_denom >= 4:
            return None

        return inverse_laplace_transform(self.obtener_sistema_unitario_simpy(),s,t)
    
    def obtener_sistema_unitario_latex_tiempo(self):

        return latex(self.obtener_sistema_unitario_tiempo())
    
    def calcular_calculo_error_en_estado_estable(self):

        return s*self.entrada.calcular_fdt()*self.obtener_sistema_unitario_simpy()
    
    def obtener_calculo_error_en_estado_estable_simpy(self):

        return simplify(self.calcular_calculo_error_en_estado_estable())
    
    def obtener_calculo_error_en_estado_estable_latex(self):

        return latex(self.obtener_calculo_error_en_estado_estable_simpy())
    
    def obtener_calculo_error_en_estado_estable_tiempo(self):

        
        _,denom = self.obtener_calculo_error_en_estado_estable_simpy().as_numer_denom()

        degree_denom = degree(denom,s)

        if degree_denom >= 4:
            return None

        return inverse_laplace_transform(self.obtener_calculo_error_en_estado_estable_simpy(),s,t)
    
    def obtener_calculo_error_en_estado_estable_latex_tiempo(self):

        return latex(self.obtener_calculo_error_en_estado_estable_tiempo())
    
    def calcular_error_en_estado_estable(self):

        return self.calcular_calculo_error_en_estado_estable().limit(s,0).evalf()



    