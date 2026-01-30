"""Đa ngôn ngữ: English / Tiếng Việt. Gọi set_lang() sau khi chọn, dùng t(key) để lấy chuỗi."""

STRINGS = {
    "en": {
        "app_title": "Translate Wikipedia",
        "lang_select_title": "Choose language",
        "lang_select_prompt": "Select interface language:",
        "lang_english": "English",
        "lang_vietnamese": "Tiếng Việt",
        # Link frame
        "link_frame_title": "Language pair & Wikipedia link",
        "source_lang_label": "From:",
        "target_lang_label": "To:",
        "url_label": "URL:",
        "url_placeholder": "https://en.wikipedia.org/wiki/...",
        "btn_fetch": "Fetch wikitext",
        "btn_translate": "Translate",
        "btn_check": "Check & Normalize",
        # Config
        "config_frame_title": "Gemini configuration",
        "api_key_label": "API key:",
        "api_key_placeholder": "Enter Gemini API key...",
        "model_label": "Model:",
        # Status
        "status_label": "Status:",
        "status_ready": "Ready",
        "status_busy": "Processing...",
        "status_fetching": "Fetching wikitext...",
        "status_translating": "Translating...",
        "status_checking": "Checking & normalizing...",
        # Log frame
        "log_frame_title": "Log",
        # Wikitext
        "wikitext_en_title": "Wikitext (source)",
        "wikitext_vi_title": "Wikitext (target)",
        # Export
        "export_frame_title": "Export Wikitext (target)",
        "btn_copy": "Copy target wikitext",
        "btn_save": "Save to file...",
        # Check result
        "check_result_title": "Check result",
        "btn_apply_normalize": "Apply normalization to target wikitext",
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
        "save_wikitext_vi": "Save target wikitext",
        # About text
        "about_text": (
            "Translate Wikipedia\n\n"
            "Choose source and target languages, fetch any Wikipedia article,\n"
            "translate via Gemini API, check layout, normalize, and export wikitext.\n\n"
            "See docs/ke-hoach.md and docs/nghien-cuu.md."
        ),
        # Log messages
        "log_fetched": "[Log] Wikitext fetched.",
        "log_error": "[Log] Error: {data}",
        "log_no_url": "[Log] No URL entered.",
        "log_fetching": "[Log] Fetching wikitext...",
        "log_translated": "[Log] Translation done.",
        "log_translate_error": "[Log] Translation error: {data}",
        "log_no_wikitext_en": "[Log] No source wikitext. Click 'Fetch wikitext' first.",
        "log_no_api_key": "[Log] No Gemini API key entered.",
        "log_translating": "[Log] Translating...",
        "log_apply_normalize": "[Log] Normalization applied to target wikitext.",
        "log_vi_empty": "[Log] Target wikitext box is empty.",
        "log_copied": "[Log] Target wikitext copied to clipboard.",
        "log_saved": "[Log] Saved to: {path}",
        "log_save_error": "[Log] Save error: {e}",
        "log_check_done": "[Log] Check (layout + content + normalize) done.",
        "log_check_error": "[Log] Check error: {data}",
        "log_no_wikitext": "[Log] No wikitext. Fetch or translate first.",
        "log_checking": "[Log] Checking & normalizing...",
        "log_startup": "[Log] App started. Enter link, API key (if needed), then Fetch / Translate / Check.",
        # Tooltips
        "tooltip_fetch": "Fetch wikitext from the Wikipedia URL (any language).",
        "tooltip_translate": "Translate wikitext from source to target language via Gemini API.",
        "tooltip_check": "Check layout, compare source/target, normalize terminology.",
        "tooltip_copy": "Copy entire target wikitext to clipboard.",
        "tooltip_save": "Save target wikitext to .wiki or .txt file.",
        # Check task labels (in do_check)
        "check_section_layout": "--- Layout ---",
        "check_section_content": "--- Content (source vs target) ---",
        "check_section_normalize": "--- Normalize ---",
    },
    "vi": {
        "app_title": "Dịch Wikipedia",
        "lang_select_title": "Chọn ngôn ngữ",
        "lang_select_prompt": "Chọn ngôn ngữ giao diện:",
        "lang_english": "English",
        "lang_vietnamese": "Tiếng Việt",
        # Link frame
        "link_frame_title": "Cặp ngôn ngữ & link Wikipedia",
        "source_lang_label": "Từ:",
        "target_lang_label": "Sang:",
        "url_label": "URL:",
        "url_placeholder": "https://en.wikipedia.org/wiki/...",
        "btn_fetch": "Lấy wikitext",
        "btn_translate": "Dịch",
        "btn_check": "Kiểm tra & Chuẩn hóa",
        # Config
        "config_frame_title": "Cấu hình Gemini",
        "api_key_label": "API key:",
        "api_key_placeholder": "Nhập API key Gemini...",
        "model_label": "Model:",
        # Status
        "status_label": "Trạng thái:",
        "status_ready": "Sẵn sàng",
        "status_busy": "Đang xử lý...",
        "status_fetching": "Đang lấy wikitext...",
        "status_translating": "Đang dịch...",
        "status_checking": "Đang kiểm tra & chuẩn hóa...",
        # Log frame
        "log_frame_title": "Log",
        # Wikitext
        "wikitext_en_title": "Wikitext (nguồn)",
        "wikitext_vi_title": "Wikitext (đích)",
        # Export
        "export_frame_title": "Xuất Wikitext (đích)",
        "btn_copy": "Copy wikitext đích",
        "btn_save": "Lưu ra file...",
        # Check result
        "check_result_title": "Kết quả kiểm tra",
        "btn_apply_normalize": "Áp dụng chuẩn hóa lên wikitext đích",
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
        "save_wikitext_vi": "Lưu wikitext đích",
        # About text
        "about_text": (
            "Dịch Wikipedia\n\n"
            "Chọn ngôn ngữ nguồn và đích, lấy bài Wikipedia bất kỳ,\n"
            "dịch qua Gemini API, kiểm tra bố cục, chuẩn hóa, xuất wikitext.\n\n"
            "Xem docs/ke-hoach.md và docs/nghien-cuu.md."
        ),
        # Log messages
        "log_fetched": "[Log] Đã lấy wikitext xong.",
        "log_error": "[Log] Lỗi: {data}",
        "log_no_url": "[Log] Chưa nhập URL.",
        "log_fetching": "[Log] Đang lấy wikitext...",
        "log_translated": "[Log] Đã dịch xong.",
        "log_translate_error": "[Log] Lỗi dịch: {data}",
        "log_no_wikitext_en": "[Log] Chưa có wikitext nguồn. Hãy bấm 'Lấy wikitext' trước.",
        "log_no_api_key": "[Log] Chưa nhập API key Gemini.",
        "log_translating": "[Log] Đang dịch...",
        "log_apply_normalize": "[Log] Đã áp dụng chuẩn hóa lên wikitext đích.",
        "log_vi_empty": "[Log] Ô wikitext đích trống.",
        "log_copied": "[Log] Đã copy wikitext đích vào clipboard.",
        "log_saved": "[Log] Đã lưu vào: {path}",
        "log_save_error": "[Log] Lỗi lưu file: {e}",
        "log_check_done": "[Log] Đã chạy kiểm tra (bố cục + nội dung + chuẩn hóa).",
        "log_check_error": "[Log] Lỗi kiểm tra: {data}",
        "log_no_wikitext": "[Log] Chưa có wikitext. Hãy Lấy wikitext hoặc Dịch trước.",
        "log_checking": "[Log] Đang kiểm tra & chuẩn hóa...",
        "log_startup": "[Log] Ứng dụng đã khởi động. Nhập link, API key (nếu cần), rồi Lấy wikitext / Dịch / Kiểm tra.",
        # Tooltips
        "tooltip_fetch": "Lấy wikitext từ link Wikipedia (mọi ngôn ngữ).",
        "tooltip_translate": "Dịch wikitext từ ngôn ngữ nguồn sang đích qua Gemini API.",
        "tooltip_check": "Kiểm tra bố cục, so sánh nguồn/đích, chuẩn hóa thuật ngữ.",
        "tooltip_copy": "Copy toàn bộ wikitext đích vào clipboard.",
        "tooltip_save": "Lưu wikitext đích ra file .wiki hoặc .txt.",
        # Check task labels
        "check_section_layout": "--- Bố cục ---",
        "check_section_content": "--- Nội dung (nguồn vs đích) ---",
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
