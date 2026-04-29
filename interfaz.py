import tkinter as tk
from tkinter import ttk, messagebox
from proyectos_clientes import Cliente, ReservaSala, AlquilerEquipo, Asesoria, Reserva
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Software FJ")
        self.root.geometry("500x400")
        
        self.crear_widgets()
        
        self.reservas = []
        
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
        
        ttk.Button(self.root, text="Cancelar Reserva", command=self.cancelar_reserva).pack()
        #----- TABLA ------
        self.tabla = ttk.Treeview(self.root, columns=("Cliente", "Servicio", "Estado", "Costo"), show="headings")
        
        self.tabla.heading("Cliente", text="Cliente")
        self.tabla.heading("Servicio", text="Servicio")
        self.tabla.heading("Estado", text="Estado")
        self.tabla.heading("Costo", text="Costo")
        
        self.tabla.pack(pady=10)
        
        
        
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
            
            costo = servicio.calcular_costo()
            
            self.reservas.append(reserva)
            
            self.tabla.insert("", "end", values=(cliente.get_nombre(), servicio.descripcion(), reserva.estado, costo))
            
            messagebox.showinfo("Exito", "Reserva creada exitosamente")
        
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def cancelar_reserva(self):
        try:
            seleccion = self.tabla.selection()
            
            if not seleccion:
                raise Exception("Seleccione una reserva")
            
            index = self.tabla.index(seleccion)
            reserva = self.reservas[index]
            
            reserva.cancelar()
            
            costo = reserva.servicio.calcular_costo()
            
            self.tabla.item(seleccion, values=(reserva.cliente.get_nombre(), reserva.servicio.descripcion(), reserva.estado, costo))
            
        except Exception as e:
            messagebox.showerror("Error", str(e))