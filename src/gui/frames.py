"""Các frame GUI: nhập link, log, wikitext EN (Phase 1)."""
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext


def build_link_frame(parent, on_fetch_click):
    """Frame nhập link Wikipedia EN và nút Lấy wikitext."""
    frame = ttk.LabelFrame(parent, text="Link Wikipedia tiếng Anh")
    ttk.Label(frame, text="URL:").pack(side=tk.LEFT, padx=(0, 4))
    entry = ttk.Entry(frame, width=70)
    entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 8))
    btn = ttk.Button(frame, text="Lấy wikitext", command=on_fetch_click)
    btn.pack(side=tk.RIGHT)
    frame.pack(fill=tk.X, padx=8, pady=6)
    return frame, entry, btn


def build_log_frame(parent):
    """Frame hiển thị log / trạng thái."""
    frame = ttk.LabelFrame(parent, text="Trạng thái")
    log = scrolledtext.ScrolledText(frame, height=4, wrap=tk.WORD, state=tk.DISABLED)
    log.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)
    frame.pack(fill=tk.X, padx=8, pady=6)
    return frame, log


def build_wikitext_en_frame(parent):
    """Frame hiển thị wikitext tiếng Anh (read-only)."""
    frame = ttk.LabelFrame(parent, text="Wikitext EN")
    text = scrolledtext.ScrolledText(frame, wrap=tk.WORD, state=tk.NORMAL)
    text.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)
    frame.pack(fill=tk.BOTH, expand=True, padx=8, pady=6)
    return frame, text


def log_append(log_widget, message):
    """Ghi thêm một dòng vào ô log (thread-safe qua main thread)."""
    log_widget.configure(state=tk.NORMAL)
    log_widget.insert(tk.END, message + "\n")
    log_widget.see(tk.END)
    log_widget.configure(state=tk.DISABLED)
