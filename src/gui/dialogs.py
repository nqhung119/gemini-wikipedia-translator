"""Hộp thoại: chọn ngôn ngữ, thông báo lỗi, tooltip (Phase 1–7)."""
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk


def choose_language():
    """Hiển thị cửa sổ chọn ngôn ngữ (English / Tiếng Việt). Trả về 'en' hoặc 'vi'.
    Dùng Tk() riêng để luôn hiển thị được trên Windows (không phụ thuộc cửa sổ cha)."""
    result = [None]

    root = tk.Tk()
    root.title("Chọn ngôn ngữ / Choose language")
    root.resizable(False, False)

    f = ttk.Frame(root, padding=20)
    f.pack(fill=tk.BOTH, expand=True)
    ttk.Label(f, text="Select interface language:\nChọn ngôn ngữ giao diện:").pack(pady=(0, 16))
    btn_frame = ttk.Frame(f)
    btn_frame.pack()
    ttk.Button(btn_frame, text="English", width=14, command=lambda: _choose("en")).pack(side=tk.LEFT, padx=6)
    ttk.Button(btn_frame, text="Tiếng Việt", width=14, command=lambda: _choose("vi")).pack(side=tk.LEFT, padx=6)

    def _choose(lang):
        result[0] = lang
        root.quit()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", lambda: _choose("vi"))
    root.update_idletasks()
    w, h = 320, 120
    x = (root.winfo_screenwidth() - w) // 2
    y = (root.winfo_screenheight() - h) // 2
    root.geometry("%dx%d+%d+%d" % (w, h, x, y))
    root.mainloop()
    return result[0] if result[0] else "vi"


def show_error(parent, title, message):
    """Hiển thị hộp thoại lỗi."""
    messagebox.showerror(title, message, parent=parent)


def show_info(parent, title, message):
    """Hiển thị hộp thoại thông tin."""
    messagebox.showinfo(title, message, parent=parent)


_tooltip_toplevel = None


def _show_tooltip(widget, text, x, y):
    """Hiển thị tooltip tại (x, y) (tọa độ root)."""
    global _tooltip_toplevel
    if _tooltip_toplevel:
        try:
            _tooltip_toplevel.destroy()
        except tk.TclError:
            pass
        _tooltip_toplevel = None
    win = widget.winfo_toplevel()
    _tooltip_toplevel = tk.Toplevel(win)
    _tooltip_toplevel.wm_overrideredirect(True)
    _tooltip_toplevel.wm_geometry(f"+{x + 12}+{y + 12}")
    label = tk.Label(
        _tooltip_toplevel,
        text=text,
        justify=tk.LEFT,
        background="#ffffc0",
        relief=tk.SOLID,
        borderwidth=1,
        padx=4,
        pady=2,
        font=("TkDefaultFont", 9),
    )
    label.pack()


def _hide_tooltip():
    global _tooltip_toplevel
    if _tooltip_toplevel:
        _tooltip_toplevel.destroy()
        _tooltip_toplevel = None


def add_tooltip(widget, text):
    """Gắn tooltip cho widget: khi rê chuột vào hiển thị text (Phase 7)."""
    def on_enter(event):
        _show_tooltip(widget, text, event.x_root, event.y_root)

    def on_leave(event):
        _hide_tooltip()

    widget.bind("<Enter>", on_enter)
    widget.bind("<Leave>", on_leave)
