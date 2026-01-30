"""Đa ngôn ngữ: English / Tiếng Việt. Gọi set_lang() sau khi chọn, dùng t(key) để lấy chuỗi."""

STRINGS = {
    "en": {
        "app_title": "Translate Wikipedia EN → VI",
        "lang_select_title": "Choose language",
        "lang_select_prompt": "Select interface language:",
        "lang_english": "English",
        "lang_vietnamese": "Tiếng Việt",
        # Link frame
        "link_frame_title": "English Wikipedia link",
        "url_label": "URL:",
        "btn_fetch": "Fetch wikitext",
        "btn_translate": "Translate to Vietnamese",
        "btn_check": "Check & Normalize",
        # Config
        "config_frame_title": "Gemini configuration",
        "api_key_label": "API key:",
        "model_label": "Model:",
        # Status
        "status_label": "Status:",
        "status_ready": "Ready",
        "status_busy": "Processing...",
        "status_fetching": "Fetching wikitext...",
        "status_translating": "Translating to Vietnamese...",
        "status_checking": "Checking & normalizing...",
        # Log frame
        "log_frame_title": "Log",
        # Wikitext
        "wikitext_en_title": "Wikitext EN",
        "wikitext_vi_title": "Wikitext VI",
        # Export
        "export_frame_title": "Export Wikitext VI",
        "btn_copy": "Copy wikitext VI",
        "btn_save": "Save to file...",
        # Check result
        "check_result_title": "Check result",
        "btn_apply_normalize": "Apply normalization to Wikitext VI",
        "check_not_run": "(Check not run yet.)",
        "no_wikitext_to_check": "No wikitext to check.",
        # Menu
        "menu_file": "File",
        "menu_save_wikitext": "Save Wikitext VI...",
        "menu_exit": "Exit",
        "menu_help": "Help",
        "menu_about": "About",
        # Dialogs
        "dialog_error": "Error",
        "dialog_translate_error": "Translation error",
        "dialog_config": "Configuration",
        "dialog_about": "About",
        "config_enter_api_key": "Please enter Gemini API key in the Gemini configuration section.",
        "save_wikitext_vi": "Save Wikitext VI",
        # About text
        "about_text": (
            "Translate Wikipedia EN → VI\n\n"
            "Fetch an English Wikipedia article, translate to Vietnamese via Gemini API,\n"
            "check layout, normalize terminology, and export wikitext source.\n\n"
            "See docs/ke-hoach.md and docs/nghien-cuu.md."
        ),
        # Log messages
        "log_fetched": "[Log] Wikitext fetched.",
        "log_error": "[Log] Error: {data}",
        "log_no_url": "[Log] No URL entered.",
        "log_fetching": "[Log] Fetching wikitext...",
        "log_translated": "[Log] Translation done.",
        "log_translate_error": "[Log] Translation error: {data}",
        "log_no_wikitext_en": "[Log] No EN wikitext. Click 'Fetch wikitext' first.",
        "log_no_api_key": "[Log] No Gemini API key entered.",
        "log_translating": "[Log] Translating to Vietnamese...",
        "log_apply_normalize": "[Log] Normalization applied to Wikitext VI.",
        "log_vi_empty": "[Log] Wikitext VI box is empty.",
        "log_copied": "[Log] Wikitext VI copied to clipboard.",
        "log_saved": "[Log] Saved to: {path}",
        "log_save_error": "[Log] Save error: {e}",
        "log_check_done": "[Log] Check (layout + content + normalize) done.",
        "log_check_error": "[Log] Check error: {data}",
        "log_no_wikitext": "[Log] No wikitext (EN or VI). Fetch or translate first.",
        "log_checking": "[Log] Checking & normalizing...",
        "log_startup": "[Log] App started. Enter link, API key (if needed), then Fetch / Translate / Check.",
        # Tooltips
        "tooltip_fetch": "Fetch wikitext source from English Wikipedia link.",
        "tooltip_translate": "Translate wikitext EN → VI via Gemini API (preserve wikitext syntax).",
        "tooltip_check": "Check layout, compare EN/VI, normalize terminology.",
        "tooltip_copy": "Copy entire Wikitext VI content to clipboard.",
        "tooltip_save": "Save Wikitext VI to .wiki or .txt file.",
        # Check task labels (in do_check)
        "check_section_layout": "--- Layout ---",
        "check_section_content": "--- Content (EN vs VI) ---",
        "check_section_normalize": "--- Normalize ---",
    },
    "vi": {
        "app_title": "Dịch Wikipedia EN → VI",
        "lang_select_title": "Chọn ngôn ngữ",
        "lang_select_prompt": "Chọn ngôn ngữ giao diện:",
        "lang_english": "English",
        "lang_vietnamese": "Tiếng Việt",
        # Link frame
        "link_frame_title": "Link Wikipedia tiếng Anh",
        "url_label": "URL:",
        "btn_fetch": "Lấy wikitext",
        "btn_translate": "Dịch sang tiếng Việt",
        "btn_check": "Kiểm tra & Chuẩn hóa",
        # Config
        "config_frame_title": "Cấu hình Gemini",
        "api_key_label": "API key:",
        "model_label": "Model:",
        # Status
        "status_label": "Trạng thái:",
        "status_ready": "Sẵn sàng",
        "status_busy": "Đang xử lý...",
        "status_fetching": "Đang lấy wikitext...",
        "status_translating": "Đang dịch sang tiếng Việt...",
        "status_checking": "Đang kiểm tra & chuẩn hóa...",
        # Log frame
        "log_frame_title": "Log",
        # Wikitext
        "wikitext_en_title": "Wikitext EN",
        "wikitext_vi_title": "Wikitext VI",
        # Export
        "export_frame_title": "Xuất Wikitext VI",
        "btn_copy": "Copy wikitext VI",
        "btn_save": "Lưu ra file...",
        # Check result
        "check_result_title": "Kết quả kiểm tra",
        "btn_apply_normalize": "Áp dụng chuẩn hóa lên Wikitext VI",
        "check_not_run": "(Chưa chạy kiểm tra.)",
        "no_wikitext_to_check": "Chưa có wikitext để kiểm tra.",
        # Menu
        "menu_file": "File",
        "menu_save_wikitext": "Lưu Wikitext VI...",
        "menu_exit": "Thoát",
        "menu_help": "Help",
        "menu_about": "Giới thiệu",
        # Dialogs
        "dialog_error": "Lỗi",
        "dialog_translate_error": "Lỗi dịch",
        "dialog_config": "Cấu hình",
        "dialog_about": "Giới thiệu",
        "config_enter_api_key": "Vui lòng nhập API key Gemini trong ô Cấu hình Gemini.",
        "save_wikitext_vi": "Lưu Wikitext VI",
        # About text
        "about_text": (
            "Dịch Wikipedia EN → VI\n\n"
            "Lấy bài Wikipedia tiếng Anh, dịch sang tiếng Việt qua Gemini API,\n"
            "kiểm tra bố cục, chuẩn hóa thuật ngữ, xuất mã nguồn wikitext.\n\n"
            "Xem docs/ke-hoach.md và docs/nghien-cuu.md."
        ),
        # Log messages
        "log_fetched": "[Log] Đã lấy wikitext xong.",
        "log_error": "[Log] Lỗi: {data}",
        "log_no_url": "[Log] Chưa nhập URL.",
        "log_fetching": "[Log] Đang lấy wikitext...",
        "log_translated": "[Log] Đã dịch xong.",
        "log_translate_error": "[Log] Lỗi dịch: {data}",
        "log_no_wikitext_en": "[Log] Chưa có wikitext EN. Hãy bấm 'Lấy wikitext' trước.",
        "log_no_api_key": "[Log] Chưa nhập API key Gemini.",
        "log_translating": "[Log] Đang dịch sang tiếng Việt...",
        "log_apply_normalize": "[Log] Đã áp dụng chuẩn hóa lên Wikitext VI.",
        "log_vi_empty": "[Log] Ô Wikitext VI trống.",
        "log_copied": "[Log] Đã copy wikitext VI vào clipboard.",
        "log_saved": "[Log] Đã lưu vào: {path}",
        "log_save_error": "[Log] Lỗi lưu file: {e}",
        "log_check_done": "[Log] Đã chạy kiểm tra (bố cục + nội dung + chuẩn hóa).",
        "log_check_error": "[Log] Lỗi kiểm tra: {data}",
        "log_no_wikitext": "[Log] Chưa có wikitext (EN hoặc VI). Hãy Lấy wikitext hoặc Dịch trước.",
        "log_checking": "[Log] Đang kiểm tra & chuẩn hóa...",
        "log_startup": "[Log] Ứng dụng đã khởi động. Nhập link, API key (nếu cần), rồi Lấy wikitext / Dịch / Kiểm tra.",
        # Tooltips
        "tooltip_fetch": "Lấy mã nguồn wikitext từ link Wikipedia tiếng Anh.",
        "tooltip_translate": "Dịch wikitext EN → VI qua Gemini API (giữ cú pháp wikitext).",
        "tooltip_check": "Kiểm tra bố cục, so sánh EN/VI, chuẩn hóa thuật ngữ.",
        "tooltip_copy": "Copy toàn bộ nội dung ô Wikitext VI vào clipboard.",
        "tooltip_save": "Lưu Wikitext VI ra file .wiki hoặc .txt.",
        # Check task labels
        "check_section_layout": "--- Bố cục ---",
        "check_section_content": "--- Nội dung (EN vs VI) ---",
        "check_section_normalize": "--- Chuẩn hóa ---",
    },
}

_current_lang = "vi"


def set_lang(lang: str):
    """Đặt ngôn ngữ hiển thị: 'en' hoặc 'vi'."""
    global _current_lang
    if lang in STRINGS:
        _current_lang = lang


def get_lang() -> str:
    """Trả về mã ngôn ngữ hiện tại."""
    return _current_lang


def t(key: str, **kwargs) -> str:
    """Lấy chuỗi theo key; nếu có kwargs thì format chuỗi (vd: t('log_error', data='...'))."""
    s = STRINGS.get(_current_lang, STRINGS["vi"]).get(key, key)
    if kwargs:
        try:
            return s.format(**kwargs)
        except KeyError:
            return s
    return s
