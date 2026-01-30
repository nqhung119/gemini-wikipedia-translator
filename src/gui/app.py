"""Cửa sổ chính tkinter — Dịch Wikipedia EN → VI (Phase 1 + 2)."""
import tkinter as tk
from tkinter import ttk
import threading

from src.gui import frames
from src.gui.dialogs import show_error
from src.wikipedia.fetch import fetch_wikitext_from_url


def run_app():
    """Khởi chạy ứng dụng GUI."""
    root = tk.Tk()
    root.title("Dịch Wikipedia EN → VI")
    root.minsize(800, 600)
    root.geometry("900x650")

    link_entry = None
    fetch_btn = None
    log_widget = None
    wikitext_en_widget = None
    fetch_running = False

    def on_fetch_done(success: bool, data: str):
        """Callback trên main thread sau khi fetch xong (hoặc lỗi)."""
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
            frames.log_append(log_widget, "[Log] Chưa nhập URL. Vui lòng dán link bài Wikipedia tiếng Anh.")
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

    # --- Link + nút
    _, link_entry, fetch_btn = frames.build_link_frame(root, do_fetch)
    link_entry.insert(0, "https://en.wikipedia.org/wiki/Front-side_bus")

    # --- Log
    _, log_widget = frames.build_log_frame(root)
    frames.log_append(log_widget, "[Log] Ứng dụng đã khởi động. Nhập link và bấm 'Lấy wikitext'.")

    # --- Wikitext EN
    _, wikitext_en_widget = frames.build_wikitext_en_frame(root)

    root.mainloop()


if __name__ == "__main__":
    run_app()
