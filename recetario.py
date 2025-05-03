import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
from PIL import Image, ImageTk
import psycopg2

# Configuración visual
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("green")

COLOR_FONDO = "#f5c2ce"
COLOR_BOTON = "#8aa93f"
COLOR_HOVER = "#ddf688"
FUENTE = "Century Gothic"

# Conexión a PostgreSQL
def conectar_db():
    return psycopg2.connect(
        host="localhost",
        database="pruebatontaR",
        user="postgres",
        password="-"
    )

# Ventana principal
app = ctk.CTk()
app.title("Recetario - Login")
app.geometry("400x400")
app.configure(fg_color=COLOR_FONDO)

id_usuario_logeado = None
usuario_logeado = None

from tkinter import messagebox  # clásico, ya está en tu entorno

# Variables de sesión
usuario_logeado = None
id_usuario_logeado = None

# ============================
# Funciones de login y registro con tkinter.messagebox
# ============================
def registrar_usuario():
    usuario = entry_usuario.get()
    contraseña = entry_contraseña.get()

    if not usuario or not contraseña:
        messagebox.showerror("Error", "Rellena todos los campos")
        return

    conn = conectar_db()
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO usuarios (nombre_usuario, email, contraseña) VALUES (%s, %s, %s)",
                       (usuario, f"{usuario}@example.com", contraseña))
        conn.commit()
        messagebox.showinfo("Registro exitoso", "Usuario registrado correctamente")
    except psycopg2.Error as e:
        messagebox.showerror("Error", f"No se pudo registrar: {e.pgerror}")
    finally:
        cursor.close()
        conn.close()

def iniciar_sesion():
    global usuario_logeado, id_usuario_logeado

    usuario = entry_usuario.get()
    contraseña = entry_contraseña.get()

    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id_usuario, nombre_usuario FROM usuarios WHERE nombre_usuario = %s AND contraseña = %s", (usuario, contraseña))
    result = cursor.fetchone()
    cursor.close()
    conn.close()

    if result:
        id_usuario_logeado, usuario_logeado = result
        messagebox.showinfo("Bienvenido", f"¡Hola {usuario_logeado}!")
        mostrar_menu_principal()
    else:
        messagebox.showerror("Error", "Usuario o contraseña incorrectos")


# Pantalla de login
titulo = ctk.CTkLabel(app, text="Iniciar Sesión", font=(FUENTE, 22))
titulo.pack(pady=20)

entry_usuario = ctk.CTkEntry(app, placeholder_text="Usuario", font=(FUENTE, 16), width=250)
entry_usuario.pack(pady=10)

entry_contraseña = ctk.CTkEntry(app, placeholder_text="Contraseña", show="*", font=(FUENTE, 16), width=250)
entry_contraseña.pack(pady=10)

btn_login = ctk.CTkButton(app, text="Iniciar Sesión", font=(FUENTE, 16), width=200,
                          fg_color=COLOR_BOTON, hover_color=COLOR_HOVER, command=iniciar_sesion)
btn_login.pack(pady=10)

btn_registro = ctk.CTkButton(app, text="Registrar", font=(FUENTE, 16), width=200,
                             fg_color=COLOR_BOTON, hover_color=COLOR_HOVER, command=registrar_usuario)
btn_registro.pack(pady=10)

# ============================
# Menú principal (después del login)
# ============================
def mostrar_menu_principal():
    for widget in app.winfo_children():
        widget.destroy()

    label_bienvenida = ctk.CTkLabel(app, text=f"Bienvenido {usuario_logeado}", font=(FUENTE, 22))
    label_bienvenida.pack(pady=20)

    btn_buscar = ctk.CTkButton(app, text="Buscar Recetas", font=(FUENTE, 16), width=220,
                               fg_color=COLOR_BOTON, hover_color=COLOR_HOVER, command=mostrar_categorias)
    btn_buscar.pack(pady=10)

    btn_agregar = ctk.CTkButton(app, text="Agregar Nueva Receta", font=(FUENTE, 16), width=220,
                                fg_color=COLOR_BOTON, hover_color=COLOR_HOVER, command=agregar_receta)
    btn_agregar.pack(pady=10)

    btn_guardadas = ctk.CTkButton(app, text="Ver Recetas Guardadas", font=(FUENTE, 16), width=220,
                                  fg_color=COLOR_BOTON, hover_color=COLOR_HOVER, command=ver_recetas_guardadas)
    btn_guardadas.pack(pady=10)

    btn_salir = ctk.CTkButton(app, text="Salir", font=(FUENTE, 16), width=220,
                              fg_color="#e06666", hover_color="#f4a3a3", command=app.quit)
    btn_salir.pack(pady=10)

# ============================
# Mostrar Categorías (subventana)
# ============================
def mostrar_categorias():
    app.iconify()  # Minimiza ventana principal

    ventana = tk.Toplevel(app)
    ventana.title("Categorías de Recetas")
    ventana.geometry("600x700")
    ventana.configure(bg=COLOR_FONDO)

    def restaurar():
        app.deiconify()  # Restaura ventana principal al cerrar esta
        ventana.destroy()

    ventana.protocol("WM_DELETE_WINDOW", restaurar)

    ctk.CTkLabel(ventana, text="Categorías", font=(FUENTE, 22, "bold")).pack(pady=10)

    frame_principal = tk.Frame(ventana, bg=COLOR_FONDO)
    frame_principal.pack(fill="both", expand=True)

    frame_categorias = tk.Frame(frame_principal, bg=COLOR_FONDO)
    frame_categorias.pack()

    frame_recetas = tk.Frame(frame_principal, bg=COLOR_FONDO)
    frame_recetas.pack_forget()

    def cargar_categorias():
        for widget in frame_categorias.winfo_children():
            widget.destroy()

        conn = conectar_db()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT id_categoria, nombre_categoria FROM categorias ORDER BY nombre_categoria ASC;")
            categorias = cursor.fetchall()
            for id_categoria, nombre_categoria in categorias:
                ctk.CTkButton(frame_categorias, text=nombre_categoria,
                              font=(FUENTE, 16), fg_color=COLOR_BOTON, hover_color=COLOR_HOVER,
                              width=300, corner_radius=15,
                              command=lambda idc=id_categoria, nom=nombre_categoria: mostrar_recetas(idc, nom)
                              ).pack(pady=6)
        finally:
            cursor.close()
            conn.close()

    def mostrar_recetas(id_categoria, nombre_categoria):
        frame_categorias.pack_forget()
        for widget in frame_recetas.winfo_children():
            widget.destroy()

        ctk.CTkLabel(frame_recetas, text=f"{nombre_categoria}", font=(FUENTE, 20, "bold")).pack(pady=10)

        conn = conectar_db()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT id_receta, titulo
                FROM recetas
                WHERE id_categoria = %s
                ORDER BY titulo ASC
            """, (id_categoria,))
            recetas = cursor.fetchall()
            if recetas:
                for id_receta, titulo in recetas:
                    ctk.CTkButton(frame_recetas, text=titulo, font=(FUENTE, 16),
                                  fg_color=COLOR_BOTON, hover_color=COLOR_HOVER,
                                  width=280, corner_radius=15,
                                  command=lambda idr=id_receta: abrir_detalle_receta(idr)).pack(pady=5)
            else:
                tk.Label(frame_recetas, text="No hay recetas en esta categoría.",
                         font=(FUENTE, 16), bg=COLOR_FONDO).pack(pady=20)
        finally:
            cursor.close()
            conn.close()

        # Botón de regresar
        ctk.CTkButton(frame_recetas, text="Regresar", font=(FUENTE, 15),
                      fg_color="#c97d7d", hover_color="#e6a6a6", width=200, corner_radius=10,
                      command=lambda: [frame_recetas.pack_forget(), frame_categorias.pack()]).pack(pady=20)

        frame_recetas.pack()

    cargar_categorias()


# ============================
# Mostrar Recetas por Categoría (subventana)
# ============================
def mostrar_recetas_por_categoria(id_categoria):
    ventana_recetas = tk.Toplevel(app)
    ventana_recetas.title("Recetas de la Categoría")
    ventana_recetas.geometry("600x500")
    ventana_recetas.configure(bg=COLOR_FONDO)

    conn = conectar_db()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT id_receta, titulo
            FROM recetas
            WHERE id_categoria = %s
            ORDER BY titulo ASC;
        """, (id_categoria,))
        recetas = cursor.fetchall()

        if recetas:
            for id_receta, titulo in recetas:
                btn = ctk.CTkButton(ventana_recetas, text=titulo, font=(FUENTE, 16),
                                    fg_color=COLOR_BOTON, hover_color=COLOR_HOVER,
                                    command=lambda idr=id_receta: abrir_detalle_receta(idr))
                btn.pack(padx=10, pady=5, fill="x")
        else:
            tk.Label(ventana_recetas, text="No hay recetas en esta categoría.",
                     font=(FUENTE, 16), bg=COLOR_FONDO).pack(pady=20)
    finally:
        cursor.close()
        conn.close()

# ============================
# Abrir Detalle de Receta (subventana)
# ============================
def abrir_detalle_receta(id_receta):
    ventana_detalle = tk.Toplevel(app)
    ventana_detalle.title("Detalle de Receta")
    ventana_detalle.geometry("800x1400")
    ventana_detalle.configure(bg=COLOR_FONDO)

    conn = conectar_db()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT titulo, descripcion, tiempo_preparacion, imagen
            FROM recetas
            WHERE id_receta = %s
        """, (id_receta,))
        receta = cursor.fetchone()

        if receta:
            titulo, descripcion, tiempo, imagen_path = receta

            tk.Label(ventana_detalle, text=titulo, font=(FUENTE, 24, "bold"),
                     bg=COLOR_FONDO, anchor="center").pack(pady=(20, 10))
            tk.Label(ventana_detalle, text=f"Tiempo de preparación: {tiempo} minutos",
                     font=(FUENTE, 16), bg=COLOR_FONDO).pack(pady=(0, 15))

            if imagen_path:
                try:
                    img = Image.open(imagen_path)
                    img = img.resize((300, 200))
                    img = ImageTk.PhotoImage(img)
                    img_label = tk.Label(ventana_detalle, image=img, bg=COLOR_FONDO)
                    img_label.image = img
                    img_label.pack(pady=10)
                except Exception as e:
                    print(f"Error cargando imagen: {e}")

            # Ingredientes
            ctk.CTkLabel(ventana_detalle, text="Ingredientes:", font=(FUENTE, 20, "underline")).pack(pady=(10, 5))
            frame_ingredientes = tk.Frame(ventana_detalle, bg=COLOR_FONDO)
            frame_ingredientes.pack(pady=5)
            cursor.execute("""
                SELECT i.nombre_ingrediente, ri.cantidad, ri.unidad
                FROM receta_ingredientes ri
                JOIN ingredientes i ON ri.id_ingrediente = i.id_ingrediente
                WHERE ri.id_receta = %s
            """, (id_receta,))
            ingredientes = cursor.fetchall()
            if ingredientes:
                for nombre, cantidad, unidad in ingredientes:
                    texto = f"- {cantidad} {unidad} de {nombre}"
                    tk.Label(frame_ingredientes, text=texto, font=(FUENTE, 16), bg=COLOR_FONDO).pack(anchor='w', padx=20)
            else:
                tk.Label(frame_ingredientes, text="No hay ingredientes registrados.",
                         font=(FUENTE, 16), bg=COLOR_FONDO).pack()

            # Preparación
            ctk.CTkLabel(ventana_detalle, text="Preparación:", font=(FUENTE, 20, "underline")).pack(pady=(20, 5))
            text_desc = tk.Text(ventana_detalle, height=6, wrap="word", font=(FUENTE, 15),
                                bd=2, relief="groove", bg="#fffdf9")
            text_desc.pack(padx=20, fill="both")
            text_desc.insert(tk.END, descripcion)
            text_desc.config(state="disabled")

            # Comentarios
            ctk.CTkLabel(ventana_detalle, text="Comentarios:", font=(FUENTE, 20, "underline")).pack(pady=(20, 5))
            frame_comentarios = tk.Frame(ventana_detalle, bg=COLOR_FONDO)
            frame_comentarios.pack(pady=5)
            cursor.execute("""
                SELECT u.nombre_usuario, c.texto_comentario
                FROM comentarios c
                JOIN usuarios u ON c.id_usuario = u.id_usuario
                WHERE c.id_receta = %s
                ORDER BY c.fecha_comentario ASC
            """, (id_receta,))
            comentarios = cursor.fetchall()
            if comentarios:
                for usuario, texto in comentarios:
                    tk.Label(frame_comentarios, text=f"{usuario}: {texto}", font=(FUENTE, 14),
                             bg=COLOR_FONDO).pack(anchor='w', padx=20)
            else:
                tk.Label(frame_comentarios, text="No hay comentarios aún.",
                         font=(FUENTE, 14), bg=COLOR_FONDO).pack()

            # Entrada de comentario
            ctk.CTkLabel(ventana_detalle, text="Agregar un comentario:", font=(FUENTE, 16)).pack(pady=(15, 5))
            entry_comentario = ctk.CTkEntry(ventana_detalle, placeholder_text="Escribe tu comentario",
                                            width=400, font=(FUENTE, 15))
            entry_comentario.pack(pady=5)

            ctk.CTkButton(ventana_detalle, text="Comentar", font=(FUENTE, 16),
                          fg_color=COLOR_BOTON, hover_color=COLOR_HOVER, width=200, corner_radius=8,
                          command=lambda: agregar_comentario(id_receta, entry_comentario.get(),
                                                             entry_comentario, frame_comentarios)).pack(pady=10)

            # Calificación
            ctk.CTkLabel(ventana_detalle, text="Califica esta receta (0-5 estrellas):", font=(FUENTE, 16)).pack(pady=10)
            entry_estrellas = ctk.CTkEntry(ventana_detalle, placeholder_text="0-5",
                                           width=100, font=(FUENTE, 16))
            entry_estrellas.pack(pady=5)

            ctk.CTkButton(ventana_detalle, text="Enviar Calificación", font=(FUENTE, 16),
                          fg_color=COLOR_BOTON, hover_color=COLOR_HOVER, width=200, corner_radius=8,
                          command=lambda: calificar_receta(id_receta, entry_estrellas.get(), entry_estrellas)).pack(pady=10)

            # Guardar favorito
            ctk.CTkButton(ventana_detalle, text="Guardar en Favoritos", font=(FUENTE, 16),
                          fg_color="#f7aa0c", hover_color="#ffe082", width=220, corner_radius=8,
                          command=lambda: guardar_receta(id_receta)).pack(pady=15)
    finally:
        cursor.close()
        conn.close()



def ver_recetas_guardadas():
    app.iconify()
    ventana_guardadas = tk.Toplevel(app)
    ventana_guardadas.title("Recetas Guardadas")
    ventana_guardadas.geometry("400x500")
    ventana_guardadas.configure(bg=COLOR_FONDO)
    def restaurar():
        app.deiconify()
        ventana_guardadas.destroy()
    ventana_guardadas.protocol("WM_DELETE_WINDOW", restaurar)

    conn = conectar_db()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT r.id_receta, r.titulo
            FROM recetas_guardadas rg
            JOIN recetas r ON rg.id_receta = r.id_receta
            WHERE rg.id_usuario = %s
            ORDER BY r.titulo ASC;
        """, (id_usuario_logeado,))
        recetas = cursor.fetchall()

        if recetas:
            for id_receta, titulo in recetas:
                btn = ctk.CTkButton(ventana_guardadas, text=titulo, font=(FUENTE, 16),
                                    fg_color=COLOR_BOTON, hover_color=COLOR_HOVER,
                                    command=lambda idr=id_receta: abrir_detalle_receta(idr))
                btn.pack(padx=10, pady=5, fill="x")
        else:
            tk.Label(ventana_guardadas, text="No has guardado recetas aún.",
                     font=(FUENTE, 16), bg=COLOR_FONDO).pack(pady=20)
    finally:
        cursor.close()
        conn.close()


def guardar_receta(id_receta):
    conn = conectar_db()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO recetas_guardadas (id_usuario, id_receta)
            VALUES (%s, %s)
            ON CONFLICT DO NOTHING;
        """, (id_usuario_logeado, id_receta))
        conn.commit()
        messagebox.showinfo("Éxito", "¡Receta guardada en tus favoritos!")
    except psycopg2.Error as e:
        messagebox.showerror("Error", f"No se pudo guardar la receta: {e.pgerror}")
    finally:
        cursor.close()
        conn.close()

def calificar_receta(id_receta, estrellas, entry_estrellas):
    try:
        estrellas = int(estrellas)
        if estrellas < 0 or estrellas > 5:
            ctk.CTkMessagebox(title="Error", message="La calificación debe ser entre 0 y 5.", icon="cancel")
            return
    except ValueError:
        ctk.CTkMessagebox(title="Error", message="Debe ser un número del 0 al 5.", icon="cancel")
        return

    conn = conectar_db()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO evaluaciones (id_receta, id_usuario, estrellas)
            VALUES (%s, %s, %s)
            ON CONFLICT (id_receta, id_usuario) DO UPDATE
            SET estrellas = EXCLUDED.estrellas;
        """, (id_receta, id_usuario_logeado, estrellas))
        conn.commit()
        entry_estrellas.delete(0, tk.END)
        ctk.CTkMessagebox(title="Gracias", message="¡Calificación registrada!", icon="check")
    finally:
        cursor.close()
        conn.close()

def agregar_comentario(id_receta, texto_comentario, entry_comentario, frame_comentarios):
    if not texto_comentario.strip():
        ctk.CTkMessagebox(title="Error", message="El comentario no puede estar vacío.", icon="cancel")
        return

    conn = conectar_db()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO comentarios (id_receta, id_usuario, texto_comentario)
            VALUES (%s, %s, %s);
        """, (id_receta, id_usuario_logeado, texto_comentario.strip()))
        conn.commit()
        entry_comentario.delete(0, tk.END)
        cargar_comentarios(id_receta, frame_comentarios)
        ctk.CTkMessagebox(title="Éxito", message="¡Comentario agregado!", icon="check")
    except psycopg2.Error as e:
        ctk.CTkMessagebox(title="Error", message=f"No se pudo agregar el comentario: {e.pgerror}", icon="cancel")
    finally:
        cursor.close()
        conn.close()

def cargar_comentarios(id_receta, frame_comentarios):
    for widget in frame_comentarios.winfo_children():
        widget.destroy()

    conn = conectar_db()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT u.nombre_usuario, c.texto_comentario
            FROM comentarios c
            JOIN usuarios u ON c.id_usuario = u.id_usuario
            WHERE c.id_receta = %s
            ORDER BY c.fecha_comentario ASC
        """, (id_receta,))
        comentarios = cursor.fetchall()

        if comentarios:
            for usuario, texto in comentarios:
                tk.Label(frame_comentarios, text=f"{usuario}: {texto}", font=(FUENTE, 14), bg=COLOR_FONDO).pack(anchor='w', padx=10)
        else:
            tk.Label(frame_comentarios, text="No hay comentarios aún.", font=(FUENTE, 14), bg=COLOR_FONDO).pack()
    finally:
        cursor.close()
        conn.close()
def agregar_receta():
    app.iconify()
    ventana = tk.Toplevel(app)
    ventana.title("Agregar Nueva Receta")
    ventana.geometry("750x1200")
    ventana.configure(bg=COLOR_FONDO)
    def restaurar():
        app.deiconify()
        ventana.destroy()
    ventana.protocol("WM_DELETE_WINDOW", restaurar)

    ingredientes_temp = []

    ctk.CTkLabel(ventana, text="Título", font=(FUENTE, 20)).pack(pady=5)
    entry_titulo = ctk.CTkEntry(ventana, width=350, font=(FUENTE, 16))
    entry_titulo.pack()

    ctk.CTkLabel(ventana, text="Descripción", font=(FUENTE, 20)).pack(pady=5)
    entry_descripcion = tk.Text(ventana, width=60, height=6, font=(FUENTE, 14))
    entry_descripcion.pack()

    ctk.CTkLabel(ventana, text="Tiempo de Preparación (min)", font=(FUENTE, 20)).pack(pady=5)
    entry_tiempo = ctk.CTkEntry(ventana, width=150, font=(FUENTE, 16))
    entry_tiempo.pack()

    ctk.CTkLabel(ventana, text="Ruta de Imagen", font=(FUENTE, 20)).pack(pady=5)
    entry_imagen = ctk.CTkEntry(ventana, width=350, font=(FUENTE, 16))
    entry_imagen.pack()

    ctk.CTkLabel(ventana, text="Selecciona Categoría", font=(FUENTE, 20)).pack(pady=5)
    conn = conectar_db()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT nombre_categoria FROM categorias ORDER BY nombre_categoria;")
        categorias_opciones = [fila[0] for fila in cursor.fetchall()]
    finally:
        cursor.close()
        conn.close()

    categoria_seleccionada = tk.StringVar(value=categorias_opciones[0])
    dropdown_categoria = ctk.CTkOptionMenu(ventana, values=categorias_opciones, variable=categoria_seleccionada, width=200, font=(FUENTE, 16))
    dropdown_categoria.pack(pady=5)

    # Ingredientes
    ctk.CTkLabel(ventana, text="Agregar Ingredientes", font=(FUENTE, 20, "bold")).pack(pady=10)
    frame_ing = tk.Frame(ventana, bg=COLOR_FONDO)
    frame_ing.pack(pady=5)

    tk.Label(frame_ing, text="Nombre", font=(FUENTE, 14), bg=COLOR_FONDO).grid(row=0, column=0, padx=5)
    tk.Label(frame_ing, text="Cantidad", font=(FUENTE, 14), bg=COLOR_FONDO).grid(row=0, column=1, padx=5)
    tk.Label(frame_ing, text="Unidad", font=(FUENTE, 14), bg=COLOR_FONDO).grid(row=0, column=2, padx=5)

    entry_nombre_ing = tk.Entry(frame_ing, width=20, font=(FUENTE, 14))
    entry_nombre_ing.grid(row=1, column=0, padx=5)
    entry_cantidad = tk.Entry(frame_ing, width=10, font=(FUENTE, 14))
    entry_cantidad.grid(row=1, column=1, padx=5)

    unidades_frecuentes = ["pz", "ml", "gr", "kg", "lb", "oz", "c/c", "taza", "c/s","L"]
    unidad_var = tk.StringVar(value=unidades_frecuentes[0])
    dropdown_unidad = ctk.CTkOptionMenu(frame_ing, values=unidades_frecuentes, variable=unidad_var, width=100, font=(FUENTE, 14))
    dropdown_unidad.grid(row=1, column=2, padx=5)

    lista_ingredientes = tk.Listbox(ventana, width=65, height=8, font=(FUENTE, 13))
    lista_ingredientes.pack(pady=10)

    def agregar_ingrediente():
        nombre = entry_nombre_ing.get().strip()
        cantidad = entry_cantidad.get().strip()
        unidad = unidad_var.get().strip()
        if not nombre or not cantidad or not unidad:
            messagebox.showwarning("Campos incompletos", "Completa todos los campos del ingrediente.")
            return
        ingredientes_temp.append((nombre, cantidad, unidad))
        lista_ingredientes.insert(tk.END, f"{cantidad} {unidad} de {nombre}")
        entry_nombre_ing.delete(0, tk.END)
        entry_cantidad.delete(0, tk.END)
        unidad_var.set(unidades_frecuentes[0])

    ctk.CTkButton(ventana, text="Agregar Ingrediente", font=(FUENTE, 16),
                  fg_color=COLOR_BOTON, hover_color=COLOR_HOVER,
                  width=200, corner_radius=10, command=agregar_ingrediente).pack(pady=10)

    def guardar_nueva_receta():
        titulo = entry_titulo.get()
        descripcion = entry_descripcion.get("1.0", tk.END).strip()
        tiempo = entry_tiempo.get()
        imagen = entry_imagen.get()
        categoria_nombre = categoria_seleccionada.get()

        if not titulo or not descripcion or not tiempo or not ingredientes_temp:
            messagebox.showerror("Error", "Completa todos los campos y agrega al menos un ingrediente.")
            return

        try:
            tiempo = int(tiempo)
        except ValueError:
            messagebox.showerror("Error", "Tiempo debe ser un número.")
            return

        conn = conectar_db()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT id_categoria FROM categorias WHERE nombre_categoria = %s", (categoria_nombre,))
            categoria = cursor.fetchone()
            if not categoria:
                messagebox.showerror("Error", "Categoría no encontrada.")
                return
            id_categoria = categoria[0]

            cursor.execute("""
                INSERT INTO recetas (titulo, descripcion, tiempo_preparacion, imagen, id_categoria, id_usuario)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id_receta;
            """, (titulo, descripcion, tiempo, imagen, id_categoria, id_usuario_logeado))
            id_receta = cursor.fetchone()[0]

            for nombre, cantidad, unidad in ingredientes_temp:
                cursor.execute("INSERT INTO ingredientes (nombre_ingrediente) VALUES (%s) ON CONFLICT (nombre_ingrediente) DO NOTHING", (nombre,))
                cursor.execute("SELECT id_ingrediente FROM ingredientes WHERE nombre_ingrediente = %s", (nombre,))
                id_ingrediente = cursor.fetchone()[0]
                cursor.execute("""
                    INSERT INTO receta_ingredientes (id_receta, id_ingrediente, cantidad, unidad)
                    VALUES (%s, %s, %s, %s)
                """, (id_receta, id_ingrediente, cantidad, unidad))

            conn.commit()
            messagebox.showinfo("Éxito", "Receta agregada correctamente.")
            ventana.destroy()

        except psycopg2.Error as e:
            messagebox.showerror("Error", f"No se pudo agregar la receta: {e.pgerror}")
        finally:
            cursor.close()
            conn.close()

    ctk.CTkButton(ventana, text="Guardar Receta", font=(FUENTE, 16),
                  fg_color="#4CAF50", hover_color="#81C784",
                  width=200, corner_radius=10, command=guardar_nueva_receta).pack(pady=20)


# ============================
# Ejecutar la aplicación
# ============================
app.mainloop()
