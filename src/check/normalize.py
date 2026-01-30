"""
Chuẩn hóa wikitext VI: thuật ngữ EN→VI (glossary), gợi ý link nội bộ.
Tham chiếu: docs/nghien-cuu.md § 5.3, docs/ke-hoach.md § 5.6.
"""
import re
from pathlib import Path

# Glossary mặc định (EN → VI); có thể bổ sung từ file.
DEFAULT_GLOSSARY: dict[str, str] = {
    "front-side bus": "bus phía trước",
    "back-side bus": "bus phía sau",
    "Northbridge": "Northbridge",  # giữ nguyên nếu đã chuẩn
    "Southbridge": "Southbridge",
}


def _load_glossary_from_file(path: Path) -> dict[str, str]:
    """Đọc glossary từ file: mỗi dòng 'EN\tVI' hoặc 'EN=VI'."""
    out: dict[str, str] = {}
    if not path.exists():
        return out
    try:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "\t" in line:
                    en, vi = line.split("\t", 1)
                elif "=" in line:
                    en, vi = line.split("=", 1)
                else:
                    continue
                out[en.strip()] = vi.strip()
    except Exception:
        pass
    return out


def get_glossary(extra_path: Path | None = None) -> dict[str, str]:
    """Trả về glossary (mặc định + file nếu có)."""
    g = dict(DEFAULT_GLOSSARY)
    path = extra_path or get_default_glossary_path()
    if path:
        g.update(_load_glossary_from_file(path))
    return g


def normalize(
    wikitext_vi: str,
    glossary: dict[str, str] | None = None,
) -> tuple[str, list[str]]:
    """
    Chuẩn hóa wikitext VI: thay thuật ngữ theo glossary; báo cáo link nội bộ.
    Trả về (wikitext_đã_chuẩn_hóa, danh_sách_báo_cáo).
    """
    if not (wikitext_vi or "").strip():
        return wikitext_vi or "", ["Wikitext VI trống."]

    glossary = glossary or get_glossary(get_default_glossary_path())
    report: list[str] = []
    text = wikitext_vi

    # Thay thế theo glossary: ưu tiên cụm dài trước để tránh thay nhầm
    for en, vi in sorted(glossary.items(), key=lambda x: -len(x[0])):
        if not en or en == vi:
            continue
        count = text.count(en)
        if count > 0:
            text = text.replace(en, vi)
            report.append(f"Thuật ngữ: đã thay '{en}' → '{vi}' ({count} lần).")

    # Liệt kê link nội bộ [[...]] để gợi ý kiểm tra
    links = re.findall(r"\[\[([^\]|]+)(?:\|[^\]]*)?\]\]", text)
    unique_links = list(dict.fromkeys(links))  # giữ thứ tự, bỏ trùng
    if unique_links:
        report.append(f"Link nội bộ: {len(unique_links)} link (gợi ý kiểm tra trên vi.wikipedia).")

    if not report:
        report.append("Chuẩn hóa: không có thay đổi (glossary rỗng hoặc không khớp).")

    return text, report


def get_default_glossary_path() -> Path:
    """Đường dẫn file glossary mặc định (config/glossary.txt)."""
    return Path(__file__).resolve().parent.parent.parent / "config" / "glossary.txt"
