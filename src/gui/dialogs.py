"""Hộp thoại: cài đặt API key, thông báo lỗi, tooltip (Phase 1–7)."""
import tkinter as tk
from tkinter import messagebox


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
