"""
So sánh sơ bộ EN vs VI: số section, độ dài; gợi ý thiếu/sai.
Tham chiếu: docs/nghien-cuu.md § 5.2, docs/ke-hoach.md § 5.5.
"""
import re


def _count_sections(wikitext: str) -> int:
    """Đếm số tiêu đề section (==...== hoặc ===...===)."""
    if not wikitext:
        return 0
    return len(re.findall(r"^=+\s+.+\s+=+\s*$", wikitext, re.MULTILINE))


def check_content(wikitext_en: str, wikitext_vi: str) -> list[str]:
    """
    So sánh wikitext EN và VI: số section, độ dài tương đối.
    Trả về danh sách gợi ý/cảnh báo (list[str]).
    """
    if not (wikitext_en or "").strip():
        return ["Không có wikitext EN để so sánh."]
    if not (wikitext_vi or "").strip():
        return ["Không có wikitext VI để so sánh."]

    warnings: list[str] = []
    en = wikitext_en.strip()
    vi = wikitext_vi.strip()

    # Số section
    en_sections = _count_sections(en)
    vi_sections = _count_sections(vi)
    if en_sections != vi_sections:
        warnings.append(
            f"Nội dung (section): EN có {en_sections} tiêu đề section, VI có {vi_sections}. "
            "Có thể thiếu hoặc thừa section."
        )

    # Độ dài (ký tự)
    len_en = len(en)
    len_vi = len(vi)
    if len_en > 0:
        ratio = len_vi / len_en
        if ratio < 0.5:
            warnings.append(
                f"Nội dung (độ dài): VI ({len_vi} ký tự) ngắn hơn nhiều so với EN ({len_en} ký tự). "
                "Có thể thiếu nội dung."
            )
        elif ratio > 1.5:
            warnings.append(
                f"Nội dung (độ dài): VI ({len_vi} ký tự) dài hơn nhiều so với EN ({len_en} ký tự). "
                "Có thể dịch dài dòng hoặc lặp."
            )

    if not warnings:
        warnings.append(
            f"Nội dung (sơ bộ): Số section EN={en_sections}, VI={vi_sections}; độ dài tương đối ổn."
        )

    return warnings
