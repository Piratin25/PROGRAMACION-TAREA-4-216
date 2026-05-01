from abc import ABC, abstractmethod
import logging
import tkinter as tk
from tkinter import ttk, messagebox

# ---------------- LOGS ----------------
logging.basicConfig(
    filename="logs.txt",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

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
        return f"{self._nombre} - {self._email}"

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
        costo = self.calcular_costo()
        return costo - (costo * (descuento / 100))

# ---------------- SERVICIOS ----------------
class ReservaSala(Servicio):
    def __init__(self, horas):
        super().__init__("Reserva Sala")
        self.horas = horas

    def calcular_costo(self):
        validar_numero_positivo(self.horas, "horas")
        return self.horas * 50000

    def descripcion(self):
        return f"Sala por {self.horas} horas"

class AlquilerEquipo(Servicio):
    def __init__(self, dias):
        super().__init__("Alquiler Equipo")
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
        if not self.cliente:
            raise ReservaError("Reserva sin cliente")
        if not self.servicio:
            raise ReservaError("Reserva sin servicio")

    def confirmar(self):
        try:
            self.validar_reserva()
            self.costo = self.servicio.calcular_costo()
        except Exception as e:
            logging.error(str(e))
            raise ReservaError("Error al confirmar reserva") from e
        else:
            self.estado = "Confirmada"
            logging.info(f"Reserva confirmada: {self.cliente.nombre}")
            return self.costo
        finally:
            logging.info("Proceso de confirmación finalizado")

    def cancelar(self):
        self.estado = "Cancelada"
        logging.info(f"Reserva cancelada: {self.cliente.nombre}")

    def mostrar(self):
        return f"{self.cliente.mostrar_info()} | {self.servicio.descripcion()} | {self.estado}"

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

    entry_nombre = ttk.Entry(form, width=35)
    entry_email = ttk.Entry(form, width=35)
    combo_servicio = ttk.Combobox(form, state="readonly",
        values=["Reserva Sala", "Alquiler Equipo", "Asesoría"])
    entry_cantidad = ttk.Entry(form, width=35)

    ttk.Label(form, text="Nombre").grid(row=0, column=0)
    entry_nombre.grid(row=0, column=1)

    ttk.Label(form, text="Email").grid(row=1, column=0)
    entry_email.grid(row=1, column=1)

    ttk.Label(form, text="Servicio").grid(row=2, column=0)
    combo_servicio.grid(row=2, column=1)

    ttk.Label(form, text="Cantidad").grid(row=3, column=0)
    entry_cantidad.grid(row=3, column=1)

    resultado = tk.StringVar()
    ttk.Label(main, textvariable=resultado, foreground="green").pack(pady=10)

    tabla = ttk.Treeview(main, columns=("Cliente","Servicio","Estado"), show="headings")
    for col in ("Cliente","Servicio","Estado"):
        tabla.heading(col, text=col)
    tabla.pack(pady=10, fill="x")

    # -------- SELECCION --------
    def seleccionar(event):
        sel = tabla.selection()
        if not sel:
            return
        i = tabla.index(sel[0])
        r = reservas[i]

        entry_nombre.delete(0, tk.END)
        entry_nombre.insert(0, r.cliente.nombre)

        entry_email.delete(0, tk.END)
        entry_email.insert(0, r.cliente.email)

        if isinstance(r.servicio, ReservaSala):
            combo_servicio.set("Reserva Sala")
            cant = r.servicio.horas
        elif isinstance(r.servicio, AlquilerEquipo):
            combo_servicio.set("Alquiler Equipo")
            cant = r.servicio.dias
        else:
            combo_servicio.set("Asesoría")
            cant = r.servicio.horas

        entry_cantidad.delete(0, tk.END)
        entry_cantidad.insert(0, str(cant))

    tabla.bind("<<TreeviewSelect>>", seleccionar)

    # -------- LIMPIAR --------
    def limpiar(event):
        if not tabla.identify_row(event.y):
            tabla.selection_remove(tabla.selection())
            entry_nombre.delete(0, tk.END)
            entry_email.delete(0, tk.END)
            entry_cantidad.delete(0, tk.END)
            combo_servicio.set("")

    tabla.bind("<Button-1>", limpiar)

    # -------- FUNCIONES --------
    def procesar():
        try:
            c = Cliente(len(clientes)+1, entry_nombre.get(), entry_email.get())
            clientes.append(c)

            cant = int(entry_cantidad.get())
            tipo = combo_servicio.get()

            if tipo == "Reserva Sala":
                s = ReservaSala(cant)
            elif tipo == "Alquiler Equipo":
                s = AlquilerEquipo(cant)
            else:
                s = Asesoria(cant)

            r = Reserva(c, s)
            reservas.append(r)
            r.confirmar()

            tabla.insert("", "end", values=(c.nombre, s.descripcion(), r.estado))
            resultado.set(f"✔ ${r.costo}")

        except Exception as e:
            logging.error(str(e))
            messagebox.showerror("Error", str(e))

    def modificar_reserva():
        try:
            sel = tabla.selection()
            if not sel:
                raise ReservaError("Seleccione una reserva")

            item = sel[0]
            i = tabla.index(item)

            c = Cliente(i+1, entry_nombre.get(), entry_email.get())

            cant = int(entry_cantidad.get())
            tipo = combo_servicio.get()

            if tipo == "Reserva Sala":
                s = ReservaSala(cant)
            elif tipo == "Alquiler Equipo":
                s = AlquilerEquipo(cant)
            else:
                s = Asesoria(cant)

            r = Reserva(c, s)
            r.confirmar()

            reservas[i] = r
            tabla.item(item, values=(c.nombre, s.descripcion(), r.estado))

            resultado.set(f"✔ Modificada ${r.costo}")
            logging.info(f"Reserva modificada: {c.nombre}")

        except Exception as e:
            logging.error(str(e))
            messagebox.showerror("Error", str(e))

    def cerrar():
        if messagebox.askyesno("Salir", "¿Cerrar aplicación?"):
            logging.info("App cerrada")
            root.destroy()

    botones = ttk.Frame(main)
    botones.pack()

    ttk.Button(botones, text="Procesar", command=procesar).grid(row=0,column=0,padx=10)
    ttk.Button(botones, text="Modificar", command=modificar_reserva).grid(row=0,column=1,padx=10)
    ttk.Button(botones, text="Cerrar", command=cerrar).grid(row=0,column=2,padx=10)

    root.mainloop()

if __name__ == "__main__":
    crear_interfaz()
    