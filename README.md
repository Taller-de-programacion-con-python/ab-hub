# AB Hub (desktop)

## Estructura mínima

- `login_screen.py` (aplicación Tkinter)
- `src/` (servicios, DB sqlite y notificador)
- Recursos PNG en la raíz (íconos usados por la UI)
- `tools/` (scripts de empaquetado y acceso directo)

## Ejecutar en otra PC (sin instalar Python)

1. En esta máquina, crear el ejecutable para Windows:
   - Abrir PowerShell en la carpeta del proyecto y ejecutar:
     ```powershell
     .\tools\build_windows.ps1
     ```
     - Genera `dist/ABHub.exe` (modo "onefile") listo para copiar en USB.
     - Si prefieres carpeta portable en lugar de un único exe:
       ```powershell
       .\tools\build_windows.ps1 -OneFolder
       ```

2. Copiar `dist/ABHub.exe` (o la carpeta `dist/ABHub/`) a un USB.

3. En la otra PC (Windows 10/11):
   - Copiar el exe o la carpeta al equipo, por ejemplo `C:\ABHub`.
   - (Opcional) Crear acceso directo en el escritorio:
     ```powershell
     .\tools\create_shortcut.ps1 -ExePath C:\ABHub\ABHub.exe -ShortcutName AB Hub
     ```
   - Doble clic en el acceso directo (o en el exe) para abrir la app.

Notas
- La base de datos sqlite se incluye dentro de `src/bloc.db`. Puedes distribuirla vacía o con datos de prueba.
- La app programa recordatorios en Windows mediante `src/notify_task.py` (usa `schtasks`). Esto requiere ejecutar como usuario con permisos suficientes.
- Si tu antivirus bloquea el exe, marca la carpeta como confiable o usa el modo `-OneFolder`.

## Ejecutar con Python (alternativa portable)
Si la otra PC tiene Python 3.11/3.12:
```powershell
python login_screen.py
```


