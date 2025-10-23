# -*- coding: utf-8 -*-
import tkinter as tk
from datetime import date, datetime
from pathlib import Path
from tkinter import font as tkfont
from tkinter import messagebox
import sys
import importlib.util

try:
    from PIL import Image, ImageTk  # type: ignore
except ImportError:  # pragma: no cover - Pillow is optional
    Image = None
    ImageTk = None


# ---------------------------------------------------------------------------
# External modules (src & src copy)
# ---------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
SRC_DIR = BASE_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

SRC_COPY_DIR = BASE_DIR / "src copy"


def load_legacy_module(alias: str, filename: str):
    path = SRC_COPY_DIR / filename
    if not path.exists():
        return None
    spec = importlib.util.spec_from_file_location(alias, path)
    if spec and spec.loader:
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        sys.modules[alias] = module
        return module
    return None


legacy_validaciones = load_legacy_module("validaciones", "01_validaciones.py")
legacy_fechas = load_legacy_module("fechas", "02_fechas.py")
legacy_mensajes = load_legacy_module("mensajes", "03_mensajes.py")


try:
    from validaciones import es_texto_vacio, es_correo_valido, es_contrasena_valida  # type: ignore
except Exception:  # pragma: no cover - fallback
    def es_texto_vacio(texto: str) -> bool:
        return not texto or str(texto).strip() == ""

    def es_correo_valido(correo: str) -> bool:
        return isinstance(correo, str) and "@" in correo and "." in correo.split("@", 1)[-1]

    def es_contrasena_valida(contrasena: str) -> bool:
        if not isinstance(contrasena, str) or len(contrasena) < 8:
            return False
        return any(c.isalpha() for c in contrasena) and any(c.isdigit() for c in contrasena)

try:
    from fechas import formatear_fecha, estado_por_dias  # type: ignore
except Exception:  # pragma: no cover
    def formatear_fecha(fecha_texto: str) -> str:
        return fecha_texto

    def estado_por_dias(fecha_texto: str) -> str:
        return ""

try:
    from mensajes import (
        mostrar_mensaje_exito,
        mostrar_mensaje_error,
        mostrar_mensaje_info,
    )  # type: ignore
except Exception:  # pragma: no cover
    def mostrar_mensaje_exito(texto: str) -> str:
        return texto

    def mostrar_mensaje_error(texto: str) -> str:
        return texto

    def mostrar_mensaje_info(texto: str) -> str:
        return texto

from auth_service import login as auth_login, registrar_usuario
from task_service import listar_tareas, agregar_tarea, actualizar_tarea
from db import get_conn

# ---------------------------------------------------------------------------
# Base palette extracted from the reference mockups
BACKGROUND_COLOR = "#E9EFEC"
SECONDARY_COLOR = "#697565"
PRIMARY_TEXT_COLOR = "#1E201E"
WHITE = "#FFFFFF"
ERROR_COLOR = "#E16F64"

# Shared design metrics (px) taken from the Figma export
DESIGN_WIDTH = 1920
DESIGN_HEIGHT = 1080
PANEL_X = 1240
FIELD_X = 152
FIELD_WIDTH = 960
FIELD_HEIGHT = 75
FIELD_RADIUS = 30

# Login screen specifics (original mockup)
LOGIN_FIRST_FIELD_Y = 463
LOGIN_SECOND_FIELD_Y = 631
LOGIN_HEADLINE_FRAME = (FIELD_X, 240, 932, 108)
LOGIN_BUTTON = (478, 799, 310, 75, 30)

# Register screen specifics (second mockup)
REGISTER_FIELD_TOPS = {
    "name": 141,
    "email": 309,
    "password": 477,
    "confirm": 645,
}
REGISTER_BUTTON = (478, 799, 310, 75, 30)
CHEVRON_IMAGE = "Vector.png"

LOGIN_CHEVRONS = [
    (1035.0, 483.5, 15.04, 35.0, 3.75),
    (1035.0, 651.0, 15.04, 35.0, 3.75),
]

REGISTER_CHEVRONS = [
    (860.96, 161.5, 15.04, 35.0, 3.75),
    (860.96, 329.0, 15.04, 35.0, 3.75),
    (860.96, 497.5, 15.04, 35.0, 3.75),
    (860.96, 665.0, 15.04, 35.0, 3.75),
]

STATUS_COLORS = {
    "VENCIDO": "#E16F64",
    "HOY": "#FDECC8",
    "PRONTO": "#EEE0DA",
    "A TIEMPO": "#DBEDDB",
}

TASK_CARD_WIDTH = 485
TASK_CARD_HEIGHT = 109
TASK_CARD_STRIPE_WIDTH = 31
TASK_CARD_RADIUS = 15
TASK_ROW_GAP = 40
SECTION_FIRST_HEADER_Y = 150
SECTION_HEADER_TO_CARDS = 105
SECTION_LINE_OFFSET = 19
SECTION_AFTER_CARDS_GAP = 140
TASK_SECTION_CONFIG = [
    {"key": "past", "label": "Anteriores"},
    {"key": "current", "label": "Actuales"},
    {"key": "future", "label": "Posteriores"},
]
TASK_CARD_X_POSITIONS = (152, 657, 1162)
TASK_STATUS_STYLES = {
    "pending": {
        "label": "Pendiente",
        "pill_bg": "#EEE0DA",
        "pill_fg": "#1E201E",
        "stripe": "#E16F64",
    },
    "done": {
        "label": "Hecho",
        "pill_bg": "#DBEDDB",
        "pill_fg": "#1E201E",
        "stripe": "#C9E7CF",
    },
}
TIMELINE_SLOTS = [
    {"title": (336, 328), "subtitle": (336, 295), "badge": (336, 372)},
    {"title": (336, 464), "subtitle": (336, 428), "badge": (336, 614)},
    {"title": (336, 762), "subtitle": (336, 728), "badge": (336, 849)},
    {"title": (669, 757), "subtitle": (669, 723), "badge": (669, 849)},
]

TIMELINE_PLACEHOLDERS = [
    {"texto": "Problemario de Matematicas", "fecha": "13/05/2025", "estado": "A TIEMPO"},
    {"texto": "Basketball", "fecha": "14/05/2025", "estado": "PRONTO"},
    {"texto": "Ingles", "fecha": "16/05/2025", "estado": "HOY"},
    {"texto": "100 oraciones", "fecha": "18/05/2025", "estado": "A TIEMPO"},
]

CARD_SLOTS = [
    {"title": (1124, 304), "subtitle": (1124, 354)},
    {"title": (1124, 451), "subtitle": (1124, 501)},
    {"title": (1124, 723), "subtitle": (1124, 804)},
    {"title": (1404, 304), "subtitle": (1404, 354)},
    {"title": (1404, 723), "subtitle": (1404, 804)},
]

CARD_PLACEHOLDERS = [
    "Materias por revisar",
    "Clases extracurriculares",
    "Recoger la ropa",
    "Actividades",
    "La revolucion mexicana...",
]


class LoginScreen(tk.Tk):
    """Main window that can toggle between login and register mockups with pixel-perfect scaling."""

    def __init__(self):
        super().__init__()
        self.title("Inicio de Sesion")
        self.configure(bg=BACKGROUND_COLOR)

        self.update_idletasks()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.scale = min(1.0, screen_width / DESIGN_WIDTH, screen_height / DESIGN_HEIGHT)
        self.scaled_width = DESIGN_WIDTH * self.scale
        self.scaled_height = DESIGN_HEIGHT * self.scale

        self.geometry(f"{int(self.scaled_width)}x{int(self.scaled_height)}")
        self.state("zoomed")
        self.update()

        self.window_width = self.winfo_width()
        self.window_height = self.winfo_height()
        self.offset_x = (self.window_width - self.scaled_width) / 2
        self.offset_y = (self.window_height - self.scaled_height) / 2

        self.canvas = tk.Canvas(
            self,
            width=self.window_width,
            height=self.window_height,
            bg=BACKGROUND_COLOR,
            highlightthickness=0,
            bd=0,
        )
        self.canvas.pack(fill="both", expand=True)
        # Scroll invisible activado por rueda del raton
        self.canvas.configure(yscrollincrement=20)
        self.canvas.bind_all("<MouseWheel>", self._on_mouse_wheel)


        self.fonts = self._prepare_fonts()
        self.overlay_widgets: list[tk.Widget] = []
        self.current_screen = "login"
        self.chevron_photo = self._load_chevron_image()
        self.image_cache: dict[tuple[str, int, int], tk.PhotoImage] = {}
        self.active_images: list[tk.PhotoImage] = []
        self.pending_email: str | None = None
        self.logged_in_user: dict[str, str] | None = None
        self.dashboard_tasks: list[dict] = []
        self.task_list_items: list[int] = []
        self.tasks_list_origin: tuple[float, float] | None = None
        self.tasks_error_item: int | None = None
        self.login_error_item: int | None = None
        self.register_error_item: int | None = None
        self.task_modal_window: tk.Toplevel | None = None
        self.task_modal_overlay: tk.Toplevel | None = None
        self.task_modal_context: dict | None = None

        self.show_login_screen()

    # ------------------------------------------------------------------
    # Shared helpers
    # ------------------------------------------------------------------
    def _prepare_fonts(self):
        """Return fonts scaled to the current factor, with Outfit fallbacks."""
        available = {name.lower(): name for name in tkfont.families()}

        preferred = ("Outfit", "Montserrat", "Arial", "Helvetica", "Calibri")
        for name in preferred:
            if name.lower() in available:
                self.primary_font_family = available[name.lower()]
                break
        else:
            self.primary_font_family = tkfont.nametofont("TkDefaultFont").actual("family")

        def create_font(size, weight="normal"):
            return tkfont.Font(
                family=self.primary_font_family,
                size=max(1, int(round(size * self.scale))),
                weight=weight,
            )

        self._font_cache = {}

        return {
            "hero": create_font(128, weight="bold"),
            "label": create_font(30),
            "label_bold": create_font(30, weight="bold"),
            "button": create_font(30),
        }

    def _font(self, size, weight="normal"):
        """Return a cached font scaled from the design size."""
        key = (size, weight)
        if key not in self._font_cache:
            self._font_cache[key] = tkfont.Font(
                family=self.primary_font_family,
                size=max(1, int(round(size * self.scale))),
                weight=weight,
            )
        return self._font_cache[key]

    def _load_chevron_image(self):
        """Load and scale the chevron icon used inside the fields."""
        path = Path(__file__).with_name(CHEVRON_IMAGE)
        if not path.exists():
            messagebox.showwarning("Recursos", f"No se encontro {CHEVRON_IMAGE}. Se dibujara el icono con lineas.")
            return None

        target_size = (
            max(1, int(round(15.04 * self.scale))),
            max(1, int(round(35 * self.scale))),
        )

        if Image and ImageTk:
            try:
                image = Image.open(path).convert("RGBA")
                image = image.resize(target_size, Image.LANCZOS)
                return ImageTk.PhotoImage(image)
            except Exception as exc:  # pragma: no cover - best effort
                messagebox.showwarning("Recursos", f"No se pudo cargar {CHEVRON_IMAGE}: {exc}")
                return None

        try:
            photo = tk.PhotoImage(file=str(path))
            if self.scale < 1.0:
                factor = max(1, round(photo.width() / target_size[0])) or 1
                photo = photo.subsample(factor, factor)
            return photo
        except tk.TclError as exc:  # pragma: no cover
            messagebox.showwarning("Recursos", f"No se pudo cargar {CHEVRON_IMAGE}: {exc}")
            return None

    def _get_image(self, filename: str, width: float, height: float):
        """Load and cache an image scaled to the current factor."""
        target_width = max(1, int(round(width * self.scale)))
        target_height = max(1, int(round(height * self.scale)))
        cache_key = (filename, target_width, target_height)
        if cache_key in self.image_cache:
            return self.image_cache[cache_key]

        path = Path(__file__).with_name(filename)
        if not path.exists():
            self.image_cache[cache_key] = None
            messagebox.showwarning("Recursos", f"No se encontro {filename}.")
            return None

        try:
            if Image and ImageTk:
                image = Image.open(path).convert("RGBA")
                image = image.resize((target_width, target_height), Image.LANCZOS)
                photo = ImageTk.PhotoImage(image)
            else:
                photo = tk.PhotoImage(file=str(path))
        except Exception as exc:  # pragma: no cover
            messagebox.showwarning("Recursos", f"No se pudo cargar {filename}: {exc}")
            self.image_cache[cache_key] = None
            return None

        self.image_cache[cache_key] = photo
        return photo

    def _place_image(self, filename: str, x: float, y: float, width: float, height: float, anchor: str = "nw"):
        photo = self._get_image(filename, width, height)
        if not photo:
            return
        item = self.canvas.create_image(self.sx(x), self.sy(y), image=photo, anchor=anchor)
        self.active_images.append(photo)
        return item

    def _clear_screen(self):
        if getattr(self, "task_modal_window", None):
            self._close_task_modal(save=False)
        self.canvas.delete("all")
        for widget in self.overlay_widgets:
            widget.destroy()
        self.overlay_widgets.clear()
        self.active_images = []
        self.task_list_items = []
        self.tasks_list_origin = None
        self.login_error_item = None
        self.register_error_item = None
        self.tasks_error_item = None

    def _draw_background(self):
        self.canvas.create_rectangle(
            0,
            0,
            self.window_width,
            self.window_height,
            fill=BACKGROUND_COLOR,
            outline="",
        )
        self._draw_panel_shadow()
        self.canvas.create_rectangle(
            self.sx(PANEL_X),
            self.sy(0),
            self.sx(DESIGN_WIDTH),
            self.sy(DESIGN_HEIGHT),
            fill=SECONDARY_COLOR,
            outline="",
        )

    def _draw_panel_shadow(self):
        shadow_width = 90
        max_alpha = 0.25
        top = self.sy(0)
        bottom = self.sy(DESIGN_HEIGHT)
        for index in range(shadow_width):
            fade = 1 - (index / shadow_width)
            blended = self._blend_colors("#000000", BACKGROUND_COLOR, max_alpha * fade)
            x0 = self.sx(PANEL_X - index - 1)
            x1 = self.sx(PANEL_X - index)
            self.canvas.create_rectangle(x0, top, x1, bottom, fill=blended, outline="")

    def _rounded_rect(self, x, y, width, height, radius, **kwargs):
        x1, y1 = x, y
        x2, y2 = x + width, y + height
        r = min(radius, width / 2, height / 2)
        points = [
            x1 + r, y1,
            x2 - r, y1,
            x2 - r, y1,
            x2, y1,
            x2, y1 + r,
            x2, y1 + r,
            x2, y2 - r,
            x2, y2 - r,
            x2, y2,
            x2 - r, y2,
            x2 - r, y2,
            x1 + r, y2,
            x1 + r, y2,
            x1, y2,
            x1, y2 - r,
            x1, y2 - r,
            x1, y1 + r,
            x1, y1 + r,
            x1, y1,
            x1 + r, y1,
        ]
        return [
            self.canvas.create_polygon(points, smooth=True, splinesteps=max(12, int(36 * self.scale)), **kwargs)
        ]

    def _draw_chevron(self, x, y, width, height, line_width):
        if self.chevron_photo:
            self.canvas.create_image(
                self.sx(x),
                self.sy(y),
                image=self.chevron_photo,
                anchor="nw",
            )
        else:
            line_size = max(1.0, line_width * self.scale)
            x0 = self.sx(x)
            y0 = self.sy(y)
            x_mid = self.sx(x + width / 2)
            y_mid = self.sy(y + height / 2)
            x1 = self.sx(x)
            y1 = self.sy(y + height)
            self.canvas.create_line(
                x0,
                y0,
                x_mid,
                y_mid,
                fill=SECONDARY_COLOR,
                width=line_size,
                capstyle=tk.ROUND,
                joinstyle=tk.ROUND,
            )
            self.canvas.create_line(
                x_mid,
                y_mid,
                x1,
                y1,
                fill=SECONDARY_COLOR,
                width=line_size,
                capstyle=tk.ROUND,
                joinstyle=tk.ROUND,
            )

    def _bind_click(self, items, callback):
        def handle_click(_event):
            callback()

        def on_enter(_event):
            self.config(cursor="hand2")

        def on_leave(_event):
            self.config(cursor="")

        for item in items:
            self.canvas.tag_bind(item, "<Button-1>", handle_click)
            self.canvas.tag_bind(item, "<Enter>", on_enter)
            self.canvas.tag_bind(item, "<Leave>", on_leave)

    # Coordinate helpers ------------------------------------------------
    def sx(self, value):
        return self.offset_x + value * self.scale

    def sy(self, value):
        return self.offset_y + value * self.scale

    def sw(self, value):
        return value * self.scale

    def sh(self, value):
        return value * self.scale

    @staticmethod
    def _blend_colors(foreground, background, alpha):
        def hex_to_rgb(value):
            value = value.lstrip("#")
            return tuple(int(value[i:i + 2], 16) for i in (0, 2, 4))

        fg_r, fg_g, fg_b = hex_to_rgb(foreground)
        bg_r, bg_g, bg_b = hex_to_rgb(background)
        r = round(fg_r * alpha + bg_r * (1 - alpha))
        g = round(fg_g * alpha + bg_g * (1 - alpha))
        b = round(fg_b * alpha + bg_b * (1 - alpha))
        return f"#{r:02x}{g:02x}{b:02x}"

    def _apply_opacity(self, hex_color: str, alpha: float) -> str:
        """Blend the given color against the background using the provided opacity."""
        alpha = max(0.0, min(1.0, alpha))
        return self._blend_colors(hex_color, BACKGROUND_COLOR, alpha)

    def _load_user_profile(self, email: str) -> dict[str, str] | None:
        correo = email.strip().lower()
        try:
            with get_conn() as con:
                row = con.execute(
                    "SELECT id, correo, nombre FROM usuarios WHERE correo=?",
                    (correo,),
                ).fetchone()
            if not row:
                return None
            name = row["nombre"] or correo.split("@", 1)[0].title()
            return {"id": row["id"], "email": row["correo"], "name": name}
        except Exception as exc:  # pragma: no cover
            print("Error cargando el perfil:", exc)
            return None

    def _prepare_dashboard_data(self):
        if not self.logged_in_user:
            self.dashboard_tasks = []
            return

        correo = self.logged_in_user["email"]
        tasks = []
        try:
            for row in listar_tareas(correo):
                record = dict(row)
                fecha = record.get("fecha", "")
                record["fecha_formateada"] = formatear_fecha(fecha) if fecha else ""
                estado = estado_por_dias(fecha) if fecha else ""
                record["estado"] = estado
                tasks.append(record)
        except Exception as exc:  # pragma: no cover
            print("Error listando tareas:", exc)
            tasks = []
        self.dashboard_tasks = tasks

    def _logout(self):
        self.logged_in_user = None
        self.dashboard_tasks = []
        self.pending_email = None
        self.show_login_screen()

    # ------------------------------------------------------------------
    # View switching
    # ------------------------------------------------------------------
    def show_login_screen(self):
        self.current_screen = "login"
        self._clear_screen()
        self._draw_background()
        self._draw_login_ui()
        self._add_login_entries()
        self._set_login_error("")

    def show_register_screen(self):
        self.current_screen = "register"
        self._clear_screen()
        self._draw_background()
        self._draw_register_ui()
        self._add_register_entries()
        self._set_register_error("")

    def show_dashboard_screen(self):
        self.current_screen = "dashboard"
        self._clear_screen()
        self.canvas.configure(bg=BACKGROUND_COLOR)
        self._prepare_dashboard_data()
        self._draw_dashboard_ui()

    # ------------------------------------------------------------------
    # Login screen
    # ------------------------------------------------------------------
    def show_tasks_screen(self):
        self.current_screen = "tasks"
        self._clear_screen()
        self.canvas.configure(bg=BACKGROUND_COLOR)
        self._prepare_dashboard_data()
        self._draw_tasks_ui()

    def _draw_tasks_ui(self):
        self.canvas.create_rectangle(
            0,
            0,
            self.window_width,
            self.window_height,
            fill=BACKGROUND_COLOR,
            outline="",
        )

        for offset in (56, 68, 80):
            self._rounded_rect(
                self.sx(54),
                self.sy(offset),
                self.sw(30),
                self.sh(8),
                self.sw(4),
                fill="#3C3D37",
                outline="",
            )

        self.canvas.create_text(
            self.sx(152),
            self.sy(18),
            text="Tareas",
            fill=PRIMARY_TEXT_COLOR,
            font=self._font(85.33),
            anchor="nw",
        )

        plus_item = self.canvas.create_text(
            self.sx(1555),
            self.sy(150),
            text="+",
            fill="#3C3D37",
            font=self._font(64),
            anchor="nw",
        )
        self._bind_click([plus_item], lambda: self._open_task_modal(None))

        sections = self._build_task_sections()

        current_header_y = SECTION_FIRST_HEADER_Y

        for config in TASK_SECTION_CONFIG:
            self.canvas.create_text(
                self.sx(152),
                self.sy(current_header_y),
                text=config["label"],
                fill=PRIMARY_TEXT_COLOR,
                font=self._font(64),
                anchor="nw",
            )
            line_y = current_header_y + SECTION_LINE_OFFSET
            self.canvas.create_line(
                self.sx(560),
                self.sy(line_y),
                self.sx(560 + 1031),
                self.sy(line_y),
                fill="#3C3D37",
                width=max(1.0, self.scale),
            )

            tasks = sections.get(config["key"], [])
            cards_y = current_header_y + SECTION_HEADER_TO_CARDS
            if not tasks:
                self.canvas.create_text(
                    self.sx(152),
                    self.sy(cards_y),
                    text="Sin tareas registradas en esta seccion.",
                    fill="#3C3D37",
                    font=self._font(24),
                    anchor="nw",
                )
                rows_drawn = 1
            else:
                for index, task in enumerate(tasks):
                    col = index % len(TASK_CARD_X_POSITIONS)
                    row = index // len(TASK_CARD_X_POSITIONS)
                    card_x = TASK_CARD_X_POSITIONS[col]
                    card_y = cards_y + row * (TASK_CARD_HEIGHT + TASK_ROW_GAP)
                    task_payload = dict(task)
                    card_items = self._draw_task_card(card_x, card_y, task_payload)
                    self._bind_click(card_items, lambda data=task_payload: self._open_task_modal(dict(data)))
                rows_drawn = (len(tasks) + len(TASK_CARD_X_POSITIONS) - 1) // len(TASK_CARD_X_POSITIONS)

            total_cards_height = rows_drawn * TASK_CARD_HEIGHT + max(0, rows_drawn - 1) * TASK_ROW_GAP
            current_header_y = cards_y + total_cards_height + SECTION_AFTER_CARDS_GAP

        nav_top = max(903, current_header_y)
        self._draw_bottom_navigation(nav_top)
        try:
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        except Exception:
            pass

    def _draw_bottom_navigation(self, base_y: float):


        nav_specs = [
            {'label': 'Inicio', 'active': False},
            {'label': 'Calendario', 'active': False},
            {'label': 'Albumes', 'active': False},
            {'label': 'Notas', 'active': False},
            {'label': 'Tareas', 'active': True},
        ]
        nav_positions = (326, 621, 880, 1154, 1428)
        block_width = 187
        block_height = 177
        indicator_width = 124
        indicator_height = 6

        for spec, pos_x in zip(nav_specs, nav_positions):
            background_color = self._apply_opacity(
                WHITE if spec["active"] else BACKGROUND_COLOR,
                0.65 if spec["active"] else 0.5,
            )
            self._rounded_rect(
                self.sx(pos_x),
                self.sy(base_y),
                self.sw(block_width),
                self.sh(block_height),
                self.sw(30),
                fill=background_color,
                outline="",
            )
            text_color = PRIMARY_TEXT_COLOR if spec["active"] else "#3C3D37"
            self.canvas.create_text(
                self.sx(pos_x + block_width / 2),
                self.sy(base_y + 37),
                text=spec["label"],
                fill=text_color,
                font=self._font(30),
                anchor="n",
            )
            indicator_color = self._apply_opacity(SECONDARY_COLOR, 1.0 if spec["active"] else 0.4)
            self._rounded_rect(
                self.sx(pos_x + (block_width - indicator_width) / 2),
                self.sy(base_y + 82),
                self.sw(indicator_width),
                self.sh(indicator_height),
                self.sw(indicator_height / 2),
                fill=indicator_color,
                outline="",
            )

    def _on_mouse_wheel(self, event):
        try:
            units = -1 * int(getattr(event, 'delta', 120) / 120)
        except Exception:
            units = -1
        try:
            self.canvas.yview_scroll(units, 'units')
        except Exception:
            pass


    def _build_task_sections(self) -> dict[str, list[dict]]:
        sections: dict[str, list[dict]] = {config["key"]: [] for config in TASK_SECTION_CONFIG}
        today = date.today()

        for record in self.dashboard_tasks:
            due_date = self._parse_due_date(record.get("fecha"))
            status = "done" if bool(record.get("done")) else "pending"
            entry = {
                "id": record.get("id"),
                "title": str(record.get("texto", "")).strip() or "Sin titulo",
                "date": record.get("fecha") or "",
                "status": status,
                "placeholder": False,
                "raw": record,
                "due": due_date,
            }
            if due_date is None:
                bucket = "future"
            elif due_date < today:
                bucket = "past"
            elif due_date == today:
                bucket = "current"
            else:
                bucket = "future"
            sections[bucket].append(entry)

        for key, items in sections.items():
            if key == "past":
                items.sort(key=lambda item: item["due"] or date.min, reverse=True)
            else:
                items.sort(key=lambda item: (item["due"] or date.max, item["title"]))
        return sections

    def _parse_due_date(self, value: str | None) -> date | None:
        if not value:
            return None
        text = str(value).strip()
        if not text:
            return None
        candidates = [text]
        if len(text) == 5 and "/" in text:
            candidates.append(f"{text}/{date.today().year}")
        for candidate in candidates:
            for fmt in ("%d/%m/%Y", "%Y-%m-%d", "%d-%m-%Y", "%d/%m/%y"):
                try:
                    return datetime.strptime(candidate, fmt).date()
                except ValueError:
                    continue
        return None

    def _draw_task_card(self, x: float, y: float, task: dict) -> list[int]:
        is_placeholder = task.get("placeholder", False)
        status_key = task.get("status", "pending")
        status_style = TASK_STATUS_STYLES.get(status_key, TASK_STATUS_STYLES["pending"])
        card_opacity = 0.85 if not is_placeholder else 0.6

        items = self._rounded_rect(
            self.sx(x),
            self.sy(y),
            self.sw(TASK_CARD_WIDTH),
            self.sh(TASK_CARD_HEIGHT),
            self.sw(TASK_CARD_RADIUS),
            fill=self._apply_opacity(WHITE, card_opacity),
            outline="",
        )

        stripe = self.canvas.create_rectangle(
            self.sx(x),
            self.sy(y),
            self.sx(x + TASK_CARD_STRIPE_WIDTH),
            self.sy(y + TASK_CARD_HEIGHT),
            fill=status_style["stripe"],
            outline="",
        )
        items.append(stripe)

        date_text = self.canvas.create_text(
            self.sx(x + 62),
            self.sy(y + 16),
            text=task.get("date", ""),
            fill=PRIMARY_TEXT_COLOR,
            font=self._font(15),
            anchor="nw",
        )
        title_text = self.canvas.create_text(
            self.sx(x + 62),
            self.sy(y + 54),
            text=task.get("title", ""),
            fill=PRIMARY_TEXT_COLOR,
            font=self._font(30),
            anchor="nw",
            width=self.sw(TASK_CARD_WIDTH - 160),
        )
        items.extend([date_text, title_text])

        pill_width = 92
        pill_height = 20
        pill_x = x + TASK_CARD_WIDTH - 130
        pill_items = self._rounded_rect(
            self.sx(pill_x),
            self.sy(y + 10),
            self.sw(pill_width),
            self.sh(pill_height),
            self.sw(pill_height / 2),
            fill=status_style["pill_bg"],
            outline="",
        )
        pill_text = self.canvas.create_text(
            self.sx(pill_x + pill_width / 2),
            self.sy(y + 10 + pill_height / 2),
            text=status_style["label"],
            fill=status_style["pill_fg"],
            font=self._font(12),
            anchor="center",
        )
        items.extend(pill_items + [pill_text])
        return items

    def _open_task_modal(self, task: dict | None):
        if not self.logged_in_user:
            messagebox.showinfo("Tareas", "Inicia sesion para gestionar tus tareas.")
            return
        if self.task_modal_window:
            return

        context: dict = {
            "mode": "edit" if task and task.get("id") else "create",
            "task": task or {},
        }
        context["title_var"] = tk.StringVar(value=task.get("title", "") if task else "")
        context["date_var"] = tk.StringVar(value=task.get("date", "") if task else "")
        context["status_var"] = tk.StringVar(value=task.get("status", "pending") if task else "pending")

        overlay = tk.Toplevel(self)
        overlay.transient(self)
        overlay.overrideredirect(True)
        overlay.geometry(f"{self.window_width}x{self.window_height}+{self.winfo_rootx()}+{self.winfo_rooty()}")
        overlay.configure(bg=PRIMARY_TEXT_COLOR)
        overlay.attributes("-alpha", 0.4)
        overlay.bind("<Button-1>", lambda _event: self._close_task_modal(save=False))
        overlay.lift()
        self.task_modal_overlay = overlay

        modal = tk.Toplevel(self)
        modal.transient(self)
        modal.configure(bg=BACKGROUND_COLOR)
        modal.resizable(False, False)
        modal.grab_set()
        width = int(round(self.sw(664)))
        height = int(round(self.sh(297)))
        x_pos = self.winfo_rootx() + int((self.window_width - width) / 2)
        y_pos = self.winfo_rooty() + int((self.window_height - height) / 2)
        modal.geometry(f"{width}x{height}+{x_pos}+{y_pos}")
        modal.protocol("WM_DELETE_WINDOW", lambda: self._close_task_modal(save=True))
        modal.bind("<Escape>", lambda _event: self._close_task_modal(save=False))
        modal.bind("<Return>", lambda _event: self._close_task_modal(save=True))
        self.task_modal_window = modal
        self.task_modal_context = context

        # Campo de titulo (con placeholder "Tarea" y subrayado estilo maqueta)
        title_entry = tk.Entry(
            modal,
            textvariable=context["title_var"],
            font=self._font(48),
            bg=BACKGROUND_COLOR,
            fg=PRIMARY_TEXT_COLOR,
            bd=0,
            highlightthickness=0,
            insertbackground=PRIMARY_TEXT_COLOR,
        )
        title_entry.place(
            x=self.sw(35),
            y=self.sh(70),
            width=self.sw(664 - 70 - 60),
        )
        underline = tk.Frame(
            modal,
            bg="#3C3D37",
            height=max(1, int(round(self.sh(2)))),
            width=int(round(self.sw(664 - 70))),
        )
        underline.place(x=self.sw(35), y=self.sh(120))

        # Reposiciona la linea para que quede siempre debajo del texto del titulo
        def _reposition_title_underline():
            try:
                modal.update_idletasks()
                uy = title_entry.winfo_y() + title_entry.winfo_height()
                underline.place_configure(x=self.sw(35), y=uy + int(round(self.sh(6))), width=int(round(self.sw(664 - 70))))
            except Exception:
                pass
        _reposition_title_underline()
        title_entry.bind('<KeyRelease>', lambda _e: _reposition_title_underline())
        title_entry.bind('<Configure>', lambda _e: _reposition_title_underline())

        # Logica de placeholder para el titulo
        context["title_placeholder"] = "Tarea"
        def _title_focus_in(_e):
            if context["title_var"].get() == context["title_placeholder"]:
                context["title_var"].set("")
                title_entry.configure(fg=PRIMARY_TEXT_COLOR)
        def _title_focus_out(_e):
            if not context["title_var"].get().strip():
                context["title_var"].set(context["title_placeholder"])
                title_entry.configure(fg="#7A7C77")
        title_entry.bind("<FocusIn>", _title_focus_in)
        title_entry.bind("<FocusOut>", _title_focus_out)
        if not context["title_var"].get().strip():
            context["title_var"].set(context["title_placeholder"])
            title_entry.configure(fg="#7A7C77")

        # Campo de fecha debajo del titulo
        date_entry = tk.Entry(
            modal,
            textvariable=context["date_var"],
            font=self._font(30),
            bg=BACKGROUND_COLOR,
            fg=PRIMARY_TEXT_COLOR,
            bd=0,
            highlightthickness=0,
            insertbackground=PRIMARY_TEXT_COLOR,
        )
        date_entry.place(
            x=self.sw(35),
            y=self.sh(155),
            width=self.sw(664 - 70),
        )

        # Placeholder para fecha
        context["date_placeholder"] = "dd/mm/aaaa"
        def _date_focus_in(_e):
            if context["date_var"].get() == context["date_placeholder"]:
                context["date_var"].set("")
                date_entry.configure(fg=PRIMARY_TEXT_COLOR)
        def _date_focus_out(_e):
            if not context["date_var"].get().strip():
                context["date_var"].set(context["date_placeholder"])
                date_entry.configure(fg="#7A7C77")
        date_entry.bind("<FocusIn>", _date_focus_in)
        date_entry.bind("<FocusOut>", _date_focus_out)
        if not context["date_var"].get().strip():
            context["date_var"].set(context["date_placeholder"])
            date_entry.configure(fg="#7A7C77")

        status_frame = tk.Frame(modal, bg=BACKGROUND_COLOR)
        status_frame.place(x=self.sw(35), y=self.sh(220))

        pending_button = tk.Button(
            status_frame,
            text="Pendiente",
            command=lambda: self._set_modal_status("pending"),
            font=self._font(16),
            bg=self._apply_opacity(WHITE, 0.6),
            fg=PRIMARY_TEXT_COLOR,
            bd=0,
            highlightthickness=0,
            padx=int(round(self.sw(24))),
            pady=int(round(self.sh(6))),
            activebackground=self._apply_opacity(WHITE, 0.7),
            activeforeground=PRIMARY_TEXT_COLOR,
        )
        pending_button.pack(side="left", padx=(0, int(round(self.sw(24)))))

        done_button = tk.Button(
            status_frame,
            text="Hecho",
            command=lambda: self._set_modal_status("done"),
            font=self._font(16),
            bg=self._apply_opacity(WHITE, 0.6),
            fg=PRIMARY_TEXT_COLOR,
            bd=0,
            highlightthickness=0,
            padx=int(round(self.sw(24))),
            pady=int(round(self.sh(6))),
            activebackground=self._apply_opacity(WHITE, 0.7),
            activeforeground=PRIMARY_TEXT_COLOR,
        )
        done_button.pack(side="left")

        context["pending_button"] = pending_button
        context["done_button"] = done_button
        self._set_modal_status(context["status_var"].get())

        close_button = tk.Button(
            modal,
            text="\u2713",
            command=lambda: self._close_task_modal(save=True),
            font=self._font(48),
            bg=BACKGROUND_COLOR,
            fg=PRIMARY_TEXT_COLOR,
            bd=0,
            highlightthickness=0,
            activebackground=BACKGROUND_COLOR,
            activeforeground=PRIMARY_TEXT_COLOR,
        )
        close_button.place(x=self.sw(664 - 90), y=self.sh(30))

        title_entry.focus_set()

    def _set_modal_status(self, status: str):
        if not self.task_modal_context:
            return
        normalized = status if status in TASK_STATUS_STYLES else "pending"
        self.task_modal_context["status_var"].set(normalized)
        pending_button: tk.Button = self.task_modal_context.get("pending_button")
        done_button: tk.Button = self.task_modal_context.get("done_button")

        if pending_button and done_button:
            if normalized == "done":
                done_style = TASK_STATUS_STYLES["done"]
                done_button.configure(bg=done_style["pill_bg"], fg=done_style["pill_fg"])
                pending_button.configure(bg=self._apply_opacity(WHITE, 0.6), fg=PRIMARY_TEXT_COLOR)
            else:
                pending_style = TASK_STATUS_STYLES["pending"]
                pending_button.configure(bg=pending_style["pill_bg"], fg=pending_style["pill_fg"])
                done_button.configure(bg=self._apply_opacity(WHITE, 0.6), fg=PRIMARY_TEXT_COLOR)

    def _close_task_modal(self, save: bool):
        if save and self.task_modal_context:
            if not self._persist_task_modal():
                return
        if self.task_modal_window:
            try:
                self.task_modal_window.grab_release()
            except tk.TclError:
                pass
            self.task_modal_window.destroy()
        if self.task_modal_overlay:
            self.task_modal_overlay.destroy()
        self.task_modal_window = None
        self.task_modal_overlay = None
        self.task_modal_context = None
        self._refresh_task_board()

    def _persist_task_modal(self) -> bool:
        context = self.task_modal_context
        if not context or not self.logged_in_user:
            return True

        title = context["title_var"].get().strip()
        date_text = context["date_var"].get().strip()
        # Normaliza placeholders a vacio
        if title == context.get("title_placeholder"):
            title = ""
        if date_text == context.get("date_placeholder"):
            date_text = ""
        status = context["status_var"].get()
        is_done = status == "done"

        if not title:
            messagebox.showerror("Tareas", "Ingresa el titulo de la tarea.")
            return False
        if date_text and not self._parse_due_date(date_text):
            messagebox.showerror("Tareas", "Ingresa la fecha en formato DD/MM/AAAA.")
            return False
        if context["mode"] == "edit" and context["task"].get("id"):
            ok = actualizar_tarea(
                self.logged_in_user["email"],
                context["task"]["id"],
                title,
                date_text,
                is_done,
            )
            if not ok:
                messagebox.showerror("Tareas", "No se pudo actualizar la tarea.")
                return False
        else:
            if not date_text:
                messagebox.showerror("Tareas", "Ingresa la fecha en formato DD/MM/AAAA.")
                return False
            ok = agregar_tarea(
                self.logged_in_user["email"],
                title,
                date_text,
                is_done,
            )
            if not ok:
                messagebox.showerror("Tareas", "No se pudo crear la tarea.")
                return False
        return True

    def _refresh_task_board(self):
        if self.current_screen == "tasks":
            self.show_tasks_screen()

    def _draw_login_ui(self):
        headline_x, headline_y, headline_w, headline_h = LOGIN_HEADLINE_FRAME
        self.canvas.create_text(
            self.sx(headline_x + headline_w / 2),
            self.sy(headline_y + headline_h / 2),
            text="BIENVENIDO",
            font=self.fonts["hero"],
            fill=PRIMARY_TEXT_COLOR,
            anchor="center",
        )

        self.canvas.create_text(
            self.sx(FIELD_X),
            self.sy(LOGIN_FIRST_FIELD_Y - 45),
            text="Correo electronico",
            font=self.fonts["label"],
            fill=PRIMARY_TEXT_COLOR,
            anchor="nw",
        )
        self.canvas.create_text(
            self.sx(FIELD_X),
            self.sy(LOGIN_SECOND_FIELD_Y - 45),
            text="Contraseña",
            font=self.fonts["label"],
            fill=PRIMARY_TEXT_COLOR,
            anchor="nw",
        )

        self._rounded_rect(
            self.sx(FIELD_X),
            self.sy(LOGIN_FIRST_FIELD_Y),
            self.sw(FIELD_WIDTH),
            self.sh(FIELD_HEIGHT),
            self.sw(FIELD_RADIUS),
            fill=WHITE,
        )
        self._rounded_rect(
            self.sx(FIELD_X),
            self.sy(LOGIN_SECOND_FIELD_Y),
            self.sw(FIELD_WIDTH),
            self.sh(FIELD_HEIGHT),
            self.sw(FIELD_RADIUS),
            fill=WHITE,
        )

        for params in LOGIN_CHEVRONS:
            self._draw_chevron(*params)

        btn_x, btn_y, btn_w, btn_h, btn_radius = LOGIN_BUTTON
        button_shapes = self._rounded_rect(
            self.sx(btn_x),
            self.sy(btn_y),
            self.sw(btn_w),
            self.sh(btn_h),
            self.sw(btn_radius),
            fill=SECONDARY_COLOR,
        )
        button_text = self.canvas.create_text(
            self.sx(btn_x + btn_w / 2),
            self.sy(btn_y + btn_h / 2),
            text="Iniciar sesión",
            font=self.fonts["button"],
            fill=WHITE,
            anchor="center",
        )
        self._bind_click(button_shapes + [button_text], self._on_login_click)

        question = self.canvas.create_text(
            self.sx(btn_x + btn_w / 2),
            self.sy(910),
            text="¿Aún no tienes una cuenta?",
            font=self.fonts["label"],
            fill=PRIMARY_TEXT_COLOR,
            anchor="n",
        )
        create_new = self.canvas.create_text(
            self.sx(btn_x + btn_w / 2),
            self.sy(950),
            text="Crea una Nueva",
            font=self.fonts["label_bold"],
            fill=PRIMARY_TEXT_COLOR,
            anchor="n",
        )
        self._bind_click([question, create_new], self.show_register_screen)

        self.login_error_item = self.canvas.create_text(
            self.sx(FIELD_X),
            self.sy(LOGIN_SECOND_FIELD_Y + FIELD_HEIGHT + 15),
            text="",
            fill=ERROR_COLOR,
            font=self._font(18),
            anchor="nw",
        )

    def _add_login_entries(self):
        entry_x_design = FIELD_X + 55
        min_chevron_x = min(x for x, *_ in LOGIN_CHEVRONS)
        entry_width_design = max(100, min_chevron_x - entry_x_design - 24)

        entry_width = self.sw(entry_width_design)
        entry_x = self.sx(entry_x_design)

        self.email_var = tk.StringVar()
        self.password_var = tk.StringVar()

        entry_kwargs = dict(
            bd=0,
            relief="flat",
            bg=WHITE,
            fg=PRIMARY_TEXT_COLOR,
            font=self.fonts["label"],
            insertbackground=PRIMARY_TEXT_COLOR,
            highlightthickness=0,
        )

        email_entry = tk.Entry(self, textvariable=self.email_var, **entry_kwargs)
        password_entry = tk.Entry(self, textvariable=self.password_var, show="*", **entry_kwargs)

        self.canvas.create_window(
            entry_x,
            self.sy(LOGIN_FIRST_FIELD_Y + FIELD_HEIGHT / 2),
            anchor="w",
            window=email_entry,
            width=entry_width,
        )
        self.canvas.create_window(
            entry_x,
            self.sy(LOGIN_SECOND_FIELD_Y + FIELD_HEIGHT / 2),
            anchor="w",
            window=password_entry,
            width=entry_width,
        )

        self.overlay_widgets.extend([email_entry, password_entry])

        if self.pending_email:
            self.email_var.set(self.pending_email)
            email_entry.icursor(tk.END)

    # ------------------------------------------------------------------
    # Register screen
    # ------------------------------------------------------------------
    def _draw_register_ui(self):
        labels = [
            ("Nombre", REGISTER_FIELD_TOPS["name"] - 45),
            ("Correo electronico", REGISTER_FIELD_TOPS["email"] - 45),
            ("Contraseña", REGISTER_FIELD_TOPS["password"] - 45),
            ("Vuelve a escribir la contraseña", REGISTER_FIELD_TOPS["confirm"] - 45),
        ]
        for text, y in labels:
            self.canvas.create_text(
                self.sx(FIELD_X),
                self.sy(y),
                text=text,
                font=self.fonts["label"],
                fill=PRIMARY_TEXT_COLOR,
                anchor="nw",
            )

        for y in REGISTER_FIELD_TOPS.values():
            self._rounded_rect(
                self.sx(FIELD_X),
                self.sy(y),
                self.sw(FIELD_WIDTH),
                self.sh(FIELD_HEIGHT),
                self.sw(FIELD_RADIUS),
                fill=WHITE,
            )

        for params in REGISTER_CHEVRONS:
            self._draw_chevron(*params)

        btn_x, btn_y, btn_w, btn_h, btn_radius = REGISTER_BUTTON
        button_shapes = self._rounded_rect(
            self.sx(btn_x),
            self.sy(btn_y),
            self.sw(btn_w),
            self.sh(btn_h),
            self.sw(btn_radius),
            fill=SECONDARY_COLOR,
        )
        button_text = self.canvas.create_text(
            self.sx(btn_x + btn_w / 2),
            self.sy(btn_y + btn_h / 2),
            text="Iniciar sesion",
            font=self.fonts["button"],
            fill=WHITE,
            anchor="center",
        )
        self._bind_click(button_shapes + [button_text], self._on_register_submit)

        question = self.canvas.create_text(
            self.sx(REGISTER_BUTTON[0] + REGISTER_BUTTON[2] / 2),
            self.sy(910),
            text="?Aun no tienes una cuenta?",
            font=self.fonts["label"],
            fill=PRIMARY_TEXT_COLOR,
            anchor="n",
        )
        create_new = self.canvas.create_text(
            self.sx(REGISTER_BUTTON[0] + REGISTER_BUTTON[2] / 2),
            self.sy(950),
            text="Crea una Nueva",
            font=self.fonts["label_bold"],
            fill=PRIMARY_TEXT_COLOR,
            anchor="n",
        )
        self._bind_click([question, create_new], self.show_login_screen)

        self.register_error_item = self.canvas.create_text(
            self.sx(FIELD_X),
            self.sy(REGISTER_FIELD_TOPS["confirm"] + FIELD_HEIGHT + 15),
            text="",
            fill=ERROR_COLOR,
            font=self._font(18),
            anchor="nw",
        )

    def _add_register_entries(self):
        entry_x_design = FIELD_X + 55
        min_chevron_x = min(x for x, *_ in REGISTER_CHEVRONS)
        entry_width_design = max(100, min_chevron_x - entry_x_design - 24)

        entry_width = self.sw(entry_width_design)
        entry_x = self.sx(entry_x_design)

        self.name_var = tk.StringVar()
        self.reg_email_var = tk.StringVar()
        self.reg_password_var = tk.StringVar()
        self.reg_confirm_var = tk.StringVar()

        entry_kwargs = dict(
            bd=0,
            relief="flat",
            bg=WHITE,
            fg=PRIMARY_TEXT_COLOR,
            font=self.fonts["label"],
            insertbackground=PRIMARY_TEXT_COLOR,
            highlightthickness=0,
        )

        name_entry = tk.Entry(self, textvariable=self.name_var, **entry_kwargs)
        email_entry = tk.Entry(self, textvariable=self.reg_email_var, **entry_kwargs)
        password_entry = tk.Entry(self, textvariable=self.reg_password_var, show="*", **entry_kwargs)
        confirm_entry = tk.Entry(self, textvariable=self.reg_confirm_var, show="*", **entry_kwargs)

        for entry, key in zip(
            (name_entry, email_entry, password_entry, confirm_entry),
            REGISTER_FIELD_TOPS.values(),
        ):
            self.canvas.create_window(
                entry_x,
                self.sy(key + FIELD_HEIGHT / 2),
                anchor="w",
            window=entry,
            width=entry_width,
        )

        self.overlay_widgets.extend([name_entry, email_entry, password_entry, confirm_entry])

    def _draw_dashboard_ui(self):
        self.canvas.create_rectangle(0, 0, self.window_width, self.window_height, fill=BACKGROUND_COLOR, outline="")

        rectangles = [
            {"x": 1448, "y": 785, "w": 128, "h": 66.5, "color": "#F4F7F6", "alpha": 0.10, "radius": 15},
            {"x": 1416, "y": 742, "w": 192, "h": 99.75, "color": "#F4F7F6", "radius": 15},
            {"x": 326, "y": 903, "w": 187, "h": 177, "color": "#FFFFFF", "alpha": 0.15, "radius": 30},
            {"x": 607, "y": 903, "w": 179, "h": 177, "color": "#E9EFEC", "alpha": 0.50, "radius": 30},
            {"x": 880, "y": 903, "w": 180, "h": 177, "color": "#E9EFEC", "alpha": 0.50, "radius": 30},
            {"x": 1154, "y": 903, "w": 180, "h": 178, "color": "#E9EFEC", "alpha": 0.50, "radius": 30},
            {"x": 1428, "y": 900, "w": 180, "h": 178, "color": "#E9EFEC", "alpha": 0.50, "radius": 30},
            {"x": 288, "y": 279, "w": 664, "h": 133, "color": "#FFFFFF", "alpha": 0.50, "radius": 15},
            {"x": 288, "y": 279, "w": 24, "h": 133, "color": "#E16F64", "radius": 15},
            {"x": 288, "y": 420, "w": 664, "h": 234, "color": "#FFFFFF", "alpha": 0.50, "radius": 15},
            {"x": 288, "y": 420, "w": 24, "h": 234, "color": "#DBEDDB", "radius": 15},
            {"x": 288, "y": 713, "w": 309, "h": 176, "color": "#FFFFFF", "alpha": 0.50, "radius": 15},
            {"x": 288, "y": 713, "w": 24, "h": 176, "color": "#FDECC8", "radius": 15},
            {"x": 621, "y": 713, "w": 331, "h": 176, "color": "#FFFFFF", "alpha": 0.50, "radius": 15},
            {"x": 621, "y": 713, "w": 24, "h": 176, "color": "#E16F64", "radius": 15},
            {"x": 1104, "y": 279, "w": 256, "h": 133, "color": "#E16F64", "radius": 15},
            {"x": 1104, "y": 436, "w": 256, "h": 133, "color": "#FDECC8", "radius": 15},
            {"x": 1104, "y": 698, "w": 256, "h": 133, "color": "#F4F7F6", "radius": 15},
            {"x": 1384, "y": 279, "w": 256, "h": 133, "color": "#DBEDDB", "radius": 15},
            {"x": 1384, "y": 698, "w": 256, "h": 133, "color": "#F4F7F6", "radius": 15},
        ]

        for rect in rectangles:
            color = rect["color"]
            if "alpha" in rect:
                color = self._apply_opacity(color, rect["alpha"])
            radius = rect.get("radius", 0)
            if radius:
                self._rounded_rect(
                    self.sx(rect["x"]),
                    self.sy(rect["y"]),
                    self.sw(rect["w"]),
                    self.sh(rect["h"]),
                    self.sw(radius),
                    fill=color,
                    outline="",
                )
            else:
                self.canvas.create_rectangle(
                    self.sx(rect["x"]),
                    self.sy(rect["y"]),
                    self.sx(rect["x"] + rect["w"]),
                    self.sy(rect["y"] + rect["h"]),
                    fill=color,
                    outline="",
                )

        nav_lines = [
            {"x": 357, "y": 985, "w": 124.67, "h": 5.4},
            {"x": 637, "y": 986, "w": 119.33, "h": 5.4},
            {"x": 910, "y": 980, "w": 120, "h": 5},
            {"x": 1184, "y": 984.9, "w": 120, "h": 5.43},
            {"x": 1458, "y": 980.82, "w": 120, "h": 5.43},
        ]
        for line in nav_lines:
            item = self._place_image("Linea divisora.png", line["x"], line["y"], line["w"], line["h"])
            if not item:
                self._rounded_rect(
                    self.sx(line["x"]),
                    self.sy(line["y"]),
                    self.sw(line["w"]),
                    self.sh(line["h"]),
                    self.sw(min(line["h"] / 2, 15)),
                    fill=SECONDARY_COLOR,
                    outline="",
                )

        self._place_image("Bienvenido.png", 180, 32, 840, 94)

        static_texts = [
            {"text": "Vista rapida", "x": 153, "y": 18, "size": 85.33, "color": "#000000"},
            {"text": "Calendario", "x": 152, "y": 150, "size": 64, "color": "#000000"},
            {"text": "Albumes", "x": 1102, "y": 150, "size": 64, "color": "#000000"},
            {"text": "Notas", "x": 1102, "y": 593, "size": 64, "color": "#000000"},
            {"text": "13:00", "x": 152, "y": 279, "size": 20, "color": "#3C3D37"},
            {"text": "14:00", "x": 152, "y": 413, "size": 20, "color": "#3C3D37"},
            {"text": "15:00", "x": 152, "y": 546, "size": 20, "color": "#1E201E"},
            {"text": "16:00", "x": 152, "y": 660, "size": 20, "color": "#3C3D37"},
            {"text": "17:00", "x": 152, "y": 754, "size": 20, "color": "#3C3D37"},
            {"text": "18:00", "x": 152, "y": 868, "size": 20, "color": "#3C3D37"},
            {"text": "Inicio", "x": 385, "y": 940, "size": 30, "color": "#1E201E"},
            {"text": "Calendario", "x": 621, "y": 940, "size": 30, "color": "#3C3D37"},
            {"text": "Albumes", "x": 913, "y": 935, "size": 30, "color": "#3C3D37"},
            {"text": "Notas", "x": 1204, "y": 940, "size": 30, "color": "#3C3D37"},
            {"text": "Tareas", "x": 1473, "y": 936, "size": 30, "color": "#3C3D37"},
        ]

        for item in static_texts:
            weight = "bold" if item.get("bold") else "normal"
            self.canvas.create_text(
                self.sx(item["x"]),
                self.sy(item["y"]),
                text=item["text"],
                fill=item["color"],
                font=self._font(item["size"], weight=weight),
                anchor=item.get("anchor", "nw"),
                justify=item.get("justify", "left"),
            )

        if self.logged_in_user:
            welcome_text = f"Hola, {self.logged_in_user['name']}!"
            self.canvas.create_text(
                self.sx(1500),
                self.sy(40),
                text=welcome_text,
                fill=PRIMARY_TEXT_COLOR,
                font=self._font(32, weight="bold"),
                anchor="ne",
            )

        logout_button = tk.Button(self, text="Cerrar Sesion", command=self._logout)
        logout_button.configure(font=self._font(16))
        self.canvas.create_window(self.sx(1500), self.sy(80), anchor="ne", window=logout_button)
        self.overlay_widgets.append(logout_button)

        timeline_tasks = list(self.dashboard_tasks[: len(TIMELINE_SLOTS)])
        placeholders = TIMELINE_PLACEHOLDERS.copy()
        while len(timeline_tasks) < len(TIMELINE_SLOTS) and placeholders:
            timeline_tasks.append(placeholders[len(timeline_tasks)])

        badge_width = 160
        badge_height = 24
        for slot, task in zip(TIMELINE_SLOTS, timeline_tasks):
            title = str(task.get("texto", "")).strip() or "Actividad"
            fecha = task.get("fecha_formateada") or task.get("fecha") or ""
            estado = str(task.get("estado", "")).upper()
            if fecha:
                fecha_fmt = formatear_fecha(fecha)
            else:
                fecha_fmt = ""
            subtitle = fecha_fmt
            if estado:
                subtitle = f"{fecha_fmt} A {estado}" if fecha_fmt else estado

            self.canvas.create_text(
                self.sx(slot["title"][0]),
                self.sy(slot["title"][1]),
                text=title,
                fill="#000000",
                font=self._font(30),
                anchor="nw",
            )
            if subtitle:
                self.canvas.create_text(
                    self.sx(slot["subtitle"][0]),
                    self.sy(slot["subtitle"][1]),
                    text=subtitle,
                    fill="#000000",
                    font=self._font(15),
                    anchor="nw",
                )

            badge_color = STATUS_COLORS.get(estado, "#D3E5EF")
            badge_x, badge_y = slot["badge"]
            self._rounded_rect(
                self.sx(badge_x),
                self.sy(badge_y),
                self.sw(badge_width),
                self.sh(badge_height),
                self.sw(15),
                fill=badge_color,
                outline="",
            )
            self.canvas.create_text(
                self.sx(badge_x + badge_width / 2),
                self.sy(badge_y + badge_height / 2),
                text=estado or "EN CURSO",
                fill="#000000",
                font=self._font(10),
                anchor="center",
            )

        card_tasks = self.dashboard_tasks[len(TIMELINE_SLOTS): len(TIMELINE_SLOTS) + len(CARD_SLOTS)]
        if len(card_tasks) < len(CARD_SLOTS):
            for idx in range(len(card_tasks), len(CARD_SLOTS)):
                placeholder_text = CARD_PLACEHOLDERS[idx % len(CARD_PLACEHOLDERS)]
                card_tasks.append({"texto": placeholder_text, "fecha": "", "estado": ""})

        for slot, task in zip(CARD_SLOTS, card_tasks):
            title = str(task.get("texto", "")).strip() or "Sin tAtulo"
            fecha = task.get("fecha_formateada") or task.get("fecha") or ""
            estado = str(task.get("estado", "")).upper()
            if fecha:
                fecha_fmt = formatear_fecha(fecha)
            else:
                fecha_fmt = ""
            subtitle = fecha_fmt
            if estado:
                subtitle = f"{fecha_fmt} A {estado}" if fecha_fmt else estado

            self.canvas.create_text(
                self.sx(slot["title"][0]),
                self.sy(slot["title"][1]),
                text=title,
                fill="#000000",
                font=self._font(30),
                anchor="nw",
            )
            if subtitle:
                self.canvas.create_text(
                    self.sx(slot["subtitle"][0]),
                    self.sy(slot["subtitle"][1]),
                    text=subtitle,
                    fill="#000000",
                    font=self._font(10),
                    anchor="nw",
                )

        image_items = [
            {"file": "Group.png", "x": 40, "y": 48, "w": 43, "h": 50},
            {"file": "basketball_svgrepo.com.png", "x": 872, "y": 470, "w": 60, "h": 60},
            {"file": "guitar_svgrepo.com.png", "x": 905, "y": 745, "w": 88, "h": 88},
            {"file": "pencil_svgrepo.png", "x": 1410, "y": 720, "w": 65, "h": 65},
        ]

        for img in image_items:
            self._place_image(img["file"], img["x"], img["y"], img["w"], img["h"])

    # ------------------------------------------------------------------
    # Actions
    # ------------------------------------------------------------------
    def _on_login_click(self):
        email = self.email_var.get().strip().lower()
        password = self.password_var.get()

        self._set_login_error("")

        if es_texto_vacio(email) or es_texto_vacio(password):
            self._set_login_error("*Completa ambos campos.")
            return

        if not es_correo_valido(email):
            self._set_login_error("*Ingresa un correo valido.")
            return

        ok, msg = auth_login(email, password)
        if not ok:
            self._set_login_error("*Correo o contraseña incorrecto/s.")
            return

        profile = self._load_user_profile(email)
        if not profile:
            self._set_login_error("*No se pudo cargar el perfil.")
            return

        self.logged_in_user = profile
        self.pending_email = email
        self._set_login_error("")
        self.show_tasks_screen()

    def _on_register_submit(self):
        name = self.name_var.get().strip()
        email = self.reg_email_var.get().strip().lower()
        password = self.reg_password_var.get()
        confirm = self.reg_confirm_var.get()

        self._set_register_error("")

        if es_texto_vacio(name):
            self._set_register_error("*Ingresa tu nombre completo.")
            return

        if not es_correo_valido(email):
            self._set_register_error("*Ingresa un correo valido.")
            return

        if not es_contrasena_valida(password):
            self._set_register_error("*La contraseña debe tener 8+ caracteres con letras y numeros.")
            return

        if password != confirm:
            self._set_register_error("*Las contraseñas no coinciden.")
            return

        ok, msg = registrar_usuario(email, password, name)
        if not ok:
            self._set_register_error("*" + msg)
            return

        self._set_register_error("")
        self.pending_email = email
        messagebox.showinfo("Crear cuenta", mostrar_mensaje_exito(msg))
        self.show_login_screen()

    def _set_login_error(self, message: str):
        if self.login_error_item:
            self.canvas.itemconfigure(self.login_error_item, text=message)

    def _set_register_error(self, message: str):
        if self.register_error_item:
            self.canvas.itemconfigure(self.register_error_item, text=message)

def main():
    app = LoginScreen()
    app.mainloop()


if __name__ == "__main__":
    main()





    def _on_mouse_wheel(self, event):
        # delta positivo desplaza hacia arriba en Windows
        units = -1 * int(event.delta / 120)
        try:
            self.canvas.yview_scroll(units, "units")
        except Exception:
            pass

    def _show_date_picker(self, anchor_widget: tk.Widget, context: dict):
        import calendar as _cal
        # Cerrar anterior si existe
        if hasattr(self, "_date_picker") and self._date_picker:
            try:
                self._date_picker.destroy()
            except Exception:
                pass
        # Derivar fecha inicial
        today = date.today()
        def parse_initial():
            txt = (context.get("date_var").get() or "").strip()
            try:
                if txt and txt != context.get("date_placeholder"):
                    dd, mm, yyyy = [int(x) for x in txt.replace('-', '/').split('/')]
                    return yyyy, mm
            except Exception:
                pass
            return today.year, today.month
        year, month = parse_initial()
        picker = tk.Toplevel(self.task_modal_window or self)
        picker.overrideredirect(True)
        picker.configure(bg=BACKGROUND_COLOR)
        self._date_picker = picker
        # Posicion cerca del input
        try:
            ax = anchor_widget.winfo_rootx()
            ay = anchor_widget.winfo_rooty() + anchor_widget.winfo_height()
        except Exception:
            ax = self.winfo_rootx() + 40
            ay = self.winfo_rooty() + 40
        w = int(max(240, round(self.sw(300))))
        h = int(max(220, round(self.sh(260))))
        picker.geometry(f"{w}x{h}+{ax}+{ay}")
        # Contenedor
        frame = tk.Frame(picker, bg=BACKGROUND_COLOR, bd=0, highlightthickness=0)
        frame.pack(fill='both', expand=True, padx=8, pady=8)
        # Cabecera con navegacion
        header = tk.Frame(frame, bg=BACKGROUND_COLOR)
        header.pack(fill='x')
        title_lbl = tk.Label(header, text='', bg=BACKGROUND_COLOR, fg=PRIMARY_TEXT_COLOR, font=self._font(18))
        title_lbl.pack(side='top', pady=(0,6))
        nav = tk.Frame(header, bg=BACKGROUND_COLOR)
        nav.pack(fill='x')
        def redraw(y, m):
            for child in days.winfo_children():
                child.destroy()
            month_name = _cal.month_name[m]
            title_lbl.configure(text=f"{month_name} {y}")
            cal = _cal.monthcalendar(y, m)
            for week in cal:
                row = tk.Frame(days, bg=BACKGROUND_COLOR)
                row.pack(fill='x')
                for d in week:
                    txt = f"{d:02d}" if d else ''
                    def make_cmd(day=d, yy=y, mm=m):
                        return lambda: _select(yy, mm, day) if day else None
                    btn = tk.Button(row, text=txt, command=make_cmd(), bd=0, padx=8, pady=4,
                                     bg=WHITE if d else BACKGROUND_COLOR, fg=PRIMARY_TEXT_COLOR,
                                     activebackground='#F4F7F6', activeforeground=PRIMARY_TEXT_COLOR,
                                     font=self._font(14))
                    btn.pack(side='left', expand=True, fill='x', padx=2, pady=2)
        def prev():
            nonlocal year, month
            month -= 1
            if month == 0:
                month = 12; year -= 1
            redraw(year, month)
        def next_():
            nonlocal year, month
            month += 1
            if month == 13:
                month = 1; year += 1
            redraw(year, month)
        ctrl = tk.Frame(nav, bg=BACKGROUND_COLOR)
        ctrl.pack()
        tk.Button(ctrl, text='<', command=prev, bd=0, bg='#EDEEEE', fg=PRIMARY_TEXT_COLOR).pack(side='left', padx=6)
        tk.Button(ctrl, text='>', command=next_, bd=0, bg='#EDEEEE', fg=PRIMARY_TEXT_COLOR).pack(side='left', padx=6)
        days = tk.Frame(frame, bg=BACKGROUND_COLOR)
        days.pack(fill='both', expand=True)
        def _select(yy, mm, dd):
            if not dd: return
            context['date_var'].set(f"{dd:02d}/{mm:02d}/{yy:04d}")
            try:
                picker.destroy()
            except Exception:
                pass
        redraw(year, month)
        # Cerrar si se hace click fuera
        picker.bind('<FocusOut>', lambda _e: picker.destroy())
        picker.focus_force()









