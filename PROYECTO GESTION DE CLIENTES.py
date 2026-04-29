from abc import ABC, abstractmethod
import logging
import tkinter as tk
from tkinter import ttk, messagebox

# ---------------- VALIDACIONES ----------------
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
    format="%(asctime)s - %(levelname)s - %(message)s"
)
# ---------------- LISTAS ----------------
clientes = []  
reservas = [] 

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
    
    @property
    def nombre(self):
        return self._nombre

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

    def calcular_costo_con_descuento(self, descuento=0):
        if descuento < 0 or descuento > 100:
            raise ValueError("Descuento debe estar entre 0 y 100")
        costo = self.calcular_costo()
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
        self.cliente = cliente
        self.servicio = servicio
        self.estado = "Pendiente"
        self.costo = 0
        
    def validar_reserva(self):
        if self.cliente is None:
            raise ReservaError("La reserva no tiene cliente asignado")
        if self.servicio is None:
            raise ReservaError("La reserva no tiene servicio asignado") 
        
    def confirmar(self):
        try:
            self.validar_reserva()
            self.costo = self.servicio.calcular_costo()
        except Exception as e:
            logging.error(str(e))
            raise ReservaError("Error al confirmar reserva") from e
        else: 
            self.estado = "Confirmada"
            logging.info(f"Reserva confirmada para {self.cliente.nombre}")
            print (f"Reserva confirmada. Costo: {self.costo}")
            return self.costo
            
        finally:
            logging.info("Proceso de confirmación finalizado")
            
             
    def cancelar(self):
        self.estado = "Cancelada"
        logging.info("Reserva cancelada")
        print ("Reserva cancelada")

    def mostrar(self):
        return f"{self.cliente.mostrar_info()} | {self.servicio.descripcion()} | Estado: {self.estado}"

# ---------------- INTERFAZ ----------------
def crear_interfaz():
    root = tk.Tk()
    root.title("Sistema de Gestión de Clientes")
    root.geometry("500x500")

    # Campos
    ttk.Label(root, text="Nombre").grid(row=0, column=0, padx=5, pady=5)
    entry_nombre = ttk.Entry(root)
    entry_nombre.grid(row=0, column=1)

    ttk.Label(root, text="Email").grid(row=1, column=0, padx=5, pady=5)
    entry_email = ttk.Entry(root)
    entry_email.grid(row=1, column=1)

    ttk.Label(root, text="Servicio").grid(row=2, column=0, padx=5, pady=5)
    combo_servicio = ttk.Combobox(root, values=[
        "Reserva Sala", "Alquiler Equipo", "Asesoría"
    ])
    combo_servicio.grid(row=2, column=1)

    ttk.Label(root, text="Cantidad").grid(row=3, column=0, padx=5, pady=5)
    entry_cantidad = ttk.Entry(root)
    entry_cantidad.grid(row=3, column=1)

    resultado = tk.StringVar()
    ttk.Label(root, textvariable=resultado).grid(row=5, column=0, columnspan=2, pady=10)

    def procesar():
        try:
            nombre = entry_nombre.get()
            email = entry_email.get()
            servicio_tipo = combo_servicio.get()
            
            try:
                cantidad = int(entry_cantidad.get())
            except ValueError:
                raise ValueError("Cantidad debe ser un número entero")

            cliente = Cliente(len(clientes) + 1, nombre, email)
            clientes.append(cliente)

            if servicio_tipo == "Reserva Sala":
                servicio = ReservaSala(cantidad)
            elif servicio_tipo == "Alquiler Equipo":
                servicio = AlquilerEquipo(cantidad)
            elif servicio_tipo == "Asesoría":
                servicio = Asesoria(cantidad)
            else:
                raise ValueError("Seleccione un servicio válido")

            reserva = Reserva(cliente, servicio)
            reservas.append(reserva)
            
            costo = reserva.confirmar()
            
            resultado.set(f"Costo: {reserva.costo} | Estado: {reserva.estado}")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    ttk.Button(root, text="Procesar", command=procesar).grid(row=4, column=0, columnspan=2, pady=10)

    root.mainloop()

# ---------------- MAIN ----------------
if __name__ == "__main__":
    crear_interfaz()
    