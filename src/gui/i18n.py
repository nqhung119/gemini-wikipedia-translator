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
        "status_translating": "Translating... (may take a few minutes)",
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
        "menu_save_wikitext": "Save target wikitext...",
        "menu_exit": "Exit",
        "menu_help": "Help",
        "menu_intro": "Introduction",
        "menu_guide": "User guide",
        # Dialogs
        "dialog_error": "Error",
        "dialog_translate_error": "Translation error",
        "error_429_hint": (
            "Hint: Free tier quota is per model. "
            "Try selecting 'gemini-3-flash-preview' instead of 'gemini-3-pro-preview', or retry in a minute."
        ),
        "dialog_config": "Configuration",
        "dialog_intro": "Introduction",
        "dialog_guide": "User guide",
        "config_enter_api_key": "Please enter Gemini API key in the Gemini configuration section.",
        "config_check_need_api_key": "Check uses AI (Gemini). Please enter Gemini API key to run check.",
        "save_wikitext_vi": "Save target wikitext",
        # Introduction
        "intro_text": (
            "Translate Wikipedia\n\n"
            "Application to translate Wikipedia articles between languages. "
            "Choose source and target languages (default: English → Vietnamese), "
            "paste a Wikipedia article URL, fetch wikitext, translate via Gemini API, "
            "then check layout, normalize terminology, and export the result."
        ),
        # User guide
        "guide_text": (
            "User guide:\n\n"
            "1. From / To: Select source and target languages (e.g. English → Vietnamese).\n\n"
            "2. URL: Paste a Wikipedia article link (any language, e.g. https://en.wikipedia.org/wiki/...).\n\n"
            "3. Fetch wikitext: Click to download the article source (wikitext).\n\n"
            "4. API key: Enter your Gemini API key in the configuration section (saved in config/config.json).\n\n"
            "5. Translate: Click to translate the source wikitext to the target language.\n\n"
            "6. Check & Normalize: Check layout (links, templates, refs), compare source/target, normalize terms. Optionally apply normalization to the target box.\n\n"
            "7. Export: Copy target wikitext to clipboard or save to .wiki / .txt file (File → Save)."
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
        "log_translating": "[Log] Sent to Gemini API. Please wait (long articles may take several minutes)...",
        "log_still_translating": "[Log] Still processing, please wait...",
        "log_apply_normalize": "[Log] Normalization applied to target wikitext.",
        "log_vi_empty": "[Log] Target wikitext box is empty.",
        "log_copied": "[Log] Target wikitext copied to clipboard.",
        "log_saved": "[Log] Saved to: {path}",
        "log_save_error": "[Log] Save error: {e}",
        "log_check_done": "[Log] AI check done.",
        "log_check_error": "[Log] Check error: {data}",
        "log_check_need_api_key": "[Log] API key required for AI check.",
        "log_no_wikitext": "[Log] No wikitext. Fetch or translate first.",
        "log_checking": "[Log] Running AI check (Gemini)...",
        "log_startup": "[Log] App started. Enter link, API key (if needed), then Fetch / Translate / Check.",
        # Tooltips
        "tooltip_fetch": "Fetch wikitext from the Wikipedia URL (any language).",
        "tooltip_translate": "Translate wikitext from source to target language via Gemini API.",
        "tooltip_check": "Run AI check (layout, content, terminology, links) via Gemini.",
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
        "status_translating": "Đang dịch... (có thể vài phút)",
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
        "menu_save_wikitext": "Lưu wikitext đích...",
        "menu_exit": "Thoát",
        "menu_help": "Help",
        "menu_intro": "Giới thiệu",
        "menu_guide": "Hướng dẫn dùng",
        # Dialogs
        "dialog_error": "Lỗi",
        "dialog_translate_error": "Lỗi dịch",
        "error_429_hint": (
            "Gợi ý: Hạn mức (quota) free tier tính theo từng model. "
            "Thử chọn model 'gemini-3-flash-preview' thay vì 'gemini-3-pro-preview', hoặc thử lại sau vài chục giây."
        ),
        "dialog_config": "Cấu hình",
        "dialog_intro": "Giới thiệu",
        "dialog_guide": "Hướng dẫn dùng",
        "config_enter_api_key": "Vui lòng nhập API key Gemini trong ô Cấu hình Gemini.",
        "config_check_need_api_key": "Kiểm tra dùng AI (Gemini). Vui lòng nhập API key Gemini để chạy kiểm tra.",
        "save_wikitext_vi": "Lưu wikitext đích",
        # Giới thiệu
        "intro_text": (
            "Dịch Wikipedia\n\n"
            "Ứng dụng dịch bài viết Wikipedia giữa các ngôn ngữ. "
            "Chọn ngôn ngữ nguồn và đích (mặc định: Tiếng Anh → Tiếng Việt), "
            "dán link bài Wikipedia, lấy wikitext, dịch qua Gemini API, "
            "sau đó kiểm tra bố cục, chuẩn hóa thuật ngữ và xuất kết quả."
        ),
        # Hướng dẫn dùng
        "guide_text": (
            "Hướng dẫn dùng:\n\n"
            "1. Từ / Sang: Chọn ngôn ngữ nguồn và đích (vd. English → Vietnamese).\n\n"
            "2. URL: Dán link bài viết Wikipedia (bất kỳ ngôn ngữ, vd. https://en.wikipedia.org/wiki/...).\n\n"
            "3. Lấy wikitext: Bấm để tải mã nguồn bài viết (wikitext).\n\n"
            "4. API key: Nhập API key Gemini vào ô Cấu hình Gemini (được lưu trong config/config.json).\n\n"
            "5. Dịch: Bấm để dịch wikitext nguồn sang ngôn ngữ đích.\n\n"
            "6. Kiểm tra & Chuẩn hóa: Kiểm tra bố cục (link, template, ref), so sánh nguồn/đích, chuẩn hóa thuật ngữ. Có thể bấm Áp dụng chuẩn hóa lên ô đích.\n\n"
            "7. Xuất: Copy wikitext đích vào clipboard hoặc Lưu ra file .wiki / .txt (File → Lưu Wikitext...)."
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
        "log_translating": "[Log] Đã gửi lên Gemini API. Vui lòng đợi (bài dài có thể mất vài phút)...",
        "log_still_translating": "[Log] Vẫn đang xử lý, vui lòng đợi thêm...",
        "log_apply_normalize": "[Log] Đã áp dụng chuẩn hóa lên wikitext đích.",
        "log_vi_empty": "[Log] Ô wikitext đích trống.",
        "log_copied": "[Log] Đã copy wikitext đích vào clipboard.",
        "log_saved": "[Log] Đã lưu vào: {path}",
        "log_save_error": "[Log] Lỗi lưu file: {e}",
        "log_check_done": "[Log] Đã chạy kiểm tra bằng AI xong.",
        "log_check_error": "[Log] Lỗi kiểm tra: {data}",
        "log_check_need_api_key": "[Log] Cần API key để chạy kiểm tra bằng AI.",
        "log_no_wikitext": "[Log] Chưa có wikitext. Hãy Lấy wikitext hoặc Dịch trước.",
        "log_checking": "[Log] Đang chạy kiểm tra bằng AI (Gemini)...",
        "log_startup": "[Log] Ứng dụng đã khởi động. Nhập link, API key (nếu cần), rồi Lấy wikitext / Dịch / Kiểm tra.",
        # Tooltips
        "tooltip_fetch": "Lấy wikitext từ link Wikipedia (mọi ngôn ngữ).",
        "tooltip_translate": "Dịch wikitext từ ngôn ngữ nguồn sang đích qua Gemini API.",
        "tooltip_check": "Chạy kiểm tra bằng AI (bố cục, nội dung, thuật ngữ, link) qua Gemini.",
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
