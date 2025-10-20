import tkinter as tk
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
from task_service import listar_tareas
from db import get_conn

# ---------------------------------------------------------------------------
# Base palette extracted from the reference mockups
BACKGROUND_COLOR = "#E9EFEC"
SECONDARY_COLOR = "#697565"
PRIMARY_TEXT_COLOR = "#1E201E"
WHITE = "#FFFFFF"

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

TIMELINE_SLOTS = [
    {"title": (336, 328), "subtitle": (336, 295), "badge": (336, 372)},
    {"title": (336, 464), "subtitle": (336, 428), "badge": (336, 614)},
    {"title": (336, 762), "subtitle": (336, 728), "badge": (336, 849)},
    {"title": (669, 757), "subtitle": (669, 723), "badge": (669, 849)},
]

TIMELINE_PLACEHOLDERS = [
    {"texto": "Problemario de Matemáticas", "fecha": "13/05/2025", "estado": "A TIEMPO"},
    {"texto": "Basketball", "fecha": "14/05/2025", "estado": "PRONTO"},
    {"texto": "Inglés", "fecha": "16/05/2025", "estado": "HOY"},
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
    "La revolución mexicana...",
]


class LoginScreen(tk.Tk):
    """Main window that can toggle between login and register mockups with pixel-perfect scaling."""

    def __init__(self):
        super().__init__()
        self.title("Inicio de Sesión")
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

        self.fonts = self._prepare_fonts()
        self.overlay_widgets: list[tk.Widget] = []
        self.current_screen = "login"
        self.chevron_photo = self._load_chevron_image()
        self.image_cache: dict[tuple[str, int, int], tk.PhotoImage] = {}
        self.active_images: list[tk.PhotoImage] = []
        self.pending_email: str | None = None
        self.logged_in_user: dict[str, str] | None = None
        self.dashboard_tasks: list[dict] = []

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
            messagebox.showwarning("Recursos", f"No se encontró {CHEVRON_IMAGE}. Se dibujará el ícono con líneas.")
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
            messagebox.showwarning("Recursos", f"No se encontró {filename}.")
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
        self.canvas.delete("all")
        for widget in self.overlay_widgets:
            widget.destroy()
        self.overlay_widgets.clear()
        self.active_images = []

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

    def show_register_screen(self):
        self.current_screen = "register"
        self._clear_screen()
        self._draw_background()
        self._draw_register_ui()
        self._add_register_entries()

    def show_dashboard_screen(self):
        self.current_screen = "dashboard"
        self._clear_screen()
        self.canvas.configure(bg=BACKGROUND_COLOR)
        self._prepare_dashboard_data()
        self._draw_dashboard_ui()

    # ------------------------------------------------------------------
    # Login screen
    # ------------------------------------------------------------------
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
            text="Correo electrónico",
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
            ("Correo electrónico", REGISTER_FIELD_TOPS["email"] - 45),
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
            text="Iniciar sesión",
            font=self.fonts["button"],
            fill=WHITE,
            anchor="center",
        )
        self._bind_click(button_shapes + [button_text], self._on_register_submit)

        question = self.canvas.create_text(
            self.sx(REGISTER_BUTTON[0] + REGISTER_BUTTON[2] / 2),
            self.sy(910),
            text="¿Aún no tienes una cuenta?",
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
            {"text": "Vista rápida", "x": 153, "y": 18, "size": 85.33, "color": "#000000"},
            {"text": "Calendario", "x": 152, "y": 150, "size": 64, "color": "#000000"},
            {"text": "Álbumes", "x": 1102, "y": 150, "size": 64, "color": "#000000"},
            {"text": "Notas", "x": 1102, "y": 593, "size": 64, "color": "#000000"},
            {"text": "13:00", "x": 152, "y": 279, "size": 20, "color": "#3C3D37"},
            {"text": "14:00", "x": 152, "y": 413, "size": 20, "color": "#3C3D37"},
            {"text": "15:00", "x": 152, "y": 546, "size": 20, "color": "#1E201E"},
            {"text": "16:00", "x": 152, "y": 660, "size": 20, "color": "#3C3D37"},
            {"text": "17:00", "x": 152, "y": 754, "size": 20, "color": "#3C3D37"},
            {"text": "18:00", "x": 152, "y": 868, "size": 20, "color": "#3C3D37"},
            {"text": "Inicio", "x": 385, "y": 940, "size": 30, "color": "#1E201E"},
            {"text": "Calendario", "x": 621, "y": 940, "size": 30, "color": "#3C3D37"},
            {"text": "Álbumes", "x": 913, "y": 935, "size": 30, "color": "#3C3D37"},
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

        logout_button = tk.Button(self, text="Cerrar sesión", command=self._logout)
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
                subtitle = f"{fecha_fmt} · {estado}" if fecha_fmt else estado

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
            title = str(task.get("texto", "")).strip() or "Sin título"
            fecha = task.get("fecha_formateada") or task.get("fecha") or ""
            estado = str(task.get("estado", "")).upper()
            if fecha:
                fecha_fmt = formatear_fecha(fecha)
            else:
                fecha_fmt = ""
            subtitle = fecha_fmt
            if estado:
                subtitle = f"{fecha_fmt} · {estado}" if fecha_fmt else estado

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

        if es_texto_vacio(email) or es_texto_vacio(password):
            messagebox.showerror("Inicio de Sesión", mostrar_mensaje_error("Completa ambos campos."))
            return

        if not es_correo_valido(email):
            messagebox.showerror("Inicio de Sesión", mostrar_mensaje_error("El correo no parece válido."))
            return

        ok, msg = auth_login(email, password)
        if not ok:
            messagebox.showerror("Inicio de Sesión", mostrar_mensaje_error(msg))
            return

        profile = self._load_user_profile(email)
        if not profile:
            messagebox.showerror("Inicio de Sesión", mostrar_mensaje_error("No se pudo cargar el perfil."))
            return

        self.logged_in_user = profile
        self.pending_email = email
        messagebox.showinfo("Inicio de Sesión", mostrar_mensaje_exito(msg))
        self.show_dashboard_screen()

    def _on_register_submit(self):
        name = self.name_var.get().strip()
        email = self.reg_email_var.get().strip().lower()
        password = self.reg_password_var.get()
        confirm = self.reg_confirm_var.get()

        if es_texto_vacio(name):
            messagebox.showerror("Crear cuenta", mostrar_mensaje_error("El nombre no puede estar vacío."))
            return

        if not es_correo_valido(email):
            messagebox.showerror("Crear cuenta", mostrar_mensaje_error("El correo no parece válido."))
            return

        if not es_contrasena_valida(password):
            messagebox.showerror(
                "Crear cuenta",
                mostrar_mensaje_error("La contraseña debe tener 8+ caracteres, con letras y números."),
            )
            return

        if password != confirm:
            messagebox.showerror("Crear cuenta", mostrar_mensaje_error("Las contraseñas no coinciden."))
            return

        ok, msg = registrar_usuario(email, password, name)
        if not ok:
            messagebox.showerror("Crear cuenta", mostrar_mensaje_error(msg))
            return

        self.pending_email = email
        messagebox.showinfo("Crear cuenta", mostrar_mensaje_exito(msg))
        self.show_login_screen()

def main():
    app = LoginScreen()
    app.mainloop()


if __name__ == "__main__":
    main()
