"""Cửa sổ chính tkinter — Dịch Wikipedia EN → VI (Phase 1–5)."""
import tkinter as tk
from tkinter import ttk

from src.gui import frames
from src.gui.background import run_background
from src.gui.dialogs import show_error
from src.wikipedia.fetch import fetch_wikitext_from_url
from src.translate.gemini_client import translate_wikitext
from src.config_loader import load_config, save_config
from src.check.layout import check_layout


def run_app():
    """Khởi chạy ứng dụng GUI."""
    root = tk.Tk()
    root.title("Dịch Wikipedia EN → VI")
    root.minsize(800, 600)
    root.geometry("900x800")

    link_entry = None
    fetch_btn = None
    translate_btn = None
    check_btn = None
    log_widget = None
    wikitext_en_widget = None
    wikitext_vi_widget = None
    check_result_widget = None
    api_key_entry = None
    model_combo = None
    status_var = None
    task_running = False

    def set_buttons_busy(busy: bool):
        """Bật/tắt trạng thái bận: disable/enable Lấy wikitext, Dịch, Kiểm tra (Phase 4–5)."""
        nonlocal task_running
        task_running = busy
        state = tk.DISABLED if busy else tk.NORMAL
        if fetch_btn:
            fetch_btn.configure(state=state)
        if translate_btn:
            translate_btn.configure(state=state)
        if check_btn:
            check_btn.configure(state=state)
        if status_var:
            status_var.set("Đang xử lý..." if busy else "Sẵn sàng")

    def on_fetch_done(success: bool, data: str):
        set_buttons_busy(False)
        if success:
            wikitext_en_widget.delete("1.0", tk.END)
            wikitext_en_widget.insert(tk.END, data)
            frames.log_append(log_widget, "[Log] Đã lấy wikitext xong.")
        else:
            frames.log_append(log_widget, f"[Log] Lỗi: {data}")
            show_error(root, "Lỗi", data)

    def do_fetch():
        url = link_entry.get().strip()
        if not url:
            frames.log_append(log_widget, "[Log] Chưa nhập URL.")
            return
        if task_running:
            return
        set_buttons_busy(True)
        if status_var:
            status_var.set("Đang lấy wikitext...")
        frames.log_append(log_widget, "[Log] Đang lấy wikitext...")

        def task():
            return fetch_wikitext_from_url(url)

        run_background(root, task, on_fetch_done)

    def on_translate_done(success: bool, data: str):
        set_buttons_busy(False)
        if success:
            wikitext_vi_widget.delete("1.0", tk.END)
            wikitext_vi_widget.insert(tk.END, data)
            frames.log_append(log_widget, "[Log] Đã dịch xong.")
        else:
            frames.log_append(log_widget, f"[Log] Lỗi dịch: {data}")
            show_error(root, "Lỗi dịch", data)

    def do_translate():
        wikitext_en = wikitext_en_widget.get("1.0", tk.END).strip()
        if not wikitext_en:
            frames.log_append(log_widget, "[Log] Chưa có wikitext EN. Hãy bấm 'Lấy wikitext' trước.")
            return
        api_key = api_key_entry.get().strip()
        model = (model_combo.get() or "gemini-1.5-flash").strip()
        if not api_key:
            frames.log_append(log_widget, "[Log] Chưa nhập API key Gemini.")
            show_error(root, "Cấu hình", "Vui lòng nhập API key Gemini trong ô Cấu hình Gemini.")
            return
        if task_running:
            return
        set_buttons_busy(True)
        if status_var:
            status_var.set("Đang dịch sang tiếng Việt...")
        frames.log_append(log_widget, "[Log] Đang dịch sang tiếng Việt...")
        save_config(api_key=api_key, model=model)

        def task():
            return translate_wikitext(wikitext_en, api_key=api_key, model=model)

        run_background(root, task, on_translate_done)

    def on_check_done(success: bool, data):
        set_buttons_busy(False)
        if success and isinstance(data, list):
            frames.set_check_result(check_result_widget, data)
            frames.log_append(log_widget, "[Log] Đã chạy kiểm tra bố cục.")
        else:
            frames.set_check_result(check_result_widget, [f"Lỗi: {data}"])
            frames.log_append(log_widget, f"[Log] Lỗi kiểm tra: {data}")

    def do_check():
        wikitext_vi = wikitext_vi_widget.get("1.0", tk.END).strip()
        wikitext_en = wikitext_en_widget.get("1.0", tk.END).strip()
        wikitext = wikitext_vi or wikitext_en
        if not wikitext:
            frames.log_append(log_widget, "[Log] Chưa có wikitext (EN hoặc VI). Hãy Lấy wikitext hoặc Dịch trước.")
            frames.set_check_result(check_result_widget, ["Chưa có wikitext để kiểm tra."])
            return
        if task_running:
            return
        set_buttons_busy(True)
        if status_var:
            status_var.set("Đang kiểm tra bố cục...")
        frames.log_append(log_widget, "[Log] Đang kiểm tra bố cục...")

        def task():
            return check_layout(wikitext)

        run_background(root, task, on_check_done)

    # --- Thanh trạng thái (Phase 4)
    _, status_var = frames.build_status_bar(root)

    # --- Link + nút Lấy wikitext + Dịch + Kiểm tra (Phase 5)
    _, link_entry, fetch_btn, translate_btn, check_btn = frames.build_link_frame(
        root, do_fetch, do_translate, do_check
    )
    link_entry.insert(0, "https://en.wikipedia.org/wiki/Front-side_bus")

    # --- Cấu hình Gemini
    _, api_key_entry, model_combo = frames.build_config_frame(root)
    cfg = load_config()
    if cfg.get("api_key"):
        api_key_entry.insert(0, cfg["api_key"])
    if cfg.get("model"):
        try:
            model_combo.set(cfg["model"])
        except tk.TclError:
            pass

    # --- Log
    _, log_widget = frames.build_log_frame(root)
    frames.log_append(log_widget, "[Log] Ứng dụng đã khởi động. Nhập link, API key (nếu cần), rồi Lấy wikitext / Dịch / Kiểm tra.")

    # --- Wikitext EN
    _, wikitext_en_widget = frames.build_wikitext_en_frame(root)

    # --- Wikitext VI
    _, wikitext_vi_widget = frames.build_wikitext_vi_frame(root)

    # --- Kết quả kiểm tra (Phase 5)
    _, check_result_widget = frames.build_check_result_frame(root)
    frames.set_check_result(check_result_widget, [])

    root.mainloop()


if __name__ == "__main__":
    run_app()
