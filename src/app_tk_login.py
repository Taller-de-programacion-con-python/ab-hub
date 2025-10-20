
import tkinter as tk
from auth_service import login, registrar_usuario
from task_service import listar_tareas, agregar_tarea

# Ventana principal de Login
root = tk.Tk()
root.title("Login")
root.geometry("320x200")
root.resizable(False, False)

frm = tk.Frame(root, padx=10, pady=10)
frm.pack(fill="both", expand=True)

correo_var = tk.StringVar()
pass_var = tk.StringVar()

tk.Label(frm, text="Correo:").grid(row=0, column=0, sticky="w")
tk.Entry(frm, textvariable=correo_var).grid(row=1, column=0, columnspan=2, sticky="we")

tk.Label(frm, text="Contraseña:").grid(row=2, column=0, sticky="w")
tk.Entry(frm, textvariable=pass_var, show="*").grid(row=3, column=0, columnspan=2, sticky="we")

status_lbl = tk.Label(frm, text="", fg="red")
status_lbl.grid(row=5, column=0, columnspan=2, sticky="we")

def do_login():
    email = correo_var.get().strip().lower()
    pw = pass_var.get()
    ok, msg = login(email, pw)
    if ok:
        status_lbl.config(text="", fg="green")
        root.withdraw()
        open_tasks_window(email)
    else:
        status_lbl.config(text=msg, fg="red")

tk.Button(frm, text="Iniciar Sesión", command=do_login).grid(row=4, column=0, sticky="w", pady=5)

def open_register():
    reg_win = tk.Toplevel(root)
    reg_win.title("Registro")
    tk.Label(reg_win, text="Nombre:").grid(row=0, column=0, sticky="w")
    name_var = tk.StringVar()
    tk.Entry(reg_win, textvariable=name_var).grid(row=0, column=1)
    tk.Label(reg_win, text="Correo:").grid(row=1, column=0, sticky="w")
    email_var = tk.StringVar()
    tk.Entry(reg_win, textvariable=email_var).grid(row=1, column=1)
    tk.Label(reg_win, text="Contraseña:").grid(row=2, column=0, sticky="w")
    pw_var = tk.StringVar()
    tk.Entry(reg_win, textvariable=pw_var, show="*").grid(row=2, column=1)
    status_reg = tk.Label(reg_win, text="", fg="red")
    status_reg.grid(row=3, column=0, columnspan=2)
    def submit_reg():
        ok, msg = registrar_usuario(email_var.get().strip().lower(), pw_var.get(), name_var.get().strip())
        if ok:
            status_reg.config(text="Cuenta creada correctamente.", fg="green")
            reg_win.after(2000, reg_win.destroy)
        else:
            status_reg.config(text=msg, fg="red")
    tk.Button(reg_win, text="Crear Cuenta", command=submit_reg).grid(row=4, column=0, columnspan=2, pady=5)

tk.Button(frm, text="Registrar", command=open_register).grid(row=4, column=1, sticky="e", pady=5)

def open_tasks_window(user_email):
    tasks_win = tk.Toplevel(root)
    tasks_win.title("Tareas")
    tk.Label(tasks_win, text="Tus tareas:").pack()
    tasks_list = tk.Listbox(tasks_win, width=50)
    tasks_list.pack(padx=5, pady=5)
    for task in listar_tareas(user_email):
        tasks_list.insert(tk.END, f"{task['texto']} ({task['fecha']})")
    tk.Label(tasks_win, text="Nueva Tarea:").pack(pady=(10,0))
    tk.Label(tasks_win, text="Descripción:").pack(anchor="w", padx=5)
    task_text_var = tk.StringVar()
    tk.Entry(tasks_win, textvariable=task_text_var).pack(fill="x", padx=5)
    tk.Label(tasks_win, text="Fecha (DD/MM):").pack(anchor="w", padx=5)
    task_date_var = tk.StringVar()
    tk.Entry(tasks_win, textvariable=task_date_var).pack(fill="x", padx=5, pady=(0,5))
    status_task = tk.Label(tasks_win, text="", fg="red")
    status_task.pack()
    def add_task():
        text = task_text_var.get().strip()
        date = task_date_var.get().strip()
        if agregar_tarea(user_email, text, date):
            task_text_var.set("")
            task_date_var.set("")
            tasks_list.delete(0, tk.END)
            for task in listar_tareas(user_email):
                tasks_list.insert(tk.END, f"{task['texto']} ({task['fecha']})")
            status_task.config(text="Tarea agregada", fg="green")
            status_task.after(3000, lambda: status_task.config(text=""))
        else:
            status_task.config(text="Error al agregar tarea", fg="red")
    tk.Button(tasks_win, text="Agregar Tarea", command=add_task).pack(pady=5)
    def do_logout():
        tasks_win.destroy()
        correo_var.set("")
        pass_var.set("")
        status_lbl.config(text="")
        root.deiconify()
    tk.Button(tasks_win, text="Cerrar Sesión", command=do_logout).pack(pady=(0,5))
    tasks_win.protocol("WM_DELETE_WINDOW", do_logout)

root.mainloop()
