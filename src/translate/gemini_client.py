"""
Dịch wikitext giữa các ngôn ngữ bằng Gemini API, giữ cấu trúc wikitext.
Tham chiếu: docs/nghien-cuu.md § 4.
"""
import google.generativeai as genai

from src.translate.chunker import chunk_wikitext

# Ngưỡng (ký tự): nếu wikitext dài hơn thì dùng chunker dịch từng phần (Phase 8).
CHUNK_THRESHOLD = 35000
# Kích thước tối đa mỗi chunk khi chia (để tránh vượt context Gemini).
CHUNK_MAX_CHARS = 45000


def _build_translate_prompt_prefix(source_lang_name: str, target_lang_name: str) -> str:
    """Tạo phần đầu prompt dịch theo cặp ngôn ngữ nguồn → đích."""
    return f"""Bạn là trợ lý dịch bài viết Wikipedia từ {source_lang_name} sang {target_lang_name}.
Nhiệm vụ: Dịch toàn bộ văn bản sau sang {target_lang_name} và GIỮ NGUYÊN cú pháp wikitext.

Quy tắc bắt buộc:
- Không xóa, không sửa nhầm: [[ ]] {{ }} <ref> </ref> | =
- Giữ nguyên tên template (cite book, cite web); chỉ dịch nội dung mô tả bên trong.
- Link [[trang|nhãn]]: dịch "nhãn" sang {target_lang_name}; "trang" có thể giữ nguyên nếu là tên riêng.
- Tiêu đề ==...==, ===...===: dịch nội dung; giữ đúng số dấu =.
- In đậm '''...''': dịch nội dung; giữ '''.
- Bảng {{| ... |}}: dịch ô chữ; giữ cú pháp |- | ! |
- <ref>...</ref>: thường không dịch nội dung ref.
- Chỉ xuất ra MỘT khối wikitext đã dịch, không thêm giải thích hay markdown.

Wikitext cần dịch:

"""


def translate_wikitext(
    wikitext_source: str,
    *,
    api_key: str,
    model: str = "gemini-3-flash-preview",
    source_lang: str = "English",
    target_lang: str = "Vietnamese",
) -> str:
    """
    Dịch wikitext từ source_lang sang target_lang qua Gemini API.
    Giữ cấu trúc wikitext (template, link, ref, bảng, tiêu đề).
    source_lang, target_lang là tên hiển thị (vd: English, Vietnamese).
    Raise ValueError nếu api_key trống; raise nếu API lỗi.
    """
    api_key = (api_key or "").strip()
    if not api_key:
        raise ValueError("Chưa nhập API key Gemini.")
    wikitext_source = (wikitext_source or "").strip()
    if not wikitext_source:
        raise ValueError("Wikitext nguồn trống.")
    source_name = (source_lang or "English").strip()
    target_name = (target_lang or "Vietnamese").strip()

    genai.configure(api_key=api_key)
    gemini_model = genai.GenerativeModel(model)
    prompt_prefix = _build_translate_prompt_prefix(source_name, target_name)
    prompt = prompt_prefix + wikitext_source
    try:
        config = genai.types.GenerationConfig(temperature=0.2)
        response = gemini_model.generate_content(prompt, generation_config=config)
    except (AttributeError, TypeError):
        response = gemini_model.generate_content(prompt)
    if not response.text:
        raise ValueError("Gemini không trả về nội dung.")
    return response.text.strip()


def translate_wikitext_chunked(
    wikitext_source: str,
    *,
    api_key: str,
    model: str = "gemini-3-flash-preview",
    source_lang: str = "English",
    target_lang: str = "Vietnamese",
    max_chars: int = CHUNK_MAX_CHARS,
    threshold: int = CHUNK_THRESHOLD,
) -> str:
    """
    Dịch wikitext từ source_lang sang target_lang; nếu bài dài hơn threshold thì chia theo chunker, dịch từng phần rồi nối.
    """
    wikitext_source = (wikitext_source or "").strip()
    if not wikitext_source:
        raise ValueError("Wikitext nguồn trống.")
    if len(wikitext_source) <= threshold:
        return translate_wikitext(
            wikitext_source,
            api_key=api_key,
            model=model,
            source_lang=source_lang,
            target_lang=target_lang,
        )
    chunks = chunk_wikitext(wikitext_source, max_chars=max_chars)
    if not chunks:
        return ""
    if len(chunks) == 1:
        return translate_wikitext(
            chunks[0],
            api_key=api_key,
            model=model,
            source_lang=source_lang,
            target_lang=target_lang,
        )
    parts = []
    for chunk in chunks:
        part = translate_wikitext(
            chunk,
            api_key=api_key,
            model=model,
            source_lang=source_lang,
            target_lang=target_lang,
        )
        parts.append(part)
    return "\n\n".join(parts)
