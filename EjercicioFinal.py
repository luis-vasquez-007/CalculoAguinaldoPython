from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import sqlite3

"""----------------------------------Funciones-----------------------------------------"""


def conexionBBDD():  # creando la base de datos
    miConexion = sqlite3.connect("registro.db")

    miCursor = miConexion.cursor()

    miCursor.execute('''
    CREATE TABLE IF NOT EXISTS empleado(
    id_empleado INTEGER PRIMARY KEY AUTOINCREMENT,
    dui varchar(10) UNIQUE not null,
    nit varchat(15) UNIQUE not null,
    nombres varchar(55) not null,
    apellidos varchar(55) not null,
    cargo varchar(55),
    salario float not null)
        ''')

    messagebox.showinfo("BBDD", "Base creada")

    miConexion.commit()
    miConexion.close()

	
	

def salirDelPrograma():  # funcion para salir del programa

	valor = messagebox.askquestion(
	    "Salir", "¿Realmente quiere salir del programa?")

	if valor == "yes":
		root.destroy()  # cierra el programa


def limpiarCuadros():

	miId.set("")
	miDui.set("")
	miNit.set("")
	miNombre.set("")
	miApellido.set("")
	miCargo.set("")
	miSalario.set("") 

def crear():
	if(len(str(miDui.get())) != 0 and len(str(miNit.get())) != 0 and len(str(miNombre.get())) != 0 and len(str(miApellido.get())) != 0 and len(str(miCargo.get())) != 0 and len(str(miSalario.get())) != 0):
		try:
			miConexion=sqlite3.connect("registro.db")

			miCursor = miConexion.cursor()

			miCursor.execute("INSERT INTO empleado VALUES(NULL, '" + miDui.get() + 
				"','" + miNit.get() + 
				"','" + miNombre.get() + 
				"','" + miApellido.get() +
				"','" + miCargo.get() +
				"','" + miSalario.get() + "')")

			miConexion.commit()
			miConexion.close()

			limpiarCuadros()

			messagebox.showinfo("BBDD", "Registro insertado con éxito.")
		except:
			messagebox.showerror("BBDD", "Valor DUI ó NIT ya existe")
	else:
		messagebox.showwarning("BBDD", "Favor llenar campos de texto")

def leer():
	miConexion=sqlite3.connect("registro.db")

	miCursor = miConexion.cursor()

	miCursor.execute("SELECT * FROM empleado WHERE dui='"+miDui.get()+"'")
	print(miDui.get())


	for empleado in miCursor:

		miId.set(empleado[0])
		miDui.set(empleado[1])
		miNit.set(empleado[2])
		miNombre.set(empleado[3])
		miApellido.set(empleado[4])
		miCargo.set(empleado[5])
		miSalario.set(empleado[6])


	miConexion.commit()
	miConexion.close()

def actualizar():
	miConexion=sqlite3.connect("registro.db")

	miCursor = miConexion.cursor()
	miCursor.execute("UPDATE empleado SET nit=?,nombres=?,apellidos=?,cargo=?,salario=? where dui=?",(miNit.get(),miNombre.get(),miApellido.get(),miCargo.get(),miSalario.get(),miDui.get()))
	miConexion.commit()
	miConexion.close()

	messagebox.showinfo("BBDD", "Registro actualizado con éxito.")

def borrar():
	miConexion=sqlite3.connect("registro.db")

	miCursor = miConexion.cursor()

	miCursor.execute("DELETE FROM empleado WHERE id_empleado=" + miId.get())

	miConexion.commit()
	miConexion.close()

	limpiarCuadros()

	messagebox.showinfo("BBDD", "Registro eliminado con éxito")

def aCercaDe():

	messagebox.showinfo("Acerca de", "Versión primera By Luis Vasquez")

"""---------------------------------------Validación de Aguinaldo----------------------------------- """
def calcularAguinaldo():
    cmbAguinando = comboTiempo.get()
    aguilando = float(miSalario.get())
    if cmbAguinando == "1 -- 3 Años":
         totalA = (aguilando/30)*15
         obteniendoAguinaldo["text"]="$",str(totalA)
    if cmbAguinando == "3 -- 10 Años":
         totalA = (aguilando/30)*19
         obteniendoAguinaldo["text"]="$",str(totalA)
    if cmbAguinando == "10 -- A más":
         totalA = (aguilando/30)*21
         obteniendoAguinaldo["text"]="$",str(totalA)

"""-------------------------Creación del menú del CRUD-------------------------"""
root = Tk()
barraMenu = Menu(root)
root.title("Sistema Calculador Aguinaldo")
root.config(menu=barraMenu, width=400, height=400)



bbddMenu = Menu(barraMenu, tearoff=0) #armando el menú
                            # saca las lineas
bbddMenu.add_command(label="Conectar", command = conexionBBDD) #acá conecto con la base de datos
bbddMenu.add_command(label="Salir", command = salirDelPrograma)

borrarMenu = Menu(barraMenu, tearoff=0)
borrarMenu.add_command(label="Limpiar campos", command = limpiarCuadros)

crudMenu = Menu(barraMenu, tearoff=0)
crudMenu.add_command(label="Crear", command = crear)
crudMenu.add_command(label="Leer", command = leer)
crudMenu.add_command(label="Actualizar", command = actualizar)
crudMenu.add_command(label="Borrar", command = borrar)

ayudaMenu = Menu(barraMenu, tearoff=0)
ayudaMenu.add_command(label="A cerca de", command = aCercaDe)

barraMenu.add_cascade(label="Base de datos", menu=bbddMenu)#acomodo los elementos en el menú
barraMenu.add_cascade(label="Limpiar", menu=borrarMenu)
barraMenu.add_cascade(label="CRUD", menu=crudMenu)
barraMenu.add_cascade(label="Ayuda", menu=ayudaMenu)

"""----------------------------------Creación de los cuadros del crud-------------------------------"""

miFrame =Frame(root)
miFrame.pack()

miId = StringVar() #tipo entry
miDui = StringVar()
miNit = StringVar()
miNombre = StringVar()
miApellido = StringVar()
miCargo = StringVar()
miSalario = StringVar()

cuadroID=Entry(miFrame, textvariable = miId)
cuadroID.grid(row=0, column = 1, padx=10, pady=10) #Se ubica en la fila 1, columna 1
cuadroID.configure(state="disabled")

cuadroDui=Entry(miFrame, textvariable = miDui)
cuadroDui.grid(row=1, column = 1, padx=10, pady=10) #Se ubica en la fila 2, columna 1
#cuadroNit.config(show="*") Esto cuando use password me será muy útil


cuadroNit=Entry(miFrame, textvariable = miNit)
cuadroNit.grid(row=2, column = 1, padx=10, pady=10) #Se ubica en la fila 3, columna 1
#cuadroNit.config(show="*") Esto cuando use password me será muy útil

cuadroNombre=Entry(miFrame, textvariable = miNombre)
cuadroNombre.grid(row=3, column = 1, padx=10, pady=10) #Se ubica en la fila 4, columna 1

cuadroApellido=Entry(miFrame, textvariable = miApellido)
cuadroApellido.grid(row=4, column = 1, padx=10, pady=10) #Se ubica en la fila 5, columna 1

cuadroCargo=Entry(miFrame, textvariable = miCargo)
cuadroCargo.grid(row=5, column = 1, padx=10, pady=10) #Se ubica en la fila 6 , columna 1

cuadroSalario=Entry(miFrame, textvariable = miSalario)
cuadroSalario.grid(row=6, column = 1, padx=10, pady=10) #Se ubica en la fila 7 , columna 1

comboTiempo=ttk.Combobox(miFrame, 
                            values=[
                                    "1 -- 3 Años", 
                                    "3 -- 10 Años",
                                    "10 -- A más"])
print(dict(comboTiempo)) 
comboTiempo.grid(row=1, column=3, padx=10, pady=10)
comboTiempo.current(0)

labelAguinaldo = Label(miFrame, text="Su Aguinaldo es:")
labelAguinaldo.grid(row=2, column=3, padx=10, pady=10)

obteniendoAguinaldo = Label(miFrame, font="Arial 18")
obteniendoAguinaldo.grid(row=3, column=3, padx=10, pady=10)


"""-----------------------------Creación de las etiquetas de los cuadros---------------------------- """

idLabel = Label(miFrame, text="Id: ")
idLabel.grid(row=0, column=0, sticky="e", padx=10, pady=10)#columna 0 para que este al costado del cuadro, fila 0

duiLabel = Label(miFrame, text="Dui: ")
duiLabel.grid(row=1, column=0, sticky="e", padx=10, pady=10)

nitLabel = Label(miFrame, text="Nit: ")
nitLabel.grid(row=2, column=0, sticky="e", padx=10, pady=10)

nombreLabel = Label(miFrame, text="Nombre: ")
nombreLabel.grid(row=3, column=0, sticky="e", padx=10, pady=10)

apellidoLabel = Label(miFrame, text="Apellido: ")
apellidoLabel.grid(row=4, column=0, sticky="e", padx=10, pady=10)

cargoLabel = Label(miFrame, text="Cargo: ")
cargoLabel.grid(row=5, column=0, sticky="e", padx=10, pady=10)

salarioLabel = Label(miFrame, text="Salario Neto: ")
salarioLabel.grid(row=6, column=0, sticky="e", padx=10, pady=10)

labelTiempo = Label(miFrame,text = "Selecciona el tiempo del Empleado")
labelTiempo.grid(row=0, column=3, sticky="e", padx=10, pady=10)

"""---------------------------------Creación de los botones del crud----------------------------------------"""

miFrame2=Frame(root)

miFrame2.pack()

botonCrear=Button(miFrame2, text="Crear", command = crear)
botonCrear.grid(row=1, column=0, sticky="e", padx=10, pady=10)

botonLeer=Button(miFrame2, text="Leer", command = leer)
botonLeer.grid(row=1, column=1, sticky="e", padx=10, pady=10)

botonActualizar=Button(miFrame2, text="Actualizar", command = actualizar)
botonActualizar.grid(row=1, column=2, sticky="e", padx=10, pady=10)

botonBorrar=Button(miFrame2, text="Borrar", command=borrar)
botonBorrar.grid(row=1, column=3, sticky="e", padx=10, pady=10)

botonBorrar=Button(miFrame2, text="Limpiar", command=limpiarCuadros)
botonBorrar.grid(row=1, column=4, sticky="e", padx=10, pady=10)

botonCalcularAguinaldo=Button(miFrame2, text="Calcular Aguinaldo", command=calcularAguinaldo)
botonCalcularAguinaldo.grid(row=1, column=5, sticky="e", padx=10, pady=10)

root.mainloop()
