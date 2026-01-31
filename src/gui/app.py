"""Cửa sổ chính tkinter — Dịch Wikipedia (nhiều cặp ngôn ngữ, mặc định EN → VI)."""
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

from src.gui import frames
from src.gui.background import run_background
from src.gui.dialogs import show_error, show_info, add_tooltip, choose_language
from src.gui.i18n import set_lang, t
from src.wikipedia.fetch import fetch_wikitext_from_url
from src.translate.gemini_client import translate_wikitext_chunked
from src.config_loader import load_config, save_config
from src.check.ai_check import check_with_ai
from src.languages import LANGUAGES, get_lang_code_from_name


def run_app():
    """Khởi chạy ứng dụng GUI."""
    lang = choose_language()
    set_lang(lang)
    root = tk.Tk()
    root.title(t("app_title"))
    root.minsize(800, 600)
    w, h = 800, 600
    root.geometry(f"{w}x{h}")
    root.update_idletasks()
    x = (root.winfo_screenwidth() - w) // 2
    y = (root.winfo_screenheight() - h) // 2
    root.geometry(f"{w}x{h}+{x}+{y}")

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
    source_lang_combo = None
    target_lang_combo = None
    status_var = None
    task_running = False
    last_normalized_wikitext = None
    translate_after_id = None  # id của root.after(30s) nhắc "vẫn đang xử lý"

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
            status_var.set(t("status_busy") if busy else t("status_ready"))

    def on_fetch_done(success: bool, data: str):
        set_buttons_busy(False)
        if success:
            wikitext_en_widget.delete("1.0", tk.END)
            wikitext_en_widget.insert(tk.END, data)
            frames.log_append(log_widget, t("log_fetched"))
        else:
            frames.log_append(log_widget, t("log_error", data=data))
            show_error(root, t("dialog_error"), data)

    def do_fetch():
        url = link_entry.get().strip()
        if url == t("url_placeholder"):
            url = ""
        if not url:
            frames.log_append(log_widget, t("log_no_url"))
            return
        if task_running:
            return
        set_buttons_busy(True)
        if status_var:
            status_var.set(t("status_fetching"))
        frames.log_append(log_widget, t("log_fetching"))

        def task():
            return fetch_wikitext_from_url(url)

        run_background(root, task, on_fetch_done)

    def on_translate_done(success: bool, data: str):
        nonlocal translate_after_id
        if translate_after_id:
            root.after_cancel(translate_after_id)
            translate_after_id = None
        try:
            root.config(cursor="")
        except tk.TclError:
            pass
        set_buttons_busy(False)
        if success:
            wikitext_vi_widget.delete("1.0", tk.END)
            wikitext_vi_widget.insert(tk.END, data)
            frames.log_append(log_widget, t("log_translated"))
        else:
            frames.log_append(log_widget, t("log_translate_error", data=data))
            msg = data
            if "429" in msg or "quota" in msg.lower():
                msg = msg + "\n\n" + t("error_429_hint")
            show_error(root, t("dialog_translate_error"), msg)

    def do_translate():
        wikitext_en = wikitext_en_widget.get("1.0", tk.END).strip()
        if not wikitext_en:
            frames.log_append(log_widget, t("log_no_wikitext_en"))
            return
        api_key = api_key_entry.get().strip()
        if api_key == t("api_key_placeholder"):
            api_key = ""
        model = (model_combo.get() or "gemini-3-flash-preview").strip()
        if not api_key:
            frames.log_append(log_widget, t("log_no_api_key"))
            show_error(root, t("dialog_config"), t("config_enter_api_key"))
            return
        if task_running:
            return
        nonlocal translate_after_id
        set_buttons_busy(True)
        if status_var:
            status_var.set(t("status_translating"))
        frames.log_append(log_widget, t("log_translating"))
        try:
            root.config(cursor="wait")
        except tk.TclError:
            pass
        def _on_still_translating():
            if task_running:
                frames.log_append(log_widget, t("log_still_translating"))
        translate_after_id = root.after(30000, _on_still_translating)
        source_name = source_lang_combo.get().strip() if source_lang_combo else "English"
        target_name = target_lang_combo.get().strip() if target_lang_combo else "Vietnamese"
        source_code = get_lang_code_from_name(source_name) or "en"
        target_code = get_lang_code_from_name(target_name) or "vi"
        save_config(api_key=api_key, model=model, source_lang=source_code, target_lang=target_code)

        def task():
            return translate_wikitext_chunked(
                wikitext_en,
                api_key=api_key,
                model=model,
                source_lang=source_name,
                target_lang=target_name,
            )

        run_background(root, task, on_translate_done)

    def do_apply_normalize():
        nonlocal last_normalized_wikitext
        if last_normalized_wikitext is not None:
            wikitext_vi_widget.delete("1.0", tk.END)
            wikitext_vi_widget.insert(tk.END, last_normalized_wikitext)
            frames.log_append(log_widget, t("log_apply_normalize"))

    def do_copy():
        """Copy nội dung Wikitext VI vào clipboard (Phase 7)."""
        text = wikitext_vi_widget.get("1.0", tk.END)
        if not text.strip():
            frames.log_append(log_widget, t("log_vi_empty"))
            return
        root.clipboard_clear()
        root.clipboard_append(text)
        root.update()
        frames.log_append(log_widget, t("log_copied"))

    def do_save():
        """Lưu Wikitext VI ra file .wiki hoặc .txt (Phase 7)."""
        text = wikitext_vi_widget.get("1.0", tk.END)
        if not text.strip():
            frames.log_append(log_widget, t("log_vi_empty"))
            return
        path = filedialog.asksaveasfilename(
            defaultextension=".wiki",
            filetypes=[("Wikitext", "*.wiki"), ("Text", "*.txt"), ("All", "*.*")],
            title=t("save_wikitext_vi"),
        )
        if not path:
            return
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(text)
            frames.log_append(log_widget, t("log_saved", path=path))
        except Exception as e:
            frames.log_append(log_widget, t("log_save_error", e=str(e)))
            show_error(root, t("dialog_error"), str(e))

    def on_check_done(success: bool, data):
        nonlocal last_normalized_wikitext
        set_buttons_busy(False)
        if success and isinstance(data, dict):
            lines = data.get("lines", [])
            last_normalized_wikitext = data.get("normalized_wikitext")
            frames.set_check_result(check_result_widget, lines)
            if apply_normalize_btn:
                apply_normalize_btn.configure(state=tk.NORMAL if last_normalized_wikitext else tk.DISABLED)
            frames.log_append(log_widget, t("log_check_done"))
        else:
            last_normalized_wikitext = None
            if apply_normalize_btn:
                apply_normalize_btn.configure(state=tk.DISABLED)
            frames.set_check_result(check_result_widget, [t("dialog_error") + ": " + str(data)])
            frames.log_append(log_widget, t("log_check_error", data=str(data)))

    def do_check():
        wikitext_vi = wikitext_vi_widget.get("1.0", tk.END).strip()
        wikitext_en = wikitext_en_widget.get("1.0", tk.END).strip()
        wikitext = wikitext_vi or wikitext_en
        if not wikitext:
            frames.log_append(log_widget, t("log_no_wikitext"))
            frames.set_check_result(check_result_widget, [t("no_wikitext_to_check")])
            return
        api_key = api_key_entry.get().strip()
        if api_key == t("api_key_placeholder"):
            api_key = ""
        if not api_key:
            frames.log_append(log_widget, t("log_check_need_api_key"))
            show_error(root, t("dialog_config"), t("config_check_need_api_key"))
            return
        if task_running:
            return
        model = (model_combo.get() or "gemini-3-flash-preview").strip()
        source_name = source_lang_combo.get().strip() if source_lang_combo else "English"
        target_name = target_lang_combo.get().strip() if target_lang_combo else "Vietnamese"
        set_buttons_busy(True)
        if status_var:
            status_var.set(t("status_checking"))
        frames.log_append(log_widget, t("log_checking"))

        def task():
            wikitext_target = wikitext_vi if wikitext_vi else wikitext_en
            wikitext_source = wikitext_en if (wikitext_en and wikitext_vi) else None
            # Khi chỉ có một ô có nội dung, coi ngôn ngữ đích = nguồn để nhãn báo cáo đúng
            tgt_name = target_name if wikitext_vi else source_name
            lines = check_with_ai(
                wikitext_target,
                api_key=api_key,
                model=model,
                source_lang_name=source_name,
                target_lang_name=tgt_name,
                wikitext_source=wikitext_source,
            )
            return {"lines": lines, "normalized_wikitext": None}

        run_background(root, task, on_check_done)

    # --- Menu (Phase 7) — đặt trước để luôn ở trên
    menubar = tk.Menu(root)
    root.config(menu=menubar)
    file_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label=t("menu_file"), menu=file_menu)
    file_menu.add_command(label=t("menu_save_wikitext"), command=do_save)
    file_menu.add_separator()
    file_menu.add_command(label=t("menu_exit"), command=root.quit)
    help_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label=t("menu_help"), menu=help_menu)
    help_menu.add_command(
        label=t("menu_intro"),
        command=lambda: show_info(root, t("dialog_intro"), t("intro_text")),
    )
    help_menu.add_command(
        label=t("menu_guide"),
        command=lambda: show_info(root, t("dialog_guide"), t("guide_text")),
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

    def _on_mousewheel_linux_up(_event):
        canvas.yview_scroll(-3, tk.UNITS)

    def _on_mousewheel_linux_down(_event):
        canvas.yview_scroll(3, tk.UNITS)

    def _bind_scroll(widget):
        widget.bind("<MouseWheel>", _on_mousewheel)
        widget.bind("<Button-4>", _on_mousewheel_linux_up)
        widget.bind("<Button-5>", _on_mousewheel_linux_down)

    content_frame.bind("<Configure>", _on_frame_configure)
    canvas.bind("<Configure>", _on_canvas_configure)
    _bind_scroll(canvas)
    _bind_scroll(content_frame)

    # --- Link + cặp ngôn ngữ + nút Lấy wikitext, Dịch, Kiểm tra (Phase 5)
    _, link_entry, fetch_btn, translate_btn, check_btn, source_lang_combo, target_lang_combo = (
        frames.build_link_frame(content_frame, do_fetch, do_translate, do_check)
    )
    add_tooltip(fetch_btn, t("tooltip_fetch"))
    add_tooltip(translate_btn, t("tooltip_translate"))
    add_tooltip(check_btn, t("tooltip_check"))

    # --- Cấu hình Gemini (API key load từ config/config.json)
    _, api_key_entry, model_combo = frames.build_config_frame(content_frame)
    cfg = load_config()
    # Khôi phục lựa chọn ngôn ngữ nguồn/đích từ config (mặc định en → vi)
    src_cfg = (cfg.get("source_lang") or "en").strip().lower()
    tgt_cfg = (cfg.get("target_lang") or "vi").strip().lower()
    for i, (code, _) in enumerate(LANGUAGES):
        if code == src_cfg:
            source_lang_combo.current(i)
            break
    for i, (code, _) in enumerate(LANGUAGES):
        if code == tgt_cfg:
            target_lang_combo.current(i)
            break
    if cfg.get("api_key"):
        api_key_entry.delete(0, tk.END)
        api_key_entry.insert(0, cfg["api_key"])
        api_key_entry.config(fg="black", show="*")
    if cfg.get("model"):
        try:
            model_combo.set(cfg["model"])
        except tk.TclError:
            pass

    # --- Log
    _, log_widget = frames.build_log_frame(content_frame)
    frames.log_append(log_widget, t("log_startup"))

    # --- Wikitext EN
    _, wikitext_en_widget = frames.build_wikitext_en_frame(content_frame)

    # --- Wikitext VI
    _, wikitext_vi_widget = frames.build_wikitext_vi_frame(content_frame)

    # --- Xuất Wikitext VI: Copy, Lưu file (Phase 7)
    _, copy_btn, save_btn = frames.build_export_frame(content_frame, do_copy, do_save)
    add_tooltip(copy_btn, t("tooltip_copy"))
    add_tooltip(save_btn, t("tooltip_save"))

    # --- Kết quả kiểm tra + nút Áp dụng chuẩn hóa (Phase 5–6)
    _, check_result_widget, apply_normalize_btn = frames.build_check_result_frame(content_frame, do_apply_normalize)

    # --- Thanh trạng thái (Phase 4) — luôn ở dưới cùng
    _, status_var = frames.build_status_bar(root)
    apply_normalize_btn.configure(state=tk.DISABLED)
    frames.set_check_result(check_result_widget, [])

    def _bind_scroll_recursive(widget):
        _bind_scroll(widget)
        for child in widget.winfo_children():
            _bind_scroll_recursive(child)

    _bind_scroll_recursive(content_frame)

    root.mainloop()


if __name__ == "__main__":
    run_app()
