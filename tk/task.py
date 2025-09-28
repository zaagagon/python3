from __future__ import annotations
import csv
import os
from dataclasses import dataclass
from datetime import datetime, date
from typing import List, Optional

import tkinter as tk
from tkinter import ttk, messagebox, filedialog

DATE_FMT = "%Y-%m-%d"

def parse_fecha(s: str) -> date:
    try:
        return datetime.strptime(s, DATE_FMT).date()
    except ValueError as e:
        raise ValueError("Fecha inválida. Use el formato YYYY-MM-DD.") from e

def to_str_fecha(d: date) -> str:
    return d.strftime(DATE_FMT)

@dataclass
class Tarea:
    id: int
    descripcion: str
    fecha_limite: date
    completada: bool = False
    categoria: str = "General"
    prioridad: int = 3  # 1 (alta) … 5 (baja)

    @staticmethod
    def encabezados_csv() -> List[str]:
        return ["id", "descripcion", "fecha_limite", "completada", "categoria", "prioridad"]

    def a_fila(self) -> List[str]:
        return [
            str(self.id),
            self.descripcion,
            to_str_fecha(self.fecha_limite),
            "1" if self.completada else "0",
            self.categoria,
            str(int(self.prioridad)),
        ]

    @staticmethod
    def desde_fila(row: List[str]) -> "Tarea":
        return Tarea(
            id=int(row[0]),
            descripcion=row[1],
            fecha_limite=parse_fecha(row[2]),
            completada=row[3] == "1",
            categoria=row[4],
            prioridad=int(row[5]),
        )

class GestorTareas:
    def __init__(self) -> None:
        self.tareas: List[Tarea] = []
        self._prox_id: int = 1

    def _actualizar_prox_id(self) -> None:
        self._prox_id = (max((t.id for t in self.tareas), default=0) + 1)

    def _buscar(self, id_tarea: int) -> Optional[Tarea]:
        return next((t for t in self.tareas if t.id == id_tarea), None)

    # -------- API ----------
    def agregar(self, descripcion: str, fecha_limite: str,
                categoria: str = "General", prioridad: int | str = 3) -> Tarea:
        if isinstance(prioridad, str) and prioridad.strip():
            prioridad = int(prioridad)
        prioridad = int(prioridad)
        if not (1 <= prioridad <= 5):
            raise ValueError("La prioridad debe estar entre 1 y 5.")
        fecha = parse_fecha(fecha_limite)
        t = Tarea(
            id=self._prox_id,
            descripcion=descripcion.strip(),
            fecha_limite=fecha,
            completada=False,
            categoria=(categoria.strip() or "General"),
            prioridad=prioridad,
        )
        self.tareas.append(t)
        self._prox_id += 1
        return t

    def listar(self, estado: Optional[str] = None, categoria: Optional[str] = None) -> List[Tarea]:
        res = self.tareas
        if estado == "Completadas":
            res = [t for t in res if t.completada]
        elif estado == "Pendientes":
            res = [t for t in res if not t.completada]
        if categoria:
            res = [t for t in res if t.categoria.lower() == categoria.lower()]
        res = sorted(res, key=lambda t: (t.fecha_limite, t.prioridad, t.id))
        return res

    def marcar(self, id_tarea: int, completada: Optional[bool] = None) -> bool:
        t = self._buscar(id_tarea)
        if not t:
            return False
        t.completada = (not t.completada) if completada is None else bool(completada)
        return True

    def editar(self, id_tarea: int, descripcion: Optional[str] = None,
               fecha_limite: Optional[str] = None,
               categoria: Optional[str] = None,
               prioridad: Optional[int | str] = None) -> bool:
        t = self._buscar(id_tarea)
        if not t:
            return False
        if descripcion and descripcion.strip():
            t.descripcion = descripcion.strip()
        if fecha_limite and fecha_limite.strip():
            t.fecha_limite = parse_fecha(fecha_limite.strip())
        if categoria and categoria.strip():
            t.categoria = categoria.strip()
        if prioridad is not None and str(prioridad).strip():
            p = int(prioridad)
            if not (1 <= p <= 5):
                raise ValueError("La prioridad debe estar entre 1 y 5.")
            t.prioridad = p
        return True

    def eliminar(self, id_tarea: int) -> bool:
        t = self._buscar(id_tarea)
        if not t:
            return False
        self.tareas.remove(t)
        return True

    # -------- Persistencia ----------
    def guardar_csv(self, ruta: str) -> None:
        with open(ruta, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(Tarea.encabezados_csv())
            for t in self.tareas:
                w.writerow(t.a_fila())

    def cargar_csv(self, ruta: str) -> None:
        if not os.path.exists(ruta):
            self.tareas = []
            self._prox_id = 1
            return
        with open(ruta, "r", newline="", encoding="utf-8") as f:
            r = csv.reader(f)
            _ = next(r, None)  # encabezado
            self.tareas = [Tarea.desde_fila(row) for row in r if row]
        self._actualizar_prox_id()

# ===================== UI (Tkinter) =====================

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gestor de Tareas")
        self.geometry("950x520")
        self.minsize(900, 480)

        # Modelo
        self.gestor = GestorTareas()
        self.archivo_actual: Optional[str] = "tareas.csv"

        # Estilos
        style = ttk.Style(self)
        # En macOS/Linux/Windows modernos, 'clam' suele verse bien
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure("TButton", padding=6)
        style.configure("Header.TLabel", font=("TkDefaultFont", 12, "bold"))
        style.configure("Muted.TLabel", foreground="#666")

        # Variables de formulario
        self.var_id = tk.StringVar()
        self.var_desc = tk.StringVar()
        self.var_fecha = tk.StringVar()
        self.var_cat = tk.StringVar()
        self.var_prio = tk.StringVar(value="3")
        self.var_estado_filtro = tk.StringVar(value="Todas")
        self.var_cat_filtro = tk.StringVar()

        self._crear_widgets()
        self._refrescar_tabla()

        # Cargar archivo inicial si existe
        if self.archivo_actual and os.path.exists(self.archivo_actual):
            self._accion_cargar(self.archivo_actual)

    # --------- Construcción de UI ----------
    def _crear_widgets(self):
        frm_top = ttk.Frame(self, padding=(10, 10, 10, 0))
        frm_top.pack(fill="x")

        ttk.Label(frm_top, text="Formulario", style="Header.TLabel").grid(row=0, column=0, sticky="w")

        frm_form = ttk.Frame(frm_top)
        frm_form.grid(row=1, column=0, sticky="ew", pady=(4, 8))
        frm_form.columnconfigure(1, weight=1)
        frm_form.columnconfigure(3, weight=1)

        # Fila 1
        ttk.Label(frm_form, text="Id (solo lectura):").grid(row=0, column=0, sticky="w", padx=(0, 6), pady=2)
        ttk.Entry(frm_form, textvariable=self.var_id, state="readonly", width=12).grid(row=0, column=1, sticky="w", pady=2)

        ttk.Label(frm_form, text="Fecha (YYYY-MM-DD):").grid(row=0, column=2, sticky="w", padx=(8, 6), pady=2)
        e_fecha = ttk.Entry(frm_form, textvariable=self.var_fecha)
        e_fecha.grid(row=0, column=3, sticky="ew", pady=2)

        # Fila 2
        ttk.Label(frm_form, text="Descripción:").grid(row=1, column=0, sticky="w", padx=(0, 6), pady=2)
        e_desc = ttk.Entry(frm_form, textvariable=self.var_desc)
        e_desc.grid(row=1, column=1, columnspan=3, sticky="ew", pady=2)

        # Fila 3
        ttk.Label(frm_form, text="Categoría:").grid(row=2, column=0, sticky="w", padx=(0, 6), pady=2)
        e_cat = ttk.Entry(frm_form, textvariable=self.var_cat)
        e_cat.grid(row=2, column=1, sticky="ew", pady=2)

        ttk.Label(frm_form, text="Prioridad (1-5):").grid(row=2, column=2, sticky="w", padx=(8, 6), pady=2)
        e_prio = ttk.Entry(frm_form, textvariable=self.var_prio, width=10)
        e_prio.grid(row=2, column=3, sticky="w", pady=2)

        # Botones de acción
        frm_btns = ttk.Frame(frm_top)
        frm_btns.grid(row=2, column=0, sticky="w", pady=(2, 8))
        ttk.Button(frm_btns, text="Nuevo", command=self._accion_nuevo).grid(row=0, column=0, padx=(0, 4))
        ttk.Button(frm_btns, text="Guardar (Alta/Edición)", command=self._accion_guardar_form).grid(row=0, column=1, padx=4)
        ttk.Button(frm_btns, text="Marcar ✓/✗", command=self._accion_marcar).grid(row=0, column=2, padx=4)
        ttk.Button(frm_btns, text="Eliminar", command=self._accion_eliminar).grid(row=0, column=3, padx=4)

        # Filtros
        frm_filters = ttk.Frame(self, padding=(10, 0, 10, 0))
        frm_filters.pack(fill="x")
        ttk.Label(frm_filters, text="Listado", style="Header.TLabel").grid(row=0, column=0, sticky="w")

        ttk.Label(frm_filters, text="Estado:").grid(row=1, column=0, sticky="w", pady=4)
        cmb_estado = ttk.Combobox(frm_filters, textvariable=self.var_estado_filtro, width=14,
                                  values=["Todas", "Pendientes", "Completadas"], state="readonly")
        cmb_estado.grid(row=1, column=1, sticky="w", padx=(4, 12))
        cmb_estado.bind("<<ComboboxSelected>>", lambda e: self._refrescar_tabla())

        ttk.Label(frm_filters, text="Categoría:").grid(row=1, column=2, sticky="w")
        e_fcat = ttk.Entry(frm_filters, textvariable=self.var_cat_filtro, width=18)
        e_fcat.grid(row=1, column=3, sticky="w", padx=(4, 12))
        ttk.Button(frm_filters, text="Aplicar filtros", command=self._refrescar_tabla).grid(row=1, column=4, padx=4)
        ttk.Button(frm_filters, text="Limpiar filtros", command=self._limpiar_filtros).grid(row=1, column=5, padx=4)

        # Tabla
        frm_table = ttk.Frame(self, padding=(10, 6, 10, 6))
        frm_table.pack(fill="both", expand=True)

        cols = ("id", "fecha", "prioridad", "categoria", "estado", "descripcion")
        self.tree = ttk.Treeview(frm_table, columns=cols, show="headings", selectmode="browse")
        self.tree.heading("id", text="Id", command=lambda: self._ordenar_por("id"))
        self.tree.heading("fecha", text="Fecha", command=lambda: self._ordenar_por("fecha"))
        self.tree.heading("prioridad", text="Prioridad", command=lambda: self._ordenar_por("prioridad"))
        self.tree.heading("categoria", text="Categoría", command=lambda: self._ordenar_por("categoria"))
        self.tree.heading("estado", text="Estado", command=lambda: self._ordenar_por("estado"))
        self.tree.heading("descripcion", text="Descripción", command=lambda: self._ordenar_por("descripcion"))

        self.tree.column("id", width=50, anchor="center")
        self.tree.column("fecha", width=110, anchor="center")
        self.tree.column("prioridad", width=80, anchor="center")
        self.tree.column("categoria", width=120, anchor="w")
        self.tree.column("estado", width=100, anchor="center")
        self.tree.column("descripcion", width=380, anchor="w")

        vsb = ttk.Scrollbar(frm_table, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(frm_table, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscroll=vsb.set, xscroll=hsb.set)
        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        frm_table.rowconfigure(0, weight=1)
        frm_table.columnconfigure(0, weight=1)

        self.tree.bind("<<TreeviewSelect>>", lambda e: self._cargar_a_formulario())

        # Barra inferior (archivo)
        frm_bottom = ttk.Frame(self, padding=(10, 0, 10, 10))
        frm_bottom.pack(fill="x")
        ttk.Button(frm_bottom, text="Abrir CSV…", command=self._menu_abrir).pack(side="left")
        ttk.Button(frm_bottom, text="Guardar CSV", command=self._menu_guardar).pack(side="left", padx=(6, 0))
        ttk.Label(frm_bottom, textvariable=tk.StringVar(value="Doble clic en encabezados para ordenar"),
                  style="Muted.TLabel").pack(side="right")

        # Permitir doble clic en encabezado también
        for c in cols:
            self.tree.heading(c, command=lambda col=c: self._ordenar_por(col))

    # --------- Acciones de UI ----------
    def _limpiar_filtros(self):
        self.var_estado_filtro.set("Todas")
        self.var_cat_filtro.set("")
        self._refrescar_tabla()

    def _ordenar_por(self, columna: str):
        # Orden local sobre lo visible en la tabla
        datos = [(self.tree.set(k, columna), k) for k in self.tree.get_children("")]
        # Tipos
        def parse_val(v):
            if columna in ("id", "prioridad"):
                try:
                    return int(v)
                except:
                    return 0
            if columna == "fecha":
                try:
                    return datetime.strptime(v, DATE_FMT).date()
                except:
                    return date.min
            return v.lower()
        datos.sort(key=lambda x: parse_val(x[0]))
        for idx, (_, k) in enumerate(datos):
            self.tree.move(k, "", idx)

    def _refrescar_tabla(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        estado = self.var_estado_filtro.get()
        categoria = self.var_cat_filtro.get().strip()
        categoria = categoria if categoria else None
        tareas = self.gestor.listar(estado=estado if estado != "Todas" else None,
                                    categoria=categoria)
        for t in tareas:
            self.tree.insert(
                "", "end", iid=str(t.id),
                values=(t.id, to_str_fecha(t.fecha_limite), t.prioridad,
                        t.categoria, ("Completada" if t.completada else "Pendiente"),
                        t.descripcion)
            )

    def _cargar_a_formulario(self):
        sel = self.tree.selection()
        if not sel:
            return
        iid = sel[0]
        vals = self.tree.item(iid, "values")
        # values: id, fecha, prioridad, categoria, estado, descripcion
        self.var_id.set(vals[0])
        self.var_fecha.set(vals[1])
        self.var_prio.set(str(vals[2]))
        self.var_cat.set(vals[3])
        self.var_desc.set(vals[5])

    def _accion_nuevo(self):
        self.var_id.set("")
        self.var_desc.set("")
        self.var_fecha.set("")
        self.var_cat.set("")
        self.var_prio.set("3")
        self.tree.selection_remove(self.tree.selection())

    def _accion_guardar_form(self):
        try:
            desc = self.var_desc.get().strip()
            fecha = self.var_fecha.get().strip()
            cat = self.var_cat.get().strip() or "General"
            prio = self.var_prio.get().strip() or "3"
            if not desc:
                messagebox.showwarning("Validación", "La descripción es obligatoria.")
                return
            if not fecha:
                messagebox.showwarning("Validación", "La fecha es obligatoria (YYYY-MM-DD).")
                return
            # Alta o edición
            if self.var_id.get():  # edición
                idt = int(self.var_id.get())
                self.gestor.editar(idt, descripcion=desc, fecha_limite=fecha, categoria=cat, prioridad=prio)
                messagebox.showinfo("Éxito", f"Tarea {idt} actualizada.")
            else:  # alta
                t = self.gestor.agregar(desc, fecha, cat, prio)
                messagebox.showinfo("Éxito", f"Tarea creada con id {t.id}.")
                self.var_id.set(str(t.id))
            self._refrescar_tabla()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _accion_marcar(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("Información", "Seleccione una tarea en la tabla.")
            return
        idt = int(sel[0])
        if self.gestor.marcar(idt):
            self._refrescar_tabla()
            self.tree.selection_set(str(idt))
        else:
            messagebox.showerror("Error", "No se encontró la tarea seleccionada.")

    def _accion_eliminar(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("Información", "Seleccione una tarea en la tabla.")
            return
        idt = int(sel[0])
        if messagebox.askyesno("Confirmar", f"¿Eliminar la tarea {idt}?"):
            if self.gestor.eliminar(idt):
                self._accion_nuevo()
                self._refrescar_tabla()

    # --------- Archivo ----------
    def _menu_abrir(self):
        ruta = filedialog.askopenfilename(
            title="Abrir CSV",
            filetypes=[("CSV", "*.csv"), ("Todos", "*.*")]
        )
        if ruta:
            self._accion_cargar(ruta)

    def _accion_cargar(self, ruta: str):
        try:
            self.gestor.cargar_csv(ruta)
            self.archivo_actual = ruta
            self._refrescar_tabla()
            messagebox.showinfo("Cargar", f"Se cargaron {len(self.gestor.tareas)} tareas de:\n{ruta}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _menu_guardar(self):
        if not self.archivo_actual:
            ruta = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV", "*.csv")],
                title="Guardar como"
            )
        else:
            ruta = self.archivo_actual
        if ruta:
            try:
                self.gestor.guardar_csv(ruta)
                self.archivo_actual = ruta
                messagebox.showinfo("Guardar", f"Tareas guardadas en:\n{ruta}")
            except Exception as e:
                messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    App().mainloop()
