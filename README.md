# AB Hub (desktop)

Proyecto UI (Tkinter) con empaquetado para Windows y estructura profesional.

## Estructura

- `src/abhub/app.py` UI principal (login/registro/tareas)
- `src/abhub/services/` servicios de dominio y DB
  - `db.py` conexión SQLite (usa `src/bloc.db` por defecto)
  - `auth_service.py`, `task_service.py`, `notify_task.py`
- `src/abhub/utils/` utilidades (validaciones/fechas/mensajes)
- `src/abhub/adapters/` adaptadores (por ejemplo, mensajes)
- `assets/images/` recursos PNG de la UI
- `src/bloc.db` base de datos SQLite incluida
- `tools/` scripts de build y acceso directo
- `ABHub.spec` configuración de PyInstaller

## Requisitos

- Python 3.11 o 3.12
- Opcional: `Pillow` para mejor escalado de imágenes
  ```powershell
  python -m pip install pillow
  ```

## Ejecutar en desarrollo

Desde la raíz del repo:

```powershell
python run.py
```

Alternativas:
- Desde la carpeta `src/`: `python -m abhub`

## Empaquetar para Windows (EXE)

1) Abrir PowerShell en la raíz del proyecto y ejecutar:

```powershell
./tools/build_windows.ps1
```

- Genera `dist/ABHub.exe` (onefile). Para carpeta portable:
  ```powershell
  ./tools/build_windows.ps1 -OneFolder
  ```

2) En otra PC (Windows 10/11): copiar `dist/ABHub.exe` o la carpeta generada.

3) (Opcional) Crear acceso directo:

```powershell
./tools/create_shortcut.ps1 -ExePath C:\ABHub\ABHub.exe -ShortcutName AB Hub
```

Notas
- La base de datos SQLite por defecto está en `src/bloc.db`. Puedes reemplazarla por una copia con datos de prueba.
- El script `src/abhub/services/notify_task.py` puede usarse por tareas programadas (schtasks) para notificaciones locales.

