"""
Kiểm tra wikitext bằng AI (Gemini): bố cục, nội dung, thuật ngữ, link nội bộ.
Dùng cho mọi cặp ngôn ngữ; không phụ thuộc glossary cố định.
"""
import google.generativeai as genai

from src.translate.gemini_client import _get_response_text

# Giới hạn ký tự gửi mỗi wikitext để tránh vượt context (vẫn đủ cho bài dài).
MAX_CHARS_PER_WIKITEXT = 150_000


def _build_check_prompt(
    wikitext_source: str | None,
    wikitext_target: str,
    source_lang_name: str,
    target_lang_name: str,
) -> str:
    """Tạo prompt yêu cầu AI kiểm tra wikitext. Dùng tiếng Anh để áp dụng mọi cặp ngôn ngữ."""
    report_lang = target_lang_name if target_lang_name else "English"
    intro = (
        "You are an expert in Wikipedia wikitext and translation quality. "
        f"Analyze the wikitext below and report by section. Output the report in: {report_lang}.\n\n"
    )
    if wikitext_source and wikitext_source.strip():
        intro += (
            "**Source wikitext** (language: " + source_lang_name + "):\n"
            "---\n" + wikitext_source.strip() + "\n---\n\n"
        )
    intro += (
        "**Target wikitext** (language: " + target_lang_name + "):\n"
        "---\n" + wikitext_target.strip() + "\n---\n\n"
    )
    tasks = [
        "**Layout**: Are [[ and ]], {{ and }}, <ref> and </ref> balanced? If there are <ref>, is {{reflist}} (or equivalent) present?",
        "**Content**: If both source and target are given — do section headers (==...==) match in count/structure? Is target length reasonable (not too short/long)? If only target — is section structure clear?",
        "**Terminology**: Is terminology in the target wikitext consistent and appropriate for the domain? Suggest corrections if any (in the target language).",
        "**Internal links**: List or count [[...]] links in the target; remind to verify them on the target language Wikipedia.",
    ]
    intro += "**Report** (concise, bullet points OK):\n"
    for t in tasks:
        intro += "- " + t + "\n"
    intro += "\nOutput only the report, no extra explanation."
    return intro


def check_with_ai(
    wikitext_target: str,
    *,
    api_key: str,
    model: str = "gemini-3-flash-preview",
    source_lang_name: str = "English",
    target_lang_name: str = "Vietnamese",
    wikitext_source: str | None = None,
) -> list[str]:
    """
    Kiểm tra wikitext đích (và nguồn nếu có) bằng AI.
    Trả về danh sách dòng báo cáo (list[str]).
    Hỗ trợ mọi cặp ngôn ngữ; thuật ngữ do AI đánh giá theo ngữ cảnh.
    """
    api_key = (api_key or "").strip()
    if not api_key:
        raise ValueError("Chưa nhập API key Gemini.")
    wikitext_target = (wikitext_target or "").strip()
    if not wikitext_target:
        raise ValueError("Wikitext đích trống.")
    source_name = (source_lang_name or "English").strip()
    target_name = (target_lang_name or "Vietnamese").strip()

    # Giới hạn độ dài để không vượt context
    def truncate(s: str, max_c: int) -> str:
        s = s.strip()
        if len(s) <= max_c:
            return s
        return s[:max_c] + "\n\n[... (truncated for check) ...]"

    wt_target = truncate(wikitext_target, MAX_CHARS_PER_WIKITEXT)
    wt_source = truncate(wikitext_source, MAX_CHARS_PER_WIKITEXT) if (wikitext_source and wikitext_source.strip()) else None

    prompt = _build_check_prompt(wt_source, wt_target, source_name, target_name)
    genai.configure(api_key=api_key)
    gemini_model = genai.GenerativeModel(model)
    
    # Gemini 3 yêu cầu temperature=1.0 (mặc định), Gemini 2.x thì 0.2 tốt hơn
    is_gemini_3 = "gemini-3" in model.lower()
    temp = 1.0 if is_gemini_3 else 0.2
    
    try:
        config = genai.types.GenerationConfig(temperature=temp)
        response = gemini_model.generate_content(prompt, generation_config=config)
    except (AttributeError, TypeError):
        response = gemini_model.generate_content(prompt)
    report_text = _get_response_text(response)
    # Chuyển báo cáo thành list dòng, bỏ dòng trống thừa
    lines = [line.strip() for line in report_text.splitlines() if line.strip()]
    return lines if lines else [report_text.strip()]
