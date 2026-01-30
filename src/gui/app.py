"""Cửa sổ chính tkinter — Dịch Wikipedia EN → VI (Phase 1)."""
import tkinter as tk
from tkinter import ttk

from src.gui import frames


def run_app():
    """Khởi chạy ứng dụng GUI."""
    root = tk.Tk()
    root.title("Dịch Wikipedia EN → VI")
    root.minsize(800, 600)
    root.geometry("900x650")

    # Biến trỏ tới widget (để callback cập nhật)
    link_entry = None
    fetch_btn = None
    log_widget = None
    wikitext_en_widget = None

    def on_fetch_click():
        url = link_entry.get().strip()
        if not url:
            frames.log_append(log_widget, "[Log] Chưa nhập URL. Vui lòng dán link bài Wikipedia tiếng Anh.")
            return
        frames.log_append(log_widget, f"[Log] Đã bấm Lấy wikitext cho: {url[:60]}...")
        # Phase 1: chưa gọi API thật; Phase 2 sẽ gọi wikipedia.fetch
        frames.log_append(log_widget, "[Log] Chức năng fetch sẽ triển khai ở Phase 2.")
        wikitext_en_widget.delete("1.0", tk.END)
        wikitext_en_widget.insert(tk.END, "(Wikitext EN sẽ hiển thị tại đây sau Phase 2)")

    # --- Link + nút
    lf, link_entry, fetch_btn = frames.build_link_frame(root, on_fetch_click)
    link_entry.insert(0, "https://en.wikipedia.org/wiki/Front-side_bus")

    # --- Log
    _, log_widget = frames.build_log_frame(root)
    frames.log_append(log_widget, "[Log] Ứng dụng đã khởi động (Phase 1). Nhập link và bấm 'Lấy wikitext'.")

    # --- Wikitext EN
    _, wikitext_en_widget = frames.build_wikitext_en_frame(root)

    root.mainloop()


if __name__ == "__main__":
    run_app()
