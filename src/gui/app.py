"""Cửa sổ chính tkinter — Dịch Wikipedia EN → VI (Phase 1–7)."""
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

from src.gui import frames
from src.gui.background import run_background
from src.gui.dialogs import show_error, show_info, add_tooltip
from src.wikipedia.fetch import fetch_wikitext_from_url
from src.translate.gemini_client import translate_wikitext_chunked
from src.config_loader import load_config, save_config
from src.check.layout import check_layout
from src.check.content import check_content
from src.check.normalize import normalize


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
    apply_normalize_btn = None
    log_widget = None
    wikitext_en_widget = None
    wikitext_vi_widget = None
    check_result_widget = None
    api_key_entry = None
    model_combo = None
    status_var = None
    task_running = False
    last_normalized_wikitext = None

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
            return translate_wikitext_chunked(wikitext_en, api_key=api_key, model=model)

        run_background(root, task, on_translate_done)

    def do_apply_normalize():
        nonlocal last_normalized_wikitext
        if last_normalized_wikitext is not None:
            wikitext_vi_widget.delete("1.0", tk.END)
            wikitext_vi_widget.insert(tk.END, last_normalized_wikitext)
            frames.log_append(log_widget, "[Log] Đã áp dụng chuẩn hóa lên Wikitext VI.")

    def do_copy():
        """Copy nội dung Wikitext VI vào clipboard (Phase 7)."""
        text = wikitext_vi_widget.get("1.0", tk.END)
        if not text.strip():
            frames.log_append(log_widget, "[Log] Ô Wikitext VI trống.")
            return
        root.clipboard_clear()
        root.clipboard_append(text)
        root.update()
        frames.log_append(log_widget, "[Log] Đã copy wikitext VI vào clipboard.")

    def do_save():
        """Lưu Wikitext VI ra file .wiki hoặc .txt (Phase 7)."""
        text = wikitext_vi_widget.get("1.0", tk.END)
        if not text.strip():
            frames.log_append(log_widget, "[Log] Ô Wikitext VI trống.")
            return
        path = filedialog.asksaveasfilename(
            defaultextension=".wiki",
            filetypes=[("Wikitext", "*.wiki"), ("Text", "*.txt"), ("All", "*.*")],
            title="Lưu Wikitext VI",
        )
        if not path:
            return
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(text)
            frames.log_append(log_widget, f"[Log] Đã lưu vào: {path}")
        except Exception as e:
            frames.log_append(log_widget, f"[Log] Lỗi lưu file: {e}")
            show_error(root, "Lỗi", str(e))

    def on_check_done(success: bool, data):
        nonlocal last_normalized_wikitext
        set_buttons_busy(False)
        if success and isinstance(data, dict):
            lines = data.get("lines", [])
            last_normalized_wikitext = data.get("normalized_wikitext")
            frames.set_check_result(check_result_widget, lines)
            if apply_normalize_btn:
                apply_normalize_btn.configure(state=tk.NORMAL if last_normalized_wikitext else tk.DISABLED)
            frames.log_append(log_widget, "[Log] Đã chạy kiểm tra (bố cục + nội dung + chuẩn hóa).")
        else:
            last_normalized_wikitext = None
            if apply_normalize_btn:
                apply_normalize_btn.configure(state=tk.DISABLED)
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
            status_var.set("Đang kiểm tra & chuẩn hóa...")
        frames.log_append(log_widget, "[Log] Đang kiểm tra & chuẩn hóa...")

        def task():
            lines = []
            normalized_wikitext = None
            # Phase 5: bố cục
            layout_warnings = check_layout(wikitext_vi or wikitext_en)
            lines.append("--- Bố cục ---")
            lines.extend(layout_warnings)
            # Phase 6: nội dung (EN vs VI)
            if wikitext_en and wikitext_vi:
                content_warnings = check_content(wikitext_en, wikitext_vi)
                lines.append("")
                lines.append("--- Nội dung (EN vs VI) ---")
                lines.extend(content_warnings)
            # Phase 6: chuẩn hóa (thuật ngữ, link)
            if wikitext_vi:
                normalized_wikitext, normalize_report = normalize(wikitext_vi)
                lines.append("")
                lines.append("--- Chuẩn hóa ---")
                lines.extend(normalize_report)
            return {"lines": lines, "normalized_wikitext": normalized_wikitext}

        run_background(root, task, on_check_done)

    # --- Menu (Phase 7) — đặt trước để luôn ở trên
    menubar = tk.Menu(root)
    root.config(menu=menubar)
    file_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="File", menu=file_menu)
    file_menu.add_command(label="Lưu Wikitext VI...", command=do_save)
    file_menu.add_separator()
    file_menu.add_command(label="Thoát", command=root.quit)
    help_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Help", menu=help_menu)
    help_menu.add_command(
        label="Giới thiệu",
        command=lambda: show_info(
            root,
            "Giới thiệu",
            "Dịch Wikipedia EN → VI\n\n"
            "Lấy bài Wikipedia tiếng Anh, dịch sang tiếng Việt qua Gemini API,\n"
            "kiểm tra bố cục, chuẩn hóa thuật ngữ, xuất mã nguồn wikitext.\n\n"
            "Xem docs/ke-hoach.md và docs/nghien-cuu.md.",
        ),
    )

    # --- Vùng cuộn: Canvas + Scrollbar chứa toàn bộ nội dung chính
    container = ttk.Frame(root)
    container.pack(fill=tk.BOTH, expand=True)

    canvas = tk.Canvas(container, highlightthickness=0)
    scrollbar = ttk.Scrollbar(container)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.config(command=canvas.yview)
    canvas.config(yscrollcommand=scrollbar.set)

    content_frame = ttk.Frame(canvas)
    canvas_window = canvas.create_window(0, 0, window=content_frame, anchor=tk.NW)

    def _on_frame_configure(_event):
        canvas.configure(scrollregion=canvas.bbox(tk.ALL))

    def _on_canvas_configure(event):
        canvas.itemconfig(canvas_window, width=event.width)

    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), tk.UNITS)

    content_frame.bind("<Configure>", _on_frame_configure)
    canvas.bind("<Configure>", _on_canvas_configure)
    canvas.bind("<MouseWheel>", _on_mousewheel)
    content_frame.bind("<MouseWheel>", _on_mousewheel)
    for child in content_frame.winfo_children():
        if isinstance(child, ttk.Frame):
            child.bind("<MouseWheel>", _on_mousewheel)

    # --- Link + nút Lấy wikitext + Dịch + Kiểm tra (Phase 5)
    _, link_entry, fetch_btn, translate_btn, check_btn = frames.build_link_frame(
        content_frame, do_fetch, do_translate, do_check
    )
    add_tooltip(fetch_btn, "Lấy mã nguồn wikitext từ link Wikipedia tiếng Anh.")
    add_tooltip(translate_btn, "Dịch wikitext EN → VI qua Gemini API (giữ cú pháp wikitext).")
    add_tooltip(check_btn, "Kiểm tra bố cục, so sánh EN/VI, chuẩn hóa thuật ngữ.")
    link_entry.insert(0, "https://en.wikipedia.org/wiki/Front-side_bus")

    # --- Cấu hình Gemini
    _, api_key_entry, model_combo = frames.build_config_frame(content_frame)
    cfg = load_config()
    if cfg.get("api_key"):
        api_key_entry.insert(0, cfg["api_key"])
    if cfg.get("model"):
        try:
            model_combo.set(cfg["model"])
        except tk.TclError:
            pass

    # --- Log
    _, log_widget = frames.build_log_frame(content_frame)
    frames.log_append(log_widget, "[Log] Ứng dụng đã khởi động. Nhập link, API key (nếu cần), rồi Lấy wikitext / Dịch / Kiểm tra.")

    # --- Wikitext EN
    _, wikitext_en_widget = frames.build_wikitext_en_frame(content_frame)

    # --- Wikitext VI
    _, wikitext_vi_widget = frames.build_wikitext_vi_frame(content_frame)

    # --- Xuất Wikitext VI: Copy, Lưu file (Phase 7)
    _, copy_btn, save_btn = frames.build_export_frame(content_frame, do_copy, do_save)
    add_tooltip(copy_btn, "Copy toàn bộ nội dung ô Wikitext VI vào clipboard.")
    add_tooltip(save_btn, "Lưu Wikitext VI ra file .wiki hoặc .txt.")

    # --- Kết quả kiểm tra + nút Áp dụng chuẩn hóa (Phase 5–6)
    _, check_result_widget, apply_normalize_btn = frames.build_check_result_frame(content_frame, do_apply_normalize)

    # --- Thanh trạng thái (Phase 4) — luôn ở dưới cùng
    _, status_var = frames.build_status_bar(root)
    apply_normalize_btn.configure(state=tk.DISABLED)
    frames.set_check_result(check_result_widget, [])

    root.mainloop()


if __name__ == "__main__":
    run_app()
