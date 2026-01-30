"""Cửa sổ chính tkinter — Dịch Wikipedia EN → VI (Phase 1–3)."""
import tkinter as tk
from tkinter import ttk
import threading

from src.gui import frames
from src.gui.dialogs import show_error
from src.wikipedia.fetch import fetch_wikitext_from_url
from src.translate.gemini_client import translate_wikitext
from src.config_loader import load_config, save_config


def run_app():
    """Khởi chạy ứng dụng GUI."""
    root = tk.Tk()
    root.title("Dịch Wikipedia EN → VI")
    root.minsize(800, 600)
    root.geometry("900x750")

    link_entry = None
    fetch_btn = None
    translate_btn = None
    log_widget = None
    wikitext_en_widget = None
    wikitext_vi_widget = None
    api_key_entry = None
    model_combo = None
    fetch_running = False
    translate_running = False

    def on_fetch_done(success: bool, data: str):
        nonlocal fetch_running
        fetch_running = False
        if fetch_btn:
            fetch_btn.configure(state=tk.NORMAL)
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
        if fetch_running:
            return
        fetch_running = True
        fetch_btn.configure(state=tk.DISABLED)
        frames.log_append(log_widget, "[Log] Đang lấy wikitext...")

        def worker():
            try:
                wikitext = fetch_wikitext_from_url(url)
                root.after(0, lambda w=wikitext: on_fetch_done(True, w))
            except Exception as e:
                err = str(e)
                root.after(0, lambda e=err: on_fetch_done(False, e))

        threading.Thread(target=worker, daemon=True).start()

    def on_translate_done(success: bool, data: str):
        nonlocal translate_running
        translate_running = False
        if translate_btn:
            translate_btn.configure(state=tk.NORMAL)
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
        if translate_running:
            return
        translate_running = True
        translate_btn.configure(state=tk.DISABLED)
        frames.log_append(log_widget, "[Log] Đang dịch sang tiếng Việt...")
        save_config(api_key=api_key, model=model)

        def worker():
            try:
                out = translate_wikitext(wikitext_en, api_key=api_key, model=model)
                root.after(0, lambda w=out: on_translate_done(True, w))
            except Exception as e:
                err = str(e)
                root.after(0, lambda e=err: on_translate_done(False, e))

        threading.Thread(target=worker, daemon=True).start()

    # --- Link + nút Lấy wikitext + Dịch
    _, link_entry, fetch_btn, translate_btn = frames.build_link_frame(root, do_fetch, do_translate)
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
    frames.log_append(log_widget, "[Log] Ứng dụng đã khởi động. Nhập link, API key (nếu cần), rồi Lấy wikitext / Dịch.")

    # --- Wikitext EN
    _, wikitext_en_widget = frames.build_wikitext_en_frame(root)

    # --- Wikitext VI
    _, wikitext_vi_widget = frames.build_wikitext_vi_frame(root)

    root.mainloop()


if __name__ == "__main__":
    run_app()
