# Importamos las librerias necesarias
#pip install pillow
#pip install sympy

import tkinter as tk #Interfaz
from tkinter import ttk #widgets botones, etiquetas,cuadros de texto, etc
from PIL import Image, ImageTk
from sympy import *
from sympy.parsing.sympy_parser import (standard_transformations, implicit_application)

#Creamos la ventana principal
root = tk.Tk()

#Configuramos la ventana
root.title("Método modificado de Newton-Raphson")
width = root.winfo_screenwidth()
height = root.winfo_screenheight()
root.geometry("%dx%d" % (width, height))

#Configuramos la imagen de fondo
img = Image.open("img/fondo.png")
img = img.resize((width, height), resample=Image.LANCZOS)
photo = ImageTk.PhotoImage(img) #Usa la imagen en la interfaz
label = tk.Label(root, image=photo)
label.place(x=0, y=0, relwidth=1, relheight=1)

#Creamos el titulo
label = tk.Label(root, text="Método modificado de Newton - Raphson", font=("Arial", 25, "bold"))
label.pack(pady=20)

#Creamos los widgets de entrada para la función, valor inicial y error
func_label = tk.Label(root, text="Ingrese la función:", font=("Arial", 12))
func_label.pack(pady=10)
func_entry = tk.Entry(root, font=("Arial", 17), width=40, bd=2, relief="solid")
func_entry.pack(pady=10)

inic_label = tk.Label(root, text="Ingrese el valor inicial:", font=("Arial", 12))
inic_label.pack(pady=10)
inic_entry = tk.Entry(root, font=("Arial", 17), width=40, bd=2, relief="solid")
inic_entry.pack(pady=10)

Ea_label = tk.Label(root, text="Ingrese el | Ea |", font=("Arial", 12))
Ea_label.pack(pady=10)
Ea_entry = tk.Entry(root, font=("Arial", 17), width=40, bd=2, relief="solid")
Ea_entry.pack(pady=10)

#Creamos el estilo para la tabla y la propia tabla
style = ttk.Style() #Modulo de los estilos de tkinter
style.configure('margintable.Treeview', font=('Arial', 12)) #Estilo de los datos
style.configure('margintable.Treeview.Heading', font=('Arial', 12, 'bold')) #Estilo del encabezado
table = ttk.Treeview(root, style='margintable.Treeview',
                     columns=("iteracion", "xi", "f(xi)", "f'(xi)", "f''(xi)", "Error"), show="headings")
 #show muestra encabezados sin mostrar contenido de las filas
table.heading("iteracion", text="Iteración")
table.heading("xi", text="xi")
table.heading("f(xi)", text="f(xi)")
table.heading("f'(xi)", text="f'(xi)")
table.heading("f''(xi)", text="f''(xi)")
table.heading("Error", text="Error")

#Definimos la función que se ejecutará al presionar el botón "Calcular"
def mod_newton_raphson():

    #Validamos los campos
    if not func_entry.get() or not inic_entry.get() or not Ea_entry.get():
        result_label.config(text="Error: Todos los campos son obligatorios.", font=("Arial", 12))
        return

    # Convertimos la función ingresada en un objeto sympy
    transformations = (standard_transformations + (implicit_application,)) #Evalua la sintaxis
    func = parse_expr(func_entry.get().replace('^', '**').replace('e', str(E)), transformations=transformations)
    x = Symbol('x')
    df = func.diff(x)
    d2f = df.diff(x)

    # Mostramos la primera y segunda derivada de la función
    df_label.config(text=f"df = {df}".replace('**', '^'), font=("Arial", 12))
    d2f_label.config(text=f"d2f = {d2f}".replace('**', '^'), font=("Arial", 12))

    # Obtenemos el valor inicial y la tolerancia ingresados
    x0 = round(float(inic_entry.get()), 4)
    ea = round(float(Ea_entry.get()), 4)

    # Validamos que la tolerancia sea un número positivo y diferente de cero
    if ea <= 0 and ea == 0:
        result_label.config(text="El Error relativo porcentual debe ser un número positivo o diferente a cero.",
                            font=("Arial", 12))
        return

    # Inicializamos las variables para el bucle while
    error_anterior = round(0, 4)
    error = ea
    iteraciones = 0

    # Realizamos el bucle while hasta que se alcance la tolerancia deseada
    while error >= ea:

        # Calculamos los valores de la función y sus derivadas en el punto actual
        f_value = round(float(func.subs(x, x0)), 4)
        df_value = round(float(df.subs(x, x0)), 4)
        d2f_value = round(float(d2f.subs(x, x0)), 4)

        # Calculamos el siguiente xi utilizando el método de Newton-Raphson modificado
        xi = round(float(x0 - ((f_value * df_value) / (df_value ** 2 - f_value * d2f_value))), 4)

        #Calculadmos el error porcentual
        if xi != 0:
            error_porcentual = round(abs((xi - x0) / xi) * 100, 4)
        else:
            error_porcentual = 0

        iteraciones += 1

        #Se inserta una fila en una tabla, que muestra el número de iteraciones, xi, resultado de la funcion, primera y
        #segunda derivada ademas del error porcentual
        table.insert("", "end", values=(iteraciones, x0, f_value, df_value, d2f_value, error_anterior))
        table.pack(padx=100, pady=(10, 100), fill="both", expand=True)

        #Esta linea valida si el siguiente resultado es igual si es asi el programa entre en un bucle y muestra por pantalla
        #el mensaje y el ultimo xi calculado al alcanzar el error ingresado
        if xi==x0:
            result_label.config(
                text="El algoritmo está en un bucle infinito. Por ende el valor aproximado de cero de la funcion es : "
                     "{:.4f}".format(x0), font=("Arial", 12))
            result_label.pack(pady=10)
        if error_porcentual==error:
            result_label.config(text="El valor aproximado de cero de la funcion es : {:.4f}".format(x0),
                                font=("Arial", 12))
            result_label.pack(pady=10)
        else:
            result_label.config(text="El valor aproximado de cero de la funcion es : {:.4f}".format(x0),
                                font=("Arial", 12))
            result_label.pack(pady=10)


        #Estas líneas de código actualizan los valores de x0, error_anterior y error para la próxima iteración.
        x0 = xi
        error_anterior = error_porcentual

        #Actualiza el error para verificar el bucle
        error = error_porcentual

        # Si el error actual es menor que la ea, salimos del bucle
        if error < ea:
            break

#Borra los datos de la tabla y los campos
def borrar(table):
    func_entry.delete(0, tk.END)
    inic_entry.delete(0, tk.END)
    Ea_entry.delete(0, tk.END)
    result_label.config(text="")
    df_label.config(text="")
    d2f_label.config(text="")
    for item in table.get_children():
        table.delete(item)


def manual():
    new_window = tk.Toplevel()
    new_window.title("Manual")
    new_window.geometry("700x500")

    # Agregar título centrado
    title_label = tk.Label(new_window, text="Manual", font=("Arial", 24), justify="center")
    title_label.pack(pady=20)

    # Desactivar propagación de tamaño de los widgets
    new_window.pack_propagate(False) #No adaptarse

    # Agregar texto alineado a la izquierda
    text_label1 = tk.Label(new_window,
                           text="1. En el primer campo, ingrese la función que desea evaluar. La función debe ser una función no lineal y pude ser ingresada con la sintaxis de Python o normal. Por ejemplo, f(x) = x^2 - 4, ó \"x**2 - 4\".",
                           justify="left", wraplength=600)
    text_label1.pack(pady=10, padx=20, anchor="w", fill="both")

    text_label2 = tk.Label(new_window,
                           text="2. En el segundo campo, ingrese el valor inicial para el cálculo de la raíz. Este valor debe ser un número real y debe estar lo más cerca posible de la raíz que desea encontrar.",
                           justify="left", wraplength=600)
    text_label2.pack(pady=10, padx=20, anchor="w", fill="both")

    text_label3 = tk.Label(new_window,
                           text="3. En el tercer campo, ingrese el error relativo porcentual deseado. Este valor debe ser un número positivo y diferente de cero. Cuanto menor sea el valor, mayor será la precisión del cálculo.",
                           justify="left", wraplength=600)
    text_label3.pack(pady=10, padx=20, anchor="w", fill="both")

    text_label4 = tk.Label(new_window,
                           text="4. Una vez que haya ingresado la función, el valor inicial y el error relativo porcentual deseado, presione el botón \"Calcular\". La calculadora calculará la raíz de la función utilizando el método modificado de Newton-Raphson y mostrará los resultados en una tabla.",
                           justify="left", wraplength=600)
    text_label4.pack(pady=10, padx=20, anchor="w", fill="both")

    text_label5 = tk.Label(new_window,
                           text="5. La tabla mostrará los siguientes valores para cada iteración del cálculo: la iteración actual, el valor de x, el valor de la función evaluada en x, el valor de la primera derivada de la función evaluada en x, el valor de la segunda derivada de la función evaluada en x y el error relativo porcentual. La raíz de la función se encuentra en la última fila de la tabla.",
                           justify="left", wraplength=600)
    text_label5.pack(pady=10, padx=20, anchor="w", fill="both")

    text_label6 = tk.Label(new_window,
                           text="6. Al presionar el botón Borrar, se eliminará todo el contenido ingresado en las entradas de la función, valor inicial y error. Además, la tabla que muestra los resultados de cálculo también será eliminada.",
                           justify="left", wraplength=600)
    text_label6.pack(pady=10, padx=20, anchor="w", fill="both")



#Boton que llama el metodo para solucionar la ecuacion
calc_button = tk.Button(root, text="Calcular" ,command=mod_newton_raphson, font=("Arial", 15), bg="#70C660")
calc_button.pack(pady=10)

#Boton que llama el metodo para borar los datos
borrar_button = tk.Button(root, text="Borrar", command=lambda: borrar(table), font=("Arial", 15), bg="#F46A5A")
borrar_button.pack(pady=10)

#Se crea el boton del manual
manual_button = tk.Button(root, text="Manual",command=manual, font=("Arial", 15), bg="#539ACE")
manual_button.place(x=width-100, y=20)


#Inicialisa los label que muestran los mensajes y los llama antes de calcular todo
result_label = tk.Label(root, text="")
df_label = tk.Label(root, text="")
d2f_label = tk.Label(root, text="")
result_label.pack()
df_label.pack()
d2f_label.pack()

#Inicia la interfaz grafica
root.mainloop()