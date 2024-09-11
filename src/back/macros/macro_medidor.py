from .macro_bloque import MacroBloque
import numpy as np

class MacroMedidor(MacroBloque):
    def __init__(self):
        super().__init__()
        self.nombre = "Medidor"
        self.precision = 0.1
        self.ruido = 0.005
        self.iteracion = 0  # Contador de iteraciones para el ajuste progresivo
        
    def medir(self, setpoint_deseado, salida_del_sistema):
        # Aumenta el contador de iteración
        self.iteracion += 1

        # Ajuste progresivo: Al principio arroja valores más lejanos, luego más cercanos
        factor_ajuste = min(1, self.iteracion / 100)  # Ajuste que va de 0 a 1 con el tiempo

        # Calcular la magnitud (norma Euclidiana) de la salida del sistema
        magnitud_salida = np.linalg.norm(salida_del_sistema)

        # Error inicial amplio que se ajusta con las iteraciones
        error_precision = np.random.uniform(-self.precision, self.precision) * (1 - factor_ajuste)
        
        # Componente de ruido constante
        error_ruido = np.random.normal(0, self.ruido)

        # Factor de ajuste basado en la magnitud de la salida del sistema
        if magnitud_salida != 0:
            factor_salida = abs(setpoint_deseado / magnitud_salida)
        else:
            factor_salida = 1  # En caso de que la salida sea 0, tomamos 1 como factor por defecto

        # Cuanto mayor sea la magnitud de la salida, mayor el error (para simular inexactitud en salidas grandes)
        if magnitud_salida > 1:
            error_amplificado = (1 - factor_salida) * np.random.uniform(0.05, 0.2) * magnitud_salida
        else:
            error_amplificado = 0

        # Calcular el valor adicional que se suma al setpoint (basado en errores ajustados y amplificados)
        algo = error_precision + error_ruido + error_amplificado

        # Resultado de la medición: setpoint + algo
        medicion_final = setpoint_deseado + algo
        print("medicion_final: ", medicion_final)
        return medicion_final
