"""Các frame GUI: nhập link, cấu hình, log, wikitext EN/VI (Phase 1–3)."""
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext

from src.gui.i18n import t


def _placeholder_focus_in(entry, placeholder, *, is_password=False):
    """Xóa chữ mờ khi focus vào ô (chỉ khi đang hiển thị placeholder)."""
    if entry.cget("fg") == "gray":
        entry.delete(0, tk.END)
        entry.config(fg="black")
        if is_password:
            entry.config(show="*")


def _placeholder_focus_out(entry, placeholder, *, is_password=False):
    """Hiện lại chữ mờ khi focus ra và ô trống."""
    if not entry.get().strip():
        entry.delete(0, tk.END)
        entry.insert(0, placeholder)
        entry.config(fg="gray")
        if is_password:
            entry.config(show="")


def build_link_frame(parent, on_fetch_click, on_translate_click=None, on_check_click=None):
    """Frame nhập link Wikipedia EN, nút Lấy wikitext, Dịch, Kiểm tra & Chuẩn hóa (Phase 5)."""
    frame = ttk.LabelFrame(parent, text=t("link_frame_title"))
    ttk.Label(frame, text=t("url_label")).pack(side=tk.LEFT, padx=(0, 4))
    url_placeholder = t("url_placeholder")
    entry = tk.Entry(frame, width=70, fg="gray")
    entry.insert(0, url_placeholder)
    entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 8))
    entry.bind("<FocusIn>", lambda e: _placeholder_focus_in(entry, url_placeholder))
    entry.bind("<FocusOut>", lambda e: _placeholder_focus_out(entry, url_placeholder))
    # Thứ tự nút: Lấy wikitext → Dịch → Kiểm tra (pack RIGHT nên pack ngược lại)
    if on_check_click:
        btn_check = ttk.Button(frame, text=t("btn_check"), command=on_check_click)
        btn_check.pack(side=tk.RIGHT)
    if on_translate_click:
        btn_translate = ttk.Button(frame, text=t("btn_translate"), command=on_translate_click)
        btn_translate.pack(side=tk.RIGHT, padx=(0, 4))
    btn_fetch = ttk.Button(frame, text=t("btn_fetch"), command=on_fetch_click)
    btn_fetch.pack(side=tk.RIGHT, padx=(0, 4))
    frame.pack(fill=tk.X, padx=8, pady=6)
    if on_translate_click and on_check_click:
        return frame, entry, btn_fetch, btn_translate, btn_check
    if on_translate_click:
        return frame, entry, btn_fetch, btn_translate
    return frame, entry, btn_fetch


def build_config_frame(parent):
    """Frame cấu hình: API key Gemini, chọn model."""
    frame = ttk.LabelFrame(parent, text=t("config_frame_title"))
    ttk.Label(frame, text=t("api_key_label")).pack(side=tk.LEFT, padx=(0, 4))
    api_key_placeholder = t("api_key_placeholder")
    api_key_entry = tk.Entry(frame, width=50, fg="gray", show="")
    api_key_entry.insert(0, api_key_placeholder)
    api_key_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 8))
    api_key_entry.bind(
        "<FocusIn>", lambda e: _placeholder_focus_in(api_key_entry, api_key_placeholder, is_password=True)
    )
    api_key_entry.bind(
        "<FocusOut>", lambda e: _placeholder_focus_out(api_key_entry, api_key_placeholder, is_password=True)
    )
    ttk.Label(frame, text=t("model_label")).pack(side=tk.LEFT, padx=(8, 4))
    model_combo = ttk.Combobox(
        frame,
        width=26,
        values=[
            "gemini-3-flash-preview",
            "gemini-3-pro-preview",
        ],
        state="readonly",
    )
    model_combo.pack(side=tk.LEFT, padx=(0, 8))
    model_combo.set("gemini-3-flash-preview")
    frame.pack(fill=tk.X, padx=8, pady=6)
    return frame, api_key_entry, model_combo


def build_status_bar(parent):
    """Thanh trạng thái: Sẵn sàng / Đang xử lý... (Phase 4)."""
    frame = ttk.Frame(parent)
    ttk.Label(frame, text=t("status_label")).pack(side=tk.LEFT, padx=(0, 4))
    status_var = tk.StringVar(value=t("status_ready"))
    status_label = ttk.Label(frame, textvariable=status_var)
    status_label.pack(side=tk.LEFT)
    frame.pack(fill=tk.X, padx=8, pady=2)
    return frame, status_var


def build_log_frame(parent):
    """Frame hiển thị log / trạng thái."""
    frame = ttk.LabelFrame(parent, text=t("log_frame_title"))
    log = scrolledtext.ScrolledText(frame, height=4, wrap=tk.WORD, state=tk.DISABLED)
    log.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)
    frame.pack(fill=tk.X, padx=8, pady=6)
    return frame, log


def build_wikitext_en_frame(parent):
    """Frame hiển thị wikitext tiếng Anh."""
    frame = ttk.LabelFrame(parent, text=t("wikitext_en_title"))
    text = scrolledtext.ScrolledText(frame, wrap=tk.WORD, state=tk.NORMAL, height=12)
    text.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)
    frame.pack(fill=tk.BOTH, expand=True, padx=8, pady=6)
    return frame, text


def build_wikitext_vi_frame(parent):
    """Frame hiển thị wikitext tiếng Việt (có thể chỉnh tay)."""
    frame = ttk.LabelFrame(parent, text=t("wikitext_vi_title"))
    text = scrolledtext.ScrolledText(frame, wrap=tk.WORD, state=tk.NORMAL, height=12)
    text.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)
    frame.pack(fill=tk.BOTH, expand=True, padx=8, pady=6)
    return frame, text


def build_export_frame(parent, on_copy_click, on_save_click):
    """Frame nút xuất: Copy wikitext VI, Lưu ra file (Phase 7)."""
    frame = ttk.LabelFrame(parent, text=t("export_frame_title"))
    btn_copy = ttk.Button(frame, text=t("btn_copy"), command=on_copy_click)
    btn_copy.pack(side=tk.LEFT, padx=(0, 8))
    btn_save = ttk.Button(frame, text=t("btn_save"), command=on_save_click)
    btn_save.pack(side=tk.LEFT)
    frame.pack(fill=tk.X, padx=8, pady=6)
    return frame, btn_copy, btn_save


def build_check_result_frame(parent, on_apply_normalize=None):
    """Frame hiển thị kết quả kiểm tra (Phase 5–6); nút Áp dụng chuẩn hóa (Phase 6)."""
    frame = ttk.LabelFrame(parent, text=t("check_result_title"))
    text = scrolledtext.ScrolledText(frame, height=6, wrap=tk.WORD, state=tk.DISABLED)
    text.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)
    if on_apply_normalize is not None:
        btn_apply = ttk.Button(frame, text=t("btn_apply_normalize"), command=on_apply_normalize)
        btn_apply.pack(pady=(0, 4))
        frame.pack(fill=tk.X, padx=8, pady=6)
        return frame, text, btn_apply
    frame.pack(fill=tk.X, padx=8, pady=6)
    return frame, text


def set_check_result(check_result_widget, lines: list):
    """Ghi danh sách cảnh báo vào ô Kết quả kiểm tra (gọi từ main thread)."""
    check_result_widget.configure(state=tk.NORMAL)
    check_result_widget.delete("1.0", tk.END)
    text = "\n".join(lines) if lines else t("check_not_run")
    check_result_widget.insert(tk.END, text)
    check_result_widget.configure(state=tk.DISABLED)


def log_append(log_widget, message):
    """Ghi thêm một dòng vào ô log (thread-safe qua main thread)."""
    log_widget.configure(state=tk.NORMAL)
    log_widget.insert(tk.END, message + "\n")
    log_widget.see(tk.END)
    log_widget.configure(state=tk.DISABLED)
