"""
Dịch wikitext giữa các ngôn ngữ bằng Gemini API, giữ cấu trúc wikitext.
Tham chiếu: docs/nghien-cuu.md § 4.
"""
import google.generativeai as genai

from src.translate.chunker import chunk_wikitext

# Ngưỡng (ký tự): nếu wikitext dài hơn thì dùng chunker dịch từng phần (Phase 8).
# Context Gemini rất lớn (200k–1M token ≈ 800k–4M ký tự); nhưng output limit thấp hơn.
# Giảm ngưỡng xuống 100k để tránh mất nội dung khi bài viết quá dài.
CHUNK_THRESHOLD = 100_000
# Kích thước tối đa mỗi chunk (an toàn cho context + output limit của Gemini).
CHUNK_MAX_CHARS = 100_000


def _build_translate_prompt_prefix(source_lang_name: str, target_lang_name: str) -> str:
    """Tạo phần đầu prompt dịch theo cặp ngôn ngữ nguồn → đích. Dùng tiếng Anh để áp dụng mọi cặp ngôn ngữ."""
    return f"""You are a Wikipedia article translation assistant. Translate from {source_lang_name} to {target_lang_name}.

Task: Translate the entire text below into {target_lang_name} and PRESERVE wikitext syntax exactly.

Rules (do not break):
- Do not remove or corrupt: [[ ]] {{ }} <ref> </ref> | =
- Keep template names (cite book, cite web, etc.); translate only the descriptive content inside.
- Links [[page|label]]: translate the "label" to {target_lang_name}; "page" may stay unchanged if it is a proper noun.
- Headings ==...==, ===...===: translate the text; keep the same number of = signs.
- Bold '''...''': translate the text; keep '''.
- Tables {{| ... |}}: translate cell text; keep syntax |- | ! |
- <ref>...</ref>: usually do not translate ref content.
- Output ONLY one block of translated wikitext, no explanation or markdown.

Wikitext to translate:

"""


def _get_response_text(response) -> str:
    """
    Lấy chuỗi text từ response Gemini. Hỗ trợ cả response.text (1.5) và
    response.candidates[0].content.parts (Gemini 3 / response không đơn phần).
    Đảm bảo lấy TẤT CẢ nội dung từ response để không bị mất.
    """
    try:
        if hasattr(response, "text") and response.text:
            return response.text.strip()
    except (ValueError, TypeError, AttributeError):
        pass
    
    # Fallback: lấy từ candidates[0].content.parts (chuẩn với Gemini 3)
    if not getattr(response, "candidates", None) or len(response.candidates) == 0:
        raise ValueError("Gemini không trả về candidate (có thể bị chặn hoặc lỗi API).")
    
    candidate = response.candidates[0]
    if not getattr(candidate, "content", None) or not getattr(candidate.content, "parts", None):
        reason = getattr(candidate, "finish_reason", None) or "unknown"
        # Kiểm tra nếu finish_reason là MAX_TOKENS - có thể bị cắt nội dung
        if "MAX_TOKENS" in str(reason).upper():
            raise ValueError(f"Gemini dừng do đạt giới hạn token (finish_reason: {reason}). Nội dung có thể bị cắt. Hãy thử giảm kích thước chunk.")
        raise ValueError(f"Gemini không trả về nội dung (finish_reason: {reason}).")
    
    parts = candidate.content.parts
    if not parts:
        raise ValueError("Gemini trả về parts rỗng.")
    
    texts = []
    for part in parts:
        if hasattr(part, "text") and part.text:
            texts.append(part.text)
    
    if not texts:
        raise ValueError("Gemini không trả về text trong parts.")
    
    full_text = "".join(texts).strip()
    
    # Cảnh báo nếu response có vẻ bị cắt (không có dấu kết thúc tự nhiên)
    if full_text and not any(full_text.endswith(end) for end in [".", "!", "?", ")", "]", "}", "|}", "==", "'''"]):
        # Có thể nội dung bị cắt - nhưng vẫn trả về để không mất hoàn toàn
        pass
    
    return full_text


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
    
    # Gemini 3 yêu cầu temperature=1.0 (mặc định), Gemini 2.x thì 0.2 tốt hơn
    is_gemini_3 = "gemini-3" in model.lower()
    temp = 1.0 if is_gemini_3 else 0.2
    
    try:
        config = genai.types.GenerationConfig(
            temperature=temp,
            max_output_tokens=65536,  # Đảm bảo output đủ dài, tránh bị cắt
        )
        response = gemini_model.generate_content(prompt, generation_config=config)
    except (AttributeError, TypeError):
        # Fallback cho API version cũ hơn
        response = gemini_model.generate_content(prompt)
    except Exception as e:
        # Xử lý lỗi API cụ thể
        error_msg = str(e)
        if "429" in error_msg or "quota" in error_msg.lower():
            raise ValueError(f"API quota exceeded hoặc rate limit. Nếu dùng gemini-3-pro-preview, lưu ý model này không có free tier trong API. Hãy thử gemini-3-flash-preview hoặc đợi vài phút rồi thử lại.\n\nLỗi gốc: {error_msg}")
        elif "permission" in error_msg.lower() or "not found" in error_msg.lower():
            raise ValueError(f"Model '{model}' không khả dụng với API key này. gemini-3-pro-preview không có free tier. Hãy thử gemini-3-flash-preview hoặc kiểm tra billing.\n\nLỗi gốc: {error_msg}")
        else:
            raise ValueError(f"Lỗi gọi Gemini API: {error_msg}")
    
    return _get_response_text(response)


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
    Tự động xử lý bài viết dài để tránh mất nội dung.
    """
    wikitext_source = (wikitext_source or "").strip()
    if not wikitext_source:
        raise ValueError("Wikitext nguồn trống.")
    
    # Nếu bài ngắn hơn threshold thì dịch trực tiếp
    if len(wikitext_source) <= threshold:
        return translate_wikitext(
            wikitext_source,
            api_key=api_key,
            model=model,
            source_lang=source_lang,
            target_lang=target_lang,
        )
    
    # Bài dài - cần chia nhỏ
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
    
    # Dịch từng chunk và ghép lại
    parts = []
    for i, chunk in enumerate(chunks):
        try:
            part = translate_wikitext(
                chunk,
                api_key=api_key,
                model=model,
                source_lang=source_lang,
                target_lang=target_lang,
            )
            if part:  # Chỉ thêm nếu có nội dung
                parts.append(part)
        except Exception as e:
            # Nếu chunk bị lỗi, thêm thông báo để không mất vị trí
            error_msg = f"\n<!-- LỖI DỊCH CHUNK {i + 1}/{len(chunks)}: {str(e)} -->\n"
            parts.append(error_msg)
            # Vẫn tiếp tục dịch các chunk còn lại
    
    if not parts:
        raise ValueError("Không thể dịch được chunk nào. Vui lòng kiểm tra API key và kết nối.")
    
    return "\n\n".join(parts)
