from abc import ABC, abstractmethod
import logging
from datetime import datetime

# ---------------- LOGS ----------------
logging.basicConfig(
    filename="logs.txt",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s"
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
        if not nombre:
            raise ClienteError("Nombre inválido")
        self._nombre = nombre

    def set_email(self, email):
        if "@" not in email:
            raise ClienteError("Email inválido")
        self._email = email

    def mostrar_info(self):
        return f"Cliente: {self._nombre} - {self._email}"

# ---------------- SERVICIO ABSTRACTO ----------------
class Servicio(ABC):
    def __init__(self, nombre):
        self.nombre = nombre

    @abstractmethod
    def calcular_costo(self):
        pass

    @abstractmethod
    def descripcion(self):
        pass

# ---------------- SERVICIOS ----------------
class ReservaSala(Servicio):
    def __init__(self, horas):
        super().__init__("Reserva de Sala")
        self.horas = horas

    def calcular_costo(self):
        if self.horas <= 0:
            raise ServicioError("Horas inválidas")
        return self.horas * 50000

    def descripcion(self):
        return f"Sala por {self.horas} horas"

class AlquilerEquipo(Servicio):
    def __init__(self, dias):
        super().__init__("Alquiler de Equipo")
        self.dias = dias

    def calcular_costo(self):
        if self.dias <= 0:
            raise ServicioError("Días inválidos")
        return self.dias * 30000

    def descripcion(self):
        return f"Equipo por {self.dias} días"

class Asesoria(Servicio):
    def __init__(self, horas):
        super().__init__("Asesoría")
        self.horas = horas

    def calcular_costo(self):
        if self.horas <= 0:
            raise ServicioError("Horas inválidas")
        return self.horas * 80000

    def descripcion(self):
        return f"Asesoría por {self.horas} horas"

# ---------------- RESERVA ----------------
class Reserva:
    def __init__(self, cliente, servicio):
        self.cliente = cliente
        self.servicio = servicio
        self.estado = "Pendiente"

    def confirmar(self):
        try:
            costo = self.servicio.calcular_costo()
            self.estado = "Confirmada"
            print(f"Reserva confirmada. Costo: {costo}")
        except Exception as e:
            logging.error(str(e))
            raise ReservaError("Error al confirmar reserva") from e

    def cancelar(self):
        self.estado = "Cancelada"
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
                cliente = Cliente(i, "", "correo.com")  # error
            else:
                cliente = Cliente(i, f"Cliente{i}", f"cliente{i}@correo.com")

            # Servicio (algunos inválidos)
            if i % 3 == 0:
                servicio = ReservaSala(i - 2)  # puede dar error
            elif i % 3 == 1:
                servicio = AlquilerEquipo(i)
            else:
                servicio = Asesoria(i)

            reserva = Reserva(cliente, servicio)

            # Confirmar reserva
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