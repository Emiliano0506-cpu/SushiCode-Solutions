"""Interfaz gráfica de SushiCode desarrollada con Tkinter."""
import tkinter as tk
from tkinter import ttk, messagebox
from decimal import Decimal, InvalidOperation

import funciones
from menu import crud as menu_crud
from pedidos import crud as pedidos_crud
from clientes import crud as clientes_crud
from modelos import Cliente


ROJO = "#c90000"
ROJO_OSCURO = "#a90000"
FONDO = "#f3f3f3"
BLANCO = "#ffffff"
TEXTO = "#292929"
GRIS = "#777777"


class SushiCodeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SushiCode")
        self.root.geometry("1120x720")
        self.root.minsize(900, 600)
        self.root.configure(bg=FONDO)
        self.db = funciones.conectar()
        self.usuario_admin = "admin"
        self.password_admin = "admin123"
        self.carrito = []
        self._estilos()
        if self.db is None:
            messagebox.showerror("Error de conexión",
                "No fue posible conectar con MySQL.\nRevisa funciones.py y ejecuta sql/schema.sql.")
            self.root.after(100, self.salir)
            return
        self.mostrar_inicio()

    def _estilos(self):
        s = ttk.Style()
        try:
            s.theme_use("clam")
        except tk.TclError:
            pass
        s.configure("Treeview", background=BLANCO, fieldbackground=BLANCO,
                    foreground=TEXTO, rowheight=28, font=("Segoe UI", 9))
        s.configure("Treeview.Heading", background="#eeeeee", foreground=TEXTO,
                    font=("Segoe UI", 9, "bold"))
        s.map("Treeview", background=[("selected", "#f2cccc")],
              foreground=[("selected", TEXTO)])
        s.configure("TCombobox", padding=5)

    def limpiar(self):
        for w in self.root.winfo_children():
            w.destroy()

    def encabezado(self, titulo, subtitulo=None):
        top = tk.Frame(self.root, bg=BLANCO, height=72)
        top.pack(fill="x")
        top.pack_propagate(False)
        tk.Label(top, text="SushiCode", bg=BLANCO, fg=ROJO,
                 font=("Segoe UI", 20, "bold")).pack(side="left", padx=24)
        tk.Label(top, text=titulo, bg=BLANCO, fg=TEXTO,
                 font=("Segoe UI", 14, "bold")).pack(side="left", padx=20)
        if subtitulo:
            tk.Label(top, text=subtitulo, bg=BLANCO, fg=GRIS,
                     font=("Segoe UI", 9)).pack(side="left", padx=4)
        tk.Frame(self.root, bg=ROJO, height=3).pack(fill="x")

    def boton(self, parent, texto, comando, secundario=False):
        return tk.Button(parent, text=texto, command=comando,
                         bg="#eeeeee" if secundario else ROJO,
                         fg=TEXTO if secundario else BLANCO,
                         activebackground=ROJO_OSCURO, activeforeground=BLANCO,
                         relief="flat", bd=0, padx=16, pady=9,
                         font=("Segoe UI", 9, "bold"), cursor="hand2")

    def tarjeta(self, parent, titulo, descripcion, comando):
        f = tk.Frame(parent, bg=BLANCO, highlightbackground="#cccccc",
                     highlightthickness=1, padx=18, pady=18)
        tk.Label(f, text="■", fg=ROJO, bg=BLANCO,
                 font=("Segoe UI", 17)).pack(anchor="w")
        tk.Label(f, text=titulo, fg=TEXTO, bg=BLANCO,
                 font=("Segoe UI", 13, "bold")).pack(anchor="w", pady=(8, 4))
        tk.Label(f, text=descripcion, fg=GRIS, bg=BLANCO,
                 font=("Segoe UI", 9), wraplength=210, justify="left").pack(anchor="w", pady=(0, 14))
        self.boton(f, "Ir ahora  ›", comando).pack(fill="x")
        return f

    def mostrar_inicio(self):
        self.limpiar()
        self.encabezado("Inicio", "Selecciona cómo deseas ingresar")
        area = tk.Frame(self.root, bg=FONDO, padx=34, pady=32)
        area.pack(fill="both", expand=True)
        tk.Label(area, text="Bienvenido a SushiCode", bg=FONDO, fg=TEXTO,
                 font=("Segoe UI", 22, "bold")).pack(anchor="w")
        tk.Label(area, text="Sistema de administración y pedidos de sushi",
                 bg=FONDO, fg=GRIS, font=("Segoe UI", 10)).pack(anchor="w", pady=(3, 25))
        cards = tk.Frame(area, bg=FONDO)
        cards.pack(anchor="w")
        self.tarjeta(cards, "Administrador", "Inicia sesión para administrar menús, platillos y pedidos.",
                     self.mostrar_login).grid(row=0, column=0, padx=(0, 18), sticky="n")
        self.tarjeta(cards, "Cliente", "Consulta los platillos disponibles y crea tu pedido.",
                     self.menu_cliente).grid(row=0, column=1, padx=18, sticky="n")
        self.boton(area, "Salir del sistema", self.salir, True).pack(anchor="w", pady=28)

    def mostrar_login(self):
        self.limpiar()
        self.encabezado("Inicio de sesión", "Acceso exclusivo para administradores")
        panel = tk.Frame(self.root, bg=BLANCO, padx=30, pady=28,
                         highlightbackground="#dddddd", highlightthickness=1)
        panel.place(relx=.5, rely=.52, anchor="center", width=410)
        tk.Label(panel, text="Inicia sesión", bg=BLANCO, fg=TEXTO,
                 font=("Segoe UI", 17, "bold")).pack(anchor="w")
        tk.Label(panel, text="Ingresa tus credenciales de administrador.",
                 bg=BLANCO, fg=GRIS, font=("Segoe UI", 9)).pack(anchor="w", pady=(2, 20))
        tk.Label(panel, text="Usuario", bg=BLANCO, fg=TEXTO).pack(anchor="w")
        usuario = ttk.Entry(panel)
        usuario.pack(fill="x", pady=(4, 13))
        tk.Label(panel, text="Contraseña", bg=BLANCO, fg=TEXTO).pack(anchor="w")
        password = ttk.Entry(panel, show="•")
        password.pack(fill="x", pady=(4, 20))
        def entrar(event=None):
            if usuario.get().strip() == self.usuario_admin and password.get() == self.password_admin:
                self.menu_admin()
            else:
                messagebox.showerror("Acceso denegado", "Usuario o contraseña incorrectos.")
                password.delete(0, "end")
                password.focus_set()
        self.boton(panel, "Iniciar sesión", entrar).pack(fill="x")
        self.boton(panel, "Regresar", self.mostrar_inicio, True).pack(fill="x", pady=(9, 0))
        password.bind("<Return>", entrar)
        usuario.focus_set()

    def menu_admin(self):
        self.limpiar()
        self.encabezado("Contenido principal", "Panel del administrador")
        area = tk.Frame(self.root, bg=FONDO, padx=30, pady=30)
        area.pack(fill="both", expand=True)
        tk.Label(area, text="¿Qué quieres gestionar?", bg=FONDO, fg=TEXTO,
                 font=("Segoe UI", 19, "bold")).pack(anchor="w")
        cards = tk.Frame(area, bg=FONDO)
        cards.pack(anchor="w", pady=22)
        self.tarjeta(cards, "Menú", "Crea menús, agrega platillos, consulta y actualiza su disponibilidad.",
                     self.admin_menu).grid(row=0, column=0, padx=(0, 18), sticky="n")
        self.tarjeta(cards, "Pedidos", "Registra pedidos, consulta sus detalles y administra sus estados.",
                     self.admin_pedidos).grid(row=0, column=1, padx=18, sticky="n")
        self.boton(area, "Cerrar sesión", self.mostrar_inicio, True).pack(anchor="w", pady=16)

    def _pagina(self, titulo, volver):
        self.limpiar()
        self.encabezado(titulo)
        cont = tk.Frame(self.root, bg=FONDO, padx=22, pady=18)
        cont.pack(fill="both", expand=True)
        self.boton(cont, "‹ Regresar", volver, True).pack(anchor="w", pady=(0, 12))
        return cont

    def _tabla(self, parent, columnas, encabezados=None, height=12):
        wrap = tk.Frame(parent, bg=BLANCO, padx=8, pady=8)
        wrap.pack(fill="both", expand=True, pady=8)
        tree = ttk.Treeview(wrap, columns=columnas, show="headings", height=height)
        for col, label in zip(columnas, encabezados or columnas):
            tree.heading(col, text=label)
            tree.column(col, width=120, anchor="w")
        sy = ttk.Scrollbar(wrap, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=sy.set)
        tree.pack(side="left", fill="both", expand=True)
        sy.pack(side="right", fill="y")
        return tree

    def _campo(self, parent, etiqueta, ancho=28, valor=""):
        f = tk.Frame(parent, bg=BLANCO)
        tk.Label(f, text=etiqueta, bg=BLANCO, fg=TEXTO,
                 font=("Segoe UI", 9)).pack(anchor="w")
        e = ttk.Entry(f, width=ancho)
        if valor:
            e.insert(0, valor)
        e.pack(fill="x", pady=(3, 8))
        return f, e

    def admin_menu(self):
        cont = self._pagina("Menú y platillos", self.menu_admin)
        acciones = tk.Frame(cont, bg=FONDO)
        acciones.pack(fill="x")
        self.boton(acciones, "Crear menú", self.form_menu).pack(side="left", padx=(0, 7))
        self.boton(acciones, "Agregar platillo", self.form_platillo).pack(side="left", padx=7)
        self.boton(acciones, "Actualizar disponibilidad", self.actualizar_disponibilidad, True).pack(side="left", padx=7)
        self.boton(acciones, "Eliminar platillo", self.eliminar_platillo, True).pack(side="left", padx=7)
        self.boton(acciones, "Actualizar lista", self.admin_menu).pack(side="right")
        tree = self._tabla(cont, ("id","nombre","categoria","precio","descripcion","disponible","menu"),
                           ("ID","Platillo","Categoría","Precio","Descripción","Disponible","Menú"))
        try:
            for p in menu_crud.platillos(self.db):
                tree.insert("", "end", values=(p[0],p[1],p[2],f"${float(p[3]):.2f}",p[4],"Sí" if p[5] else "No",p[6]))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def form_menu(self):
        self._form_simple("Crear menú", [("Nombre", "nombre"), ("Descripción", "descripcion")],
            lambda v: menu_crud.agregar_menu(v["nombre"],v["descripcion"],self.db),
            "Menú guardado correctamente.")

    def form_platillo(self):
        menus = menu_crud.menus(self.db)
        if not menus:
            messagebox.showwarning("Falta un menú", "Primero crea un menú para poder agregar platillos.")
            return
        self.limpiar()
        self.encabezado("Agregar platillo")
        panel = tk.Frame(self.root, bg=BLANCO, padx=24, pady=20)
        panel.pack(fill="both", expand=True, padx=24, pady=20)
        tk.Label(panel, text="Datos del platillo", bg=BLANCO, fg=TEXTO,
                 font=("Segoe UI", 15, "bold")).pack(anchor="w", pady=(0, 14))
        labels = [("Nombre","nombre"),("Descripción","descripcion"),("Categoría","categoria"),("Precio","precio")]
        entries={}
        for label,key in labels:
            f,e=self._campo(panel,label)
            f.pack(fill="x")
            entries[key]=e
        tk.Label(panel,text="Menú al que pertenece",bg=BLANCO).pack(anchor="w")
        opciones=[f"{m[0]} - {m[1]}" for m in menus]
        combo=ttk.Combobox(panel,values=opciones,state="readonly")
        combo.pack(fill="x",pady=(3,12)); combo.current(0)
        disponible=tk.BooleanVar(value=True)
        tk.Checkbutton(panel,text="Disponible",variable=disponible,bg=BLANCO).pack(anchor="w",pady=5)
        def guardar():
            try:
                nombre=entries["nombre"].get().strip()
                precio=float(entries["precio"].get())
                if not nombre or precio<0: raise ValueError("Escribe un nombre y un precio válido.")
                id_menu=int(combo.get().split(" - ",1)[0])
                if not messagebox.askyesno("Confirmar", "¿Estás seguro de agregar este platillo?"): return
                ident=menu_crud.agregar_platillo(id_menu,nombre,entries["descripcion"].get(),
                    entries["categoria"].get(),precio,disponible.get(),self.db)
                messagebox.showinfo("Guardado",f"Platillo agregado correctamente. ID: {ident}")
                for e in entries.values(): e.delete(0,"end")
                entries["nombre"].focus_set()
                combo.current(0); disponible.set(True)
            except Exception as e: messagebox.showerror("No se pudo guardar",str(e))
        self.boton(panel,"Guardar platillo",guardar).pack(anchor="w",pady=12)
        self.boton(panel,"Regresar",self.admin_menu,True).pack(anchor="w")

    def _form_simple(self, titulo, campos, guardar_fn, mensaje):
        self.limpiar()
        self.encabezado(titulo)
        panel=tk.Frame(self.root,bg=BLANCO,padx=26,pady=22)
        panel.pack(fill="both",expand=True,padx=24,pady=20)
        entries={}
        for label,key in campos:
            f,e=self._campo(panel,label)
            f.pack(fill="x")
            entries[key]=e
        def guardar():
            valores={k:e.get().strip() for k,e in entries.items()}
            if any(not x for x in valores.values()):
                messagebox.showwarning("Datos incompletos","Completa todos los campos.")
                return
            if not messagebox.askyesno("Confirmar",f"¿Estás seguro de guardar {titulo.lower()}?"): return
            try:
                guardar_fn(valores)
                messagebox.showinfo("Correcto",mensaje)
                for e in entries.values(): e.delete(0,"end")
                next(iter(entries.values())).focus_set()
            except Exception as e: messagebox.showerror("Error",str(e))
        self.boton(panel,"Guardar",guardar).pack(anchor="w",pady=10)
        self.boton(panel,"Regresar",self.admin_menu,True).pack(anchor="w")

    def _seleccion_id(self, tree, titulo):
        sel=tree.selection()
        if not sel:
            messagebox.showwarning(titulo,"Selecciona primero un registro de la tabla.")
            return None
        return tree.item(sel[0],"values")[0]

    def actualizar_disponibilidad(self):
        rows=menu_crud.platillos(self.db)
        if not rows:
            messagebox.showinfo("Platillos","No hay platillos registrados.")
            return
        win=tk.Toplevel(self.root); win.title("Actualizar disponibilidad"); win.configure(bg=BLANCO)
        win.geometry("380x190"); win.transient(self.root); win.grab_set()
        tk.Label(win,text="Selecciona un platillo",bg=BLANCO).pack(anchor="w",padx=18,pady=(18,5))
        cb=ttk.Combobox(win,state="readonly",values=[f"{r[0]} - {r[1]} ({'Disponible' if r[5] else 'No disponible'})" for r in rows])
        cb.pack(fill="x",padx=18); cb.current(0)
        var=tk.BooleanVar(value=bool(rows[0][5]))
        def cambio(event=None):
            var.set(bool(rows[cb.current()][5]))
        cb.bind("<<ComboboxSelected>>",cambio)
        tk.Checkbutton(win,text="Disponible",variable=var,bg=BLANCO).pack(anchor="w",padx=18,pady=8)
        def guardar():
            if not messagebox.askyesno("Confirmar","¿Estás seguro de actualizar la disponibilidad?",parent=win): return
            cur=self.db.cursor()
            try:
                cur.execute("UPDATE Platillos SET disponibilidad=%s WHERE id_platillo=%s",(var.get(),rows[cb.current()][0]))
                self.db.commit(); win.destroy(); self.admin_menu()
                messagebox.showinfo("Correcto","Disponibilidad actualizada.")
            except Exception as e:
                self.db.rollback(); messagebox.showerror("Error",str(e),parent=win)
        self.boton(win,"Guardar cambios",guardar).pack(pady=6)

    def eliminar_platillo(self):
        rows=menu_crud.platillos(self.db)
        if not rows:
            messagebox.showinfo("Platillos","No hay platillos registrados."); return
        win=tk.Toplevel(self.root); win.title("Eliminar platillo"); win.geometry("390x150")
        win.configure(bg=BLANCO); win.transient(self.root); win.grab_set()
        tk.Label(win,text="Platillo que deseas eliminar",bg=BLANCO).pack(anchor="w",padx=18,pady=(18,5))
        cb=ttk.Combobox(win,state="readonly",values=[f"{r[0]} - {r[1]}" for r in rows])
        cb.pack(fill="x",padx=18); cb.current(0)
        def borrar():
            if not messagebox.askyesno("Confirmar eliminación","¿Estás seguro de eliminar este platillo? Esta acción no se puede deshacer.",parent=win): return
            try:
                menu_crud.eliminar_platillo(rows[cb.current()][0],self.db)
                win.destroy(); self.admin_menu()
                messagebox.showinfo("Correcto","Platillo eliminado.")
            except Exception as e: messagebox.showerror("No se pudo eliminar",str(e),parent=win)
        self.boton(win,"Eliminar",borrar).pack(pady=10)

    def menu_cliente(self):
        cont=self._pagina("Menú disponible",self.mostrar_inicio)
        self.boton(cont,"Crear pedido",self.form_pedido_cliente).pack(anchor="e")
        tree=self._tabla(cont,("nombre","categoria","precio","descripcion","menu"),
                         ("Platillo","Categoría","Precio","Descripción","Menú"))
        try:
            for p in menu_crud.platillos(self.db,True):
                tree.insert("","end",values=(p[1],p[2],f"${float(p[3]):.2f}",p[4],p[6]))
            if not tree.get_children():
                tk.Label(cont,text="No hay platillos disponibles por el momento.",bg=FONDO,fg=GRIS).pack()
        except Exception as e: messagebox.showerror("Error",str(e))

    def form_pedido_cliente(self, admin=False):
        disponibles=menu_crud.platillos(self.db,True)
        if not disponibles:
            messagebox.showinfo("Sin platillos","No hay platillos disponibles para pedir."); return
        self.carrito=[]
        self.limpiar()
        self.encabezado("Realizar pedido","Selecciona tus platillos y completa tus datos")
        main=tk.Frame(self.root,bg=FONDO,padx=20,pady=14); main.pack(fill="both",expand=True)
        left=tk.Frame(main,bg=BLANCO,padx=14,pady=12); left.pack(side="left",fill="both",expand=True,padx=(0,10))
        right=tk.Frame(main,bg=BLANCO,padx=14,pady=12); right.pack(side="right",fill="y")
        tk.Label(left,text="1. Productos",bg=BLANCO,font=("Segoe UI",13,"bold")).pack(anchor="w")
        product_tree=self._tabla(left,("id","nombre","precio"),("ID","Platillo","Precio"),height=9)
        # Tabla compacta en el panel de productos.
        for p in disponibles: product_tree.insert("","end",values=(p[0],p[1],f"${float(p[3]):.2f}"))
        qtyrow=tk.Frame(left,bg=BLANCO); qtyrow.pack(fill="x",pady=8)
        tk.Label(qtyrow,text="Cantidad:",bg=BLANCO).pack(side="left")
        qty=ttk.Spinbox(qtyrow,from_=1,to=99,width=6); qty.pack(side="left",padx=8); qty.set(1)
        cart_tree=self._tabla(left,("platillo","cantidad","subtotal"),("Pedido","Cant.","Subtotal"),height=5)
        totalvar=tk.StringVar(value="Total: $0.00")
        tk.Label(right,text="2. Cliente y entrega",bg=BLANCO,font=("Segoe UI",13,"bold")).pack(anchor="w",pady=(0,10))
        fields={}
        for label,key in [("Nombre","nombre"),("Apellido paterno","apellido"),("Teléfono","telefono"),("Ciudad","ciudad"),("Estado","estado")]:
            f,e=self._campo(right,label,24); f.pack(fill="x"); fields[key]=e
        tk.Label(right,text="Si ya tienes ID de cliente, puedes usarlo:",bg=BLANCO,fg=GRIS,wraplength=240).pack(anchor="w",pady=(6,2))
        id_entry=ttk.Entry(right); id_entry.pack(fill="x")
        def agregar():
            sel=product_tree.selection()
            if not sel: messagebox.showwarning("Selecciona","Selecciona un platillo."); return
            try: cantidad=int(qty.get())
            except ValueError: messagebox.showerror("Cantidad","Ingresa una cantidad válida."); return
            if cantidad<1: messagebox.showerror("Cantidad","La cantidad debe ser mayor a cero."); return
            pid=int(product_tree.item(sel[0],"values")[0])
            p=next(x for x in disponibles if int(x[0])==pid)
            self.carrito.append((pid,cantidad,float(p[3]),p[1]))
            cart_tree.insert("","end",values=(p[1],cantidad,f"${cantidad*float(p[3]):.2f}"))
            total=sum(x[1]*x[2] for x in self.carrito)
            totalvar.set(f"Total: ${total:.2f}")
            qty.set(1)
        self.boton(left,"Agregar seleccionado",agregar).pack(anchor="w",pady=(0,8))
        tk.Label(right,textvariable=totalvar,bg=BLANCO,fg=ROJO,font=("Segoe UI",14,"bold")).pack(anchor="w",pady=14)
        def registrar():
            if not self.carrito:
                messagebox.showwarning("Pedido vacío","Agrega al menos un platillo."); return
            try:
                if id_entry.get().strip():
                    ident=int(id_entry.get())
                    if not clientes_crud.buscar(ident,self.db):
                        messagebox.showerror("Cliente","No existe un cliente con ese ID."); return
                    id_cliente=ident
                else:
                    requeridos=["nombre","apellido","ciudad","estado"]
                    if any(not fields[k].get().strip() for k in requeridos):
                        messagebox.showwarning("Datos incompletos","Completa nombre, apellido paterno, ciudad y estado."); return
                    cliente=Cliente(fields["nombre"].get(),fields["apellido"].get(),
                        telefono=fields["telefono"].get(),ciudad=fields["ciudad"].get(),estado=fields["estado"].get())
                    if not messagebox.askyesno("Confirmar","¿Estás seguro de registrar tus datos y crear este pedido?"): return
                    id_cliente=clientes_crud.insertar(cliente,self.db)
                if id_entry.get().strip() and not messagebox.askyesno("Confirmar pedido","¿Estás seguro de realizar este pedido?"): return
                pedido_id,total=pedidos_crud.crear_pedido(id_cliente,[(x[0],x[1],x[2]) for x in self.carrito],self.db)
                volver = self.admin_pedidos if admin else self.mostrar_inicio
                otro = (lambda: self.form_pedido_cliente(admin=True)) if admin else self.form_pedido_cliente
                self.mensaje_exito(pedido_id,total,volver=volver,otro=otro)
            except Exception as e:
                messagebox.showerror("No se pudo realizar el pedido",str(e))
        self.boton(right,"Confirmar pedido",registrar).pack(fill="x")
        volver = self.admin_pedidos if admin else self.menu_cliente
        self.boton(right,"Cancelar",volver,True).pack(fill="x",pady=(8,0))

    def admin_pedidos(self):
        cont=self._pagina("Administración de pedidos",self.menu_admin)
        bar=tk.Frame(cont,bg=FONDO); bar.pack(fill="x")
        self.boton(bar,"Registrar pedido",self.form_pedido_admin).pack(side="left",padx=(0,7))
        self.boton(bar,"Ver detalle",lambda:self.ver_detalle(tree),True).pack(side="left",padx=7)
        self.boton(bar,"Cambiar estado",lambda:self.cambiar_estado(tree),True).pack(side="left",padx=7)
        self.boton(bar,"Eliminar pedido",lambda:self.eliminar_pedido(tree),True).pack(side="left",padx=7)
        self.boton(bar,"Actualizar",self.admin_pedidos).pack(side="right")
        tree=self._tabla(cont,("id","cliente","fecha","estado","total"),
                         ("Pedido","Cliente","Fecha","Estado","Total"))
        try:
            for r in pedidos_crud.consultar(self.db):
                tree.insert("","end",values=(r[0],f"{r[1]} {r[2]}",r[3],r[4],f"${float(r[5]):.2f}"))
        except Exception as e: messagebox.showerror("Error",str(e))

    def ver_detalle(self,tree):
        ident=self._seleccion_id(tree,"Detalle"); 
        if not ident: return
        rows=pedidos_crud.detalle(ident,self.db)
        win=tk.Toplevel(self.root); win.title(f"Detalle del pedido {ident}"); win.geometry("650x360")
        t=self._tabla(win,("id","platillo","cantidad","precio","subtotal"),
                      ("ID","Platillo","Cantidad","Precio unitario","Subtotal"))
        for r in rows: t.insert("","end",values=(r[0],r[2],r[3],f"${float(r[4]):.2f}",f"${float(r[5]):.2f}"))

    def cambiar_estado(self,tree):
        ident=self._seleccion_id(tree,"Actualizar pedido")
        if not ident: return
        win=tk.Toplevel(self.root); win.title("Cambiar estado"); win.geometry("350x190"); win.configure(bg=BLANCO)
        tk.Label(win,text=f"Nuevo estado del pedido #{ident}",bg=BLANCO).pack(pady=(22,8))
        cb=ttk.Combobox(win,state="readonly",values=["En preparación","En camino","Entregado","Cancelado"])
        cb.pack(fill="x",padx=22); cb.current(0)
        def guardar():
            if not messagebox.askyesno("Confirmar","¿Estás seguro de actualizar el estado?",parent=win): return
            try:
                pedidos_crud.cambiar_estado(ident,cb.get(),self.db)
                win.destroy(); self.admin_pedidos()
                messagebox.showinfo("Correcto","Estado actualizado.")
            except Exception as e: messagebox.showerror("Error",str(e),parent=win)
        self.boton(win,"Guardar cambios",guardar).pack(pady=14)

    def eliminar_pedido(self,tree):
        ident=self._seleccion_id(tree,"Eliminar pedido")
        if not ident: return
        if not messagebox.askyesno("Confirmar eliminación",
            f"¿Estás seguro de eliminar el pedido #{ident}? Se eliminarán también sus detalles."): return
        try:
            pedidos_crud.eliminar(ident,self.db); self.admin_pedidos()
            messagebox.showinfo("Correcto","Pedido eliminado.")
        except Exception as e: messagebox.showerror("Error",str(e))

    def form_pedido_admin(self):
        self.form_pedido_cliente(admin=True)

    def mensaje_exito(self,pedido_id,total,volver,otro=None):
        self.limpiar()
        self.encabezado("Página de mensaje")
        panel=tk.Frame(self.root,bg=BLANCO)
        panel.place(relx=.5,rely=.52,anchor="center")
        tk.Label(panel,text="¡Tu pedido fue realizado con éxito!",bg=BLANCO,
                 fg=TEXTO,font=("Segoe UI",15)).pack(padx=50,pady=(35,10))
        tk.Label(panel,text="✓",bg="#24bf60",fg=BLANCO,font=("Segoe UI",22,"bold"),
                 width=2).pack(pady=8)
        tk.Label(panel,text=f"Pedido #{pedido_id}  |  Total: ${total:.2f}",
                 bg=BLANCO,fg=GRIS,font=("Segoe UI",10)).pack(pady=8)
        if otro:
            self.boton(panel,"Realizar otro pedido",otro).pack(fill="x",padx=45,pady=(12,6))
        self.boton(panel,"Página principal",volver,True).pack(fill="x",padx=45,pady=(0,35))

    def salir(self):
        if self.db is not None:
            try: self.db.close()
            except Exception: pass
            self.db=None
        self.limpiar()
        self.root.configure(bg=BLANCO)
        panel=tk.Frame(self.root,bg=BLANCO)
        panel.place(relx=.5,rely=.5,anchor="center")
        tk.Label(panel,text="SushiCode",bg=BLANCO,fg=ROJO,
                 font=("Segoe UI",25,"bold")).pack(pady=8)
        tk.Label(panel,text="Muchas gracias por utilizar SushiCode",
                 bg=BLANCO,fg=TEXTO,font=("Segoe UI",15)).pack(pady=12)
        self.root.after(2600,self.root.destroy)


def iniciar():
    root=tk.Tk()
    app=SushiCodeApp(root)
    root.protocol("WM_DELETE_WINDOW",app.salir)
    root.mainloop()


if __name__ == "__main__":
    iniciar()
