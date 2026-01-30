"""
Danh sách ngôn ngữ hỗ trợ dịch Wikipedia (mã + tên hiển thị).
Mặc định: nguồn English (en), đích Vietnamese (vi).
"""
# (code, display_name) — tên dùng trong dropdown và trong prompt Gemini
LANGUAGES = [
    ("en", "English"),
    ("vi", "Vietnamese"),
    ("zh", "中文"),
    ("fr", "Français"),
    ("de", "Deutsch"),
    ("ja", "日本語"),
    ("ko", "한국어"),
    ("es", "Español"),
    ("ru", "Русский"),
    ("th", "ไทย"),
    ("it", "Italiano"),
    ("pt", "Português"),
    ("ar", "العربية"),
    ("id", "Bahasa Indonesia"),
]

DEFAULT_SOURCE = "en"
DEFAULT_TARGET = "vi"


def get_lang_name(code: str) -> str:
    """Trả về tên hiển thị của ngôn ngữ theo mã. Nếu không có thì trả về code."""
    code = (code or "").strip().lower()
    for c, name in LANGUAGES:
        if c == code:
            return name
    return code or "?"


def get_lang_code_from_name(display_name: str) -> str | None:
    """Trả về mã ngôn ngữ theo tên hiển thị. Không khớp thì trả về None."""
    display_name = (display_name or "").strip()
    for code, name in LANGUAGES:
        if name == display_name:
            return code
    return None


def lang_display_names() -> list[str]:
    """Danh sách tên hiển thị (để đưa vào Combobox)."""
    return [name for _, name in LANGUAGES]
