import tkinter as tk
from tkinter import ttk, messagebox
from proyectos_clientes import Cliente, ReservaSala, AlquilerEquipo, Asesoria, Reserva
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Software FJ")
        self.root.geometry("500x400")
        
        self.crear_widgets()
        
    def crear_widgets(self):
        #------ CLIENTE ------
        ttk.Label(self.root, text="Nombre").pack()
        self.nombre = ttk.Entry(self.root)
        self.nombre.pack()
        
        ttk.Label(self.root, text="Email").pack()
        self.email = ttk.Entry(self.root)
        self.email.pack()
        
        #------ SERVICIO ------
        ttk.Label(self.root, text="Tipo de servicio").pack()
        self.tipo = ttk.Combobox(self.root, values=["Sala", "Equipo", "Asesoria"])
        self.tipo.pack()
        
        ttk.Label(self.root, text="Cantidad (horas/dias)").pack()
        self.cantidad = ttk.Entry(self.root)
        self.cantidad.pack()
        
        #----- BOTON ------
        ttk.Button(self.root, text="Crear Reserva", command=self.crear_reserva).pack(pady=10)
        
    def crear_reserva(self):
        try:
            nombre = self.nombre.get()
            email = self.email.get()
            tipo = self.tipo.get()
            cantidad = int(self.cantidad.get())

            cliente = Cliente(1, nombre, email)
            
            if tipo == "Sala":
                servicio = ReservaSala(cantidad)
            elif tipo == "Equipo":
                servicio = AlquilerEquipo(cantidad)
            else:
                servicio = Asesoria(cantidad)
                
            reserva = Reserva(cliente, servicio)
            reserva.confirmar()
            
            messagebox.showinfo("Exito", "Reserva creada exitosamente")
        
        except Exception as e:
            messagebox.showerror("Error", str(e))