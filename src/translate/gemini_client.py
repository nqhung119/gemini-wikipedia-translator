"""
Dịch wikitext EN → VI bằng Gemini API, giữ cấu trúc wikitext.
Tham chiếu: docs/nghien-cuu.md § 4.
"""
import google.generativeai as genai

from src.translate.chunker import chunk_wikitext

# Ngưỡng (ký tự): nếu wikitext EN dài hơn thì dùng chunker dịch từng phần (Phase 8).
CHUNK_THRESHOLD = 35000
# Kích thước tối đa mỗi chunk khi chia (để tránh vượt context Gemini).
CHUNK_MAX_CHARS = 45000

TRANSLATE_PROMPT_PREFIX = """Bạn là trợ lý dịch bài viết Wikipedia từ tiếng Anh sang tiếng Việt.
Nhiệm vụ: Dịch toàn bộ văn bản sau sang tiếng Việt và GIỮ NGUYÊN cú pháp wikitext.

Quy tắc bắt buộc:
- Không xóa, không sửa nhầm: [[ ]] {{ }} <ref> </ref> | =
- Giữ nguyên tên template (cite book, cite web); chỉ dịch nội dung mô tả bên trong nếu là câu tiếng Anh.
- Link [[trang|nhãn]]: dịch "nhãn" sang tiếng Việt; "trang" có thể giữ EN.
- Tiêu đề ==...==, ===...===: dịch nội dung; giữ đúng số dấu =.
- In đậm '''...''': dịch nội dung; giữ '''.
- Bảng {| ... |}: dịch ô chữ; giữ cú pháp |- | ! |
- <ref>...</ref>: thường không dịch nội dung ref.
- Chỉ xuất ra MỘT khối wikitext đã dịch, không thêm giải thích hay markdown.

Wikitext cần dịch:

"""


def translate_wikitext(
    wikitext_en: str,
    *,
    api_key: str,
    model: str = "gemini-1.5-flash",
) -> str:
    """
    Dịch wikitext tiếng Anh sang tiếng Việt qua Gemini API.
    Giữ cấu trúc wikitext (template, link, ref, bảng, tiêu đề).
    Raise ValueError nếu api_key trống; raise nếu API lỗi.
    """
    api_key = (api_key or "").strip()
    if not api_key:
        raise ValueError("Chưa nhập API key Gemini.")
    wikitext_en = (wikitext_en or "").strip()
    if not wikitext_en:
        raise ValueError("Wikitext EN trống.")

    genai.configure(api_key=api_key)
    gemini_model = genai.GenerativeModel(model)
    prompt = TRANSLATE_PROMPT_PREFIX + wikitext_en
    try:
        config = genai.types.GenerationConfig(temperature=0.2)
        response = gemini_model.generate_content(prompt, generation_config=config)
    except (AttributeError, TypeError):
        response = gemini_model.generate_content(prompt)
    if not response.text:
        raise ValueError("Gemini không trả về nội dung.")
    return response.text.strip()


def translate_wikitext_chunked(
    wikitext_en: str,
    *,
    api_key: str,
    model: str = "gemini-1.5-flash",
    max_chars: int = CHUNK_MAX_CHARS,
    threshold: int = CHUNK_THRESHOLD,
) -> str:
    """
    Dịch wikitext EN → VI; nếu bài dài hơn threshold thì chia theo chunker, dịch từng phần rồi nối (Phase 8).
    """
    wikitext_en = (wikitext_en or "").strip()
    if not wikitext_en:
        raise ValueError("Wikitext EN trống.")
    if len(wikitext_en) <= threshold:
        return translate_wikitext(wikitext_en, api_key=api_key, model=model)
    chunks = chunk_wikitext(wikitext_en, max_chars=max_chars)
    if not chunks:
        return ""
    if len(chunks) == 1:
        return translate_wikitext(chunks[0], api_key=api_key, model=model)
    parts = []
    for i, chunk in enumerate(chunks):
        part = translate_wikitext(chunk, api_key=api_key, model=model)
        parts.append(part)
    return "\n\n".join(parts)
