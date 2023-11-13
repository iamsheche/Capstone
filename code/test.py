import tkinter as tk

def mostrarVentanaSecundaria():
    ventana_secundaria = tk.Toplevel()
    ventana_secundaria.title("Ventana Secundaria")
    ventana_secundaria.geometry("400x300")

    btn_tomar_foto = tk.Button(ventana_secundaria, text="Tomar Foto", command=lambda: print("Botón presionado"))
    btn_tomar_foto.pack()

    ventana_secundaria.mainloop()

# Crear la ventana principal
ventana_principal = tk.Tk()
ventana_principal.geometry("600x400")

# Botón para abrir la ventana secundaria
btn_abrir_ventana = tk.Button(ventana_principal, text="Abrir Ventana Secundaria", command=mostrarVentanaSecundaria)
btn_abrir_ventana.pack()

ventana_principal.mainloop()
