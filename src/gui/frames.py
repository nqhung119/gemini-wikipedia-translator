"""Các frame GUI: nhập link, cấu hình, log, wikitext EN/VI (Phase 1–3)."""
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext


def build_link_frame(parent, on_fetch_click, on_translate_click=None):
    """Frame nhập link Wikipedia EN, nút Lấy wikitext và nút Dịch sang tiếng Việt."""
    frame = ttk.LabelFrame(parent, text="Link Wikipedia tiếng Anh")
    ttk.Label(frame, text="URL:").pack(side=tk.LEFT, padx=(0, 4))
    entry = ttk.Entry(frame, width=70)
    entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 8))
    btn_fetch = ttk.Button(frame, text="Lấy wikitext", command=on_fetch_click)
    btn_fetch.pack(side=tk.RIGHT, padx=(0, 4))
    if on_translate_click:
        btn_translate = ttk.Button(frame, text="Dịch sang tiếng Việt", command=on_translate_click)
        btn_translate.pack(side=tk.RIGHT)
        frame.pack(fill=tk.X, padx=8, pady=6)
        return frame, entry, btn_fetch, btn_translate
    frame.pack(fill=tk.X, padx=8, pady=6)
    return frame, entry, btn_fetch


def build_config_frame(parent):
    """Frame cấu hình: API key Gemini, chọn model."""
    frame = ttk.LabelFrame(parent, text="Cấu hình Gemini")
    ttk.Label(frame, text="API key:").pack(side=tk.LEFT, padx=(0, 4))
    api_key_entry = ttk.Entry(frame, width=50, show="*")
    api_key_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 8))
    ttk.Label(frame, text="Model:").pack(side=tk.LEFT, padx=(8, 4))
    model_combo = ttk.Combobox(
        frame,
        width=22,
        values=["gemini-1.5-flash", "gemini-1.5-pro", "gemini-2.0-flash", "gemini-2.5-flash"],
        state="readonly",
    )
    model_combo.pack(side=tk.LEFT, padx=(0, 8))
    model_combo.set("gemini-1.5-flash")
    frame.pack(fill=tk.X, padx=8, pady=6)
    return frame, api_key_entry, model_combo


def build_status_bar(parent):
    """Thanh trạng thái: Sẵn sàng / Đang xử lý... (Phase 4)."""
    frame = ttk.Frame(parent)
    ttk.Label(frame, text="Trạng thái:").pack(side=tk.LEFT, padx=(0, 4))
    status_var = tk.StringVar(value="Sẵn sàng")
    status_label = ttk.Label(frame, textvariable=status_var)
    status_label.pack(side=tk.LEFT)
    frame.pack(fill=tk.X, padx=8, pady=2)
    return frame, status_var


def build_log_frame(parent):
    """Frame hiển thị log / trạng thái."""
    frame = ttk.LabelFrame(parent, text="Log")
    log = scrolledtext.ScrolledText(frame, height=4, wrap=tk.WORD, state=tk.DISABLED)
    log.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)
    frame.pack(fill=tk.X, padx=8, pady=6)
    return frame, log


def build_wikitext_en_frame(parent):
    """Frame hiển thị wikitext tiếng Anh."""
    frame = ttk.LabelFrame(parent, text="Wikitext EN")
    text = scrolledtext.ScrolledText(frame, wrap=tk.WORD, state=tk.NORMAL, height=12)
    text.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)
    frame.pack(fill=tk.BOTH, expand=True, padx=8, pady=6)
    return frame, text


def build_wikitext_vi_frame(parent):
    """Frame hiển thị wikitext tiếng Việt (có thể chỉnh tay)."""
    frame = ttk.LabelFrame(parent, text="Wikitext VI")
    text = scrolledtext.ScrolledText(frame, wrap=tk.WORD, state=tk.NORMAL, height=12)
    text.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)
    frame.pack(fill=tk.BOTH, expand=True, padx=8, pady=6)
    return frame, text


def log_append(log_widget, message):
    """Ghi thêm một dòng vào ô log (thread-safe qua main thread)."""
    log_widget.configure(state=tk.NORMAL)
    log_widget.insert(tk.END, message + "\n")
    log_widget.see(tk.END)
    log_widget.configure(state=tk.DISABLED)
