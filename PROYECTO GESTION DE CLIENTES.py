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

    @property
    def email(self):
        return self._email

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

    def confirmar(self):
        self.costo = self.servicio.calcular_costo()
        self.estado = "Confirmada"
        return self.costo

# ---------------- INTERFAZ ----------------
def crear_interfaz():
    root = tk.Tk()
    root.title("Sistema de Reservas")
    root.geometry("850x650")

    main = ttk.Frame(root, padding=20)
    main.pack(fill="both", expand=True)

    ttk.Label(main, text="Sistema de Reservas", font=("Segoe UI", 18, "bold")).pack(pady=10)

    form = ttk.Frame(main)
    form.pack(pady=10)

    ttk.Label(form, text="Nombre").grid(row=0, column=0)
    entry_nombre = ttk.Entry(form, width=35)
    entry_nombre.grid(row=0, column=1)

    ttk.Label(form, text="Email").grid(row=1, column=0)
    entry_email = ttk.Entry(form, width=35)
    entry_email.grid(row=1, column=1)

    ttk.Label(form, text="Servicio").grid(row=2, column=0)
    combo_servicio = ttk.Combobox(form, state="readonly",
        values=["Reserva Sala", "Alquiler Equipo", "Asesoría"])
    combo_servicio.grid(row=2, column=1)

    ttk.Label(form, text="Cantidad").grid(row=3, column=0)
    entry_cantidad = ttk.Entry(form, width=35)
    entry_cantidad.grid(row=3, column=1)

    resultado = tk.StringVar()
    ttk.Label(main, textvariable=resultado, foreground="green").pack(pady=10)

    columnas = ("Cliente", "Servicio", "Estado")
    tabla = ttk.Treeview(main, columns=columnas, show="headings")

    for col in columnas:
        tabla.heading(col, text=col)

    tabla.pack(pady=10, fill="x")

    # -------- SELECCIONAR --------
    def seleccionar_reserva(event):
        seleccionado = tabla.selection()
        if not seleccionado:
            return

        item = seleccionado[0]
        indice = tabla.index(item)
        reserva = reservas[indice]

        entry_nombre.delete(0, tk.END)
        entry_nombre.insert(0, reserva.cliente.nombre)

        entry_email.delete(0, tk.END)
        entry_email.insert(0, reserva.cliente.email)

        if isinstance(reserva.servicio, ReservaSala):
            combo_servicio.set("Reserva Sala")
            cantidad = reserva.servicio.horas
        elif isinstance(reserva.servicio, AlquilerEquipo):
            combo_servicio.set("Alquiler Equipo")
            cantidad = reserva.servicio.dias
        else:
            combo_servicio.set("Asesoría")
            cantidad = reserva.servicio.horas

        entry_cantidad.delete(0, tk.END)
        entry_cantidad.insert(0, str(cantidad))

    tabla.bind("<<TreeviewSelect>>", seleccionar_reserva)

    # -------- LIMPIAR SELECCION --------
    def limpiar_seleccion(event):
        item = tabla.identify_row(event.y)
        if not item:
            tabla.selection_remove(tabla.selection())
            entry_nombre.delete(0, tk.END)
            entry_email.delete(0, tk.END)
            entry_cantidad.delete(0, tk.END)
            combo_servicio.set("")

    tabla.bind("<Button-1>", limpiar_seleccion)

    # -------- FUNCIONES --------
    def procesar():
        try:
            cliente = Cliente(len(clientes)+1, entry_nombre.get(), entry_email.get())
            clientes.append(cliente)

            cantidad = int(entry_cantidad.get())
            tipo = combo_servicio.get()

            if tipo == "Reserva Sala":
                servicio = ReservaSala(cantidad)
            elif tipo == "Alquiler Equipo":
                servicio = AlquilerEquipo(cantidad)
            else:
                servicio = Asesoria(cantidad)

            reserva = Reserva(cliente, servicio)
            reservas.append(reserva)
            reserva.confirmar()

            tabla.insert("", "end", values=(cliente.nombre, servicio.descripcion(), reserva.estado))
            resultado.set(f"✔ Costo: ${reserva.costo}")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def modificar_reserva():
        try:
            seleccionado = tabla.selection()
            if not seleccionado:
                raise Exception("Seleccione una reserva")

            item = seleccionado[0]
            indice = tabla.index(item)

            cliente = Cliente(indice+1, entry_nombre.get(), entry_email.get())

            cantidad = int(entry_cantidad.get())
            tipo = combo_servicio.get()

            if tipo == "Reserva Sala":
                servicio = ReservaSala(cantidad)
            elif tipo == "Alquiler Equipo":
                servicio = AlquilerEquipo(cantidad)
            else:
                servicio = Asesoria(cantidad)

            reserva = Reserva(cliente, servicio)
            reserva.confirmar()

            reservas[indice] = reserva
            tabla.item(item, values=(cliente.nombre, servicio.descripcion(), reserva.estado))

            resultado.set(f"✔ Modificada | ${reserva.costo}")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def cerrar_app():
        if messagebox.askyesno("Salir", "¿Deseas cerrar la aplicación?"):
            root.destroy()

    botones = ttk.Frame(main)
    botones.pack(pady=10)

    ttk.Button(botones, text="Procesar", command=procesar).grid(row=0, column=0, padx=10)
    ttk.Button(botones, text="Modificar", command=modificar_reserva).grid(row=0, column=1, padx=10)
    ttk.Button(botones, text="Cerrar", command=cerrar_app).grid(row=0, column=2, padx=10)

    root.mainloop()

# ---------------- MAIN ----------------
if __name__ == "__main__":
    crear_interfaz()
    