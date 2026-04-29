from abc import ABC, abstractmethod
import logging
from datetime import datetime

# ---------------- VALIDACIONES REUTILIZABLES ----------------
def validar_texto_vacio(valor, campo):
    if not valor or valor.strip() == "":
        raise ValueError(f"El campo {campo} no puede estar vacío")

def validar_email(email):
    if "@" not in email or "." not in email:
        raise ValueError("Email inválido")

def validar_numero_positivo(valor, campo):
    if valor <= 0:
        raise ValueError(f"{campo} debe ser mayor que 0")

# ---------------- LOGS ----------------
logging.basicConfig(
    filename="logs.txt",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

# ---------------- EXCEPCIONES ----------------
class ErrorSistema(Exception):
    pass

class ClienteError(ErrorSistema):
    pass

class ServicioError(ErrorSistema):
    pass

class ReservaError(ErrorSistema):
    pass

# ---------------- CLASE ABSTRACTA ----------------
class Entidad(ABC):
    def __init__(self, id):
        self._id = id
        
    def get_id(self):
        return self._id
    
    @abstractmethod
    def mostrar_info(self):
        pass

# ---------------- CLIENTE ----------------
class Cliente(Entidad):
    def __init__(self, id, nombre, email):
        super().__init__(id)
        self.set_nombre(nombre)
        self.set_email(email)

    def set_nombre(self, nombre):
        try:
            validar_texto_vacio(nombre, "nombre")
            self._nombre = nombre
        except Exception as e:
            logging.error(str(e))
            raise ClienteError("Error en nombre") from e

    def set_email(self, email):
        try:
            validar_email(email)
            self._email = email
        except Exception as e:
            logging.error(str(e))
            raise ClienteError("Error en email") from e
    
    def get_nombre(self):
        return self._nombre
    
    def get_email(self):
        return self._email

    def mostrar_info(self):
        return f"Cliente: [{self.get_id()}]: {self.get_nombre()} - {self.get_email()}"

# ---------------- SERVICIO ABSTRACTO ----------------
class Servicio(ABC):
    def __init__(self, nombre):
        self._nombre = nombre
        
    def get_nombre(self):
        return self._nombre
    
    @abstractmethod
    def calcular_costo(self):
        pass

    @abstractmethod
    def descripcion(self):
        pass

    # 🔥 MÉTODO SOBRECARGADO
    def calcular_costo_con_descuento(self, descuento=0):
        if descuento < 0 or descuento > 100:
            raise ServicioError("Descuento invalido")
        costo = self.calcular_costo()
        if descuento > 0:
            costo -= costo * (descuento / 100)
        return costo

# ---------------- SERVICIOS ----------------
class ReservaSala(Servicio):
    def __init__(self, horas):
        super().__init__("Reserva de Sala")
        self.horas = horas

    def calcular_costo(self):
        validar_numero_positivo(self.horas, "horas")
        return self.horas * 50000

    def descripcion(self):
        return f"Sala por {self.horas} horas"

class AlquilerEquipo(Servicio):
    def __init__(self, dias):
        super().__init__("Alquiler de Equipo")
        self.dias = dias

    def calcular_costo(self):
        validar_numero_positivo(self.dias, "días")
        return self.dias * 30000

    def descripcion(self):
        return f"Equipo por {self.dias} días"

class Asesoria(Servicio):
    def __init__(self, horas):
        super().__init__("Asesoría")
        self.horas = horas

    def calcular_costo(self):
        validar_numero_positivo(self.horas, "horas")
        return self.horas * 80000

    def descripcion(self):
        return f"Asesoría por {self.horas} horas"

# ---------------- RESERVA ----------------
class Reserva:
    def __init__(self, cliente, servicio):
        if not isinstance(cliente, Cliente):
            raise ReservaError("Cliente invalido")
        if not isinstance(servicio, Servicio):
            raise ReservaError("Servicio invalido")
        
        self.cliente = cliente
        self.servicio = servicio
        self.estado = "Pendiente"
        self.fecha = datetime.now()

    def confirmar(self):
        try:
            if self.estado == "Confirmada":
                raise ReservaError("La reserva ya esta confirmada")
            
            costo = self.servicio.calcular_costo()
            
        except Exception as e:
            logging.error(str(e))
            raise ReservaError("Error al confirmar reserva") from e
        
        else:
            self.estado = "Confirmada"
            logging.info(f"Reserva confirmada para {self.cliente.get_nombre()}")
            print(f"Reserva confirmada. Costo: {costo}")
        
        finally:
            logging.info("Intento de confirmacion procesado")
            
        if self.estado == "Cancelada":
            raise ReservaError("No se puede confirmar una reserva cancelada")
        
    def cancelar(self):
        if self.estado == "Cancelada":
            raise ReservaError("La reserva ya esta cancelada")
        
        if self.estado == "Confirmada":
            raise ReservaError("No se puede cancelar una reserva confirmada")
        
        self.estado = "Cancelada"
        logging.info(f"Reserva cancelada: {self.cliente.get_nombre()}")
        print("Reserva cancelada")

    def mostrar(self):
        return f"{self.cliente.mostrar_info()} | {self.servicio.descripcion()} | Estado: {self.estado}"

# ---------------- SIMULACIÓN ----------------
def simulacion():
    operaciones = []

    for i in range(10):
        try:
            # Cliente (algunos inválidos)
            if i == 2:
                cliente = Cliente(i, "", "correo.com")
            else:
                cliente = Cliente(i, f"Cliente{i}", f"cliente{i}@correo.com")

            # Servicio (algunos inválidos)
            if i % 3 == 0:
                servicio = ReservaSala(i - 2)
            elif i % 3 == 1:
                servicio = AlquilerEquipo(i)
            else:
                servicio = Asesoria(i)

            reserva = Reserva(cliente, servicio)

            # 🔥 uso del método con descuento
            costo = servicio.calcular_costo_con_descuento(10)
            print(f"Costos con descuento: {costo}")
            logging.info(f"Costo calculado con descuentos: {costo}")
            
            reserva.confirmar()

            operaciones.append(reserva.mostrar())

        except Exception as e:
            logging.error(str(e))
            print(f"Error controlado: {e}")

        finally:
            print("Operación procesada\n")

    print("\n--- RESUMEN ---")
    for op in operaciones:
        print(op)

# ---------------- MAIN ----------------
if __name__ == "__main__":
    simulacion()
    